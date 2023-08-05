# awd

a window director;

awd directs [ewmh][]-compatible x windows managers to layout windows;

awd is not a window manager; so there is no need to replace the current window
manager;

## install

    pip install awd

## usage

to run awd in command line:

    awd [options]

it is recommended to bind awd command to a keyboard shortcut; consult your
window manager documentation for how to do this; alternatively, use
[`xbindkeys`][xbindkeys];

## example

-   cascade:

        awd --cascade

-   horizontal tile:

        awd --horizontal

-   vertical tile:

        awd --vertical

## troubleshoot

### enable debug mode

enable debug mode for additional logs:

    awd --debug

### hide desktop icons

some file managers manage the desktop by adding a window containing icons; this
can be disabled with any of these commands:

    dconf write /org/gnome/desktop/background/show-desktop-icons false

    gsettings set org.gnome.background show-desktop-icons false

### exclude windows by names

if there are windows that awd doesnt handle properly, they can be excluded:

    awd --exclude {name}

awd will ignore windows whose names contain `name`;

`--exclude` can be used multiple times;

## license

Copyright (C) 2016-2018 Cyker Way

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

[GNU General Public License v3.0]: https://www.gnu.org/licenses/gpl-3.0.txt
[ewmh]: https://specifications.freedesktop.org/wm-spec/wm-spec-latest.html
[xbindkeys]: https://www.nongnu.org/xbindkeys/xbindkeys.html

