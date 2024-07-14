from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from fdt2k_commands import *

def set_vertical_monitor_layout(qtile):
    qtile.cmd_spawn(command.home_screen_layout)

def run_prompt(qtile):
    qtile.cmd_spawn(command.run)

def set_horizontal_monitor_layout(qtile):
    qtile.cmd_spawn(command.work_screen_layout)


def set_samsung_monitor_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_layout)


def set_samsung_monitor_dual_layout(qtile):
    qtile.cmd_spawn(command.samsung_screen_dual_layout)

curr_screen = 0
def move_cursor(arg):
    screeninfo = [
        s for s in subprocess.check_output("xrandr").decode("utf-8").split()
        if s.count("+") == 2
    ]
   # logger.error("screens %s" , screeninfo)
    # if arg == "left":
    #    match = [s for s in screeninfo if s.endswith("+0+0")][0]
    # elif arg == "right":
    #    match = [s for s in screeninfo if not s.endswith("+0+0")][0]
    match = screeninfo[arg]
    data = [item.split("x") for item in match.split("+")]
   # logger.error("data %s" , data)

    numbers = [int(n) for n in [item for sublist in data for item in sublist]]
   # logger.error("numbers %s" , numbers)

    coord = [str(int(n))
             for n in [(numbers[0]/2)+numbers[2], (numbers[1]/2)+numbers[3]]]
   # logger.error("coords %s" , coord)

    subprocess.Popen(["xdotool", "mousemove", coord[0], coord[1]])
def toggle_screen_focus(qtile):
    global curr_screen
    screen_name = "middle"
    if curr_screen == 0:
        curr_screen = 1
        screen_name = "right"
    elif curr_screen == 1:
        curr_screen = 2
        screen_name = "left"
    else:
        curr_screen = 0

    qtile.cmd_spawn(
        "notify-send --hint=string:x-dunst-stack-tag:screenfocus  \"focused %s screen \"" % screen_name)
    qtile.cmd_to_screen(curr_screen)
    move_cursor(curr_screen)


def pick_theme(qtile):
     qtile.cmd_spawn(command.theme+' '+wsp['current'])


mod = "mod4"
alt = "mod1"
ctrl = "control"
shft = "shift"

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


    Key([mod, alt, shft], "Down", lazy.layout.shrink()),
    Key([mod, alt, shft], "Up", lazy.layout.grow()),

    Key([mod, shft], "Return", lazy.layout.toggle_split()),

    Key([mod, shft], "n", lazy.layout.normalize()),

    # screen focus
    Key([mod], "q", lazy.function(toggle_screen_focus)),


    # Computer control
    Key([mod, ctrl], "r", lazy.restart()),
    #Key([mod, ctrl], "q", lazy.shutdown()),
    Key([mod], "l", lazy.spawn(command.lock)),
    Key([mod], "Return", lazy.spawn(command.terminal)),


    Key([mod], "w", lazy.window.kill()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, shft], "Tab", lazy.screen.prev_group()),
   # Key([mod, ctrl], "l", lazy.spawn(command.suspend)),




    # Toggle between different layouts as defined below


    #Key([mod], "r", lazy.spawncmd()),


    # app shortcuts

    Key([mod, alt], "n", lazy.spawn("networkmanager_dmenu")),
    Key([mod, alt], "q", lazy.spawn(command.browser)),
    Key([mod, alt], "a", lazy.spawn(command.app_menu)),
    #Key([mod], "r", lazy.spawn(command.run)),
    Key([mod], "r", lazy.function(run_prompt)),
    Key([mod, alt], "p", lazy.spawn(command.pacman)),
    Key([mod, ctrl], "p", lazy.spawn(command.power)),
    Key([mod, alt], "b", lazy.spawn(command.barrier)),
   # Key([mod, alt], "t", lazy.spawn(command.theme+' '+wsp['current'])),
    Key([mod, alt], "t", lazy.function(pick_theme)),
    Key([mod, alt], "v", lazy.spawn(command.virt)),

    Key([mod, alt], "e", lazy.spawn(command.configure)),
    Key([mod, alt], "s", lazy.spawn(command.sound)),
    Key([mod, alt], "d", lazy.spawn(command.screen_layout)),

    # screens options
    Key([mod, alt], "2", lazy.spawn(command.middle_screen_brightness)),
    Key([mod, alt], "3", lazy.spawn(command.right_screen_brightness)),
    Key([mod, alt], "1", lazy.spawn(command.left_screen_brightness)),

    Key([mod, alt], "c", lazy.spawn(command.copyq)),
    

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

