import shlex
import logging
import subprocess


def check(paths, enabled_checks, excludes=None, quiet=False, verbose=False):
    """
    :param paths: List of paths to check
    :param enabled_checks: List of enabled cppchecks
    :param quiet: Quiet cppcheck output
    """
    paths = ' '.join(paths)
    checks = 'warning' if not enabled_checks else ','.join(enabled_checks)
    quiet = '-q' if quiet else ''

    cmd = 'cppcheck --force --enable={} {} {}'.format(checks, paths, quiet)

    output = ''
    try:
        output = subprocess.check_output(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        if verbose:
            logging.exception(str(e))

        logging.error(e.output)


    logging.info(output)
