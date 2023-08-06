# Created by Q-ays.
# whosqays@gmail.com


"""
    Example::

        from wisdoms.config import c
        c.get('name')
"""

import yaml
from wisdoms.utils import joint4path


def find_env(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            env = f.read().strip()
            if env:
                print('~~~~~~~~~~~~~~~~~~~~~~~~ success ~~~~~~~~~~~~~~~~~~~~~\n .env file path is ', path, '\n')
                return env
            else:
                raise Exception('contents of .env file is None')
    except FileNotFoundError as e:
        # print(e)
        print('.env file path ', path, ' match failed')
        return False


def find_config(path):
    try:
        with open(path) as f:
            print('~~~~~~~~~~~~~~~~~~~~~~~~ success ~~~~~~~~~~~~~~~~~~~~~\n config file path is ', path, '\n')
            configuration = yaml.load(f)
            if configuration:
                return configuration
            else:
                raise Exception('contents of config.yml file is None')
    except FileNotFoundError as e:
        # print(e)
        print('config.yml file path ', path, ' match failed')
        return False


class Config:
    """
    读取yml配置文件
    """

    def __init__(self, layer=4):
        """
        可自动定义层数
        :param layer:
        """

        env_path = '.env'

        env = None

        for i in range(layer):
            env = find_env(env_path)

            if env:
                break
            else:
                env_path = joint4path('..', env_path)

        self.configuration = None
        if env:
            config_path = joint4path('config', env + '.yml')

            for i in range(layer):
                configuration = find_config(config_path)

                if configuration:
                    self.configuration = configuration
                    break
                else:
                    config_path = joint4path('..', config_path)
        else:
            print('~~~~~~~~~~~~~~~~~ can not find .env file :< ~~~~~~~~~~~~~~~~~~~')

    def get(self, key):
        if self.configuration:
            return self.configuration[key]
        else:
            return {'err_code': 'maybe environment variable is missed'}

    def to_dict(self):
        if self.configuration:
            return self.configuration


# class Config:
#     """
#     读取yml配置文件
#     """
#
#     def __init__(self):
#
#         try:
#             with open('../.env', 'r', encoding='utf-8') as f:
#                 env = f.read().strip()
#         except FileNotFoundError as e:
#             print('file path is ../../.env')
#             with open('../../.env', 'r', encoding='utf-8') as f:
#                 env = f.read().strip()
#
#         if env:
#             try:
#                 with open('./config/' + env + '.yml') as f:
#                     self.configuration = yaml.load(f)
#             except FileNotFoundError as e:
#                 print('file path is ../config')
#                 with open('../config/' + env + '.yml') as f:
#                     self.configuration = yaml.load(f)
#
#     def get(self, key):
#         if self.configuration:
#             return self.configuration[key]
#         else:
#             return {'err_code': 'maybe environment variable is missed'}
#
#     def to_dict(self):
#         if self.configuration:
#             return self.configuration


c = Config(5)
