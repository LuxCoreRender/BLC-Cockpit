# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Getters and setters for settings.

This module implements the synchronization between the addon preferences and
the input file exported to BlendLuxCore.
"""

_needs_reload = "bpy" in locals()

import json

import bpy

from . import utils

if _needs_reload:
    import importlib

    utils = importlib.reload(utils)


SETTINGS_FILENAME = "blc_settings.json"
SETTINGS_SUBFOLDER = "settings"
SETTINGS_INIT = {
    "wheel_source": 0,
    "path_to_wheel": None,
    "path_to_folder": None,
    "reinstall_upon_reloading": False,
}


def get_settings_file_path():
    """Path to settings file."""
    settings_folder = utils.get_user_dir(SETTINGS_SUBFOLDER)
    settings_file =  settings_folder / SETTINGS_FILENAME
    return settings_file


def _get_settings():
    """Get settings dictionary from json file.

    Create json file if it does not exist and (re)initialize it if needed.
    If settings file path is not known (BlendLuxCore not installed), return
    internal dictionary.
    """
    if not (settings_file := get_settings_file_path()):
        raise RuntimeError("Missing BlendLuxCore")

    settings_file.touch(exist_ok=True)
    try:
        with open(settings_file, "r", encoding="utf-8") as fsettings:
            return json.load(fsettings)
    except json.JSONDecodeError:
        with open(settings_file, "w", encoding="utf-8") as fsettings:
            # (Re)init settings file
            json.dump(SETTINGS_INIT, fsettings)
        return _get_settings()


def _set_settings(settings):
    """Write settings in json file."""
    if not (settings_file := get_settings_file_path()):
        raise RuntimeError("Missing BlendLuxCore")
    settings_file = get_settings_file_path()
    with open(settings_file, "w", encoding="utf-8") as fsettings:
        json.dump(settings, fsettings)


def _get(setting):
    """Read a given setting."""
    settings = _get_settings()
    return settings[setting]


def _set(setting, value):
    """Set a given setting."""
    settings = _get_settings()
    settings[setting] = value
    _set_settings(settings)


def get_wheel_source(_):
    """Getter for wheel source preference."""
    return _get("wheel_source")


def set_wheel_source(_, value):
    """Setter for wheel source preference."""
    _set("wheel_source", value)


def get_path_to_wheel(_):
    """Getter for path to wheel preference."""
    return _get("path_to_wheel")


def set_path_to_wheel(_, value):
    """Setter for path to wheel preference."""
    _set("path_to_wheel", value)


def get_path_to_folder(_):
    """Getter for path to folder preference."""
    return _get("path_to_folder")


def set_path_to_folder(_, value):
    """Setter for path to folder preference."""
    _set("path_to_folder", value)


def get_reinstall_upon_reloading(_):
    """Getter for 'reinstall upon reloading' preference."""
    return _get("reinstall_upon_reloading")


def set_reinstall_upon_reloading(_, value):
    """Setter for 'reinstall upon reloading' preference."""
    _set("reinstall_upon_reloading", value)
