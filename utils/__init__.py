# SPDX-FileCopyrightText: 2025 Authors (see AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools

ADDON_NAME = "BlendLuxHelper"

def get_bl_idname():
    """Get bl_idname from __package__."""
    components = __package__.split('.')
    prefix = list(itertools.takewhile(lambda x: x != ADDON_NAME, components))
    prefix.append(ADDON_NAME)
    return '.'.join(prefix)
