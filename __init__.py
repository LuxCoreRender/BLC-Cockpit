# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

_needs_reload = "bpy" in locals()

import bpy

from . import ui

if _needs_reload:
    import importlib
    ui = importlib.reload(ui)
    print(f"Reloading: {ui}")

def register():
    ui.register()

def unregister():
    ui.unregister()
