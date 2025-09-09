# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

_needs_reload = "bpy" in locals()

import json
import os

import bpy

from . import utils
from . import get_set

if _needs_reload:
    import importlib

    utils = importlib.reload(utils)
    get_set = importlib.reload(get_set)

SPLIT_FACTOR = 1 / 3

enum_wheel_sources = (
    ("PyPI", "PyPI", "Get PyLuxCore from Python Package Index (PyPI)", 0),
    (
        "LocalWheel",
        "Local Wheel",
        "Get PyLuxCore from a local wheel file, not including dependencies",
        1,
    ),
    (
        "LocalFolder",
        "Local Wheel + dependencies",
        "Get PyLuxCore from a local folder, containing PyLuxCore wheel "
        "and all its dependencies",
        2,
    ),
)

class BLH_Settings(bpy.types.AddonPreferences):
    """Addon preferences panel."""

    bl_idname = utils.get_bl_idname()

    wheel_source: bpy.props.EnumProperty(
        name="Source",
        description="PyLuxCore source",
        items=enum_wheel_sources,
        # default="PyPI",
        get=get_set.get_wheel_source,
        set=get_set.set_wheel_source,
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

    settings_file: bpy.props.StringProperty(
        name="Settings file",
        get=get_set.get_settings_file_path,
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

        # Settings file
        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR)
        split.label(text="Settings file:")
        split.prop(self, "settings_file", text="")

    def draw(self, context):
        self._draw_settings()

# Register new operator
def register():
    bpy.utils.register_class(BLH_Settings)

def unregister():
    bpy.utils.unregister_class(BLH_Settings)
