======
 loap
======

Provides a ``LogOptionsArgumentParser`` subclass of ``argparse.ArgumentParser`` which adds the ``--quiet`` / ``-q`` and ``--debug`` options. Additionally it initializes the ``logging`` module, by default to the ``INFO`` log level, or to ``WARN`` or ``DEBUG`` if the respective verbosity options are given.
