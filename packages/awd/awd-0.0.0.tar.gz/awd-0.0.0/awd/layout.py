#!/usr/bin/env python3

'''
Layout module.

This module contains layout handlers which lay windows into different layout
patterns.

To implement a new layout, define a new layout handler and add it to
`LAYOUT_HANDLERZ`.
'''

from awd.api import get_workarea
from awd.api import move_resize_window
from awd.api import set_active_window
import awd.logging_better as log

def _order_windows(windows, active_window):
    '''
    Order windows. Active window comes last.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    list
        A list of window objects, in which active window comes last.
    '''
    tmp = None
    ans = []
    for window in windows:
        if window.id == active_window.id:
            tmp = window
        else:
            ans.append(window)
    if tmp is not None:
        ans.append(tmp)
    return ans

def _move_resize_window(window, x, y, w, h):
    '''
    Changes the size and location of the specified window.

    This function takes border width into account.

    Parameters
    ----------
    window
        A window object.
    x
        X coord.
    y
        Y coord.
    w
        Width.
    h
        Height.

    Returns
    -------
    None
        None.
    '''
    # Find top window.
    top = window
    while True:
        resp = top.query_tree()
        if top == resp.root or resp.parent == resp.root:
            break
        top = resp.parent

    # Get left and top offsets. This is done by translating coord (0, 0) in the
    # given window to the top window.
    resp = top.translate_coords(window, 0, 0)
    l = resp.x
    t = resp.y

    # Get right and bottom offsets. This is done by computing size difference.
    win_geo = window.get_geometry()
    top_geo = top.get_geometry()
    r = top_geo.width - win_geo.width - l
    b = top_geo.height - win_geo.height - t

    # Move and resize window. WM will take care of the location, so we just need
    # to take care of the size.
    move_resize_window(window, x, y, w - l - r, h - t - b)
    log.d(['move_resize_window', x, y, w - l - r, h - t - b])

def cascade(windows, active_window):
    '''
    Cascade windows.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Get work area.
    workarea = get_workarea()

    ngrid = 16  # Magic: Number of grids on each axis.
    nwin = 10   # Magic: Number of grids a window occupies on each axis.

    xstep, ystep = workarea[2] // ngrid, workarea[3] // ngrid

    x, y, w, h = xstep, ystep, nwin * xstep, nwin * ystep
    for window in _order_windows(windows, active_window):
        log.d([window, x, y, w, h])
        _move_resize_window(window, x, y, w, h)
        set_active_window(window)
        if len(windows) == 1:
            break
        x += (ngrid - 2 - nwin) * xstep // (len(windows) - 1)
        y += (ngrid - 2 - nwin) * ystep // (len(windows) - 1)

def hstack(windows, active_window):
    '''
    Stack windows horizontally.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Get work area.
    workarea = get_workarea()

    x = workarea[0]
    y = workarea[1]
    w = workarea[2] // len(windows)
    h = workarea[3]

    for window in _order_windows(windows, active_window):
        log.d([window, x, y, w, h])
        _move_resize_window(window, x, y, w, h)
        x += w

def vstack(windows, active_window):
    '''
    Stack windows vertically.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Get work area.
    workarea = get_workarea()

    x = workarea[0]
    y = workarea[1]
    w = workarea[2]
    h = workarea[3] // len(windows)

    for window in _order_windows(windows, active_window):
        log.d([window, x, y, w, h])
        _move_resize_window(window, x, y, w, h)
        y += h

def tmain(windows, active_window):
    '''
    Two-row layout, top row is main row.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Process the active window.
    workarea = get_workarea()
    width = workarea[2]
    height = workarea[3] // 2
    _move_resize_window(active_window, 0, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, height, width // (len(windows) - 1), height
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            _move_resize_window(window, x, y, w, h)
            x += w

def bmain(windows, active_window):
    '''
    Two-row layout, bottom row is main row.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Process the active window.
    workarea = get_workarea()
    width = workarea[2]
    height = workarea[3] // 2
    _move_resize_window(active_window, 0, height, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, 0, width // (len(windows) - 1), height
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            _move_resize_window(window, x, y, w, h)
            x += w

def lmain(windows, active_window):
    '''
    Two-col layout, left col is main col.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Process the active window.
    workarea = get_workarea()
    width = workarea[2] // 2
    height = workarea[3]
    _move_resize_window(active_window, 0, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = width, 0, width, height // (len(windows) - 1)
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            _move_resize_window(window, x, y, w, h)
            y += h

def rmain(windows, active_window):
    '''
    Two-col layout, right col is main col.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    # Process the active window.
    workarea = get_workarea()
    width = workarea[2] // 2
    height = workarea[3]
    _move_resize_window(active_window, width, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, 0, width, height // (len(windows) - 1)
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            _move_resize_window(window, x, y, w, h)
            y += h

def _rowgrid(windows, active_window, nrows, ncols):
    '''
    Grid layout, row-major.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.
    nrows:
        Number of rows.
    ncols:
        Number of cols.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    if nrows * ncols < len(windows):
        log.w('Warning: Not enough space. Windows may overlap.')

    workarea = get_workarea()
    width = workarea[2] // ncols
    height = workarea[3] // nrows
    x, y, w, h = 0, 0, width, height
    for i, window in enumerate(_order_windows(windows, active_window)):
        y, x = divmod(i % (nrows * ncols), ncols)
        x *= width
        y *= height
        _move_resize_window(window, x, y, w, h)

def rowgrid22(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 2)
def rowgrid23(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 3)
def rowgrid24(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 4)
def rowgrid32(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 2)
def rowgrid33(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 3)
def rowgrid34(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 4)
def rowgrid42(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 2)
def rowgrid43(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 3)
def rowgrid44(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 4)

def _colgrid(windows, active_window, nrows, ncols):
    '''
    Grid layout, col-major.

    Parameters
    ----------
    windows : list
        A list of window objects.
    active_window : object
        The active window object.
    nrows:
        Number of rows.
    ncols:
        Number of cols.

    Returns
    -------
    None
        None.
    '''
    if len(windows) == 0:
        return

    if nrows * ncols < len(windows):
        log.w('Warning: Not enough space. Windows may overlap.')

    workarea = get_workarea()
    width = workarea[2] // ncols
    height = workarea[3] // nrows
    x, y, w, h = 0, 0, width, height
    for i, window in enumerate(_order_windows(windows, active_window)):
        x, y = divmod(i % (nrows * ncols), nrows)
        x *= width
        y *= height
        _move_resize_window(window, x, y, w, h)

def colgrid22(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 2)
def colgrid23(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 3)
def colgrid24(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 4)
def colgrid32(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 2)
def colgrid33(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 3)
def colgrid34(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 4)
def colgrid42(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 2)
def colgrid43(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 3)
def colgrid44(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 4)

# Layout handlers.
LAYOUT_HANDLERZ = {
    'cascade': cascade,
    'hstack': hstack,
    'vstack': vstack,
    'bmain': bmain,
    'lmain': lmain,
    'rmain': rmain,
    'tmain': tmain,
    'rowgrid22': rowgrid22,
    'rowgrid23': rowgrid23,
    'rowgrid24': rowgrid24,
    'rowgrid32': rowgrid32,
    'rowgrid33': rowgrid33,
    'rowgrid34': rowgrid34,
    'rowgrid42': rowgrid42,
    'rowgrid43': rowgrid43,
    'rowgrid44': rowgrid44,
    'colgrid22': colgrid22,
    'colgrid23': colgrid23,
    'colgrid24': colgrid24,
    'colgrid32': colgrid32,
    'colgrid33': colgrid33,
    'colgrid34': colgrid34,
    'colgrid42': colgrid42,
    'colgrid43': colgrid43,
    'colgrid44': colgrid44,
}
