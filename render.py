import jinja2
import os
import urllib

def guess_autoescape(template_name):
    """Use autoescape for all the templates we've got so far.

    """
    return True

tmpldir = os.path.join(os.path.dirname(__file__), 'templates')
loader = jinja2.FileSystemLoader(tmpldir, encoding='utf-8')
myenv = jinja2.Environment(loader=loader,
                           trim_blocks=True, autoescape=True,
                           line_statement_prefix="#")
myenv.filters['urlencode'] = urllib.quote

def render(template_name, context={}):
    """Render the template named in `template`.

    - `context` may be used to provide variables to the template.

    """
    template = myenv.get_template(template_name)
    return template.render(context)
