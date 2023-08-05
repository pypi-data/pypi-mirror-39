# awd

a window director;

awd directs windows managers to do something useful; for example, to layout
windows;

awd works with any [ewmh][]-compatible x window managers, but is not a window
manager itself; so there is no need to replace the current window manager to use
awd;

## install

    pip install awd

## usage

run in command line:

    awd [options]

## shortcuts

optionally, you can bind `awd` to a keyboard shortcut. the binding method may
be wm-specific. some notable examples are:

-   in `compiz`, you can configure keyboard shortcuts with `ccsm` in menu item
    `general -> commands`.

-   in a plain x window system, you can use `xbindkeys` to configure keyboard
    shortcuts. `xbindkeys` features a tool `xbindkeys_config` for easy gui
    configuration.

for other window managers, please consult their manuals.

## troubleshooting

### enable debug mode

enable debug mode to dump window information:

    awd --debug

### hide all desktop icons

some file managers manage the desktop by adding a window containing icons. the
desktop can be disabled with either of these two commands:

    dconf write /org/gnome/desktop/background/show-desktop-icons false

    gsettings set org.gnome.background show-desktop-icons false

### hide windows by names

if there are windows that `awd` doesn't handle properly, they can be excluded:

    awd --exclude {name}

window names matching `name` won't be handled by `awd`.

multiple `--exclude` options are supported.

## license

Copyright (C) 2016 Cyker Way

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

[ewmh]: https://specifications.freedesktop.org/wm-spec/wm-spec-latest.html
[GNU General Public License v3.0]: https://www.gnu.org/licenses/gpl-3.0.txt

