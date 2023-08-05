#!/usr/bin/env python3

'''
A wacky manager of window manager.
'''

import argparse
import argparse_better
import sys

from traceback import print_exc

from awd.api import get_active_window
from awd.api import get_current_desktop
from awd.api import get_desktop_viewport
from awd.api import get_windows
from awd.api import get_wm_desktop
from awd.api import get_wm_name
from awd.api import set_active_window
from awd.util import is_window_in_viewport
from awd.util import printerr
from awd.util import die

##  program name;
prog = 'awd'

epilog = '''\
available layouts:
    rowgrid[x][y]       row-major grid layout (2 <= x, y <= 4)
    colgrid[x][y]       col-major grid layout (2 <= x, y <= 4)
'''

def filter_windows(windows, desktop, viewport, excludes):
    '''
    Filter out windows which are not in the desktop or not in the viewport.

    Parameters
    ----------
    windows : list
        A list of windows.
    desktop : int
        A desktop number.
    viewport : list
        A viewport.
    excludes : list
        A list of window name exclude patterns.

    Returns
    -------
    list
        A list of windows that pass the filter.
    '''
    ans = []
    for window in windows:

        # Filter by desktop.
        if get_wm_desktop(window) != desktop:
            continue

        # Filter by viewport.
        if not is_window_in_viewport(window, viewport):
            continue

        # Filter by window name.
        wm_name = get_wm_name(window)
        if any([x in wm_name for x in excludes]):
            continue

        ans.append(window)
    return ans

def layout_windows(windows, layout, active_window):
    '''
    Layout windows.

    Parameters
    ----------
    windows : list
        A list of windows.
    layout : str
        Layout name.
    active_window : object
        The active window object.
    '''
    LAYOUT_HANDLERZ[layout](windows, active_window)

def parse_args():

    '''
    parse command line arguments;
    '''

    parser = argparse.ArgumentParser(
        prog=prog,
        description='a window director;',
        formatter_class=argparse_better.HelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help='display help message;',
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='debug mode;',
    )
    parser.add_argument(
        '-e', '--exclude',
        action='append',
        default=[],
        metavar='pattern',
        help='excluded window names;',
    )

    layouts = parser.add_argument_group('layouts')

    layouts.add_argument(
        '--cascade',
        action='store_true',
        help='cascade;',
    )
    layouts.add_argument(
        '--horizontal',
        action='store_true',
        help='tile horizontally;',
    )
    layouts.add_argument(
        '--vertical',
        action='store_true',
        help='tile vertically;',
    )
    layouts.add_argument(
        '--left',
        action='store_true',
        help='main window on the left;',
    )
    layouts.add_argument(
        '--right',
        action='store_true',
        help='main window on the right;',
    )
    layouts.add_argument(
        '--top',
        action='store_true',
        help='main window on the top;',
    )
    layouts.add_argument(
        '--bottom',
        action='store_true',
        help='main window on the bottom;',
    )
    layouts.add_argument(
        '--grid',
        action='store_true',
        help='grid;',
    )

    layout_opts = parser.add_argument_group('layout options')

    layout_opts.add_argument(
        '--row',
        type=int,
        metavar='row',
        help='number of grid rows;',
    )
    layout_opts.add_argument(
        '--col',
        type=int,
        metavar='col',
        help='number of grid cols;',
    )

    args = parser.parse_args()

    ##  check conflicts;
    mutex = [ k for k in [
        'cascade', 'horizontal', 'vertical', 'left', 'right', 'top', 'bottom',
        'grid',
    ] if getattr(args, k, False) ]
    if len(mutex) > 1:
        die('layout confict: ' + ', '.join(mutex))

    return args

def main():

    '''
    main function;
    '''

    ##  parse args;
    args = parse_args()
    print(args)
    sys.exit()

    layout = args.layout
    exclude = args.exclude

    # Set log level.
    logger.setLevel({v: k for k, v in LOGLEVELZ.items()}[loglevel])

    # Get all windows managed by WM.
    windows = get_windows()
    logger.d('all windows %s', windows)

    # Get current active window.
    active_window = get_active_window()
    logger.d('active_window %s', active_window)

    # Get current desktop.
    desktop = get_current_desktop()
    logger.d('current desktop %s', desktop)

    # Get current viewport.
    viewport = get_desktop_viewport()
    logger.d('current viewport %s', viewport)

    # Filter windows by desktop and viewport.
    windows = filter_windows(windows, desktop, viewport, exclude)
    logger.d('filtered windows %s', windows)

    # Layout windows.
    layout_windows(windows, layout, active_window)

    # Activate the original active window.
    set_active_window(active_window)

if __name__ == '__main__':
    main()

