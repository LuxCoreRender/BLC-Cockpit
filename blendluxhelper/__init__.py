# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

_needs_reload = "bpy" in locals()

import bpy

from . import addon_preferences
from . import operators

if _needs_reload:
    import importlib

    addon_preferences = importlib.reload(addon_preferences)


def register():
    bpy.utils.register_class(operators.BLH_InstallWheel)
    bpy.utils.register_class(addon_preferences.BLH_Settings)


def unregister():
    bpy.utils.unregister_class(operators.BLH_InstallWheel)
    bpy.utils.unregister_class(addon_preferences.BLH_Settings)
