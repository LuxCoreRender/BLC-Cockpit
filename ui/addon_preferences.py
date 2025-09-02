# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired by
# https://github.com/blender/blender/blob/main/intern/cycles/blender/addon/properties.py

_needs_reload = "bpy" in locals()

import bpy

from .. import utils

if _needs_reload:
    import importlib

    utils = importlib.reload(utils)

enum_sources = (
    ("PyPI", "PyPI", "Get PyLuxCore from Python Package Index (PyPI)"),
    (
        "LocalWheel",
        "Local Wheel",
        "Get PyLuxCore from a local wheel file, not including dependencies",
    ),
    (
        "LocalBundle",
        "Local Wheel + dependencies",
        "Get PyLuxCore from a local folder, bundling PyLuxCore wheel "
        "and all its dependencies",
    ),
)


class LuxCoreHelperSettings(bpy.types.AddonPreferences):
    """Addon preferences panel."""

    bl_idname = utils.get_bl_idname()

    source: bpy.props.EnumProperty(
        name="Source",
        description="PyLuxCore source",
        items=enum_sources,
        default="PyPI",
    )

    path_to_wheel: bpy.props.StringProperty(
        name="Path to Wheel file",
        subtype="FILE_PATH",
    )

    path_to_bundle: bpy.props.StringProperty(
        name="Path to Folder containing Wheel + dependencies",
        subtype="DIR_PATH",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="PyLuxCore source:")

        # Source selector
        row = layout.row()
        row.prop(self, "source", expand=True)

        if self.source == "PyPI":
            return

        if self.source == "LocalWheel":
            # File
            row = layout.row()
            row.prop(self, "path_to_wheel")

        if self.source == "LocalBundle":
            # Folder
            row = layout.row()
            row.prop(self, "path_to_bundle")


classes = (LuxCoreHelperSettings,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
