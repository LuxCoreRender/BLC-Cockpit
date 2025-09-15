# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Helper for BlendLuxCore development and testing.

This helper is a Blender addon, which provides ability to configure the way
pyluxcore is loaded in BlendLuxCore.
The configuration is exported to BlendLuxCore via a json file, placed in a user
directory.
"""

_needs_reload = "bpy" in locals()

import bpy

from . import addon_preferences

if _needs_reload:
    import importlib

    addon_preferences = importlib.reload(addon_preferences)
    print(f"Reloading: {__package__}")


def register():
    addon_preferences.register()


def unregister():
    addon_preferences.unregister()
