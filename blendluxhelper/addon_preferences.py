# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""This module implements the preferences panel of the add-on."""

_needs_reload = "bpy" in locals()

import bpy
import sys
from pathlib import Path

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

# Hardcoded target directory for symlink creation
HARDCODED_TARGET_DIR = Path("/tmp/blendluxhelper_symlinks")  # Change this path if needed

class BLHSettings(bpy.types.AddonPreferences):
    """Addon preferences panel."""

    bl_idname = utils.get_bl_idname()

    wheel_source: bpy.props.EnumProperty(
        name="Source",
        description="PyLuxCore source",
        items=enum_wheel_sources,
        get=get_set.get_wheel_source,
        set=get_set.set_wheel_source,
    )

    wheel_version: bpy.props.StringProperty(
        name="Wheel version",
        description="Wheel version, for PyPI",
        get=get_set.get_wheel_version,
        set=get_set.set_wheel_version,
    )

    path_to_wheel: bpy.props.StringProperty(
        name="Path to Wheel",
        description="Path to PyLuxCore Wheel file",
        subtype="FILE_PATH",
        get=get_set.get_path_to_wheel,
        set=get_set.set_path_to_wheel,
    )

    path_to_folder: bpy.props.StringProperty(
        name="Path to Folder",
        description=(
            "Path to Folder containing PyLuxCore Wheel + the other "
            "dependencies"
        ),
        subtype="DIR_PATH",
        get=get_set.get_path_to_folder,
        set=get_set.set_path_to_folder,
    )

    reinstall_upon_reloading: bpy.props.BoolProperty(
        name="Reinstall upon reloading",
        description="Reinstall every time BlendLuxCore is reloaded",
        get=get_set.get_reinstall_upon_reloading,
        set=get_set.set_reinstall_upon_reloading,
    )

    settings_file: bpy.props.StringProperty(
        name="Settings file",
        get=lambda _: str(get_set.get_settings_file_path()),
    )

    def _draw_source_selection(self, layout):
        """Draw source selection subpanel.

        Prerequisite: BlendLuxCore must be found
        """

        if not utils.get_blc_module():
            row = layout.row()
            row.label(text="< BlendLuxCore not found >")
            return

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
            row = layout.row()
            split = row.split(factor=SPLIT_FACTOR)
            split.label(text="Wheel Version (blank for default):")
            split.prop(self, "wheel_version", text="")
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
            raise RuntimeError(f"Unhandled wheel source: {self.wheel_source}")

        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR)
        split.label(text="Reloading:")
        split.prop(self, "reinstall_upon_reloading")

        # Settings file
        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR)
        split.label(text="Output file (read-only):")
        split.prop(self, "settings_file", text="")


    def draw(self, context):
        """Draw advanced settings panel (callback)."""
        layout = self.layout

        # Draw source selection subpanel
        self._draw_source_selection(layout)
        layout.separator()

        # Add the symlink creation operator button
        row = layout.row()
        split = row.split(factor=SPLIT_FACTOR)
        split.label(text="Extension Editable Mode:")
        split.operator(
            "blendluxhelper.editable_install",
            text="Install Editable",
        )


class BLH_OT_EditableInstall(bpy.types.Operator):
    """Install an extension (namely BlendLuxCore) in editable mode.

    This operator creates a symlink to an addon source directory in a given
    Blender repository, as documented here:

    https://developer.blender.org/docs/handbook/extensions/addon_dev_setup/\
#setting-up-project

    This allows to run and test the extension while continuing to develop it.

    Nota #1: To uninstall, simply use the standard procedure for uninstalling
    extensions.
    Nota #2: This feature is for development and debugging purposes only.
    In other case, please install extension according to standard procedure.
    """
    bl_idname = "blendluxhelper.editable_install"
    bl_label = "Install Editable"
    bl_options = {'REGISTER', 'UNDO'}

    source_dir: bpy.props.StringProperty(
        name="Source Directory",
        description="Directory to link to",
        subtype="DIR_PATH"
    )
    blender_repo: bpy.props.StringProperty(
        name="Blender repository",
        description=(
            "Blender repository name where the link should be created. "
            "Nota: if this directory does not exist, it will be created."
        ),
        default="blc_dbg"
    )

    def execute(self, context):
        src = Path(self.source_dir).expanduser().resolve()
        dst_folder = Path(bpy.utils.user_resource(
            "EXTENSIONS", path=self.blender_repo, create=True)
        )
        symlink_name = src.parts[-1]
        symlink_path = dst_folder / symlink_name

        # Validate source directory
        if not src.is_dir():
            self.report({'ERROR'}, f"Source directory does not exist: {src}")
            return {'CANCELLED'}

        # Ensure target folder exists
        try:
            dst_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.report({'ERROR'}, f"Could not create target folder: {dst_folder}, error: {e}")
            return {'CANCELLED'}

        if symlink_path.exists():
            self.report({'ERROR'}, f"Symlink path already exists: {symlink_path}")
            return {'CANCELLED'}

        try:
            if sys.platform == "win32":
                symlink_path.symlink_to(src, target_is_directory=True)
            else:
                symlink_path.symlink_to(src)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create symlink: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Symlink created: {symlink_path} -> {src}")
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(BLHSettings)
    bpy.utils.register_class(BLH_OT_EditableInstall)

def unregister():
    bpy.utils.unregister_class(BLHSettings)
    bpy.utils.unregister_class(BLH_OT_EditableInstall)
