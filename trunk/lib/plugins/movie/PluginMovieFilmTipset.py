# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie
import string
import re

plugin_name = "FilmTipset.se"
plugin_description = "FilmTipset.se"
plugin_url = "www.filmtipset.se"
plugin_language = _("Swedish")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.0"

class Plugin(movie.Movie):

	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = 'http://www.filmtipset.se/film/' + str(self.movie_id)

	def get_image(self):
		self.image_url = ''
		tmp = gutils.trim(self.page, 'src="posters/', '"')
		if tmp != '':
			self.image_url = 'http://www.filmtipset.se/posters/' + tmp

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, 'Originaltitel:', '</span>')
		if self.o_title == '':
			self.o_title = gutils.trim(self.page, '<h1>', '</h1>')

	def get_title(self):
		self.title = gutils.trim(self.page, '<h1>', '</h1>')

	def get_director(self):
		self.director = gutils.trim(self.page, 'Regiss&ouml;r:', '</span>')

	def get_plot(self):
		self.plot = gutils.trim(self.page, 'Filminfo:', '</h2>')

	def get_year(self):
		self.year = gutils.trim(self.page, 'Utgivnings&aring;r:', '</span>')

	def get_runtime(self):
		self.runtime = string.strip(gutils.trim(self.page, 'L&auml;ngd:', ' min'))

	def get_genre(self):
		self.genre = string.strip(gutils.trim(self.page, 'Nyckelord:', '</span>'))

	def get_cast(self):
		self.cast = gutils.trim(self.page, 'Sk&aring;despelare:', '</span>')
		self.cast = string.replace(self.cast, ', ', '\n')

	def get_classification(self):
		self.classification = ''

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = string.strip(gutils.trim(self.page, 'Produktionsland:', '</span>'))

	def get_rating(self):
		self.rating = "0"

	def get_notes(self):
		self.notes = ''
		tmp = gutils.trim(self.page, 'Alt. titel:', '</span>')
		if tmp != '':
			self.notes = self.notes + 'Alt. titel:' + string.strip(gutils.strip_tags(tmp))


class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search   = "http://www.filmtipset.se/search.cgi?field=name&field=orgname&show_graded=1&search_value="
		self.translated_url_search = "http://www.filmtipset.se/search.cgi?field=name&field=orgname&show_graded=1&search_value="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page, 'Matchning', 'Hittade')
		return self.page

	def get_searches(self):
		elements1 = re.split('href="film/', self.page)
		elements1[0] = None
		for element in elements1:
			if element <> None:
				self.ids.append(gutils.before(element,'"'))
				self.titles.append(
					string.replace(gutils.trim(element, 'title="', '"'), '&nbsp;', ' ')
				)

