#! /usr/bin/env python

import subprocess
import setuptools
import distutils.command.upload


PACKAGE = 'loap'
VERSION = '0.2.3'
CODE_SIGNING_GPG_ID = '83C58714F20D8D34F46ECA64102464A385AF6563'


def setup():
    setuptools.setup(
        name=PACKAGE,
        version=VERSION,
        author='Nathan Wilcox',
        author_email='nejucomo@gmail.com',
        license='GPLv3',
        url='https://github.com/nejucomo/{}'.format(PACKAGE),

        description=(
            'LogOptionsArgumentParser: add --debug and --quiet options ' +
            'with std logging module.'
        ),

        packages=setuptools.find_packages(),

        install_requires=[
            'mock',
        ],

        test_suite='{}.tests'.format(PACKAGE),

        cmdclass={
            'release': ReleaseCommand,
            'upload': UploadCommand,
        },
    )


class ReleaseCommand (setuptools.Command):
    """Prepare and distribute a release"""

    description = __doc__

    user_options = [
        ('dry-run', None, 'Do not git tag or upload.')
    ]

    def initialize_options(self):
        """init options"""
        self.dry_run = False

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        def real_abort(tmpl, *args):
            raise SystemExit('ABORT: {}'.format(tmpl.format(*args)))

        def dry_abort(tmpl, *args):
            print 'ABORT: {}'.format(tmpl.format(*args))
            print 'Continuing after ABORT due to --dry-run.'

        abort = dry_abort if self.dry_run else real_abort

        def fmt_args(args):
            return ' '.join([repr(a) for a in args])

        def make_sh_func(subprocfunc):
            def shfunc(*args):
                print 'Running: {}'.format(fmt_args(args))
                try:
                    return subprocfunc(args)
                except subprocess.CalledProcessError as e:
                    abort(str(e))
            return shfunc

        def dry_run(*args):
            print 'Not running (--dry-run): {}'.format(fmt_args(args))

        sh = make_sh_func(subprocess.check_call)
        shout = make_sh_func(subprocess.check_output)
        shdry = dry_run if self.dry_run else sh

        gitstatus = shout('git', 'status', '--porcelain')
        if gitstatus.strip():
            abort('dirty working directory:\n{}', gitstatus)

        branch = shout('git', 'rev-parse', '--abbrev-ref', 'HEAD').strip()
        if branch != 'release':
            abort('must be on release branch, not {!r}', branch)

        version = shout('python', './setup.py', '--version').strip()

        shdry(
            'git', 'tag', '--annotate',
            '--local-user', CODE_SIGNING_GPG_ID,
            '--message', 'Created by ``setup.py release``.',
            version,
        )

        shdry('git', 'push', '--follow-tags', 'origin', branch)

        shdry(
            'python', './setup.py', 'sdist', 'bdist_wheel',
        )
        sdist = 'dist/{}-{}.tar.gz'.format(PACKAGE, version)
        bdist = 'dist/{}-{}-py2-none-any.whl'.format(PACKAGE, version)
        shdry(
            'gpg', '--detach-sign', '-a', sdist,
        )
        shdry(
            'gpg', '--detach-sign', '-a', bdist,
        )
        shdry(
            'twine', 'upload', sdist, sdist + '.asc', bdist, bdist + '.asc',
        )


class UploadCommand (distutils.command.upload.upload):
    description = distutils.command.upload.upload.__doc__

    def run(self):
        raise SystemExit(
            'Please use the release command, ' +
            'rather than directly uploading.')


if __name__ == '__main__':
    setup()
