# -*- coding: utf-8 -*-
from Services import BaseServices
from loader import render_to_string
import os
from re import match


class ServicesError(Exception):
    pass


class TaksManagerServices:
    def __init__(self,nodeenv , command, suffix, service_directory, project_directory):
        self.nodeenv = nodeenv
        self.command = command
        self.suffix = suffix
        self.services_path = service_directory
        self.project_directory = project_directory
        self.service = BaseServices(command='systemd', suffix='service', service_directory='/etc/systemd/system')

    def get_game_list(self):
        game_file = "gamecode_%s" %self.nodeenv
        __path = os.path.join(self.project_directory, file)
        with open(__path, 'r') as f:
             l=f.read().split('\n')
        return l

    def make_service_name(self, role='MANAGER', project='*', game='*'):
        re_str = "TM_{Role}_{ProjectName}_{Game}.service$".format(Role=role, ProjectName=project, Game=game)
        return re_str

    def manager(self, role, project, action):
        re_str = self.make_service_name(role, project)
        services = self.service.list_services(re_str)
        for i in services:
            print self.service.turn_service(i, action)

    def render(self, Game):
        Role ="MANAGER"
        Game = Game
        env = self.nodeenv
        exec_path = os.path.join(self.project_directory, "bin/www")

    def update(self, project, Role, Number=None):
        pass
