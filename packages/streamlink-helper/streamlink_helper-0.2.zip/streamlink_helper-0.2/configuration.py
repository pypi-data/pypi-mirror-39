import yaml
import requests
import os
from util import HEADERS


class Configuration:
    def __init__(self):
        directory = os.path.join(os.environ['APPDATA'], "streamlink_helper")
        if not os.path.exists(directory):
            os.makedirs(directory)
        config_path = os.path.join(directory, "config.yml")
        try:
            f = open(config_path, "r")
            f.close()
        except FileNotFoundError:
            configfile = open(config_path, "w+")
            yaml.dump({"user_id": "", "ask_on_startup": True}, configfile)
            configfile.close()

        self.__read_configuration(config_path)

    @property
    def user_id(self):
        return self._user_id

    @property
    def quality_order_of_preference(self):
        return self._quality_order_of_preference

    def __read_configuration(self, config_path):
        with open(config_path, 'r') as configfile:
            cfgdata = yaml.load(configfile)
            if cfgdata["ask_on_startup"]:
                self.__user_configure()
                if not self.user_id:
                    return
            else:
                self._user_id = cfgdata["user_id"]
                self._quality_order_of_preference = cfgdata["quality_order_of_preference"]
        with open(config_path, "w") as configfile:
            yaml.dump({"user_id": self._user_id,
                       "quality_order_of_preference": self._quality_order_of_preference,
                       "ask_on_startup": False}, configfile)

    def __user_configure(self):
        print("Your settings have not been configured yet. Set them here in the console,"
              " or edit the config.yml by hand.")
        self._user_id = self.__get_user_id()
        if not self._user_id:
            return
        self._quality_order_of_preference = self.__get_quality()

    @staticmethod
    def __get_user_id():
        username = input("Please enter the name of your twitch.tv account: ")
        params = {
            'login': username
        }
        user_id_api_url = "https://api.twitch.tv/helix/users"
        user_data_response = requests.get(user_id_api_url, params=params, headers=HEADERS)
        if not user_data_response.json()["data"]:
            print("Couldn't get id for entered username")
            return False
        else:
            user_id = user_data_response.json()["data"][0]["id"]
        return user_id

    @staticmethod
    def __get_quality():
        preferred_quality = False
        quality_list = ["160p", "360p", "480p", "720p", "1080p", "720p60", "1080p60"]
        while preferred_quality not in quality_list:
            preferred_quality = input("Please enter your preferred stream quality. Leave blank for 1080p60 or enter s "
                                      "to (s)how options: ")
            if preferred_quality == "s":
                for i in quality_list:
                    print(i)
            if not preferred_quality:
                preferred_quality = "1080p60"
        return quality_list[:(quality_list.index(preferred_quality)+1)]
