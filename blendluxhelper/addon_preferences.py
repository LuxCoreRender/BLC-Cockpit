# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired by
# https://github.com/blender/blender/tree/main/scripts/addons_core/node_wrangler
# https://github.com/blender/blender/tree/main/intern/cycles/blender/addon/properties.py

_needs_reload = "bpy" in locals()

import bpy

from . import utils
from . import operators

if _needs_reload:
    import importlib

    utils = importlib.reload(utils)
    operators = importlib.reload(operators)

enum_sources = (
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

    source: bpy.props.EnumProperty(
        name="Source",
        description="PyLuxCore source",
        items=enum_sources,
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

    def draw(self, context):
        layout = self.layout
        layout.label(text="PyLuxCore source:")

        # Source selector
        row = layout.row()
        row.prop(self, "source", expand=True)

        if self.source == "PyPI":
            return

        # From this point, we deal with local files

        box = layout.box()

        if self.source == "LocalWheel":
            # File
            row = box.row()
            row.prop(self, "path_to_wheel")

        if self.source == "LocalFolder":
            # Folder
            row = box.row()
            row.prop(self, "path_to_folder")

        row = box.row()
        row.prop(self, "reinstall_upon_reloading")

        row = box.row()
        row.operator(operators.BLH_InstallWheel.bl_idname, text="Reinstall wheel")
