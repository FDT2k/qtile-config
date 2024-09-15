from libqtile.config import Group, ScratchPad, DropDown, Match


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

# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        groups.append(Group(get_group_name(workspace, room)))




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



#end of workspaces