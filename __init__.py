# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

_needs_reload = "bpy" in locals()

import bpy

from . import blendluxhelper

if _needs_reload:
    import importlib

    blendluxhelper = importlib.reload(blendluxhelper)
    print(f"Reloading: {blendluxhelper}")


def register():
    blendluxhelper.register()


def unregister():
    blendluxhelper.unregister()
