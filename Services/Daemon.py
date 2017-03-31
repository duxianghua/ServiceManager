# -*- coding: utf-8 -*-
from Services import ManagerServices, template
from optparse import OptionParser
import os
from re import match
from commands import getstatusoutput
import json
import sys

Service_Format = "TM_{Role}_{ProjectName}_{GAMEID}"

class TASKMQ(object):
    def __init__(self, Project_Path, service_directory, ServerID=None):
        self.ServerID = ServerID
        self.BIN_PATH = '/usr/bin/node'
        self.Project_Path = Project_Path
        self.service = ManagerServices(command='systemctl', suffix='service', services_path=service_directory)

    def get_game_list(self):
        __path = os.path.join(self.project_root, 'gamecode_staging')
        with open(__path, 'r') as f:
            return f.read().split('\n')

    @staticmethod
    def project_re(Project, Role):
        if isinstance(p, basestring):
            re_str = "TM_{Role}_{ProjectName}_*.service$".format(ProjectName=Project.upper(), Role=Role)
        else:
            raise TypeError("Not String type for %s" %p)
        return re_str

    def manager(self, project, action):
        re_str = self.project_re(project)
        services = self.service.list_services(re_str)
        for i in services:
            print self.service.turn_service(i, action)

    def update(self, project, Role, Number=None):
        re_str = self.project_re(project)
        if Role == 'MANAGER':
            for i in self.get_game_list:
                _role = 'MANAGER'
                _project = project
                _exec_path = '/usr/share/nodejs/taskmq-manager/bin/www'
                _env = 'staging'
                _service = "TM_{Role}_{ProjectName}_{GAMEID}".format(Role=_role, ProjectName=_project, GAMEID=i)
                content = _template('taskmq.conf',
                          role = _role,
                          project = _project,
                          exec_path = _exec_path,
                          service = _service,
                          env = _env
                    )
                self.service.update_service(item['service'], content)

        elif Role == 'WORKER':
            pass
        else:
            raise ValueError("Role type error: %s" %Role)
