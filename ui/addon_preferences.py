# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later
import bpy

class CockpitAddonPreferences(bpy.types.AddonPreferences):

    bl_idname = __package__

    def draw(self, context):
        print("Draw")
        layout = self.layout()

        # Source selector
        row = layout.row()
        row.label(text="Source:")
        row.prop(self, "source", expand=True)
