"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import pylons_globals, render_mako as render
from pylons import c, config, session
#from pylons.i18n import _, ungettext, N_, get_lang, set_lang
from pylons.i18n import _, get_lang, set_lang, add_fallback
from webhelpers.html import literal

from webgriffith.model import meta

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
        
    def __before__(self):
        session_changed = False
        if 'lang' not in session:
            session['lang'] = config["view.language"]
            session_changed = True
        if 'template' not in session:
            session['template'] = config["view.template"]
            session_changed = True
        if 'items_per_page' not in session:
            session['items_per_page'] = int(config["view.items_per_page"])
            session_changed = True

        if session_changed:
            session.save()

        set_lang(session['lang'])
        #add_fallback('griffith')

        #c.config = config
        #c.session = session
        c.header = config["view.header"]


def render_def(template_name, name, **kwargs):
    globs = pylons_globals()
 
    if kwargs:
        globs = globs.copy()
        globs.update(kwargs)
 
    template = globs['app_globals'].mako_lookup.get_template(template_name).get_def(name)
    return literal(template.render_unicode(**globs))
