""" Common server object.

Contains data and methods common to all types of don't starve together servers when using dstacademy's dontstarvetogether docker image.
"""

__author__ = "lego_engineer"
__maintainer__ = "lego_engineer"
__email__ = "protopeters@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2018, lego_engineer"

from pathlib import Path
from abc import ABC, abstractmethod
from dst_server_deploy.helpers import (id_generator, ask_yes_no, ask_path,
                                       choose_preset, input_int, input_csv, fileio_csv)

class ServerCommon(ABC):
    """ Common server parameters. """

    _instance = None

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

        ServerCommon._singleton_init(server_token=server_token,
                                     world_name=world_name,
                                     world_desc=world_desc,
                                     pvp_enabled=pvp_enabled,
                                     caves_enabled=caves_enabled,
                                     mods_enabled=mods_enabled,
                                     world_customization_enabled=world_customization_enabled,
                                     set_lanugage_enabled=set_lanugage_enabled,
                                     access_controls_enabled=access_controls_enabled,
                                     offline_settings_enabled=offline_settings_enabled,
                                     set_gamemode_enabled=set_gamemode_enabled,
                                     vote_enabled=vote_enabled)

        # Server specific initialization.
        if self.caves_enabled or self.world_customization_enabled:
            self._input_world_data()

    @classmethod
    def _singleton_init(cls,
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
        """ This method provides a singleton like design pattern.

        This design pattern has been chosen so that data may be shared between child classes.

        :param str server_token: The server token unique to each game owner.
        :param str world_name: The world name.
        :param str world_desc: The world description.
        :param bool pvp_enabled: Is PvP allowed?
        :param bool caves_enabled: Are caves enabled? (This will rename server files accordingly.)
        :param bool mods_enabled: Are mods to be enabled on this server?
        :param bool set_lanugage_enabled: Should the server use a non-english language?
        :param bool access_controls_enabled: Should the server have access controls
            (password / steam group)?
        :param bool offline_settings_enabled: Should the server not be listed
            online or only accessable from lan?
        :param bool set_gamemode_enabled: Should the server use a particular
            gamemode or server intentions?
        :param bool vote_enabled: Should voting be enabled on the server?
        """

        if cls._instance is None:
            cls.cluster_key = id_generator()
            cls.server_token = str(server_token)
            cls.world_name = str(world_name)
            cls.world_desc = str(world_desc)
            cls.pvp_enabled = bool(pvp_enabled)
            cls.base_container_name = "-".join(cls.world_name.split())

            # Mods are consistant. They can be defined here.
            cls.mods_enabled = bool(mods_enabled)
            cls.mod_list_csv = None
            cls.mod_override = None
            if cls.mods_enabled:
                cls._input_mod_data()

            # Language is consistant. It can be defined here.
            cls.server_language = None
            cls.language_options = ["brazilian",
                                    "bulgarian",
                                    "czech",
                                    "danish",
                                    "dutch",
                                    "english",
                                    "finnish",
                                    "french",
                                    "german",
                                    "greek",
                                    "hungarian",
                                    "italian",
                                    "japanese",
                                    "korean",
                                    "norwegian",
                                    "polish",
                                    "portuguese",
                                    "romanian",
                                    "russian",
                                    "schinese",
                                    "spanish",
                                    "swedish",
                                    "tchinese",
                                    "thai",
                                    "turkish",
                                    "ukrainian"]
            cls.set_lanugage_enabled = set_lanugage_enabled
            if cls.set_lanugage_enabled:
                cls._input_language()

            # Access controls are consistant. They can be defined here.
            cls.access_controls_enabled = access_controls_enabled
            cls.access_controls = {}
            cls.access_controls_types = ['PASSWORD', 'MAX_PLAYERS', 'WHITELIST_SLOTS', 'ADMINLIST',
                                         'WHITELIST', 'BLOCKLIST', 'STEAM_GROUP_ID',
                                         'STEAM_GROUP_ONLY', 'STEAM_GROUP_ADMINS', 'CONSOLE_ENABLE']
            for access_type in cls.access_controls_types:
                cls.access_controls[access_type] = None

            if cls.access_controls_enabled:
                cls._input_access_controls()


            cls.offline_settings_enabled = offline_settings_enabled
            cls.offline_enabled = None
            cls.lan_only = None
            if cls.offline_settings_enabled:
                cls._input_offline_settings()

            cls.set_gamemode_enabled = set_gamemode_enabled
            cls.game_mode = None
            cls.game_mode_types = ['survival', 'endless', 'wilderness']
            cls.game_intention = None
            cls.game_intention_types = ['social', 'cooperative', 'competitive', 'madness']
            if cls.set_gamemode_enabled:
                cls._input_game_mode()

            cls.voting = None
            cls.kick_voting = None
            cls.vote_enabled = vote_enabled
            if cls.vote_enabled:
                cls._input_vote_settings()

            # World presets are inconsistant. They cannot be defined here.
            cls.caves_enabled = bool(caves_enabled)
            cls.world_customization_enabled = bool(world_customization_enabled)
            if cls.caves_enabled or cls.world_customization_enabled:
                cls.shard_master_ip = cls.base_container_name + '-forest'
                cls.shard_slave_ip = cls.base_container_name + '-cave'


            # Make it so the class canot be changed again.
            cls._instance = cls

    @classmethod
    def _input_mod_data(cls):
        """ Request information regarding the server's mods. """
        if ask_yes_no("Would you like to input the mod list as a csv file?"):
            cls.mod_list_csv = fileio_csv('Please provide a relative path to your modlist.csv')
        else:
            cls.mod_list_csv = input_csv("Please provide the mod's Steam IDs as "
                                         "a comma or space seperated list")

        mod_override_path = ask_path("Please provide a relative path to your modoverrides.lua")
        with mod_override_path.open('r') as file_obj:
            # Filter out the new line characters.
            cls.mod_override = file_obj.read().replace('\n', '')

    @classmethod
    def _input_language(cls):
        """ Request information regarding the server's language. """
        cls.server_language = choose_preset(cls.language_options)

    @classmethod
    def _input_access_controls(cls):
        """ Request information regarding the server's access controls. """

        are_there_admins = False
        are_there_whitelisted = False

        if ask_yes_no("Should the maximum number of players be modified?"):
            cls.access_controls['MAX_PLAYERS'] = \
                input_int('How many players should be allowed?')

        if ask_yes_no("Should the server be linked to a Steam group?"):
            cls.access_controls['STEAM_GROUP_ID'] = \
                input_int('What Steam Group ID should the server be linked to?')

            cls.access_controls['STEAM_GROUP_ONLY'] = \
                str(ask_yes_no("Should the server be resticted to this group?")).lower()

            cls.access_controls['STEAM_GROUP_ADMINS'] = \
                str(ask_yes_no("Should Steam group admins be server admins?")).lower()

            are_there_admins = are_there_admins or cls.access_controls['STEAM_GROUP_ADMINS']

        elif ask_yes_no("Should the server be password protected?"):
            cls.access_controls['PASSWORD'] = input('What should the server password be?\n')

        if ask_yes_no("Do you wish to specify server administrators?"):
            if ask_yes_no("Would you like to input the admin list as a csv file?"):
                cls.access_controls['ADMINLIST'] = \
                    fileio_csv('Please provide a relative path to your adminlist.csv')
            else:
                cls.access_controls['ADMINLIST'] = \
                    input_csv('Please specify the Klei usernames of the server admins as comma ' \
                    'or space seperated values')

            are_there_admins = True

        if are_there_admins:
            cls.access_controls['CONSOLE_ENABLE'] = \
                str(ask_yes_no("Should the console be avalible for server admins?")).lower()

        if ask_yes_no("Do you wish to specify whitelisted players?"):
            are_there_whitelisted = True
            if ask_yes_no("Would you like to input the whitelist as a csv file?"):
                cls.access_controls['WHITELIST'] = \
                    fileio_csv('Please provide a relative path to your whitelist.csv')
            else:
                cls.access_controls['WHITELIST'] = \
                    input_csv('Please specify the Klei usernames of the whitelisted players' \
                    ' as comma or space seperated values')

        if are_there_admins or are_there_whitelisted:
            if ask_yes_no("Should spaces be reserved for admins and whitelisted players?"):
                cls.access_controls['WHITELIST_SLOTS'] = \
                    input_int('Please specify how many spaces should be reserved?')

        if ask_yes_no("Do you wish to specify blacklisted players?"):
            if ask_yes_no("Would you like to input the blacklist as a csv file?"):
                cls.access_controls['BLOCKLIST'] = \
                    fileio_csv('Please provide a relative path to your blacklist.csv')
            else:
                cls.access_controls['BLOCKLIST'] = \
                    input_csv('Please specify the Klei usernames of the blacklisted players' \
                    ' as comma or space seperated values')

    @classmethod
    def _input_offline_settings(cls):
        """ Request information regaring the server's offline settings. """
        cls.offline_enabled = not ask_yes_no('Should the server be listed publicly?')
        cls.lan_only = ask_yes_no('Is this a LAN only server?')

    @classmethod
    def _input_game_mode(cls):
        """ Request information regarding the server's game mode and intention. """
        cls.game_mode = choose_preset(cls.game_mode_types)
        cls.game_intention = choose_preset(cls.game_intention_types)

    @classmethod
    def _input_vote_settings(cls):
        """ Request information regarding server voting. """
        cls.voting = ask_yes_no('Should voting be enabled?')
        if cls.voting:
            cls.kick_voting = ask_yes_no('Should voting to kick players be enabled?')

    @abstractmethod
    def _input_world_data(self):
        """ Request information regarding the servers world data. """
        raise NotImplementedError

    @classmethod
    def _write_common_env_params(cls, path):
        """ Write out the default enviromental parameters.

        :param str or pathlib.Path path: The file of the output file. This file will be overwritten.
        """
        path = Path(path)
        if path.is_file():
            print("File '{}' already exists and will be overwritten.".format(path.resolve()))
            input("Press enter to continue, Ctrl-C to exit...")

        with path.open("w+") as file_obj:
            file_obj.write("NAME=%s\n" %cls.world_name)
            file_obj.write("TOKEN=%s\n" %cls.server_token)
            file_obj.write("DESCRIPTION=%s\n" %cls.world_desc)
            file_obj.write("PVP_ENABLE=%s\n" %str(cls.pvp_enabled).lower())
            file_obj.write("PAUSE_WHEN_EMPTY=true\n")

            if cls.caves_enabled:
                file_obj.write("SHARD_ENABLE=%s\n" %str(cls.caves_enabled).lower())
                file_obj.write("SHARD_CLUSTER_KEY=%s\n" %cls.cluster_key)
                file_obj.write("SHARD_MASTER_IP=%s\n" %cls.shard_master_ip)

            if cls.set_lanugage_enabled:
                file_obj.write("LANGUAGE=%s\n" %cls.server_language)

            if cls.access_controls_enabled:
                for access_type in cls.access_controls_types:
                    if cls.access_controls[access_type] is not None:
                        file_obj.write("%s=%s\n" %(access_type, cls.access_controls[access_type]))

            if cls.offline_settings_enabled:
                file_obj.write("OFFLINE_ENABLE=%s\n" %str(cls.offline_enabled).lower())
                file_obj.write("LAN_ONLY=%s\n" %str(cls.lan_only).lower())

            if cls.set_gamemode_enabled:
                file_obj.write("GAME_MODE=%s\n" %cls.game_mode)
                file_obj.write("INTENTION=%s\n" %cls.game_intention)

            if cls.vote_enabled:
                file_obj.write("VOTE_ENABLE=%s\n" %str(cls.voting).lower())
                file_obj.write("VOTE_KICK_ENABLE=%s\n" %str(cls.kick_voting).lower())

            if cls.mods_enabled:
                file_obj.write("\nMODS=%s\n" %cls.mod_list_csv)
                file_obj.write("MODS_OVERRIDES=%s\n\n" %cls.mod_override)
