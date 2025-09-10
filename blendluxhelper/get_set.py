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


SETTINGS_FILE = utils.get_user_dir("settings") / "blc_settings.json"
SETTINGS_INIT = {
    "wheel_source": 0,
    "path": None,
}


def _get_settings():
    """Get settings dictionary from json file.

    Create json file if it does not exist and (re)initialize it if needed.
    """
    SETTINGS_FILE.touch(exist_ok=True)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as fsettings:
            return json.load(fsettings)
    except json.JSONDecodeError:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as fsettings:
            # (Re)init settings file
            json.dump(SETTINGS_INIT, fsettings)
        return _get_settings()


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
    with open(SETTINGS_FILE, "w", encoding="utf-8") as fsettings:
        json.dump(settings, fsettings)
