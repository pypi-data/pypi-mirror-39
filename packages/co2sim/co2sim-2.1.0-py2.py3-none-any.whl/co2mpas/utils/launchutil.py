# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# Copyright 2014-2017 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"Utils for configuring and using elaborate logs and handling `main()` failures."

from co2mpas import (__version__ as proj_ver, __file__ as proj_file,
                     __updated__ as proj_date)
import collections
import functools as fnt
import glob
import io
import logging
import os.path as osp
import os
import re
import shutil
import sys
import docopt
import yaml
import warnings


class CmdException(Exception):
    """Polite user-message avoiding ``exit(msg)`` when ``main()`` invoked from python."""
    pass


#: Load  this file automatically if it exists in HOME and configure logging,
#: unless overridden with --logconf.
default_logconf_file = osp.expanduser(osp.join('~', '.co2_logconf.yaml'))


def _set_numpy_logging():
    rlog = logging.getLogger()
    if not rlog.isEnabledFor(logging.DEBUG):
        import numpy as np
        np.seterr(divide='ignore', invalid='ignore')


def init_logging(level=None, frmt=None, logconf_file=None,
                 color=False, default_logconf_file=default_logconf_file,
                 not_using_numpy=False, **kwds):
    """
    :param level:
        tip: use :func:`is_any_log_option()` to decide if should be None
        (only if None default HOME ``logconf.yaml`` file is NOT read).
    :param default_logconf_file:
        Read from HOME only if ``(level, frmt, logconf_file)`` are none.
    :param kwds:
        Passed directly to :func:`logging.basicConfig()` (e.g. `filename`);
        used only id default HOME ``logconf.yaml`` file is NOT read.
    """
    ## Only read default logconf file in HOME
    #  if no explicit arguments given.
    #
    no_args = all(i is None for i in [level, frmt, logconf_file])
    if no_args and osp.exists(default_logconf_file):
        logconf_file = default_logconf_file

    if logconf_file:
        from logging import config as lcfg

        logconf_file = osp.expanduser(logconf_file)
        if osp.splitext(logconf_file)[1] in '.yaml' or '.yml':
            with io.open(logconf_file) as fd:
                log_dict = yaml.safe_load(fd)
                lcfg.dictConfig(log_dict)
        else:
            lcfg.fileConfig(logconf_file)

        logconf_src = logconf_file
    else:
        if level is None:
            level = logging.INFO
        if not frmt:
            frmt = "%(asctime)-15s:%(levelname)5.5s:%(name)s:%(message)s"
        logging.basicConfig(level=level, format=frmt, **kwds)
        rlog = logging.getLogger()
        rlog.level = level  # because `basicConfig()` does not reconfig root-logger when re-invoked.

        logging.getLogger('pandalone.xleash.io').setLevel(logging.WARNING)

        if color and sys.stderr.isatty():
            from rainbow_logging_handler import RainbowLoggingHandler

            color_handler = RainbowLoggingHandler(
                sys.stderr,
                color_message_debug=('grey', None, False),
                color_message_info=('blue', None, False),
                color_message_warning=('yellow', None, True),
                color_message_error=('red', None, True),
                color_message_critical=('white', 'red', True),
            )
            formatter = formatter = logging.Formatter(frmt)
            color_handler.setFormatter(formatter)

            ## Be conservative and apply color only when
            #  log-config looks like the "basic".
            #
            if rlog.handlers and isinstance(rlog.handlers[0], logging.StreamHandler):
                rlog.removeHandler(rlog.handlers[0])
                rlog.addHandler(color_handler)
        logconf_src = 'explicit(level=%s)' % level

    if not not_using_numpy:
        _set_numpy_logging()

    logging.captureWarnings(True)

    ## Disable warnings on AIO but not when developing.
    #
    if os.environ.get('AIODIR'):
        warnings.filterwarnings(action="ignore", category=DeprecationWarning)
        warnings.filterwarnings(action="ignore", module="scipy",
                                message="^internal gelsd")
        warnings.filterwarnings(action="ignore", module="dill",
                                message="^unclosed file")
        warnings.filterwarnings(action="ignore", module="importlib",
                                message="^can't resolve")

    log.debug('Logging-configurations source: %s', logconf_src)


def is_any_log_option(argv):
    """
    Return true if any -v/--verbose/--debug etc options are in `argv`

    :param argv:
        If `None`, use :data:`sys.argv`; use ``[]`` to explicitly use no-args.
    """
    log_opts = '-v --verbose -d --debug --vlevel'.split()
    if argv is None:
        argv = sys.argv
    return argv and set(log_opts) & set(argv)


def exit_with_pride(reason=None,
                    warn_color='\x1b[31;1m', err_color='\x1b[1m',
                    logger=None):
    """
    Return an *exit-code* and logs error/fatal message for ``main()`` methods.

    :param reason:
        - If reason is None, exit-code(0) signifying OK;
        - if exception,  print colorful (if tty) stack-trace, and exit-code(-1);
        - otherwise, prints str(reason) colorfully (if tty) and exit-code(1),
    :param warn_color:
        ansi color sequence for stack-trace (default: red)
    :param err_color:
        ansi color sequence for stack-trace (default: white-on-red)
    :param logger:
        which logger to use to log reason (must support info and fatal).

    :return:
        (0, 1 -1), for reason == (None, str, Exception) respectively.

    Note that returned string from ``main()`` are printed to stderr and
    exit-code set to bool(str) = 1, so print stderr separately and then
    set the exit-code.

    For colors use :meth:`RainbowLoggingHandler.getColor()`, defaults:
    - '\x1b[33;1m': yellow+bold
    - '\x1b[31;1m': red+bold

    Note: it's better to have initialized logging.
    """
    if reason is None:
        return 0
    if not logger:
        logger = log

    if isinstance(reason, BaseException):
        color = err_color
        exit_code = -1
        logmeth = fnt.partial(logger.fatal, exc_info=True)
    else:
        color = warn_color
        exit_code = 1
        logmeth = logger.error

    if sys.stderr.isatty():
        reset = '\x1b[0m'
        reason = '%s%s%s' % (color, reason, reset)

    logmeth(reason)
    return exit_code


def build_version_string(verbose):
    v = '%s-%s' % (proj_name, proj_ver)
    if verbose:
        v_infos = collections.OrderedDict([
            ('co2mpas_version', proj_ver),
            ('co2mpas_rel_date', proj_date),
            ('co2mpas_path', osp.dirname(proj_file)),
            ('python_version', sys.version),
            ('python_path', sys.prefix),
            ('PATH', os.environ.get('PATH', None)),
        ])
        v = ''.join('%s: %s\n' % kv for kv in v_infos.items())
    return v


def print_autocompletions():
    """
    Prints the auto-completions list from docopt in stdout.

    .. Note::
        Must be registered as `setup.py` entry-point.
    """
    from . import docoptutils
    docoptutils.print_wordlist_from_docopt(__doc__)


def _generate_files_from_streams(
        dst_folder, file_stream_pairs, force, file_category):
    if not osp.exists(dst_folder):
        if force:
            os.makedirs(dst_folder)
        else:
            raise CmdException(
                "Destination folder '%s' does not exist!  "
                "Use --force to create it." % dst_folder)
    if not osp.isdir(dst_folder):
        raise CmdException(
            "Destination '%s' is not a <output-folder>!" % dst_folder)

    for src_fname, stream_factory in file_stream_pairs:
        dst_fpath = osp.join(dst_folder, src_fname)
        if osp.exists(dst_fpath) and not force:
            msg = "Creating %s file '%s' skipped, already exists! \n  " \
                  "Use --force to overwrite it."
            log.info(msg, file_category, dst_fpath)
        else:
            log.info("Creating %s file '%s'...", file_category, dst_fpath)
            with open(dst_fpath, 'wb') as fd:
                shutil.copyfileobj(stream_factory(), fd, 16 * 1024)


def _get_internal_file_streams(internal_folder, incl_regex=None):
    """
    :return: a mappings of {filename--> stream-gen-function}.

    REMEMBER: Add internal-files also in `setup.py` & `MANIFEST.in` and
    update checks in `./bin/package.sh`.
    """
    import pkg_resources

    samples = pkg_resources.resource_listdir(__name__,  # @UndefinedVariable
                                             internal_folder)
    if incl_regex:
        incl_regex = re.compile(incl_regex)
    return {f: fnt.partial(pkg_resources.resource_stream,  # @UndefinedVariable
            __name__,
            osp.join(internal_folder, f))
            for f in samples
            if not incl_regex or incl_regex.match(f)}


_input_file_regex = re.compile(r'^\w')


def file_finder(xlsx_fpaths, file_ext='*.xlsx'):
    files = set()
    for f in xlsx_fpaths:
        if osp.isfile(f):
            files.add(f)
        elif osp.isdir(f):
            files.update(glob.glob(osp.join(f, file_ext)))

    return [f for f in sorted(files) if _input_file_regex.match(osp.basename(f))]


_re_override = re.compile(r"^\s*([^=]+)\s*=\s*(.*?)\s*$")
