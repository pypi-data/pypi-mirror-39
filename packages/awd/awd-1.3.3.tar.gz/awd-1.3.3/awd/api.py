#!/usr/bin/env python3

'''
ewmh api module;
'''

from ewmh_ext import EWMH

##  ewmh object;
ewmh = None

def _get_ewmh():

    '''
    get the ewmh object;
    '''

    global ewmh
    if ewmh is None:
        ewmh = EWMH()
    return ewmh

def get_windows(excludes=None):

    '''
    get windows in current desktop;

    exclude certain windows based on their types, states, etc.;

    ## params

    excludes:list
    :   window name exclude pattern;

    ## return

    :list
    :   a list of windows;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()

    windows = []
    for w in ewmh.getClientListStacking():
        w_type = ewmh.getWmWindowType(w, True)
        w_state = ewmh.getWmState(w, True)
        w_desktop = ewmh.getWmDesktop(w)
        w_name = ewmh.getWmName(w)

        if '_NET_WM_WINDOW_TYPE_DESKTOP' in w_type:
            continue
        elif '_NET_WM_WINDOW_TYPE_DOCK' in w_type:
            continue

        if '_NET_WM_STATE_HIDDEN' in w_state:
            continue
        elif '_NET_WM_STATE_STICKY' in w_state:
            continue

        if desktop != w_desktop:
            continue

        if excludes is not None:
            if any((e in w_name for e in excludes)):
                continue

        windows.append(w)
    return windows

def place_window(window, x, y, w, h):

    '''
    place a window; coords include borders;
    '''

    ewmh = _get_ewmh()
    ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    ewmh.setWmState(window, 0, '_NET_WM_STATE_FULLSCREEN')
    l, r, t, b = ewmh.getFrameExtents(window) or (0, 0, 0, 0)

    ##  `ewmh.setMoveResizeWindow` works inconsistently across different window
    ##  managers; so we directly call x method to move and resize window;
    window.configure(x=x, y=y, width=(w - l - r), height=(h - t - b))

    ewmh.setActiveWindow(ewmh.getActiveWindow())
    ewmh.display.flush()

def _layout_cascade(windows, **kwargs):

    '''
    layout: cascade;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    n = len(windows)

    for window in windows:
        place_window(window, x, y, w // 2, h // 2)
        if n < 2: break
        x, y = x + w // 2 // (n - 1), y + h // 2 // (n - 1)

def _layout_horizontal(windows, **kwargs):

    '''
    layout: horizontal;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    n = len(windows)

    for window in windows:
        place_window(window, x, y, w // n, h)
        x, y = x + w // n, y

def _layout_vertical(windows, **kwargs):

    '''
    layout: vertical;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    n = len(windows)

    for window in windows:
        place_window(window, x, y, w, h // n)
        x, y = x, y + h // n

def _layout_left(windows, **kwargs):

    '''
    layout: left;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    windows = windows[::-1]
    n = len(windows)

    for window in windows[:1]:
        place_window(window, x, y, w // 2, h)
    for window in windows[1:]:
        place_window(window, x + w // 2, y, w // 2, h // (n - 1))
        x, y = x, y + h // (n - 1)

def _layout_right(windows, **kwargs):

    '''
    layout: right;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    windows = windows[::-1]
    n = len(windows)

    for window in windows[:1]:
        place_window(window, x + w // 2, y, w // 2, h)
    for window in windows[1:]:
        place_window(window, x, y, w // 2, h // (n - 1))
        x, y = x, y + h // (n - 1)

def _layout_top(windows, **kwargs):

    '''
    layout: top;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    windows = windows[::-1]
    n = len(windows)

    for window in windows[:1]:
        place_window(window, x, y, w, h // 2)
    for window in windows[1:]:
        place_window(window, x, y + h // 2, w // (n - 1), h // 2)
        x, y = x + w // (n - 1), y

def _layout_bottom(windows, **kwargs):

    '''
    layout: bottom;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    windows = windows[::-1]
    n = len(windows)

    for window in windows[:1]:
        place_window(window, x, y + h // 2, w, h // 2)
    for window in windows[1:]:
        place_window(window, x, y, w // (n - 1), h // 2)
        x, y = x + w // (n - 1), y

def _layout_grid(windows, rows, cols):

    '''
    layout: grid;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]

    for i, window in enumerate(windows):
        place_window(
            window,
            x + w // cols * (i % cols),
            y + h // rows * ((i // cols) % rows),
            w // cols,
            h // rows,
        )

def layout_windows(windows, layout, **kwargs):

    '''
    layout windows;
    '''

    handlers = {
        'cascade'   : _layout_cascade,
        'horizontal': _layout_horizontal,
        'vertical'  : _layout_vertical,
        'left'      : _layout_left,
        'right'     : _layout_right,
        'top'       : _layout_top,
        'bottom'    : _layout_bottom,
        'grid'      : _layout_grid,
    }

    handler = handlers.get(layout)

    if handler is None:
        raise Exception('invalid layout: {}'.format(layout))

    handler(windows, **kwargs)

