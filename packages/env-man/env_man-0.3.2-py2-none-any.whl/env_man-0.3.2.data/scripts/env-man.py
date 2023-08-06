#!python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import platform
import string
import sys
from os.path import join
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
import re
import json


class EnvFile:
    def __init__(self):
        self.env_content = {}
        self.app_config = {}
        self.current_env = ''
        self.env_list = []
        self.env_root = ''
        self.configs_path = ''
        self.style = None

    @property
    def style(self):
        return self.style

    @style.setter
    def style(self, value):
        self.style = value

    @property
    def configs_path(self):
        return self.configs_path

    @configs_path.setter
    def configs_path(self, value):
        self.configs_path = value

    @property
    def env_root(self):
        return self.env_root

    @env_root.setter
    def env_root(self, value):
        self.env_root = value

    @property
    def env_content(self):
        return self.env_content

    @env_content.setter
    def env_content(self, value):
        self.env_content = value

    @property
    def app_config(self):
        return self.app_config

    @app_config.setter
    def app_config(self, value):
        self.app_config = value

    @property
    def current_env(self):
        return self.current_env

    @current_env.setter
    def current_env(self, value):
        self.current_env = value

    @property
    def env_list(self):
        return self.env_list

    @env_list.setter
    def env_list(self, value):
        self.env_list = value

    @staticmethod
    def read(path):
        regex = re.compile(r'''^([^\s=]+) *=(?:[\s"']*)(.*?)(?:[\s"']*)$''')
        result = {}

        with open(path) as file:
            for line in file:
                match = regex.match(line)
                if match is not None:
                    result[match.group(1)] = match.group(2)

        return result

    def import_file(self, path, env_name):
        self.env_content[env_name] = self.read(path)
        self.env_content[env_name]["CURRENT_ENVIRONMENT"] = env_name
        pprint(self.env_content)

    def export_file(self, env_name, path=''):
        template = string.Template('$key="$value"\n')
        path = path if path != '' else env_name.lower() + ".env"

        with open(path, 'w') as env_file:
            for key, value in self.env_content[env_name.lower()].items():
                env_file.write(template.substitute(key=unicode(key), value=unicode(value)))
                pprint(template.substitute(key=unicode(key), value=unicode(value)))

        print()

    def save(self):
        for env_name in self.env_list:
            self.save_config(join(self.configs_path, env_name + '.config'), self.env_content[env_name])

        self.save_config(join(self.env_root, 'env-man.config'), self.app_config)

    @staticmethod
    def save_config(file_path, content):
        with open(file_path, 'w') as outfile:
            json.dump(content, outfile, indent=4, sort_keys=True)

    def load(self):
        self.env_root = os.path.abspath(__file__).replace('env-man.py', '')
        self.app_config = self.load_config(self.env_root + 'env-man.config')
        self.current_env = self.app_config["CURRENT_ENVIRONMENT"]
        self.env_list = self.app_config["ENVIRONMENT_LIST"]

        if 'CONFIGS_PATH' in self.app_config.keys():
            self.configs_path = self.app_config['CONFIGS_PATH']
        else:
            self.configs_path = ''

        if self.configs_path == '':
            self.set_configs_path()

        for env_name in self.env_list:
            self.env_content[env_name] = self.load_config(join(self.configs_path, env_name + '.config'))

    def set_configs_path(self):
        configs_path_questions = [
            {
                'type': 'input',
                'name': 'configs_path',
                'message': 'Inform the path for Environment Configuration Files:'
            }
        ]

        self.configs_path = prompt(configs_path_questions, style=self.style)['configs_path']

        if self.configs_path == '':
            confirm_path_questions = [
                {
                    'type': 'confirm',
                    'name': 'confirm_path',
                    'message': 'Should I set default path? (' + self.env_root + ')',
                    'default': False
                }
            ]

            if prompt(confirm_path_questions, style=self.style)['confirm_path']:
                self.configs_path = self.env_root
                self.app_config["CONFIGS_PATH"] = self.configs_path
                self.save_config(self.env_root + 'env-man.config', self.app_config)
            else:
                print('Please set the configs path directory using (ChangeConfigsDirectory) menu option')
        else:
            self.app_config["CONFIGS_PATH"] = self.configs_path
            self.save_config(self.env_root + 'env-man.config', self.app_config)

    @staticmethod
    def load_config(file_path):
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                return json.load(json_file)

    def set_variables(self, env_name, current_os):
        if current_os == 'Darwin':
            self.set_mac_variables(env_name.lower())
        elif current_os == 'Linux':
            self.set_linux_variables(env_name.lower())
        elif current_os == 'Windows':
            self.set_windows_variables(env_name.lower())
        else:
            return

        self.current_env = env_name

        #
        # if os.path.isfile(self.env_root + env_name + '.config'):
        #     with open(self.env_root + env_name + '.config') as json_file:
        #         self.env_content = json.load(json_file)

    def clear_variables(self, current_os):
        if current_os == 'Darwin':
            self.clear_mac_variables(self.current_env)
        elif current_os == 'Linux':
            self.clear_linux_variables(self.current_env)
        elif current_os == 'Windows':
            self.clear_windows_variables(self.current_env)

        self.current_env = ''

    def set_windows_variables(self, env_name):
        template = string.Template('setx $key "$value"')

        for key, value in self.env_content[env_name.lower()].items():
            print(template.substitute(key=key, value=value))
            os.system(template.substitute(key=key, value=value))

    def set_mac_variables(self, env_name):
        export_commands = '#env-man-begin\n'
        template = string.Template('export $key="$value"\n')

        for key, value in self.env_content[env_name.lower()].items():
            export_commands += template.substitute(key=key, value=value)

        export_commands += '#env-man-end\n'

        with open(os.path.expanduser('~/.env-man_profile'), 'w+') as base_profile:
            base_profile.write(export_commands)

        print(export_commands)

    def set_linux_variables(self, env_name):
        pass

    def clear_mac_variables(self, current_env):
        export_commands = '#env-man-begin\n'
        template = string.Template('export $key="$value"\n')

        for key, value in self.env_content[current_env].items():
            export_commands += template.substitute(key=key, value='')

        export_commands += '#env-man-end\n'

        with open(os.path.expanduser('~/.env-man_profile'), 'w+') as base_profile:
            base_profile.write(export_commands)

        print(export_commands)

    def clear_linux_variables(self, current_env):
        pass

    def clear_windows_variables(self, current_env):
        template = string.Template('setx $key ""')

        for key, value in self.env_content[current_env.lower()].items():
            print(template.substitute(key=key, value=value))
            os.system(template.substitute(key=key))


def main(argv):
    env_man = EnvFile()
    env_man.load()
    current_os = platform.system()

    env_man.style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    if len(argv) > 1 and argv[0] == 'set':
        env_name = argv[1]
        env_man.set_variables(env_name, current_os)
    else:
        print('Hi, welcome to Environment Manager')

        op_mode_questions = [
            {
                'type': 'rawlist',
                'name': 'opmode',
                'message': 'Choose the action:',
                'choices': ['ReadEnv', 'ImportEnv', 'ExportEnv', 'SetEnvironment',
                            'ClearEnvironment', 'Save', 'Reload', 'ChangeConfigsDirectory', 'Exit']
            }
        ]

        env_questions = [
            {
                'type': 'rawlist',
                'name': 'env',
                'message': 'Choose the environment:',
                'choices': env_man.env_list
            },
        ]

        path_questions = [
            {
                'type': 'input',
                'name': 'path',
                'message': 'Inform the path:'
            }
        ]

        op_mode = prompt(op_mode_questions, style=env_man.style)
        chosen_op_mode = op_mode['opmode']

        while chosen_op_mode != 'Exit':
            # pprint(op_mode['opmode'])

            if chosen_op_mode == 'ReadEnv':
                env_path = prompt(path_questions, style=env_man.style)['path']
                pprint(env_man.read(env_path))

            elif chosen_op_mode == 'ImportEnv':
                env_path = prompt(path_questions, style=env_man.style)['path']
                env_name = prompt(env_questions, style=env_man.style)['env'].lower()
                env_man.import_file(env_path, env_name)

            elif chosen_op_mode == 'ExportEnv':
                env_path = prompt(path_questions, style=env_man.style)['path']
                env_name = prompt(env_questions, style=env_man.style)['env'].lower()
                env_man.export_file(env_name, env_path)

            elif chosen_op_mode == 'Save':
                env_man.save()

            elif chosen_op_mode == 'Reload':
                env_man.load()

            elif chosen_op_mode == 'SetEnvironment':
                env_name = prompt(env_questions, style=env_man.style)['env'].lower()
                env_man.set_variables(env_name, current_os)

            elif chosen_op_mode == 'ClearEnvironment':
                env_man.clear_variables(current_os)

            elif chosen_op_mode == 'ChangeConfigsDirectory':
                env_man.set_configs_path()

            op_mode = prompt(op_mode_questions, style=env_man.style)
            chosen_op_mode = op_mode['opmode']


if __name__ == "__main__":
    main(sys.argv[1:])
