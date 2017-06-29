# -*- coding: utf-8 -*-
from os import path, remove, listdir
from commands import getstatusoutput
import errno
from jinja2 import Environment, FileSystemLoader
from re import match


def template(template_name,
             searchpath="/root/ServiceManager/templates/",
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
    vars = dict(*args, **kwargs)
    service_str = _template.render(vars)
    return service_str

def get_template(template_name, dir='templates'):
    """
    Loads and returns a template for the given name.
    """
    _ENV = Environment(loader=FileSystemLoader(dir))
    return _ENV.get_template(template_name)

def render_to_string(template_name, context=None, dir=None):
    """
    Loads a template and renders it with a context. Returns a string.
    """
    if dir:
        template = get_template(template_name, dir)
    else:
        template = get_template(template_name)
    return template.render(context)


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
        service_file_path = self.path_service(service)
        if replace == False and path.exists(service_file_path):
            return

        with open(name=service_file_path, mode='w') as f:
            f.write(content)

    def delete_service(self, service):
        service_file_path = self.path_service(service)
        self.turn_service(service, 'stop')
        if self.command == 'systemctl':
            self.turn_service(service, 'disable')
        remove(service_file_path)

    def turn_service(self, service, action):
        cmd = "{0} {1} {2}".format(self.command, action, service)
        (status, output) = getstatusoutput(cmd)
        return output

    def list_services(self, re_str):
       l = [i for i in listdir(self.services_path) if match(re_str, i)]
       return [i.split('.')[0] for i in l]

class BaseServices(object):
    def __init__(self, command=None, suffix=None, service_directory=None, project_directory=None):
        self.command = command
        self.suffix = suffix
        self.services_path = service_directory
        self.project_directory = project_directory

    def path_service(self, service):
        service_file = "{0}.{1}".format(service, self.suffix)
        full_path = path.join(self.services_path, service_file)
        return full_path

    def update_service(self, service, content, replace=False):
        service_file_path = self.path_service(service)
        if replace == False and path.exists(service_file_path):
            return

        with open(name=service_file_path, mode='w') as f:
            f.write(content)

    def delete_service(self, service):
        service_file_path = self.path_service(service)
        self.turn_service(service, 'stop')
        if self.command == 'systemctl':
            self.turn_service(service, 'disable')
        remove(service_file_path)

    def turn_service(self, service, action):
        cmd = "{0} {1} {2}".format(self.command, action, service)
        (status, output) = getstatusoutput(cmd)
        return output

    def list_services(self, re_str):
       l = [i for i in listdir(self.services_path) if match(re_str, i)]
       return [i.split('.')[0] for i in l]