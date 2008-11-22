import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from webgriffith.lib.base import BaseController, render
#from webgriffith import model

log = logging.getLogger(__name__)

class SettingsController(BaseController):

    def index(self):
        c.session = session
        return render("/%s/settings.mako" % session['template'])

    def set(self):
        session_changed = False
        if 'lang' in request.params:
            lang = request.params['lang']
            if lang in ('en', 'pl', 'de'): # TODO: get all supported translations via lib.get_translations()
                session['lang'] = lang
                session_changed = True
        if 'tpl' in request.params:
            template = request.params['tpl']
            if template in ('default',): # TODO: get from lib.get_templates()
                session['template'] = tpl
                session_changed = True
        if 'items' in request.params:
            try:
                items_per_page = int(request.params['items'])
            except:
                log.warning("Wrong number for items_per_page: %s", request.params['items_per_page'])
            else:
                if items_per_page < 2:
                    items_per_page = 1
                session['items_per_page'] = items_per_page
                session_changed = True
        if session_changed:
            session.save()

        redirect_to(action='index', id=None)
