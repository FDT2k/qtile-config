from libqtile.config import Group, ScratchPad, DropDown, Match
from libqtile.log_utils import logger
from libqtile import layout, bar, widget, hook
from workspace_state import workspace_state
from workspace_conf import workspaces,rooms,get_group_name
# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.


def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [ get_group_name(workspace, room) for room in rooms]

def to_workspace(workspace):
    """ Change current workspace to another one.
    """
    def f(qtile):
       
        current_workspace = workspace_state.get_current()
        
        # Sauvegarde du groupe actif
        workspace_state.set_active_group(current_workspace, qtile.current_group.name)
        
        # Mise à jour de l'espace de travail courant
        workspace_state.set_current(workspace)
       
        #dispatch the workspace's groups in order on each screen
        for idx,screen in enumerate(qtile.screens):
            g = qtile.groups_map[
                get_group_name(workspace,rooms[idx])
            ]
            screen.set_group(g)
            for i,__widget in enumerate( screen.top.widgets):
               # logger.error("screens %s %s" , type(__widget) is widget.groupbox.GroupBox, __widget)
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
        current_workspace = workspace_state.get_current()
        qtile.groups_map[get_group_name(current_workspace, room)].cmd_toscreen(toggle=False)
    return f

def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        active_group = workspace_state.get_active_group(workspace)
        qtile.current_window.togroup(active_group)
    return f

def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        current_workspace = workspace_state.get_current()
        qtile.current_window.togroup(get_group_name(current_workspace, room))
    return f

