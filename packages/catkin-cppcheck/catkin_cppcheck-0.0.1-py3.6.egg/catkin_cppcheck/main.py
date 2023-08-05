import cppcheck

import os
import logging

from catkin_pkg.packages import find_package_paths
from catkin_tools.metadata import find_enclosing_workspace


def prepare_arguments(parser):
    parser.add_argument('-e', '--enable', action='append',
        choices=[
            'all', 'warning', 'style', 'performance', 'portability', 'information', 'unusedFunction', 'missingInclude'
        ],
        help='cppcheck check options'
    )
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Quiet cppcheck output')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output for plugin')

    return parser


def run_cppcheck(args):
    enable_checks = args.enable
    quiet = args.quiet
    verbose = args.verbose

    cwd = os.getcwd()
    # Find root of catkin workspace
    ws = find_enclosing_workspace(cwd)

    if ws:
        # Find all packages in the workspace
        package_paths = find_package_paths(ws)
        # Get absolute paths
        package_paths = [os.path.join(ws, p) for p in package_paths]
        # Run cppcheck on the catkin package paths
        cppcheck.check(package_paths, enable_checks, quiet=quiet, verbose=verbose)
    else:
        logging.error('No catkin workspace found. Is "{}" contained in a workspace?'.format(cwd))


description = dict(
    verb='cppcheck',
    description='Run cppcheck on catkin packages',
    main=run_cppcheck,
    prepare_arguments=prepare_arguments
)
