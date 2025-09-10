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


def _get_settings():
    """Get settings dictionary from json file.

    Create json file if it does not exist and (re)initialize it if needed.
    """
    settings_folder = utils.get_user_dir(SETTINGS_SUBFOLDER)
    settings_file =  settings_folder / SETTINGS_FILENAME
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
    with open(SETTINGS_FILE, "w", encoding="utf-8") as fsettings:
        json.dump(settings, fsettings)


def get_settings_file_path(_):
    """Path to settings file."""
    return str(SETTINGS_FILE)


def get_wheel_source(_):
    """Getter for wheel source preference."""
    settings = _get_settings()
    return settings["wheel_source"]


def set_wheel_source(_, value):
    """Setter for wheel source preference."""
    settings = _get_settings()
    settings["wheel_source"] = value
    _set_settings(settings)


def get_path_to_wheel(_):
    """Getter for path to wheel preference."""
    settings = _get_settings()
    return settings["path_to_wheel"]


def set_path_to_wheel(_, value):
    """Setter for path to wheel preference."""
    settings = _get_settings()
    settings["path_to_wheel"] = value
    _set_settings(settings)


def get_path_to_folder(_):
    """Getter for path to folder preference."""
    settings = _get_settings()
    return settings["path_to_folder"]


def set_path_to_folder(_, value):
    """Setter for path to folder preference."""
    settings = _get_settings()
    settings["path_to_folder"] = value
    _set_settings(settings)


def get_reinstall_upon_reloading(_):
    """Getter for 'reinstall upon reloading' preference."""
    settings = _get_settings()
    return settings["reinstall_upon_reloading"]


def set_reinstall_upon_reloading(_, value):
    """Setter for 'reinstall upon reloading' preference."""
    settings = _get_settings()
    settings["reinstall_upon_reloading"] = value
    _set_settings(settings)
