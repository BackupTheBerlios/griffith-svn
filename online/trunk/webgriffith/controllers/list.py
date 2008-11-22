import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.cache import beaker_cache
from webhelpers import paginate
from math import ceil

#from webgriffith.lib.base import BaseController, render
from webgriffith.lib.base import *
from webgriffith import model

log = logging.getLogger(__name__)

class ListController(BaseController):

    #@beaker_cache(expire=60, type='memory', query_args=True)
    def page(self, id):
        page_nr = int(id) # routes will allow \d+ only here, no worry

        items_per_page = int(session['items_per_page'])
        items = meta.Session.query(model.Movie)

        page = paginate.Page(items, page=page_nr, items_per_page=items_per_page)

        if 'partial' in request.params:
            return render_def("/%s/list.mako" % session['template'], "showpage", movies=page)
        else:
            return render("/%s/list.mako" % session['template'], extra_vars={"movies": page})

    def verbose(self, id):
        page_nr = int(id) # routes will allow \d+ only here, no worry

        items_per_page = int(session['items_per_page'])
        items = meta.Session.query(model.Movie)

        page = paginate.Page(items, page=page_nr, items_per_page=items_per_page)

        if 'partial' in request.params:
            return render_def("/%s/verbose_list.mako" % session['template'], "showpage", movies=page)
        else:
            return render("/%s/verbose_list.mako" % session['template'], extra_vars={"movies": page})

