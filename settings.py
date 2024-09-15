
import os
import json

mod = "mod4"
alt = "mod1"
ctrl = "control"
shft = "shift"

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