# -*- coding: utf-8 -*-
from os import path, remove, listdir
from commands import getstatusoutput
import errno
from jinja2 import Environment, FileSystemLoader
from re import match


def template(template_name,
             searchpath="templates",
             *args,
             **kwargs):
    """
    :param template_name:
    :param searchpath:
    :param args:
    :param kwargs:
    :return:
    """
    env = Environment(loader=FileSystemLoader(searchpath))
    _template = env.get_template(template_name)
    service_str = _template.render(*args, **kwargs)
    return service_str


class ManagerServices(object):
    def __init__(self, command, suffix, services_path):
        self.command = command
        self.suffix = suffix
        self.services_path = services_path

    def path_service(self, service):
        service_file = "{0}.{1}".format(service, self.suffix)
        full_path = path.join(self.services_path, service_file)
        return full_path

    def update_service(self, service, content, replace=False):
        service_file = self.path_service(service)
        if path.exists(service_file) and replace == False:
            return

        try:
            f = open(service_file, 'w')
            try:
                f.write(content)
            finally:
                f.close()
        except IOError as e:
            if e.errno not in (errno.ENOENT, errno.EISDIR, errno.EINVAL):
                raise

    def delete_service(self, service):
        service_file = self.path_service(service)
        self.turn_service(service, 'stop')
        if self.command == 'systemctl':
            self.turn_service(service, 'disable')
        remove(service_file)

    def turn_service(self, service, action):
        cmd = "{0} {1} {2}".format(self.command, action, service)
        (status, output) = getstatusoutput(cmd)
        return output

    def list_services(self, re_str):
       l = [i for i in listdir(self.services_path) if match(re_str, i)]
       return [i.split('.')[0] for i in l]
