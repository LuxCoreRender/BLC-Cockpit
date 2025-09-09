# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired by
# https://github.com/blender/blender/tree/main/scripts/addons_core/node_wrangler
# https://github.com/blender/blender/tree/main/intern/cycles/blender/addon/properties.py

_needs_reload = "bpy" in locals()

import json
import os

import bpy

from . import utils

if _needs_reload:
    import importlib

    utils = importlib.reload(utils)

SPLIT_FACTOR = 1 / 3

enum_wheel_sources = (
    ("PyPI", "PyPI", "Get PyLuxCore from Python Package Index (PyPI)"),
    (
        "LocalWheel",
        "Local Wheel",
        "Get PyLuxCore from a local wheel file, not including dependencies",
    ),
    (
        "LocalFolder",
        "Local Wheel + dependencies",
        "Get PyLuxCore from a local folder, containing PyLuxCore wheel "
        "and all its dependencies",
    ),
)

class BLH_Settings(bpy.types.AddonPreferences):
    """Addon preferences panel."""

    bl_idname = utils.get_bl_idname()

    wheel_source: bpy.props.EnumProperty(
        name="Source",
        description="PyLuxCore source",
        items=enum_wheel_sources,
        default="PyPI",
    )

    path_to_wheel: bpy.props.StringProperty(
        name="Path to File",
        description="Path to PyLuxCore Wheel file",
        subtype="FILE_PATH",
    )

    path_to_folder: bpy.props.StringProperty(
        name="Path to Folder",
        description="Path to Folder containing PyLuxCore Wheel + the other dependencies",
        subtype="DIR_PATH",
    )

    reinstall_upon_reloading: bpy.props.BoolProperty(
        name="Reinstall upon reloading",
        description="Reinstall every time BlendLuxCore is reloaded",
    )

    def _draw_settings(self):
        """Draw advanced settings panel."""
        layout = self.layout

        row = layout.row()
        row.label(
            text=(
                "WARNING! THE FOLLOWING SETTINGS MAY CAUSE BLENDLUXCORE "
                "TO BECOME UNUSABLE. "
                "*** DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING. ***"
            )
        )
        # Source selector
        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR, align=True)
        split.label(text="Wheel source:")
        row = split.row()
        row.prop(self, "wheel_source", expand=True)

        if self.wheel_source == "PyPI":
            pass
        elif self.wheel_source == "LocalWheel":
            # File
            row = layout.row()
            split = row.split(factor=SPLIT_FACTOR)
            split.label(text="Path to File:")
            split.prop(self, "path_to_wheel", text="")
        elif self.wheel_source == "LocalFolder":
            # Folder
            row = layout.row()
            split = row.split(factor=SPLIT_FACTOR)
            split.label(text="Path to Folder:")
            split.prop(self, "path_to_folder", text="")
        else:
            raise RuntimeError(f"Unhandled wheel source: {wheel_source}")

        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR)
        split.label(text="Reloading")
        split.prop(self, "reinstall_upon_reloading")

    def draw(self, context):
        self._draw_settings()

# Register new operator
def register():
    bpy.utils.register_class(BLH_Settings)

def unregister():
    bpy.utils.unregister_class(BLH_Settings)
