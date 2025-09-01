# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later
_needs_reload = "bpy" in locals()

import bpy

from .. import utils

if _needs_reload:
    import importlib
    utils = importlib.reload(utils)

enum_sources = (
    ('Standard', "Standard", "Get pyluxcore from Python Package Index (PyPI)"),
    ('Local', "Local", "Get pyluxcore from local file"),
)
bpy.types.Scene.src_type = bpy.props.EnumProperty(items=enum_sources)


class HelperAddonPreferences(bpy.types.AddonPreferences):

    bl_idname = utils.get_bl_idname()

    def draw(self, context):
        layout = self.layout

        # Source selector
        row = layout.row()
        row.label(text="Source:")
        row.prop(context.scene, "src_type", expand=True)
