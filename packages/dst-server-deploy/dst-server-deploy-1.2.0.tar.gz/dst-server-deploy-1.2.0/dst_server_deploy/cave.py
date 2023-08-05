""" Cave Server Deployement fo ruse with  dstacademy's dontstarvetogether docker image.

If you want help setting these things, look at https://github.com/fairplay-zone/docker-dontstarvetogether/blob/develop/docs/configuration.md for reference.
"""

__author__ = "lego_engineer"
__maintainer__ = "lego_engineer"
__email__ = "protopeters@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2018, lego_engineer"

from dst_server_deploy.helpers import ask_yes_no, choose_preset, ask_path
from dst_server_deploy import ServerCommon
from dst_server_deploy.data.presets import CAVE as CAVE_PRESETS

class CaveServer(ServerCommon):
    """ Cave (underworld) specific data. """

    def __init__(self,
                 server_token,
                 world_name,
                 world_desc,
                 pvp_enabled=False,
                 caves_enabled=False,
                 mods_enabled=False,
                 world_customization_enabled=False,
                 set_lanugage_enabled=False,
                 access_controls_enabled=False,
                 offline_settings_enabled=False,
                 set_gamemode_enabled=False,
                 vote_enabled=False):

        # Custom stuff
        self.is_master = False
        self.container_port = '11000'
        self.presets = CAVE_PRESETS

        super().__init__(server_token = server_token,
                         world_name = world_name,
                         world_desc = world_desc,
                         pvp_enabled = pvp_enabled,
                         caves_enabled = caves_enabled,
                         mods_enabled = mods_enabled,
                         world_customization_enabled = world_customization_enabled,
                         set_lanugage_enabled = set_lanugage_enabled,
                         access_controls_enabled = access_controls_enabled,
                         offline_settings_enabled = offline_settings_enabled,
                         set_gamemode_enabled = set_gamemode_enabled,
                         vote_enabled = vote_enabled)

        if self.caves_enabled:
            self.container_name = self.shard_slave_ip
        else:
            self.container_name = self.base_container_name
        self.env_file_path = self.container_name + '.env'

    def _input_world_data(self):
        """ Request information regarding the server's world data. """

        if not self.world_customization_enabled:
            self.level_override = self.presets['DEFAULT']
        else:
            if ask_yes_no("Would you like to select a caves/underworld world configuration from presets?"):
                self.level_override = self.presets[choose_preset(self.presets.keys())]
            else:
                level_override_path = ask_path('Please provide a relative path to a ' \
                                               'caves/underworld leveldataoverride.lua')
                with level_override_path.open('r') as file_obj:
                    # Strip out the new line characters.
                    self.level_override = file_obj.read().replace('\n', '')

    def write_env_param(self):
        """ Write the enviromental parameters to file. """
        self._write_common_env_params(self.env_file_path)
        with open(self.env_file_path, "a") as file_obj:
            if self.caves_enabled:
                file_obj.write("SHARD_IS_MASTER=%s\n" %str(self.is_master).lower())
                file_obj.write("SHARD_NAME=%s\n" %self.container_name)
                file_obj.write("SERVER_PORT=%s\n" %self.container_port)

            if self.caves_enabled or self.world_customization_enabled:
                file_obj.write("\nLEVELDATA_OVERRIDES=%s\n\n" %self.level_override)
