# -*- coding: UTF-8 -*-

__revision__ = '$Id: sql.py 301 2006-04-08 13:12:18Z piotrek $'

# Copyright (c) 2005 Vasco Nunes
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
import sqlite
import os.path
import gutils
import gtk

class GriffithSQL:
	con = None
	cursor = None
	
	def __init__(self, config, debug, griffith_dir):
		self.griffith_dir = griffith_dir
		self.config = config
		self.debug = debug
		try:
			self.con = sqlite.connect(os.path.join(griffith_dir, \
				config.get('default_db')), autocommit=1)
			self.cursor = self.con.cursor()
		except:
			self.debug.show("Error reading database file")
			import sys
			sys.exit()
			
		self.check_if_table_exists()

	def new_db(self, parent): #{{{
		"""initializes a new griffith database file"""
		response = gutils.question(self, \
			_("Are you sure you want to create a new database?\nYou will lose ALL your current data!"), \
			1, parent.main_window)
		if response == gtk.RESPONSE_YES:
			response_sec = gutils.question(self, \
				_("Last chance!\nDo you confirm that you want\nto lose your current data?"), \
				1, parent.main_window)
			if response_sec == gtk.RESPONSE_YES:
				# delete images
				for root, dirs, files in os.walk(os.path.join(self.griffith_dir,"posters"), topdown=False):
					for name in files:
						os.remove(os.path.join(root, name))
				# delete db
				parent.db.con.close()
				os.unlink(os.path.join(self.griffith_dir,self.config.get('default_db')))
				# create/connect db
				parent.db = GriffithSQL(self.config, self.debug, self.griffith_dir)
				parent.clear_details()
				parent.total = 0
				parent.count_statusbar()
				parent.treemodel.clear()
				from initialize	import dictionaries
				dictionaries(parent)
			else:
				pass
		else:
			pass
	#}}}

	# create tables ----------------------------------------------------{{{
	def create_db(self):
		self.create_table_movies()
		self.create_table_volumes()
		self.create_table_loans()
		self.create_table_people()
		self.create_table_media()

	def create_table_movies(self, backup=False):
		if backup:
			self.debug.show("Creating 'movies' temporary table...")
			query = "CREATE TEMPORARY TABLE movies_backup"
		else:
			self.debug.show("Creating 'movies' table...")
			query = "CREATE TABLE movies"
		query += """
			(
				'id' INTEGER PRIMARY KEY,
				'volume_id' INT NOT NULL DEFAULT '0',
				'collection_id' INT NOT NULL DEFAULT '0',
				'original_title' VARCHAR(255) NOT NULL,
				'title' VARCHAR(255),
				'director' VARCHAR(100),
				'number' INT(11) NOT NULL,
				'image' TEXT,
				'plot' TEXT,
				'country' VARCHAR(100),
				'year' INT(4),
				'runtime' INT(4),
				'classification' VARCHAR(50),
				'genre' VARCHAR(100),
				'studio' VARCHAR(50),
				'site' VARCHAR(100),
				'imdb' VARCHAR(100),
				'actors' TEXT,
				'trailer' VARCHAR(100),
				'rating' INT(1) DEFAULT 0,
				'loaned' INT(1) NOT NULL DEFAULT '0',
				'media' INT(1) DEFAULT '0',
				'num_media' INT(2),
				'obs' TEXT,
				'seen' INT(1) NOT NULL DEFAULT '0',
				'region' INT DEFAULT 2,
				'condition' INT DEFAULT 3,
				'color' INT DEFAULT 0,
				'layers' INT DEFAULT 4
			)
		"""
		self.cursor.execute(query)

	def create_table_loans(self, backup=False):
		query = ''
		if backup:
			self.debug.show("Creating 'loans' temporary table...")
			query = "CREATE TEMPORARY TABLE loans_backup"
		else:
			self.debug.show("Creating 'loans' table...")
			query = "CREATE TABLE loans"
		query += """
			(
				id INTEGER PRIMARY KEY,
				person_id INT(11) NOT NULL default '0',
				movie_id INTEGER default '0',
				volume_id INTEGER default '0',
				collection_id INTEGER default '0',
				date DATE NOT NULL default '0000-00-00',
				return_date DATE
			)
		"""
		self.cursor.execute(query)
			
	def create_table_people(self, backup=False):
		if backup:
			self.debug.show("Creating 'people' temporary table...")
			query = "CREATE TEMPORARY TABLE people_backup"
		else:
			self.debug.show("Creating 'people' table...")
			query = "CREATE TABLE people"
		query += """
			(
				id INTEGER PRIMARY KEY,
				name VARCHAR(200) NOT NULL,
				email VARCHAR(150),
				phone VARCHAR(50)
			)
		"""
		self.cursor.execute(query)
	
	def create_table_volumes(self):
		self.debug.show("Creating 'volumes' table...")
		self.cursor.execute ("""
			CREATE TABLE volumes
			(
				'id' INTEGER PRIMARY KEY,
				'name' STRING NOT NULL,
				'loaned' INT(1) NOT NULL default '0'
			);
			INSERT INTO 'volumes' VALUES (0,'','0');
			""")
			
	def create_table_collections(self):
		self.debug.show("Creating 'collections' table...")
		self.cursor.execute ("""
			CREATE TABLE collections
			(
				'id' INTEGER PRIMARY KEY,
				'name' STRING NOT NULL,
				'loaned' INT(1) NOT NULL default '0'
			);
			INSERT INTO 'collections' VALUES (0,'','0');
			""")

	def create_table_media(self):
		self.debug.show("Creating 'media' table...")
		self.cursor.execute ("""
			CREATE TABLE media
			(
				'id' INTEGER PRIMARY KEY,
				'name' STRING NOT NULL
			);
			INSERT INTO 'media' VALUES (0, "DVD");
			INSERT INTO 'media' VALUES (1, "DVD-R");
			INSERT INTO 'media' VALUES (2, "DVD-RW");
			INSERT INTO 'media' VALUES (3, "DVD+R");
			INSERT INTO 'media' VALUES (4, "DVD+RW");
			INSERT INTO 'media' VALUES (5, "DVD-RAM");
			INSERT INTO 'media' VALUES (6, "CD");
			INSERT INTO 'media' VALUES (7, "CD-RW");
			INSERT INTO 'media' VALUES (8, "VCD");
			INSERT INTO 'media' VALUES (9, "SVCD");
			INSERT INTO 'media' VALUES (10, "VHS");
			INSERT INTO 'media' VALUES (11, "BETACAM");
		""")

	def create_table_languages(self):
		self.debug.show("Creating 'languages' table...")
		self.cursor.execute ("""
			CREATE TABLE languages
			(
				'id' INTEGER PRIMARY KEY,
				'name' STRING NOT NULL
			);
			INSERT INTO 'languages' VALUES (0,'');
		""")

	def create_table_movie_lang(self):
		self.debug.show("Creating 'movie_lang' table...")
		self.cursor.execute ("""
			CREATE TABLE movie_lang
			(
				'movie_id' INTEGER NOT NULL,
				'lang_id' INTEGER NOT NULL,
				'type' INTEGER
			);
		""")

	def create_table_tags(self):
		self.debug.show("Creating 'tags' table...")
		self.cursor.execute ("""
			CREATE TABLE tags
			(
				'id' INTEGER PRIMARY KEY,
				'name' STRING NOT NULL
			);
			INSERT INTO 'tags' VALUES (0, '""" + _("Favourite") + "');" \
		)

	def create_table_movie_tag(self):
		self.debug.show("Creating 'movie_tag' table...")
		self.cursor.execute ("""
			CREATE TABLE movie_tag
			(
				'movie_id' INTEGER NOT NULL,
				'tag_id' INTEGER NOT NULL
			);
		""")
	# }}}

	# upgrade tables ---------------------------------------------------{{{
	def check_if_table_exists(self):
		try:
			self.cursor.execute("SELECT id FROM movies LIMIT 1")
		except:
			self.create_db()
		try:
			self.cursor.execute("SELECT id FROM volumes LIMIT 1")
		except:
			self.create_table_volumes()
		try:
			self.cursor.execute("SELECT id FROM collections LIMIT 1")
		except:
			self.create_table_collections()
		try:
			self.cursor.execute("SELECT id FROM media LIMIT 1")
		except:
			self.create_table_media()
			self.update_old_media()
		try:
			self.cursor.execute("SELECT id FROM languages LIMIT 1")
		except:
			self.create_table_languages()
		try:
			self.cursor.execute("SELECT movie_id FROM movie_lang LIMIT 1")
		except:
			self.create_table_movie_lang()
		try:
			self.cursor.execute("SELECT id FROM tags LIMIT 1")
		except:
			self.create_table_tags()
		try:
			self.cursor.execute("SELECT movie_id FROM movie_tag LIMIT 1")
		except:
			self.create_table_movie_tag()

		# "empty" language is needed
		if self.get_value(field="name", table="languages", where="id = '0'") == None:
			self.cursor.execute("INSERT INTO languages VALUES('0', '')")

		# check old media
		if self.count_records("movies", "media='DVD'") > 0:
			self.update_old_media()
			
		# see if a db update is needed...
		# a) movie table
		columns = {
			'id'             : 1,
			'volume_id'      : 1,
			'collection_id'  : 1,
			'original_title' : 1,
			'title'          : 1,
			'director'       : 1,
			'number'         : 1,
			'image'          : 1,
			'plot'           : 1,
			'country'        : 1,
			'year'           : 1,
			'runtime'        : 1,
			'classification' : 1,
			'genre'          : 1,
			'studio'         : 1,
			'site'           : 1,
			'imdb'           : 1,
			'actors'         : 1,
			'trailer'        : 1,
			'rating'         : 1,
			'loaned'         : 1,
			'media'          : 1,
			'num_media'      : 1,
			'obs'            : 1,
			'seen'           : 1,
			'region'         : 1,
			'condition'      : 1,
			'color'          : 1,
			'layers'         : 1
		}
		need_upgrade = False
		for column in columns:
			try:
				self.cursor.execute("SELECT %s FROM movies LIMIT 1"%column)
			except:
				columns[column] = 0	# column is missing
				need_upgrade = True
		if need_upgrade:
			self.upgrade_table("movies", columns)

		# b) loans table
		columns = {
			'id'            : 1,
			'movie_id'      : 1,
			'volume_id'     : 1,
			'collection_id' : 1,
			'person_id'     : 1,
			'date'          : 1,
			'return_date'   : 1
		}
		need_upgrade = False
		for column in columns:
			try:
				self.cursor.execute("SELECT %s FROM loans LIMIT 1"%column)
			except:
				columns[column] = 0	# column is missing
				need_upgrade = True
		if need_upgrade:
			self.upgrade_table("loans", columns)
			
	def upgrade_table(self, table, columns):
		self.debug.show("Upgrading database: processing %s table..." % table)
		eval("self.create_table_%s(backup=True)"%table)
		sql_query = "INSERT INTO %s_backup ("%table
		i = 0
		for column in columns:
			i = i+1
			sql_query += column
			if i == len(columns):
				sql_query += ' '
			else:
				sql_query += ', '
		sql_query += ") SELECT "
		i = 0
		for column in columns:
			i = i+1
			if columns[column] == 1:
				sql_query += column
			else:
				sql_query += "''"
			if i == len(columns):
				sql_query += ' '
			else:
				sql_query += ', '
				
		sql_query += " FROM %s" % table
		self.cursor.execute(sql_query)
		self.cursor.execute("DROP TABLE %s" % table)
		eval("self.create_table_%s()"%table)
		self.cursor.execute("INSERT INTO %s SELECT * FROM %s_backup" % (table, table))
		self.cursor.execute("DROP TABLE %s_backup"%table)
		self.con.commit()

	def update_old_media(self):
		self.debug.show("Upgrading old media values...")
		self.cursor.execute("""
			UPDATE movies SET media = '0' WHERE media = 'DVD';
			UPDATE movies SET media = '1' WHERE media = 'DVD-R';
			UPDATE movies SET media = '2' WHERE media = 'DVD-RW';
			UPDATE movies SET media = '3' WHERE media = 'DVD+R';
			UPDATE movies SET media = '4' WHERE media = 'DVD+RW';
			UPDATE movies SET media = '5' WHERE media = 'DVD-RAM';
			UPDATE movies SET media = '6' WHERE media = 'DivX';
			UPDATE movies SET media = '6' WHERE media = 'DIVX';
			UPDATE movies SET media = '6' WHERE media = 'XviD';
			UPDATE movies SET media = '6' WHERE media = 'XVID';
			UPDATE movies SET media = '6' WHERE media = 'WMV';
			UPDATE movies SET media = '6' WHERE media = 'WMV';
			UPDATE movies SET media = '8' WHERE media = 'VCD';
			UPDATE movies SET media = '9' WHERE media = 'SVCD'; 	
			UPDATE movies SET media = '10' WHERE media = 'VHS';
			UPDATE movies SET media = '11' WHERE media = 'BETACAM';
		""")
		self.con.commit()

	# }}}

	# add data ---------------------------------------------------------{{{
	def add_movie(self, data):
		# TODO: make use of parent data {{{
		i = 0
		languages_ids = {}
		for item in self.get_all_data("languages", what="id"):
			languages_ids[i] = item['id']
			i = i+1
		i = 0
		volume_combo_ids = {}
		for item in self.get_all_data("volumes", what="id"):
			volume_combo_ids[i] = item['id']
			i = i+1
		i = 0
		collection_combo_ids = {}
		for item in self.get_all_data("collections", what="id"):
			collection_combo_ids[i] = item['id']
			i = i+1
		i = 0
		tags_ids = {}
		for item in self.get_all_data("tags", what="id"):
			tags_ids[i] = item['id']
			i = i+1
		#}}}

		plot_buffer = data.am_plot.get_buffer()
		with_buffer = data.am_with.get_buffer()
		obs_buffer = data.am_obs.get_buffer()
		number = data.am_number.get_text()
		(filepath, filename) = os.path.split(data.am_picture_name.get_text())
		query = """
			INSERT INTO 'movies' ('id', 'original_title', 'title', 'director', 'plot', 'image', 'year',
			'runtime', 'actors', 'country', 'genre', 'media', 'classification', 'studio', 'site', 'color',
			'region', 'layers', 'condition', 'imdb', 'trailer', 'obs', 'num_media', 'loaned', 'rating', 'seen',
			'number', 'volume_id', 'collection_id')
			VALUES (Null,'""" + gutils.gescape(data.am_original_title.get_text()) + "','" +\
			gutils.gescape(data.am_title.get_text())+"','" +\
			gutils.gescape(data.am_director.get_text())+"','" +\
			gutils.gescape(plot_buffer.get_text(plot_buffer.get_start_iter(), plot_buffer.get_end_iter()))+"','" +\
			filename+"','" +\
			data.am_year.get_text()+"','" +\
			data.am_runtime.get_text()+"','" +\
			gutils.gescape(with_buffer.get_text(with_buffer.get_start_iter(), with_buffer.get_end_iter()))+"','" +\
			gutils.gescape(data.am_country.get_text())+"','" +\
			gutils.gescape(data.am_genre.get_text())+"','" +\
			str(data.am_media.get_active())+"','" +\
			gutils.gescape(data.am_classification.get_text())+"','" +\
			gutils.gescape(data.am_studio.get_text())+"','" +\
			data.am_site.get_text()+"','" +\
			str(int(data.am_color.get_active()))+"','" +\
			str(int(data.am_region.get_active()))+"','" +\
			str(int(data.am_layers.get_active()))+"','" +\
			str(int(data.am_condition.get_active()))+"','" +\
			data.am_imdb.get_text()+"','" +\
			data.am_trailer.get_text()+"','" +\
			gutils.gescape(obs_buffer.get_text(obs_buffer.get_start_iter(), obs_buffer.get_end_iter()))+"','" +\
			data.am_discs.get_text()+"','0','" +\
			str(int(data.rating_slider_add.get_value()))+"','" +\
			str(int(data.am_seen.get_active()))+"','" +\
			number+"', '" +\
			str(volume_combo_ids[data.am_volume_combo.get_active()]) + "', '"+\
			str(collection_combo_ids[data.am_collection_combo.get_active()]) + "')"
		self.cursor.execute(query)

		id = self.get_value(field="id", table="movies", where="number = '%s'" % number)

		# languages
		selected = {}
		for i in data.am_languages:
			if i['id'].get_active() > 0:
				lang_id = languages_ids[i['id'].get_active()]
				type = i['type'].get_active()
				if not selected.has_key(lang_id):
					selected[lang_id] = {}
				selected[lang_id][type] = True
		for lang in selected.keys():
			for type in selected[lang].keys():
				self.cursor.execute("INSERT INTO movie_lang(movie_id, lang_id, type) VALUES ('%s', '%s', '%s');" % (id, lang, type) )

		# tags 
		selected = {}
		for i in tags_ids:
			if data.am_tags[i].get_active() == True:
				selected[tags_ids[i]] = 1
		for i in selected.keys():
			self.cursor.execute("INSERT INTO movie_tag(movie_id, tag_id) VALUES ('%s', '%s');" % (id, i) )

	def add_volume(self, name):
		# check if volume already exists
		for volume in self.get_all_data("volumes", what="name"):
			if name == volume['name']:
				self.debug.show("Volume '%s' already exists"%name)
				return False
		self.debug.show("Adding '%s' volume to database..."%name)
		try:
			self.cursor.execute("INSERT INTO 'volumes'('id', 'name', 'loaned') VALUES (Null,'"+
				gutils.gescape(name)+"','0');")
		except:
			return False
		return True

	def add_collection(self, name):
		# check if volume already exists
		for collection in self.get_all_data("collections", what="name"):
			if name == collection['name']:
				self.debug.show("Collection '%s' already exists"%name)
				return False
		self.debug.show("Adding '%s' collection to database..."%name)
		try:
			self.cursor.execute("INSERT INTO 'collections'('id', 'name', 'loaned') VALUES (Null,'"+
				gutils.gescape(name)+"','0');")
		except:
			return False
		return True

	def add_language(self, name):
		if name == None or name == '':
			self.debug.show("You didn't write name for new language")
			return False
		name = gutils.gescape(name)
		# check if language already exists
		for language in self.get_all_data("languages", what="name"):
			if name == language['name']:
				self.debug.show("Language '%s' already exists"%name)
				return False
		self.debug.show("Adding '%s' language to database..."%name)
		try:
			self.cursor.execute("INSERT INTO 'languages'('id', 'name') VALUES (Null,'"+
				gutils.gescape(name)+"');")
		except:
			return False
		return True

	def add_tag(self, name):
		if name == None or name == '':
			self.debug.show("You didn't write name for new tag")
			return False
		# check if tag already exists
		for tag in self.get_all_data("tags", what="name"):
			if name == tag['name']:
				self.debug.show("Tag '%s' already exists"%name)
				return False
		self.debug.show("Adding '%s' tag to database..."%name)
		try:
			self.cursor.execute("INSERT INTO 'tags'('id', 'name') VALUES (Null,'"+
				gutils.gescape(name)+"');")
		except:
			return False
		return True
	# }}}

	# select data ------------------------------------------------------{{{
	def get_all_data(self, table_name="movies", order_by=None, where=None, what=None):
		if what == None:
			what = "*"
		sql="SELECT %s FROM %s" %(what, table_name)
		if where:
			sql = sql + " WHERE %s" % where
		if order_by != None:
			sql = sql + " ORDER BY %s" % order_by
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def get_value(self, field, table, where=None):
		query = "SELECT %s FROM %s" % (field, table)
		if where:
			query += " WHERE %s" % where
		self.cursor.execute(query)
		try: 
			value = self.cursor.fetchone()[0]
		except:
			value = None
		return value

	def select_movie_by_num(self,number):
		self.cursor.execute("SELECT * FROM movies WHERE number = '"+number+"' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_original_title(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE original_title LIKE '%"+txt+"%' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_title(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE title LIKE '%"+txt+"%' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_director(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE director LIKE '%"+txt+"%' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_rating(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE rating LIKE '"+txt+"' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_year(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE year = '"+txt+"' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_genre(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE genre LIKE '%"+txt+"%' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movie_by_actors(self,txt):
		self.cursor.execute("SELECT * FROM movies WHERE actors LIKE '%"+txt+"%' ORDER BY number ASC")
		return self.cursor.fetchall()

	def select_movies_by_volume(self,volume_id):
		self.cursor.execute("SELECT * FROM movies WHERE volume_id = '%s' ORDER BY number ASC" % volume_id)
		return self.cursor.fetchall()

	def select_movies_by_collection(self,collection):
		self.cursor.execute("SELECT * FROM movies WHERE collection_id = '%s' ORDER BY number ASC" % collection)
		return self.cursor.fetchall()

	def select_person_by_name(self, name):
		self.cursor.execute("SELECT * FROM people WHERE name = '"+name+"'")
		return self.cursor.fetchall()

	def select_person_by_id(self, p_id):
		self.cursor.execute("SELECT * FROM people WHERE id = '"+str(p_id)+"'")
		return self.cursor.fetchall()

	def get_loaned_movies(self):
		self.cursor.execute("SELECT * FROM movies WHERE loaned='1' ORDER BY number")
		return self.cursor.fetchall()

	def get_not_seen_movies(self):
		self.cursor.execute("SELECT * FROM movies WHERE seen='0' ORDER BY number")
		return self.cursor.fetchall()

	def get_loan_info(self, movie_id=None, volume_id=None, collection_id=None):
		query = "SELECT * FROM loans WHERE "
		if collection_id>0:
			query += "collection_id='%s'" % str(collection_id)
		elif volume_id>0:
			query += "volume_id='%s'" % str(volume_id)
		else:
			query += "movie_id='%s'" % str(movie_id)
		query +=  " AND return_date = ''"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def get_loan_history(self, movie_id=None, volume_id=None, collection_id=None):
		query = "SELECT * FROM loans WHERE return_date <> '' AND ("
		if collection_id>0:
			query += "collection_id='%s'" % str(collection_id)
		if volume_id>0:
			if collection_id>0:
				query += " OR "
			query += "volume_id='%s'" % str(volume_id)
		if movie_id>0:
			if collection_id>0 or volume_id>0:
				query += " OR "
			query += " movie_id='%s'" % str(movie_id)
		query +=  ")"
		self.cursor.execute(query)
		return self.cursor.fetchall()
	# }}}

	# remove data ------------------------------------------------------{{{
	def remove_movie_by_num(self,number):
		if self.is_movie_loaned(movie_number=number):
			self.debug.show("Movie (number=%s) is loaned. Can't delete!")
			return False
		id = self.get_value(field="id", table="movies", where="number = '%s'" % number)
		if id != None:
			self.cursor.execute("DELETE FROM movie_lang WHERE movie_id = '%s'" % id)
			self.cursor.execute("DELETE FROM movie_tag WHERE movie_id = '%s'" % id)
			self.cursor.execute("DELETE FROM movies WHERE number = '"+number+"'")
			self.con.commit()

	def remove_volume(self, id=None, name=None):
		if id != None:
			name = self.get_value(field="name", table="volumes", where=" id = '%s'" % id)
		elif name != None and name != '' and id == None:
			name =	gutils.gescape(name)
			id = self.get_value(field="id", table="volumes", where="name = '%s'" % name)
			if id != None:
				id = str(int(id))
		if str(id) == '0' or id == None:
			self.debug.show("You have to select volume first")
			return False
		movies = int(self.get_value(field="count(id)", table="movies", where="volume_id = '%s'" % id))
		if movies > 0:
			gutils.warning(self, msg="%s movie(s) in this volume.\nRemoval is possible only if there is no movie assigned to volume"%str(movies))
			return False
		self.debug.show("Removing '%s' volume (id=%s) from database..."%(name, id))
		try:
			self.cursor.execute("DELETE FROM volumes WHERE id = '%s'" % id)
		except:
				return False
		return True

	def remove_collection(self, id=None, name=None):
		if id != None:
			name = self.get_value(field="name", table="collections", where="id = '%s'" % id)
		elif name != None and name != '' and id == None:
			name =	gutils.gescape(name)
			id = self.get_value(field="id", table="collections", where="name = '%s'" % name)
			id = str(int(id))
		if str(id) == '0' or id == None:
			self.debug.show("You have to select collection first")
			return False
		movies = int(self.get_value(field="count(id)", table="movies", where="collection_id = '%s'" % id))
		if movies > 0:
			gutils.warning(self, msg="%s movie(s) in this collection.\nRemoval is possible only if there is no movie assigned to collection"%str(movies))
			return False
		self.debug.show("Removing '%s' collection (id=%s) from database..."%(name, id))
		try:
			self.cursor.execute("DELETE FROM collections WHERE id = '%s'" % id)
		except:
				return False
		return True

	def remove_language(self, id=None, name=None):
		if id != None:
			name = self.get_value(field="name", table="languages", where="id = '%s'"%id)
		elif name != None and name != '' and id == None:
			name =	gutils.gescape(name)
			id = self.get_value(field="id", table="languages", where="name = '%s'"%name)
			id = str(int(id))
		if str(id) == '0' or id == None:
			self.debug.show("You have to select language first")
			return False

		movies = int(self.get_value(field="count(movie_id)", table="movie_lang", where="lang_id = '%s'" % id))
		if movies > 0:
			gutils.warning(self, msg="%s movie(s) are assigned to this language.\nChange movie details first!"%str(movies))
			return False

		self.debug.show("Removing '%s' language (id=%s) from database..."%(name, id))
		try:
			self.cursor.execute("DELETE FROM languages WHERE id = '%s'" % id)
		except:
				return False
		return True

	def remove_tag(self, id=None, name=None):
		if id != None:
			name = self.get_value(field="name", table="tags", where="id = '%s'"%id)
		elif name != None and name != '' and id == None:
			name =	gutils.gescape(name)
			id = self.get_value(field="id", table="tags", where="name = '%s'"%name)
			id = str(int(id))
		if str(id) == '0' or id == None:
			self.debug.show("You have to select tag first")
			return False

		movies = int(self.get_value(field="count(movie_id)", table="movie_tag", where="tag_id = '%s'" % id))
		if movies > 0:
			gutils.warning(self, msg="%s movie(s) are assigned to this tag.\nChange movie details first!"%str(movies))
			return False

		self.debug.show("Removing '%s' tag (id=%s) from database..."%(name, id))
		try:
			self.cursor.execute("DELETE FROM tags WHERE id = '%s'" % id)
		except:
				return False
		return True

	def remove_person_by_name(self, number):
		self.cursor.execute("DELETE FROM people WHERE name = '"+number+"'")
	# }}}

	# update data ------------------------------------------------------{{{
	def update_collection(self, id, name=None, volume_id=None, loaned=None):
		if str(id) == '0':
			self.debug.show("You have to select collection first")
			return False
		if name!=None:
			tmp = self.get_value(field="id", table="collections", where="name='%s'"%name)
			if tmp != None:
				self.debug.show("This name is already in use (id=%s)"%tmp)
				gutils.warning(self, msg="This name is already in use!")
				return False
			try:
				self.cursor.execute("UPDATE collections SET name = '%s' WHERE id = '%s';"%(name,id))
			except:
				self.debug.show("ERROR during updating collection's name!")
				return False
			return True
		if loaned==1:
			try:
				self.cursor.execute("""
					UPDATE collections SET loaned='1' WHERE id='%s';
					UPDATE movies SET loaned='1' WHERE collection_id='%s';
				""" % (id, id))
			except:
				self.debug.show("ERROR during updating collection's loan data!")
				return False
			if volume_id:
				try:
					self.cursor.execute("UPDATE volumes SET loaned='1' WHERE id='%s';"%volume_id)
				except:
					self.debug.show("ERROR during updating volume's loan data!")
					return False
			return True
		elif loaned==0:
			try:
				self.cursor.execute("""
					UPDATE collections SET loaned='0' WHERE id='%s';
					UPDATE movies SET loaned='0' WHERE collection_id='%s';
				""" %( id, id))
			except:
				self.debug.show("ERROR during updating collection's loan data!")
				return False
			if volume_id:
				try:
					self.cursor.execute("UPDATE volumes SET loaned='0' WHERE id='%s';"%volume_id)
				except:
					self.debug.show("ERROR during updating volume's loan data!")
					return False
			return True
		return False

	def update_volume(self, id, name=None, loaned=None):
		if str(id) == '0':
			self.debug.show("You have to select volume first")
			return False
		if name!=None:
			tmp = self.get_value(field="id", table="volumes", where="name='%s'"%name)
			if tmp != None:
				self.debug.show("This name is already in use (id=%s)"%tmp)
				gutils.warning(self, msg="This name is already in use!")
				return False
			try:
				self.cursor.execute("UPDATE volumes SET name = '%s' WHERE id = '%s';"%(name,id))
			except:
				self.debug.show("ERROR during updating volume's name!")
				return False
			return True
		if loaned==1:
			try:
				self.cursor.execute("""
					UPDATE volumes SET loaned=1 WHERE id='%s';
					UPDATE movies SET loaned=1 WHERE volume_id='%s';
				"""%(id, id))
			except:
				self.debug.show("ERROR during updating volume's loan data!")
				return False
			return True
		elif loaned==0:
			try:
				self.cursor.execute("""
					UPDATE volumes SET loaned=0 WHERE id='%s';
					UPDATE movies SET loaned=0 WHERE volume_id='%s';
				"""%(id, id))
			except:
				self.debug.show("ERROR during updating volume's loan data!")
				return False
			return True
		return False

	def update_language(self, id, name):
		if str(id) == '0':
			self.debug.show("You have to select language first")
			return False
		tmp = self.get_value(field="id", table="languages", where="name='%s'"%name)
		if tmp != None:
			self.debug.show("This name is already in use (id=%s)"%tmp)
			gutils.warning(self, msg="This name is already in use!")
			return False
		try:
			self.cursor.execute("UPDATE languages SET name ='%s' WHERE id='%s';" % (name, id))
		except:
			self.debug.show("ERROR during updating language name!")
			return False
		return True

	def update_tag(self, id, name):
		if id == None:
			self.debug.show("You have to select tag first")
			return False
		if name == '':
			self.debug.show("Tag's name is empty")
			return False
		tmp = self.get_value(field="id", table="tags", where="name='%s'"%name)
		if tmp != None:
			self.debug.show("This name is already in use (id=%s)"%tmp)
			gutils.warning(self, msg="This name is already in use!")
			return False
		try:
			self.cursor.execute("UPDATE tags SET name ='%s' WHERE id='%s';" % (name,id))
		except:
			self.debug.show("ERROR during updating tag name!")
			return False
		return True
	#}}}

	def count_records(self,table_name, where='1'):
		self.cursor.execute("SELECT COUNT(id) FROM %s" % (table_name) + " WHERE %s" % (where))
		return int(self.cursor.fetchone()[0])
		
	def is_movie_loaned(self,movie_id=None, movie_number=None):
		if movie_id==None and movie_number == None:
			return None
		if movie_id:
			self.cursor.execute("SELECT loaned FROM movies WHERE id = '%s'" % movie_id)
		if movie_number:
			self.cursor.execute("SELECT loaned FROM movies WHERE number = '%s'" % movie_number)
		return self.cursor.fetchone()[0]

	def is_volume_loaned(self,volume):
		self.cursor.execute("SELECT loaned FROM volumes WHERE id = '%s'" % volume)
		return self.cursor.fetchone()[0]

	def is_collection_loaned(self,collection):
		self.cursor.execute("SELECT loaned FROM collections WHERE id = '%s'" % collection)
		return self.cursor.fetchone()[0]

# vim: fdm=marker
