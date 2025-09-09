# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools

import addon_utils

ADDON_NAME = "BlendLuxHelper"

def get_bl_idname():
    """Get bl_idname from __package__."""
    components = __package__.split('.')
    prefix = list(itertools.takewhile(lambda x: x != ADDON_NAME, components))
    prefix.append(ADDON_NAME)
    return '.'.join(prefix)

def get_blc_module():
    """Get BlendLuxCore module."""
    modules = (m for m in addon_utils.modules() if m.bl_info["name"] == "BlendLuxCore")
    for module in modules:
        break
    else:
        module = None
    return module

def get_user_dir(name):
    """Get a user writeable directory, create it if not existing."""
    return pathlib.Path(
        bpy.utils.extension_path_user("blendluxcore", path=name, create=True)
    )
