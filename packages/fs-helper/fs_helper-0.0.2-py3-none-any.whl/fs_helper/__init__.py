import logging
import os.path
from os import makedirs


def lazy_filename(text, ext=''):
    """Return a filename string for the given text and optional extension (ext)

    - http://stackoverflow.com/a/7406369
    """
    # Strip out and replace some things in case text is a url
    text = text.split('://')[-1].strip('/').replace('/', '--')
    ext = '.{}'.format(ext) if ext else ''

    return "".join([
        c
        for c in text
        if c.isalpha() or c.isdigit() or c in (' ', '-', '_', '+', '.')
    ]).rstrip().replace(' ', '-') + ext


def get_logger(module_name,
               logdir='~/logs',
               file_format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
               stream_format='%(asctime)s: %(message)s',
               file_level=logging.DEBUG,
               stream_level=logging.INFO):
    """Return a logger object with a file handler and stream/console handler

    - file_format: used for logging file handler; if empty string or None,
      don't use a file handler
    - stream_format: used for logging stream/console handler; if empty string
      or None, don't use a stream handler
    - file_level: logging level for file handler
    - stream_level: logging level for stream/console handler
    """
    assert file_format or stream_format, 'Must supply a file_format or stream_format'


    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    if file_format:
        logdir = os.path.abspath(os.path.expanduser(logdir))
        if not os.path.isdir(logdir):
            makedirs(logdir)
        logfile = os.path.join(logdir, '{}.log'.format(module_name))
        file_handler = logging.FileHandler(logfile, mode='a')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s: %(message)s'
        ))
        logger.addHandler(file_handler)
    if stream_format:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(stream_level)
        console_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.addHandler(console_handler)
    return logger
