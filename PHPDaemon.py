# -*- coding: utf-8 -*-
from Services import ManagerServices, template
from optparse import OptionParser
import os
from re import match
from commands import getstatusoutput
import json

SERVICE_ID = "1"
SERVICE_TEMPLATE = "php-daemon.conf"
SERVICE_FORMAT = ""
PHPBIN = "/usr/bin/php"
PROJECT_PATH = "/var/www/html/bigtwo_engine_web_v2/"

parser = OptionParser()
parser.add_option("-P", "--project", dest="project",
                  help="enter project name", action="store")

parser.add_option("-A", "--action", dest="action",
                  help="Enter the action:[start|restart|stop|update|status]", action="store")


class PHPDAEMON(object):
    def __init__(self, serverid=SERVICE_ID, phpbin=PHPBIN, project_root=PROJECT_PATH):
        """
        说明:
        :param serverid:
        :param phpbin:
        :param project_root:
        """
        self.serverid = serverid
        self.phpbin = phpbin
        self.project_root = project_root
        self.service = ManagerServices(command='initctl', suffix='conf', services_path='/etc/init/')

    def get_project_list(self):
        l = [i for i in os.listdir(self.project_root) if os.path.isdir(os.path.join(self.project_root, i))]
        return [i for i in l if match(r'^[A-Za-z1-9]*^', i)]

    @staticmethod
    def project_re(p):
        if isinstance(p, basestring):
            re_str = "GE_{0}_.*\.conf$".format(p.upper())
        else:
            raise TypeError("Not String type for %s" %p)
        print re_str
        return re_str

    def manager(self, project, action):
        re_str = self.project_re(project)
        services = self.service.list_services(re_str)
        print services
        for i in services:
            print self.service.turn_service(i, action)

    def get_params(self, project):
        exec_file = os.path.join(self.project_root, project, 'install.php')
        if os.path.isfile(exec_file):
            cmd = "{0} {1} {2}".format(self.phpbin, exec_file, self.serverid)
        else:
            raise IOError("File not found for %s" %exec_file)

        (status, output) = getstatusoutput(cmd)

        if status != 0:
            raise RuntimeError("%s" %output)

        data = json.loads(output)
        if data['status'] != 'ok':
            raise RuntimeError("result have error")

        return data['result']

    def update(self, project):
        re_str = self.project_re(project)
        items = self.get_params(project)
        old_services = self.service.list_services(re_str)
        new_services = [i['service'] for i in items]
        remove_services = list(set(old_services).difference(set(new_services)))
        add_services = list(set(new_services).difference(set(old_services)))
        for i in old_services:
            self.service.delete_service(i)

        for item in items:
            content = template(template_name=SERVICE_TEMPLATE,
                               service=item['service'],
                               exec_path=item['exec'],
                               params=item['params'],
                               ServiceENV=item['env']
            )
            self.service.update_service(item['service'], content)
        return len(old_services),len(add_services)

def main(project, action):
    daemon = PHPDAEMON()
    projectlist = daemon.get_project_list()
    if project in projectlist:
        if action in ['start','status','stop','restart']:
            daemon.manager(project, action)
        elif action == 'update':
            daemon.update(project)
        else:
            parser.print_help()
    else:
        print "The project does not exist"
        print projectlist

if __name__ == '__main__':
    daemon = PHPDAEMON()
    (options, args) = parser.parse_args()
    if options.project and options.action:
        main(options.project, options.action)
    else:
        parser.print_help()
