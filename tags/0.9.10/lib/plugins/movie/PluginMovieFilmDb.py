﻿# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007-2009 Michael Jahn
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

import gutils
import movie
import string, re

plugin_name         = 'FilmDb.de'
plugin_description  = 'FILMDB.DE'
plugin_url          = 'www.filmdb.de'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = '<mikej06@hotmail.com>'
plugin_version      = '1.1'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode   = 'iso-8859-1'
		self.movie_id = id
		self.url      = "http://www.filmdb.de/filmanzeige.php?alle=1&filmid=" + self.movie_id

	def get_image(self):
		tmp = gutils.trim(self.page, 'plakat.php?', '\'')
		if tmp:
			page_image = self.open_page(url='http://www.filmdb.de/plakat.php?' + tmp)
			tmp = gutils.trim(self.page, 'bilder.filmdb.de', '\'')
			if tmp:
				self.image_url = 'http://bilder.filmdb.de' + tmp

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<h1>', '</h1>')

	def get_title(self):
		self.title = gutils.trim(self.page, '<h1>', '</h1>')

	def get_director(self):
		self.director = ''
		elements = re.split('regisseursuche.php?', self.page)
		elements[0] = ''
		listelement = ''
		for element in elements:
			if element <> '':
				self.director = self.director + listelement + gutils.trim(element, '>', '</a>')
				listelement = ', '

	def get_plot(self):
		self.plot = gutils.trim(self.page, 'noshade style=\'color:#FFCCCC;\'>', '<')
		if self.plot == '':
			self.plot = gutils.trim(self.page, 'noshade style=\'color:#FFCCCC;\'>', '"')
		self.plot = self.plot.replace('\t', '')
		self.plot = self.plot.replace('\n', '')
		self.plot = self.plot.replace('\x93', '"')
		self.plot = self.plot.replace('\x84', '"')

	def get_year(self):
		elements = string.split(self.page, 'landjahrsuche.php')
		if len(elements) > 1:
			self.year = gutils.trim(elements[2], '>', '</a>')
		else:
			self.year = ''

	def get_runtime(self):
		self.runtime = ""
		tmp = gutils.trim(self.page, 'L&auml;nge: ', '<')
		if tmp <> '':
			elements = string.split(tmp, ':')
			try:
				hours = int(elements[0])
				mins = int(elements[1])
				self.runtime = str(hours * 60 + mins)
			except:
				self.runtime = ""

	def get_genre(self):
		self.genre = gutils.after(gutils.trim(self.page, 'genresuche.php', '</a>'), '>')

	def get_cast(self):
		self.cast = ""
		tmp = gutils.trim(self.page, 'function schauspiel()', '}')
		if tmp == '':
			tmp = self.page
		elements = string.split(tmp, 'schauspielersuche.php')
		elements[0] = ''
		for element in elements:
			if element <> '':
				self.cast = self.cast + gutils.clean(gutils.trim(element, '>', '</a>')) + '\n'

	def get_classification(self):
		self.classification = ""

	def get_studio(self):
		self.studio = ""

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = "http://www.filmdb.de/filmanzeige.php?filmid=" + self.movie_id

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		elements = string.split(self.page, 'landjahrsuche.php')
		if len (elements) > 0:
			self.country = gutils.trim(elements[1], '>', '</a>') + '\n'

	def get_rating(self):
		self.rating = gutils.trim(self.page, 'Unsere User haben diesen Film mit ', ' bewertet.')
		self.rating = self.rating.replace('%', '')
		self.rating = gutils.strip_tags(self.rating)
		elements = self.rating.split('.')
		try:
			tmprating = int(elements[0])
			self.rating = str(tmprating / 10)
		except:
			self.rating = '0'

	def get_notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search   = "http://www.filmdb.de/globalsuche.php?name="
		self.translated_url_search = "http://www.filmdb.de/globalsuche.php?name="
		self.encode                = 'iso-8859-1'
		self.remove_accents        = False

	def search(self,parent_window):
		self.open_search(parent_window)
		return self.page

	def get_searches(self):
		elements = re.split('(?:href=["]*filmanzeige[.]php[?]filmid=)', self.page)
		elements[0] = ''
		for element in elements:
			if element <> '':
				idmatch = re.search('([>]|["])', element)
				if idmatch:
					self.ids.append(element[:idmatch.end() - 1])
					self.titles.append(gutils.trim(element, '>', '<') + ' - ' +
						gutils.trim(gutils.after(element, '</a>'), '<td>', '</td>') + ' - ' +
						gutils.trim(gutils.after(element, '<td>'), '<td>', '</td>'))

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
	#
	# Configuration for automated tests:
	# dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
	#
	test_configuration = {
		'Rocky Balboa' : [  1,  1 ],
		'Arahan'       : [  1,  1 ],
		'Märchen'      : [ 23, 23 ]
	}

class PluginTest:
	#
	# Configuration for automated tests:
	# dict { movie_id -> dict { arribute -> value } }
	#
	# value: * True/False if attribute only should be tested for any value
	#        * or the expected value
	#
	test_configuration = {
		'Rocky Balboa' : { 
			'title'               : 'Rocky Balboa',
			'o_title'             : 'Rocky Balboa',
			'director'            : 'Sylvester Stallone',
			'plot'                : True,
			'cast'                : 'Dolph Lundgren\n\
Sylvester Stallone\n\
Carl Weathers\n\
Mike Tyson\n\
Burt Young\n\
Talia Shire\n\
Burgess Meredith\n\
Tony Burton\n\
Mr. T\n\
Milo Ventimiglia\n\
Frank Stallone\n\
Michael Buffer\n\
Geraldine Hughes\n\
Lahmard J. Tate\n\
Don Sherman\n\
Robert Michael Kelly\n\
LeRoy Neiman\n\
Stu Nahan\n\
Tobias Segal\n\
Skip Bayless\n\
Gunnar Peterson\n\
Marc Ratner\n\
Henry G. Sanders\n\
Rick Buchborn\n\
Ricky Cavazos\n\
Charles Johnson\n\
Angela Boyd\n\
Ana Gerena\n\
Fran Pultro\n\
Tim Carr\n\
Joe Cortez\n\
Jody Giambelluca\n\
Carter Mitchell\n\
A.J. Benza\n\
Yahya\n\
Maureen Schilling\n\
James Binns\n\
Jack Lazzarado\n\
Barney Fitzpatrick\n\
Antonio Tarver\n\
Nick Baker\n\
Jim Lampley\n\
Matt Frack\n\
Louis Giansante\n\
Kevin King Templeton\n\
Paul Dion Monte\n\
Dana Jacobson\n\
Brian Kenny\n\
Woody Paige\n\
Pedro Lovell\n\
Larry Merchant\n\
Bert Randolph Sugar\n\
Bernard Fernández\n\
Vinod Kumar\n\
Anthony Lato Jr.\n\
Max Kellerman\n\
Lou DiBella\n\
Johnnie Hobbs Jr.\n\
Jay Crawford\n\
Gary Compton\n\
James Francis Kelly III',
			'country'             : 'USA',
			'genre'               : 'Drama',
			'classification'      : False,
			'studio'              : False,
			'o_site'              : False,
			'site'                : 'http://www.filmdb.de/filmanzeige.php?filmid=Rocky Balboa',
			'trailer'             : False,
			'year'                : 2006,
			'notes'               : False,
			'runtime'             : 102,
			'image'               : True,
			'rating'              : False
		},
		'Tatort -%3Cwbr %2F%3E M%26auml%3Brchenwald' : { 
			'title'               : 'Tatort - Märchenwald',
			'o_title'             : 'Tatort - Märchenwald',
			'director'            : 'Christiane Balthasar',
			'plot'                : True,
			'cast'                : 'Maria Furtwängler\n\
Hannes Jaenicke\n\
Charly Hübner\n\
Ingo Naujoks\n\
Michael Wittenborn',
			'country'             : 'D',
			'genre'               : False,
			'classification'      : False,
			'studio'              : False,
			'o_site'              : False,
			'site'                : 'http://www.filmdb.de/filmanzeige.php?filmid=Tatort -%3Cwbr %2F%3E M%26auml%3Brchenwald',
			'trailer'             : False,
			'year'                : 2004,
			'notes'               : False,
			'runtime'             : 90,
			'image'               : True,
			'rating'              : False
		},
		'Arahan' : { 
			'title'               : 'Arahan',
			'o_title'             : 'Arahan',
			'director'            : 'Ryoo Seung-Wan',
			'plot'                : True,
			'cast'                : 'So-yi Yoon\n\
Doo-hong Jung\n\
Ryu Seung-beom\n\
Ahn Sung-ki\n\
Yun Ju-Sang',
			'country'             : 'RK',
			'genre'               : 'Actionkomödie',
			'classification'      : False,
			'studio'              : False,
			'o_site'              : False,
			'site'                : 'http://www.filmdb.de/filmanzeige.php?filmid=Arahan',
			'trailer'             : False,
			'year'                : 2004,
			'notes'               : False,
			'runtime'             : 109,
			'image'               : False,
			'rating'              : False
		}
	}
