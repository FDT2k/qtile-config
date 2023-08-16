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

import subprocess, json
import sys
from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
from typing import List  # noqa: F401
#from rofi import Rofi
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

#rofi_l = Rofi(rofi_args=['-theme', '~/.config/rofi/left_toolbar.rasi'])
#rofi_r = Rofi(rofi_args=['-theme', '~/.config/rofi/right_toolbar.rasi'])


def get_net_dev():
    get_dev = "ip addr show | awk '/inet.*brd/{print $NF; exit}'"
    ps = subprocess.Popen(get_dev,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode('ascii').strip()
    return(output)


internet = ' Yei Internet is working!'
def get_public_ip():
    try:
        raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
        answer = raw.json()["Answer"].split()[4]
    except Exception as e:
        return "0.0.0.0"
    else:
        return answer
       
public_ip = get_public_ip()

if public_ip.startswith('0'):
    internet = "OMG You Have No Internet"
    
wifi = get_net_dev()
if wifi.startswith('w'):
    wifi_icon=' '
else:
    wifi_icon=' '


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
            'Spotify':'i',
            'crx_edcmabgkbicempmpgmniellhbjopafjh':'s',
            'calendar.google.com':'s'
            }

    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    if group:
        client.togroup(group)

home = os.path.expanduser('~')

#pywall import 
# from https://github.com/gibranlp/QARSlp/blob/6da11eb970a8b2560912eddef1615ebbbc19a048/dotfiles/.config/qtile/funct.py#L26
##### Import Pywal Palette ##### 
with open(home + '/.cache/wal/colors.json') as wal_import:
    data = json.load(wal_import)
    wallpaper = data['wallpaper']
    alpha = data['alpha']
    colors = data['colors']
    val_colors = list(colors.values())
    def getList(val_colors):
        return [*val_colors]
    
def init_colors():
    return [*val_colors]

color = init_colors()


def network_widget(qtile):
    get_ssid = "iwgetid -r"
    pos = subprocess.Popen(get_ssid,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ssid = pos.communicate()[0].decode('ascii').strip()
    get_status = "nmcli radio wifi"
    ps = subprocess.Popen(get_status,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    status = ps.communicate()[0].decode('ascii').strip()
    if status == 'enabled':
        connected = ' Turn Wifi Off'
        active = "off"
    else:
        connected = ' Turn Wifi On'
        active= "on"
    options = [connected,' Bandwith Monitor (CLI)', ' Network Manager (CLI)', ' Network Manager (GUI)']
    index, key = rofi_r.select(wifi_icon + internet + "\n ", options)
    if key == -1:
        rofi_r.close()
    else:
        if index ==0:
            subprocess.run("nmcli radio wifi " + active, shell=True)
        elif index==1:
            qtile.cmd_spawn(term + ' -e bmon')
        elif index==2:
            qtile.cmd_spawn(term + ' -e nmtui')
        else:
            qtile.cmd_spawn('nm-connection-editor')
        
class command:
    #terminal = get_alternatives(['terminator', 'gnome-terminal', 'xterm'])
    autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), 'bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')
    home_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/home-layout.sh')
    work_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/vertical_layout.sh')
    samsung_screen_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/samsung-uwide-no-edp.sh')
    samsung_screen_dual_layout = os.path.join(os.path.dirname(__file__), 'bin/monitor_layout/samsung-uwide-with-edp.sh')
    terminal = "terminator -b"
    volume_up = os.path.join(os.path.dirname(__file__), 'bin/raisevolume')
    volume_down =  os.path.join(os.path.dirname(__file__), 'bin/lowervolume')
    volume_mute =  os.path.join(os.path.dirname(__file__), 'bin/mutevolume')
    shoot = os.path.join(os.path.dirname(__file__), 'bin/shot.sh')
    record = os.path.join(os.path.dirname(__file__), 'bin/record.sh')
    browser = os.path.join(os.path.dirname(__file__), 'bin/run.sh browser.d Browser')
    app_menu = os.path.join(os.path.dirname(__file__), 'bin/run.sh run.d App')
    configure = os.path.join(os.path.dirname(__file__), 'bin/run.sh configure.d Configure')
    run = os.path.join(os.path.dirname(__file__), 'bin/run')
    pacman = os.path.join(os.path.dirname(__file__), 'bin/run.sh pacman.d Pacman')
    barrier = os.path.join(os.path.dirname(__file__), 'bin/run.sh barrier.d Barrier')
    middle_screen_brightness = os.path.join(os.path.dirname(__file__), 'bin/brightness.sh HDMI-A-1')
    right_screen_brightness = os.path.join(os.path.dirname(__file__), 'bin/brightness.sh DVI-I-1')
    left_screen_brightness = os.path.join(os.path.dirname(__file__), 'bin/brightness.sh DVI-I-1-0')
    sound = os.path.join(os.path.dirname(__file__), 'bin/pulsaudio/sound-output.sh')
    theme = os.path.join(os.path.dirname(__file__), 'bin/theme/pick')
    screen_layout = os.path.join(os.path.dirname(__file__), 'bin/run.sh screenlayout.d "Monitor Layout"')
    

class theme:
    bg = "#283033"
    fg = "#FFFFFF"
    bg_active = "#ea3b0a"
    margin = 10

def set_vertical_monitor_layout(qtile):
    qtile.cmd_spawn(command.home_screen_layout)


def set_horizontal_monitor_layout(qtile):
    qtile.cmd_spawn(command.work_screen_layout)

def set_samsung_monitor_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_layout)

def set_samsung_monitor_dual_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_dual_layout)


curr_screen=0
def toggle_screen_focus(qtile):
    global curr_screen
    screen_name = "middle"
    if curr_screen == 0:
        curr_screen = 1
        screen_name = "right"
    elif curr_screen == 1:
        curr_screen = 2
        screen_name="left"
    else:
        curr_screen = 0


    qtile.cmd_spawn("notify-send --hint=string:x-dunst-stack-tag:screenfocus  \"focused %s screen \"" % screen_name)
    qtile.cmd_to_screen(curr_screen)
    move_cursor(curr_screen)

    


def move_cursor( arg):
    screeninfo = [
      s for s in subprocess.check_output("xrandr").decode("utf-8").split()\
      if s.count("+") == 2
    ]
   # logger.error("screens %s" , screeninfo)
    #if arg == "left":
    #    match = [s for s in screeninfo if s.endswith("+0+0")][0]
    #elif arg == "right":
    #    match = [s for s in screeninfo if not s.endswith("+0+0")][0]
    match = screeninfo[arg]
    data = [item.split("x") for item in match.split("+")]
   # logger.error("data %s" , data)

    numbers = [int(n) for n in [item for sublist in data for item in sublist]]
   # logger.error("numbers %s" , numbers)

    coord = [str(int(n)) for n in [(numbers[0]/2)+numbers[2], (numbers[1]/2)+numbers[3]]]
   # logger.error("coords %s" , coord)

    subprocess.Popen(["xdotool", "mousemove", coord[0], coord[1]])




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


    Key([mod, alt,shft], "Down", lazy.layout.shrink()),
    Key([mod, alt,shft], "Up", lazy.layout.grow()),

    Key([mod, shft], "Return", lazy.layout.toggle_split()),

    Key([mod, shft], "n", lazy.layout.normalize()),

#screen focus
    Key([mod], "q",lazy.function(toggle_screen_focus) ),
   

    # Computer control
    Key([mod, ctrl], "r", lazy.restart()),
    Key([mod, ctrl], "q", lazy.shutdown()),
    Key([mod], "l", lazy.spawn(command.lock)),
    Key([mod], "Return", lazy.spawn(command.terminal)),


    Key([mod], "w", lazy.window.kill()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, shft], "Tab", lazy.screen.prev_group()),
    Key([mod, ctrl], "l", lazy.spawn(command.suspend)),




    # Toggle between different layouts as defined below


    #Key([mod], "r", lazy.spawncmd()),


    #app shortcuts

    #Key([mod, alt], "n", lazy.spawn("networkmanager_dmenu")),
    Key([mod, alt], "q", lazy.spawn(command.browser)),
    Key([mod, alt], "a", lazy.spawn(command.app_menu)),
    Key([mod], "r", lazy.spawn(command.run)),
    Key([mod, alt], "p", lazy.spawn(command.pacman)),
    Key([mod, alt], "b", lazy.spawn(command.barrier)),
    Key([mod, alt], "t", lazy.spawn(command.theme)),

    Key([mod, alt], "e", lazy.spawn(command.configure)),
    Key([mod, alt], "s", lazy.spawn(command.sound)),
    Key([mod, alt], "l", lazy.spawn(command.screen_layout)),

    #screens options
    Key([mod, alt], "2", lazy.spawn(command.middle_screen_brightness)),
    Key([mod, alt], "3", lazy.spawn(command.right_screen_brightness)),
    Key([mod, alt], "1", lazy.spawn(command.left_screen_brightness)),
   # Key([mod, alt], "n", lazy.function(network_widget)),
    
    # launch graphic layout
#    Key([mod, alt], "y", lazy.function(set_vertical_monitor_layout)),
#    Key([mod, alt], "x", lazy.function(set_horizontal_monitor_layout)),
#    Key([mod, alt], "c", lazy.function(set_samsung_monitor_layout)),
#    Key([mod, alt], "v", lazy.function(set_samsung_monitor_dual_layout)),

    Key([mod, alt], '9', lazy.spawn(command.volume_down)),


    # sounds & printscreen
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(command.volume_down)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(command.volume_up)),
    Key([], "XF86AudioMute", lazy.spawn(command.volume_mute)),
   # Key([mod,alt], "+", lazy.spawn(command.volume_up)),
    Key([], 'Print', lazy.spawn(command.shoot)),
    Key([shft], 'Print', lazy.spawn(command.record)),




]

#groups = [Group(i) for i in "asdfuiop"]

groups = [
    Group('a', label='a'),
    Group('s', label='s'),
    Group('d', label='d'),
    Group('f', label='f'),
    Group('u', label='u'),
    Group('i', label='i'),
    Group('o', label='o'),
    Group('p', label='p'),
#    Group(name='l' ,label='plop', matches=[Match(wm_class=["firefox"])]),
    Group('y', label= 'y'),
    Group('x', label= 'x'),
    Group('c', label= 'c'),
    Group('v', label= 'v'),
    Group('b', label= 'b')

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


groups.append(ScratchPad("scratchpad",[
        DropDown("term", "terminator -r \"dialog\" -p hold -l floating   -b")
        ]))

keys.extend([
    Key([mod], 'F12', lazy.group['scratchpad'].dropdown_toggle('term')),
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
                margin=theme.margin
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

FONT_SIZE=12



screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),

                 widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.GroupBox(disable_drag= True,
                                background="#CACACA",
                                foreground=theme.fg,
                                active='#000000',
                                inactive= "#999999",
                                this_current_screen_border=theme.bg_active,
                                borderwidth=1,
                                highlight_method='block',
                                font='Open Sans',
                                fontsize=12
                                ),
                widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◤",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Prompt(),


                widget.WindowName(padding=0),

               # widget.TextBox("default config", name="default"),

                 widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.NetGraph(
                    bandwidth_type="up",
                    type="linefill",
                    background="#CACACA",

                    line_width=1
                ),

                 widget.CPUGraph(
                    type="box",
                    graph_color=theme.bg_active,
                    border_color=theme.bg_active,
                    background="#CACACA",
                    border_width=2,
                    line_width=1
                ),
                 widget.MemoryGraph(
                    type="box",
                    graph_color=theme.bg_active,
                    border_color=theme.bg_active,
                    background="#CACACA",

                    border_width=2,
                    line_width=1
                ),
                widget.Battery(),
                 widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.Systray(),
                widget.Clock(format='%d.%m.%Y %H:%M'),

         #       widget.Volume(get_volume_command="pamixer --get-volume",emoji=True),
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
   #         widget.WindowName(),
   #         widget.Systray(),
#            widget.Prompt(name="proj"),
            ], 30),
        ),
    Screen(
        top=bar.Bar([
            widget.CurrentLayout(),
            widget.GroupBox(disable_drag= True),
#            widget.Prompt(),
   #         widget.WindowName(),
   #         widget.Systray(),
#            widget.Prompt(name="proj"),
            ], 30),
        )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
     Click([mod,shft], "Button1", lazy.window.toggle_floating()),
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
""" floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'role': 'dialog'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'xcalc'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'eww'}
], border_color=theme.bg_active) """

floating_layout = layout.Floating(float_rules=[
        Match(wm_type='utility'),
        Match(wm_type='notification'),
        Match(wm_type='toolbar'),
        Match(wm_type='splash'),
        Match(wm_type='dialog'),
        Match(wm_class='file_progress'),
        Match(wm_class='confirm'),
        Match(wm_class='dialog'),
        Match(wm_class='download'),
        Match(wm_class="xcalc"),
        Match(wm_class='error'),
        Match(wm_class='notification'),
        Match(wm_class='splash'),
        Match(wm_class='toolbar'),
        Match(func=lambda c: c.has_fixed_size()),
        Match(func=lambda c: c.has_fixed_ratio())
],border_color=theme.bg_active)

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
