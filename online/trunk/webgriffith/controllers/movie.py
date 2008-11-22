import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from webgriffith.lib.base import *
from webgriffith import model

log = logging.getLogger(__name__)
        

class MovieController(BaseController):

    def view(self, id):
        movie = meta.Session.query(model.Movie).filter_by(number=id).first()
        if movie:
            c.movie = movie
            return render("/%s/movie.mako" % session['template'])
        else:
            return abort(404)
