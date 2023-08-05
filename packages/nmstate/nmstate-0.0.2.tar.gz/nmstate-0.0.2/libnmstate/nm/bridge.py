#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from libnmstate.nm import nmclient


BRIDGE_TYPE = 'linux-bridge'


def create_setting(iface_state, base_con_profile):
    bridge = iface_state.get(BRIDGE_TYPE)
    if not bridge:
        return None

    bridge_setting = None
    if base_con_profile:
        bridge_setting = base_con_profile.get_setting_bridge()
        if bridge_setting:
            bridge_setting = bridge_setting.duplicate()

    if not bridge_setting:
        bridge_setting = nmclient.NM.SettingBridge.new()

    return bridge_setting


def get_info(device):
    """
    Provides the current active values for a device
    """
    info = {}
    if device.get_device_type() == nmclient.NM.DeviceType.BRIDGE:
        info[BRIDGE_TYPE] = {
            'port': []
        }
    return info
