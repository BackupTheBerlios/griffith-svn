# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007 Michael Jahn
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

plugin_name		= 'AdultFilmDatabase.com'
plugin_description	= 'ADULTFILMDATABASE.COM'
plugin_url		= 'www.adultfilmdatabase.com'
plugin_language		= _('English')
plugin_author		= 'Michael Jahn'
plugin_author_email	= '<mikej06@hotmail.com>'
plugin_version		= '1.0'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.adultfilmdatabase.com/video.cfm?videoid=" + self.movie_id

	def get_image(self):
		self.image_url = 'http://www.adultfilmdatabase.com/Graphics/Boxes/200' + gutils.trim(self.page, '/Graphics/Boxes/200', '"')

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<h2>', '</h2>')

	def get_title(self):
		self.title = gutils.trim(self.page, '<h2>', '</h2>')

	def get_director(self):
		self.director = ''
		delimiter = ''
		elements = string.split(self.page, '<a HREF="/director.cfm')
		elements[0] = ''
		for element in elements:
			if element <> '':
				self.director = self.director + gutils.trim(element, '>', '<') + delimiter
				delimiter = ', '

	def get_plot(self):
		self.plot = gutils.trim(self.page, 'COLSPAN="2"><BR>', '</td>')

	def get_year(self):
		self.year = gutils.strip_tags(gutils.trim(self.page, 'Year:', '<tr>'))

	def get_runtime(self):
		self.runtime = gutils.strip_tags(gutils.trim(self.page, 'Length:', '<tr>'))

	def get_genre(self):
		self.genre = gutils.trim(self.page, 'Genres:</td>', '</td>')
		if self.genre == '':
			self.genre = gutils.trim(self.page, 'Genre:</td>', '</td>')
		self.genre = self.genre.replace('\t', '')
		self.genre = self.genre.replace('\n', '')
		self.genre = self.genre.replace('\r', '')
		
	def get_cast(self):
		self.cast = ''
		elements = string.split(self.page, '<a HREF="/actor.cfm')
		elements[0] = ''
		for element in elements:
			if element <> '':
				self.cast = self.cast + gutils.trim(element, '<U>', '</U>') + '\n'

	def get_studio(self):
		self.studio = gutils.trim(self.page, 'Studio:', '<tr>')

	def get_site(self):
		self.site = 'http://www.adultfilmdatabase.com/video.cfm?videoid=' + self.movie_id

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search   = "http://www.adultfilmdatabase.com/lookup.cfm?searchtype=Video&find="
		self.translated_url_search = "http://www.adultfilmdatabase.com/lookup.cfm?searchtype=Video&find="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		return gutils.trim(self.page, "Search Results for", "	</tr>")

	def get_searches(self):
		elements = string.split(self.page, '\t\t\t\t\t\t<a HREF="/video.cfm?videoid=')
		if len(elements) > 1:
			elements[0] = ''
			for element in elements:
				if element <> '':
					self.ids.append(gutils.before(element, '"'))
					title = gutils.trim(element, "<U>", "</U>")
					if title == '':
						title = gutils.strip_tags(gutils.trim(element, '>', '</a>'))
					self.titles.append(title)
		else:
			videoid = gutils.trim(self.page, 'VideoID" VALUE="', '">')
			if videoid <> '':
				self.ids.append(videoid)
				self.titles.append(gutils.trim(self.page, '<h2>', '</h2>'))
