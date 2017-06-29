from jinja2 import Environment, FileSystemLoader


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