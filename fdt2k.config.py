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

import subprocess
import json
import sys
import os
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
from typing import List  # noqa: F401

from fdt2k_workspaces import *
#from fdt2k_widgets import *

groups = []


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
       
        #'VirtualBox Manager': 'o',
        #'discord': 'p',
        #'spotify': 'i',
        #'Spotify': 'i',
        #'crx_edcmabgkbicempmpgmniellhbjopafjh': 's',
        #'calendar.google.com': 's',
        'bia-manager-electron':'d'
    }
    wm_class = client.window.get_wm_class()[0]
    group = apps.get(wm_class, None)
    logger.error("class %s %s" , wm_class,group)
    if group:
        client.togroup(get_group_name(wsp['current'], group))
        #to_room(group)
#        client.togroup(group)



home = os.path.expanduser('~')

# pywall import
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



class theme:
    bg = color[0]
    fg = color[7]
    bg_active = color[1]
    contrasted = color[6]
    bg_other=  color[8]
     
    margin = 10

class theme_neg:
    bg = color[2]
    fg = color[0]
    bg_active = color[6]
    contrasted = color[7]
    bg_other=  color[6]
    
    margin = 10





groups=init_groups(groups)


groups.append(ScratchPad(name='scratchpad', dropdowns=[
    DropDown('terminal', 'terminator', width=0.9,
             height=0.9, x=0.05, y=0.05, opacity=0.95, match =Match(wm_class='terminator'), on_focus_lost_hide=False),
    DropDown('spotify', 'spotify', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=0.8, match =Match(wm_class='spotify'), on_focus_lost_hide=False),
    DropDown('telegram', 'telegram-desktop', width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=1, match =Match(wm_class='telegram-desktop'), on_focus_lost_hide=False),
    DropDown('mixer', 'pavucontrol', width=0.4,
             height=0.6, x=0.3, y=0.1, opacity=1),
    DropDown('bitwarden', 'bitwarden-desktop',
             width=0.6, height=0.6, x=0.2, y=0.1, opacity=1 ,match =Match(wm_class='bitwarden-desktop'), on_focus_lost_hide=False),
    DropDown('clickup', 'clickup',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='clickup'), on_focus_lost_hide=False),
    DropDown('thunderbird', 'thunderbird',
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,on_focus_lost_hide=False),
    DropDown('blueman', 'blueman-manager',
             width=0.4, height=0.6, x=0.3, y=0.1, opacity=1 ,on_focus_lost_hide=False),
    DropDown('gitahead', 'gitahead',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='gitahead'), on_focus_lost_hide=False),
    DropDown('doc', 'google-chrome-stable',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='google-chrome'), on_focus_lost_hide=False),          
     DropDown('discord', 'discord',
              width=0.8, height=0.8, x=0.1, y=0.1, opacity=1,match =Match(wm_class='discord'), on_focus_lost_hide=False),              
],single=True))

keys.extend([
    Key([mod,ctrl], "1", lazy.group['scratchpad'].dropdown_toggle('terminal')),
    Key([mod,ctrl], "2", lazy.group['scratchpad'].dropdown_toggle('telegram')),
    Key([mod,ctrl], "3", lazy.group['scratchpad'].dropdown_toggle('bitwarden')),
    Key([mod,ctrl], "4", lazy.group['scratchpad'].dropdown_toggle('clickup')),
    Key([mod,ctrl], "5", lazy.group['scratchpad'].dropdown_toggle('blueman')),
    Key([mod,ctrl], "6", lazy.group['scratchpad'].dropdown_toggle('thunderbird')),
    Key([mod,ctrl], "8", lazy.group['scratchpad'].dropdown_toggle('gitahead')),
    Key([mod,ctrl], "9", lazy.group['scratchpad'].dropdown_toggle('mixer')),
    Key([mod,ctrl], "0", lazy.group['scratchpad'].dropdown_toggle('doc')),
    Key([mod,ctrl], "d", lazy.group['scratchpad'].dropdown_toggle('discord')),

])

# Assign shared hotkeys for each room we have.
# Decision about actual group to open is made dynamically.
for room in rooms:
    keys.append(Key([mod], room, lazy.function(
        to_room(room))))
    keys.append(Key([mod, "shift"], room, lazy.function(
        window_to_room(room))))

#end of workspaces

layouts = [
    #    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    layout.MonadThreeCol(
       margin=theme.margin,
       border_focus=theme.bg_active,
       border_normal=theme.bg,
       border_width=4

    ),
    layout.Max(
          border_width=2,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin
    ),
    layout.Bsp(
        border_width=4,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin
    ),
  
    #     layout.Columns(),
    # layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(
      
       # active_fg=theme.bg_active,
        active_bg=theme.bg_active,
        bg_color=theme.bg,
        panel_width=200,
          border_width=2,
        border_focus=theme.bg_active,
        border_normal=theme.bg,
        margin=theme.margin,
        section_top=theme.margin,
        section_bottom=theme.margin,
        margin_left=theme.margin,
        margin_y = theme.margin,
        padding_y = theme.margin
    ),
    layout.MonadTall(
       margin=theme.margin,
       border_focus=theme.bg_active,
       border_normal=theme.bg,
       border_width=4

    ),
    layout.RatioTile(
       margin=theme.margin,
       border_focus=theme.bg_active,
       border_normal=theme.bg,
       border_width=4

    ),
    # layout.VerticalTile(),
    #layout.Zoomy(columnwidth=500),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

FONT_SIZE = 12

"""
               
                widget.TextBox(
                    font="Arial",
                    foreground=color[0],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[1],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[2],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[3],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[4],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[5],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[6],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=color[7],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[8],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),

                 widget.TextBox(
                    font="Arial",
                    foreground=color[9],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[10],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                 widget.TextBox(
                    font="Arial",
                    foreground=color[11],
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                """

screens = [
    Screen(
        top=bar.Bar(
           
            [
                widget.Spacer(10),
                widget.CurrentLayoutIcon(
                    padding = 0,
                    scale = 0.5,
                ),

                widget.CurrentLayout(),
               
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.GroupBox(disable_drag=True,
                                background=theme_neg.bg,
                                foreground=theme_neg.fg,
                                active=theme_neg.fg,
                                inactive=theme_neg.contrasted,
                                this_current_screen_border=theme.bg,
                                other_current_screen_border=theme.bg_other,
                                other_screen_border=theme.bg_other,
                                borderwidth=1,
                                highlight_method='border',
                                font='Open Sans',
                                fontsize=12,
                                visible_groups=get_workspace_groups(wsp['current']),
                                ),
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◤ ",
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
                widget.Spacer(10),
            ],
            28,
            background=theme.bg,
            margin= [10,10,0,10],
            

        ),
    ),
    Screen(
        top=bar.Bar([
            widget.Spacer(10),
                widget.CurrentLayout(),
               
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◢",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
                widget.GroupBox(disable_drag=True,
                                background=theme_neg.bg,
                                foreground=theme_neg.fg,
                                active=theme_neg.fg,
                                inactive=theme_neg.contrasted,
                                this_current_screen_border=theme.bg,
                                other_current_screen_border=theme.bg_other,
                                other_screen_border=theme.bg_other,
                                borderwidth=1,
                                highlight_method='border',
                                font='Open Sans',
                                fontsize=12,
                                visible_groups=get_workspace_groups(wsp['current']),
                                ),
                widget.TextBox(
                    font="Arial",
                    foreground=theme_neg.bg,
                    text="◤ ",
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
                widget.TextBox(
                    font="Arial",
                    foreground="#CACACA",
                    text="◤ ",
                    fontsize=(FONT_SIZE*5.25),
                    padding=-1
                ),
              widget.Spacer(10),
               
            ], 28,background=theme.bg, margin= [10,10,0,10]),
    ),
    #Screen(
    #    top=bar.Bar([
    #        widget.Spacer(10),
    #            widget.CurrentLayout(),
    #           
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #           widget.GroupBox(disable_drag=True,
    #                            background=theme_neg.bg,
    #                            foreground=theme_neg.fg,
    #                            active=theme_neg.fg,
    #                            inactive=theme_neg.contrasted,
    #                            this_current_screen_border=theme.bg,
    #                            other_current_screen_border=theme.bg_other,
    #                            other_screen_border=theme.bg_other,
    #                            borderwidth=1,
    #                            highlight_method='border',
    #                            font='Open Sans',
    #                            fontsize=12,
    #                            visible_groups=get_workspace_groups(wsp['current']),
    #                            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground=theme_neg.bg,
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.Prompt(),
#
#
    #            widget.WindowName(padding=0),
#
    #            # widget.TextBox("default config", name="default"),
#
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◢",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #            widget.NetGraph(
    #                bandwidth_type="up",
    #                type="linefill",
    #                background="#CACACA",
#
    #                line_width=1
    #            ),
#
    #            widget.CPUGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.MemoryGraph(
    #                type="box",
    #                graph_color=theme.bg_active,
    #                border_color=theme.bg_active,
    #                background="#CACACA",
#
    #                border_width=2,
    #                line_width=1
    #            ),
    #            widget.TextBox(
    #                font="Arial",
    #                foreground="#CACACA",
    #                text="◤ ",
    #                fontsize=(FONT_SIZE*5.25),
    #                padding=-1
    #            ),
    #             widget.Systray(),
    #          widget.Spacer(10),
    #           
    #        ], 28,background=theme.bg, margin= [10,10,0,10]),
    #)
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Click([mod, shft], "Button1", lazy.window.toggle_floating()),
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
    {'wmclass': 'copyq'},
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
    Match(wm_class='copyq'),
    Match(wm_class="xcalc"),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='bitwarden'),
    Match(wm_class='blueman-manager'),
    Match(func=lambda c: c.has_fixed_size()),
    Match(func=lambda c: c.has_fixed_ratio())
], border_normal=theme.fg, border_focus=theme.bg,border_width=4)

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
