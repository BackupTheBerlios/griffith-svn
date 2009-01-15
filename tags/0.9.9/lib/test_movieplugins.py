# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2008
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

#
# The code within this file is only used to automatically test movie plugins
# which support that.
# The movie plugin which should be tested has to be added to the
# PluginTester.test_plugins list and has to define to classes
# SearchPluginTest and PluginTest
# Both classes provide a member called test_configuration which is a
# dict in both cases.
#
# SearchPluginTest.test_configuration:
# dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
#
# PluginTest.test_configuration:
# dict { movie_id -> dict { arribute -> value } }
#
# value: * True/False if attribute should only be tested for any value or nothing
#        * or the expected value
#

import gettext
import sys
import initialize
import gdebug
import gutils
import config
import os
from time import sleep
try:
	import gtk
	import gobject
except:
	pass
	
sys.path.append('plugins/movie')

#
# test class for movie plugin classes Plugin and SearchPlugin
# it simulates the resolving of movie data for configured movies and
# compares the results with the expected once
#
class PluginTester:
	test_plugins = [
		'PluginMovieAmazon',
		'PluginMovieFilmeVonAZ',
		'PluginMovieIMDB-de',
		'PluginMovieKinoDe',
		'PluginMovieOFDb',
		'PluginMovieZelluloid',
	]

	#
	# simulates the search for a movie title and compares
	# the count of results with the expected count
	#
	def test_search(self, plugin, logFile, title, cntOriginal, cntTranslated):
		global debug, myconfig
		result = True
		plugin.debug = debug
		plugin.config = myconfig
		# plugin.translated_url_search
		plugin.url = plugin.translated_url_search
		if plugin.remove_accents:
			plugin.title = gutils.remove_accents(title, 'utf-8')
		else:
			plugin.title = title
		plugin.search_movies(None)
		plugin.get_searches()
		if not len(plugin.ids) - 1 == cntOriginal:	# first entry is always '' (???)
			print "Title (Translated): %s - expected: %d - found: %d" % (title, cntOriginal, len(plugin.ids) - 1)
			logFile.write("Title (Translated): %s - expected: %d - found: %d\n\n" % (title, cntOriginal, len(plugin.ids) - 1))
			for titleFound in plugin.titles:
				logFile.write(titleFound)
				logFile.write('\n')
			logFile.write('\n\n')
			result = False
		# plugin.original_url_search
		plugin.url = plugin.original_url_search
		if plugin.remove_accents:
			plugin.title = gutils.remove_accents(title, 'utf-8')
		else:
			plugin.title = title
		plugin.search_movies(None)
		plugin.get_searches()
		if not len(plugin.ids) - 1 == cntTranslated:	# first entry is always '' (???)
			print "Title (Original): %s - expected: %d - found: %d" % (title, cntTranslated, len(plugin.ids) - 1)
			logFile.write("Title (Original): %s - expected: %d - found: %d\n\n" % (title, cntTranslated, len(plugin.ids) - 1))
			for titleFound in plugin.titles:
				logFile.write(titleFound)
				logFile.write('\n')
			logFile.write('\n\n')
			result = False
		return result

	#
	# check every configured movie title
	#
	def do_test_searchplugin(self, plugin_name, domsgbox=True):
		result = True
		
		plugin = __import__(plugin_name)
		try:
			pluginTestConfig = plugin.SearchPluginTest()
		except:
			print "Warning: SearchPlugin test could not be executed for %s because of missing configuration class SearchPluginTest." % plugin_name
			pluginTestConfig = None
		
		if not pluginTestConfig == None:
			logFile = open(plugin_name + '-searchtest.txt', 'w+')
			try:
				for i in pluginTestConfig.test_configuration:
					searchPlugin = plugin.SearchPlugin()
					if not self.test_search(searchPlugin, logFile, i, pluginTestConfig.test_configuration[i][0], pluginTestConfig.test_configuration[i][1]):
						result = False
					sleep(1) # needed for amazon
			finally:
				logFile.close()
		
		if domsgbox:
			if not result:
				gutils.error(self, 'SearchPluginTest %s: Test NOT successful !' % plugin_name)
			else:
				gutils.info(self, 'SearchPluginTest %s: Test successful !' % plugin_name)
		
		return result

	#
	# simulates the resolving of movie data for configured movies and
	# compares the results with the expected once
	#
	def test_one_movie(self, movieplugin, logFile, results_expected):
		global debug, myconfig
		result = True
		self.movie = movieplugin
		self.movie.parent_window = None
		self.movie.locations = self.locations
		self.movie.debug = debug
		self.movie.config = myconfig

		fields_to_fetch = ['o_title', 'title', 'director', 'plot', 'cast', 'country', 'genre',
				'classification', 'studio', 'o_site', 'site', 'trailer', 'year',
				'notes', 'runtime', 'image', 'rating']

		self.movie.fields_to_fetch = fields_to_fetch
	
		self.movie.get_movie(None)
		self.movie.parse_movie()

		results = {}
		if 'year' in fields_to_fetch:
			results['year'] = self.movie.year
			fields_to_fetch.pop(fields_to_fetch.index('year'))
		if 'runtime' in fields_to_fetch:
			results['runtime'] = self.movie.runtime
			fields_to_fetch.pop(fields_to_fetch.index('runtime'))
		if 'cast' in fields_to_fetch:
			results['cast'] = gutils.convert_entities(self.movie.cast)
			fields_to_fetch.pop(fields_to_fetch.index('cast'))
		if 'plot' in fields_to_fetch:
			results['plot'] = gutils.convert_entities(self.movie.plot)
			fields_to_fetch.pop(fields_to_fetch.index('plot'))
		if 'notes' in fields_to_fetch:
			results['notes'] = gutils.convert_entities(self.movie.notes)
			fields_to_fetch.pop(fields_to_fetch.index('notes'))
		if 'rating' in fields_to_fetch:
			if self.movie.rating:
				results['rating'] = float(self.movie.rating)
			fields_to_fetch.pop(fields_to_fetch.index('rating'))
		# poster
		if 'image' in fields_to_fetch:
			if self.movie.image:
				results['image'] = self.movie.image
			fields_to_fetch.pop(fields_to_fetch.index('image'))
		# other fields
		for i in fields_to_fetch:
			results[i] = gutils.convert_entities(self.movie[i])
			
		# check the fields
		for i in results_expected:
			i_val = results_expected[i]
			if isinstance(i_val, bool):
				if i_val:
					if not results.has_key(i) or len(results[i]) < 1:
						print "Test error: %s: Value expected but nothing returned.\nKey: %s" % (movieplugin.movie_id, i)
						logFile.write("Test error: %s: Value expected but nothing returned.\nKey: %s\n\n" % (movieplugin.movie_id, i))
						result = False
				else:
					if results.has_key(i) and len(results[i]) > 0:
						print "Test error: %s: No value expected but something returned.\nKey: %s\nValue: %s" % (movieplugin.movie_id, i, results[i])
						logFile.write("Test error: %s: No value expected but something returned.\nKey: %s\nValue: %s\n\n" % (movieplugin.movie_id, i, results[i]))
						result = False
			else:
				if not results.has_key(i):
					print "Test error: %s: Value expected but nothing returned.\nKey: %s" % (movieplugin.movie_id, i)
					logFile.write("Test error: %s: Value expected but nothing returned.\nKey: %s\n\n" % (movieplugin.movie_id, i))
					result = False
				else:
					if not results[i] == i_val:
						print "Test error: %s: Wrong value returned.\nKey: %s\nValue expected: %s\nValue returned: %s" % (movieplugin.movie_id, i, i_val, results[i])
						logFile.write("Test error: %s: Wrong value returned.\nKey: %s\nValue expected: %s\nValue returned: %s\n\n" % (movieplugin.movie_id, i, i_val, results[i]))
						result = False
		return result
	
	#
	# check every configured movie
	#
	def do_test_plugin(self, plugin_name, domsgbox=True):
		result = True
		
		plugin = __import__(plugin_name)
		try:
			pluginTestConfig = plugin.PluginTest()
		except:
			print "Warning: Plugin test could not be executed for %s because of missing configuration class PluginTest." % plugin_name
			pluginTestConfig = None
		
		if not pluginTestConfig == None:
			logFile = open(plugin_name + '-loadtest.txt', 'w+')
			try:
				for i in pluginTestConfig.test_configuration:
					moviePlugin = plugin.Plugin(i)
					if not self.test_one_movie(moviePlugin, logFile, pluginTestConfig.test_configuration[i]):
						result = False
					sleep(1) # needed for amazon
			finally:
				logFile.close()

		if domsgbox:
			if not result:
				gutils.error(self, 'PluginTest %s: Test NOT successful !' % plugin_name)
			else:
				gutils.info(self, 'PluginTest %s: Test successful !' % plugin_name)
		
		return result

	#
	# main method
	# iterates through all plugins which should be auto-tested
	# and executes the Plugin and SearchPlugin test methods
	#
	def do_test(self, domsgbox=True):
		global debug, myconfig
		debug = self.debug = gdebug.GriffithDebug()
		#self.debug.set_debug(True)
		self._tmp_home = None
		self._tmp_config = 'griffith.cfg'
		initialize.locations(self)
		gettext.install('griffith', self.locations['i18n'], unicode=1)
		configFileName = os.path.join(self.locations['home'], self._tmp_config)
		myconfig = self.config = config.Config(file=configFileName)
		search_successful = ''
		search_unsuccessful = ''
		get_successful = ''
		get_unsuccessful = ''
		# test all plugins ?
		test_all = True
		dialog = gtk.MessageDialog(None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, 'Test all plugins ?')
		dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES,
			gtk.STOCK_NO, gtk.RESPONSE_NO)
		dialog.set_default_response(gtk.RESPONSE_NO)
		dialog.set_skip_taskbar_hint(False)
		response = dialog.run()
		dialog.destroy()
		if not response == gtk.RESPONSE_YES:
			test_all = False
		# iterate through all testable plugins
		for i in self.test_plugins:
			if domsgbox and test_all == False:
				# ask for test of that specific plugin
				dialog = gtk.MessageDialog(None,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, 'Test plugin %s ?' %i)
				dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES,
					gtk.STOCK_NO, gtk.RESPONSE_NO)
				dialog.set_default_response(gtk.RESPONSE_NO)
				dialog.set_skip_taskbar_hint(False)
				response = dialog.run()
				dialog.destroy()
				if not response == gtk.RESPONSE_YES:
					continue
			plugin = __import__(i)
			# search test
			if self.do_test_searchplugin(i, False):
				search_successful = search_successful + i + ', '
			else:
				search_unsuccessful = search_unsuccessful + i + ', '
			# movie test
			if self.do_test_plugin(i, False):
				get_successful = get_successful + i + ', '
			else:
				get_unsuccessful = get_unsuccessful + i + ', '
		if domsgbox:
			gutils.info(self, 'SearchPluginTests\n  Success: %s\n  Failed: %s\n\nPluginTests\n  Success: %s\n  Failed: %s' % (search_successful, search_unsuccessful, get_successful, get_unsuccessful))

#
# Start the tests
#
gtk.gdk.threads_init()
gtk.gdk.threads_enter()
PluginTester().do_test()
#gtk.main()
gtk.gdk.threads_leave()