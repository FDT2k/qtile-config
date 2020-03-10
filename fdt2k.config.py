# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

#from libqtile import xcbq
#xcbq.keysyms["XF86AudioRaiseVolume"] = 0x1008ff13
#xcbq.keysyms["XF86AudioLowerVolume"] = 0x1008ff11
#xcbq.keysyms["XF86AudioMute"] = 0x1008ff12


import os
import subprocess
mod = "mod4"
alt = "mod1"
ctrl = "control"
shft =  "shift"

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

@hook.subscribe.client_new
def agroup(client):
    # replace class_name with the actual
    # class name of the app
    # you can use xprop to find it
    apps = {
            'Telegram': 'p',
            'VirtualBox Manager':'o',
            'Mail':'p',
            'discord':'p',
            'spotify':'i',
            'Spotify':'i'
            }

    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    if group:
        client.togroup(group)


class command:
    #terminal = get_alternatives(['terminator', 'gnome-terminal', 'xterm'])
    autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), 'bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')
    home_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/home-layout.sh')
    work_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/vertical_layout.sh')
    samsung_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/samsung-uwide-no-edp.sh')
    terminal = "terminator -b"
    volume_up = "raisevolume"
    volume_down = "lowervolume"
    shoot = os.path.join(os.path.dirname(__file__), 'bin/shot.sh')

class theme:
    bg = "#283033"
    fg = "#FFFFFF"
    bg_active = "#ea3b0a"

def set_vertical_monitor_layout(qtile):
    qtile.cmd_spawn(command.home_screen_layout)


def set_horizontal_monitor_layout(qtile):
    qtile.cmd_spawn(command.work_screen_layout)

def set_samsung_monitor_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_layout)


keys = [
    # Switch between windows in current stack pane
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod, shft], "space", lazy.layout.rotate()),



    # Move windows up or down in current stack
    Key([mod, ctrl], "Down", lazy.layout.shuffle_down()),
    Key([mod, ctrl], "Up", lazy.layout.shuffle_up()),
    Key([mod, ctrl], "Right", lazy.layout.shuffle_right()),
    Key([mod, ctrl], "Left", lazy.layout.shuffle_left()),

    Key([mod, alt], "Down", lazy.layout.grow_down()),
    Key([mod, alt], "Up", lazy.layout.grow_up()),
    Key([mod, alt], "Left", lazy.layout.grow_left()),
    Key([mod, alt], "Right", lazy.layout.grow_right()),

    Key([mod, shft], "Return", lazy.layout.toggle_split()),


    # Computer control
    Key([mod, ctrl], "r", lazy.restart()),
    Key([mod, ctrl], "q", lazy.shutdown()),
    Key([mod], "l", lazy.spawn(command.lock)),
    Key([mod], "Return", lazy.spawn(command.terminal)),


    Key([mod], "w", lazy.window.kill()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, ctrl], "l", lazy.spawn(command.suspend)),




    # Toggle between different layouts as defined below


    Key([mod], "r", lazy.spawncmd()),


    #app shortcuts

    Key([mod, alt], "n", lazy.spawn("networkmanager_dmenu")),
    Key([mod, alt], "q", lazy.spawn("brave")),
    Key([mod, alt], "w", lazy.spawn("thunderbird")),
    Key([mod, alt], "e", lazy.spawn("pavucontrol")),

    # launch graphic layout
    Key([mod, alt], "y", lazy.function(set_vertical_monitor_layout)),
    Key([mod, alt], "x", lazy.function(set_horizontal_monitor_layout)),
    Key([mod, alt], "c", lazy.function(set_samsung_monitor_layout)),


    # sounds & printscreen
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(command.volume_down)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(command.volume_up)),
    Key([], 'Print', lazy.spawn(command.shoot)),

]

#groups = [Group(i) for i in "asdfuiop"]

groups = [
    Group('a', label= 'wrk(a)'),
    Group('s', label='wrk(s)'),
    Group('d', label='proj(d)'),
    Group('f', label='read(f)'),
    Group('u', label='media(u)'),
    Group('i'),
    Group('o', label='virt(o)'),
    Group('p', label='comlink(p)'),
    Group(name='l' ,label='plop', matches=[Match(wm_class=["firefox"])]),
    Group('y', label= 'work(y)'),
    Group('x', label= 'work(x)'),
    Group('c', label= 'work(c)')

]

#groups.extend([Group('comm')])
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
    #    Key([mod, shft], i.name, lazy.window.togroup(i.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
    #     Key([mod, shft, ctrl], i.name, lazy.window.togroup(i.name)),

        # move window to group
         Key([mod, shft], i.name, lazy.window.togroup(i.name)),
    ])



#dropdown
# groups.append(
#     ScratchPad("scratchpad", [
#         # define a drop down terminal.
#         # it is placed in the upper third of screen by default.
#         DropDown("term", "terminator", opacity=0.88, height=0.55, width=0.80, ),
#
#         # define another terminal exclusively for qshell at different position
#         DropDown("qshell", "terminator -e qshell",
#                  x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
#                  on_focus_lost_hide=True)
#     ]), )
#
# keys.extend([
#     # Scratchpad
#     # toggle visibiliy of above defined DropDown named "term"
#     Key([mod], 'F12', lazy.group['scratchpad'].dropdown_toggle('term')),
#     Key([mod], 'F11', lazy.group['scratchpad'].dropdown_toggle('qshell')),
# ])


layouts = [
#    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
     layout.Bsp(
                border_width=2,
                border_focus=theme.bg_active,
                border_normal=theme.bg,
                margin=5
                ),
     layout.Max(),

#     layout.Columns(),
    # layout.Matrix(),
     layout.MonadTall(),
     layout.MonadWide(),
#     layout.RatioTile(),
    # layout.Tile(),
     layout.TreeTab(
        border_width=0,
        vspace=0,
        active_fg="000000",
        active_bg="ffffff"
     ),
    # layout.VerticalTile(),
#     layout.Zoomy(columnwidth=500),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(disable_drag= True,
                                background=theme.bg,
                                foreground=theme.fg,
                                active='#ffffff',
                                this_current_screen_border=theme.bg_active,
                                borderwidth=1,
                                highlight_method='block',
                                font='Open Sans',
                                fontsize=12
                                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("default config", name="default"),
                widget.Systray(),
                widget.Clock(format='%d.%m.%Y %H:%M'),
                widget.Battery(),
                widget.Volume(get_volume_command="pamixer --get-volume-human"),
                widget.QuickExit(),
            ],
            28,
            background=theme.bg
        ),
    ),
    Screen(
        top=bar.Bar([
            widget.CurrentLayout(),
            widget.GroupBox(disable_drag= True),
#            widget.Prompt(),
            widget.WindowName(),
            widget.Prompt(name="proj"),
            ], 30),
        )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
