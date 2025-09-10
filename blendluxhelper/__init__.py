# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Package initializer."""

_needs_reload = "bpy" in locals()

import bpy

from . import addon_preferences

if _needs_reload:
    import importlib

    addon_preferences = importlib.reload(addon_preferences)


def register():
    addon_preferences.register()


def unregister():
    addon_preferences.unregister()
