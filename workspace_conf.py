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


def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)


