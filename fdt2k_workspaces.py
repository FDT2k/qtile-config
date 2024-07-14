from libqtile.log_utils import logger
from libqtile import layout, bar, widget, hook
from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from fdt2k_keybindings import *

# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    ('1', 'F1'),
    ('2', 'F2'),
    ('3', 'F3'),
    ('4', 'F4'),
    ('o', 'F5'),
    ('p', 'F6'),
]

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "asdfq"

# Oops, time for a little hack there.
# This is a global object with information about current workspace.
# (viable as config code, not sure about client-server though)
wsp = {
    'current': workspaces[0][0], # first workspace is active by default
}


# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.

def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)

# ... and information about active group in the each workspace.
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0]) # first room is active by default
    }

def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [ get_group_name(workspace, room) for room in rooms]

def to_workspace(workspace):
    """ Change current workspace to another one.
    """
    def f(qtile):
        global wsp

        # we need to save current active room(group) somewhere
        # to return to it later
        wsp[wsp['current']]['active_group'] = qtile.current_group.name

        # now we can change current workspace to the new one
        # (no actual switch there)
        wsp['current'] = workspace
        # and navigate to the active group from the workspace
        # (actual switch)
        #qtile.groups_map[
        #    wsp[workspace]['active_group']
        #].cmd_toscreen(toggle=False)
       
        #dispatch the workspace's groups in order on each screen
        for idx,screen in enumerate(qtile.screens):
            g = qtile.groups_map[
                get_group_name(workspace,rooms[idx])
            ]
            screen.set_group(g)
            for i,__widget in enumerate( screen.top.widgets):
                logger.error("screens %s %s" , type(__widget) is widget.groupbox.GroupBox, __widget)
                if type(__widget) is widget.groupbox.GroupBox :
                    __widget.visible_groups=get_workspace_groups(workspace)
                    __widget.draw()



        #set_group(self, new_group, save_prev=True, warp=True):
        # we also need to change subset of visible groups in the GroupBox widget
        #qtile.widgets_map['groupbox'].visible_groups=get_workspace_groups(workspace)

        #logger.error("screens %s" , qtile.widgets_map)
       # qtile.widgets_map['groupbox'].draw()
        # You can do some other cosmetic stuff here.
        # For example, change Bar background depending on the current workspace.
        #qtile.widgets_map['groupbox'].bar.background="ff0000"

        
    return f

def to_room(room):
    """ Change active room to another within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.groups_map[get_group_name(wsp['current'], room)].cmd_toscreen(toggle=False)
    return f

def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(wsp[workspace]['active_group'])
    return f

def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(get_group_name(wsp['current'], room))
    return f


def init_groups(groups):
    global workspaces
    global rooms
    global keys
    # Create individual Group for each (workspace,room) combination we have
    for workspace, hotkey in workspaces:
        for room in rooms:
            groups.append(Group(get_group_name(workspace, room)))

    # Assign individual hotkeys for each workspace we have
    for workspace, hotkey in workspaces:
        keys.append(Key([mod], hotkey, lazy.function(
            to_workspace(workspace))))
        keys.append(Key([mod, "shift"], hotkey, lazy.function(
            window_to_workspace(workspace))))
    return groups