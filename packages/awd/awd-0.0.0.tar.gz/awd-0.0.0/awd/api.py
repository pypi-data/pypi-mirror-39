#!/usr/bin/env python3

'''Xlib/EWMH API module.'''

from Xlib.display import Display
from ewmh import EWMH

# Display object.
disp = None

# EWMH object.
ewmh = None

def _get_display():
    '''
    Get the display object.

    Returns
    -------
    object
        The display object.
    '''
    global disp
    if disp is None:
        disp = Display()
    return disp

def _get_ewmh():
    '''
    Get the EWMH object.

    Returns
    -------
    object
        The EWMH object.
    '''
    global ewmh
    if ewmh is None:
        ewmh = EWMH()
    return ewmh

def get_windows():
    '''
    Get all X Windows managed by the Window Manager.

    Sticky windows are excluded.

    Returns
    -------
    list
        A list of windows managed by the Window Manager.
    '''
    ewmh = _get_ewmh()
    windows = []
    for w in ewmh.getClientList():
        wm_state = ewmh.getWmState(w, True)
        if '_NET_WM_STATE_STICKY' not in wm_state:
            windows.append(w)
    return windows

def get_desktop_geometry():
    '''
    Get the common size of all desktops.

    Returns
    -------
    list
        The common size of all desktops.
    '''
    ewmh = _get_ewmh()
    return list(ewmh.getDesktopGeometry())

def get_desktop_viewport():
    '''
    Get the top left corner of each desktop's viewport.

    Returns
    -------
    list
        The [top, left] corner of each desktop's viewport.
    '''
    ewmh = _get_ewmh()
    return list(ewmh.getDesktopViewPort())

def get_current_desktop():
    '''
    Get the index of the current desktop.

    Returns
    -------
    int
        The index of the current desktop.
    '''
    ewmh = _get_ewmh()
    return ewmh.getCurrentDesktop()

def get_active_window():
    '''
    Get the active window.

    Returns
    -------
    object
        The active window object.
    '''
    ewmh = _get_ewmh()
    return ewmh.getActiveWindow()

def get_workarea():
    '''
    Get the work area.

    Returns
    -------
    list
        The work area [x, y, w, h].
    '''
    ewmh = _get_ewmh()
    return list(ewmh.getWorkArea())

def get_wm_name(window):
    '''
    Get name of the window.

    Parameters
    ----------
    window : object
        A window object.

    Returns
    -------
    str
        Name of the window.
    '''
    ewmh = _get_ewmh()
    return ewmh.getWmName(window).decode()

def get_wm_desktop(window):
    '''
    Get the desktop the window is in.

    Parameters
    ----------
    window : object
        A window object.

    Returns
    -------
    int
        A desktop number.
    '''
    ewmh = _get_ewmh()
    return ewmh.getWmDesktop(window)

def set_active_window(window):
    '''
    Set the active window.

    Parameters
    ----------
    window : object
        A window object.

    Returns
    -------
    None
        None.
    '''
    ewmh = _get_ewmh()
    ewmh.setActiveWindow(window)
    ewmh.display.flush()

def move_resize_window(window, x, y, w, h):
    '''
    Changes the size and location of the specified window.

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
    disp = _get_display()
    window.configure(x=x, y=y, width=w, height=h)
    disp.flush()

