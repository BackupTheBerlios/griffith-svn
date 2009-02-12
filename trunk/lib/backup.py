# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ożarowski
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

import gtk
import os.path
import zipfile
import logging
import datetime
log = logging.getLogger("Griffith")
import config
import edit
import gutils
import sql

def backup(self):
    """perform a compressed griffith database/posters/preferences backup"""
    #if self.db.session.bind.engine.name != 'sqlite':
    #    gutils.error(self, _("Backup function is available only for SQLite engine for now"), self.widgets['window'])
    #    return False

    default_name = "%s_backup_%s.zip" % (self.config.get('name','griffith', section='database'),\
                    datetime.date.isoformat(datetime.datetime.now()))
    filename = gutils.file_chooser(_("Save Griffith backup"), \
        action=gtk.FILE_CHOOSER_ACTION_SAVE, name=default_name, buttons= \
        (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))

    if filename and filename[0]:
        proceed = True

        zipfilename = filename[0].decode('utf-8')
        if os.path.isfile(zipfilename):
            response = gutils.question(_("File exists. Do you want to overwrite it?"), window=self.widgets['window'])
            if response != gtk.RESPONSE_YES:
                proceed = False

        if proceed:
            try:
                if zipfile.zlib is not None:
                    mzip = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
                else:
                    mzip = zipfile.ZipFile(zipfilename, 'w')
            except:
                gutils.error(self, _("Error creating backup"), self.widgets['window'])
                return False
            if self.db.session.bind.engine.name == 'sqlite':
                mzip.write(os.path.join(self.locations['home'],'griffith.cfg').encode('utf-8'))
                fileName = os.path.join(self.locations['home'], self.config.get('name','griffith', section='database') + '.db').encode('utf-8')
                mzip.write(fileName)
            else:
                from tempfile import mkdtemp
                from shutil import rmtree
                from StringIO import StringIO
                from sqlalchemy import create_engine
                import copy
                import db

                tmp_dir = mkdtemp()
                tmp_config = copy.deepcopy(self.config)
                tmp_config._file = os.path.join(tmp_dir, 'griffith.cfg')
                tmp_config.set('type', 'sqlite', section='database')
                tmp_config.set('file', 'griffith.db', section='database')
                tmp_config.save()
                mzip.write(tmp_config._file)

                tmp_file = os.path.join(tmp_dir, 'griffith.db')
                tmp_engine = create_engine("sqlite:///%s" % tmp_file)
                db.metadata.create_all(bind=tmp_engine)

                # SQLite doesn't care about foreign keys much so we can just copy the data
                for table in db.metadata.sorted_tables:
                    if table.name in ('posters', 'filters'):
                        continue # see below
                    data = table.select(bind=self.db.session.bind).execute().fetchall()
                    if data:
                        table.insert(bind=tmp_engine).execute(data)
                
                # posters
                for poster in db.metadata.tables['posters'].select(bind=self.db.session.bind).execute():
                    db.metadata.tables['posters'].insert(bind=tmp_engine).execute(md5sum=poster.md5sum, data=StringIO(poster.data).read())

                mzip.write(tmp_file)
                rmtree(tmp_dir)
            gutils.info(_("Backup has been created"), self.widgets['window'])

def restore(self):
    """restores a griffith compressed backup"""
    filename = gutils.file_chooser(_("Restore Griffith backup"), \
                    action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons= \
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    if filename[0]:
        try:
            zip = zipfile.ZipFile(filename[0], 'r')
        except:
            gutils.error(self, _("Can't read backup file"), self.widgets['window'])
            return False
        mypath = os.path.join(self.locations['posters'])
        old_config_file = False
        for each in zip.namelist():
            file_to_restore = os.path.split(each)
            if not os.path.isdir(file_to_restore[1]):
                if file_to_restore[1] == '':
                    continue
                if file_to_restore[1].endswith('.jpg'):
                    myfile = os.path.join(mypath, file_to_restore[1])
                else:
                    myfile = os.path.join(self.locations['home'], file_to_restore[1])
                if file_to_restore[1].endswith('.conf'):
                    old_config_file = myfile
                outfile = open(myfile, 'wb')
                outfile.write(zip.read(each))
                outfile.flush()
                outfile.close()
        zip.close()

        # restore config file
        self.config = config.Config(file=os.path.join(self.locations['home'],'griffith.cfg'))
        if old_config_file:
            log.info('Old config file detected. Please note that it will not be used.')
            f = open(old_config_file, 'r')
            old_config_raw_data = f.read()
            f.close()
            if old_config_raw_data.find('griffith.gri') >= -1:
                self.config.set('file', 'griffith.gri', section='database')

        self.db.session.bind.engine.dispose() # close DB

        # check if file needs conversion
        if self.config.get('file', 'griffith.db', section='database').lower().endswith('.gri'):
            log.info('Old database format detected. Converting...')
            from dbupgrade import convert_from_old_db
            old_db_filename = os.path.join(self.locations['home'], self.config.get('file', section='database'))
            self.db = convert_from_old_db(self, old_db_filename, os.path.join(self.locations['home'], 'griffith.db'))
            if self.db:
                self.config.save()
            else:
                log.error('Cant convert old database, exiting.')
                import sys
                sys.exit(4)
        else:
            self.db = sql.GriffithSQL(self.config, self.locations['home'], self.locations)

        from initialize import dictionaries, people_treeview
        dictionaries(self)
        people_treeview(self)
        # let's refresh the treeview
        self.clear_details()
        self.populate_treeview()
        gutils.info(_("Backup restored"), self.widgets['window'])

def merge(self):    # FIXME
    """
        Merge database from:
        * compressed backup
        * SQLite2 *.gri file
        * SQLite3 *.db file
    """
    filename = gutils.file_chooser(_("Restore Griffith backup"), \
        action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons= \
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, \
        gtk.STOCK_OPEN, gtk.RESPONSE_OK))[0]
    if filename:
        from tempfile import mkdtemp
        from shutil import rmtree, move

        #tmp_config={}
        #tmp_config.get('type', 'sqlite', section='database')

        if filename.lower().endswith('.zip'):
            tmp_dir = mkdtemp()
            try:
                zip = zipfile.ZipFile(filename, 'r')
            except:
                gutils.error(self, _("Can't read backup file"), self.widgets['window'])
                return False
            for each in zip.namelist():
                file_to_restore = os.path.split(each)
                if not os.path.isdir(file_to_restore[1]):
                    myfile = os.path.join(tmp_dir, file_to_restore[1])
                    outfile = open(myfile, 'wb')
                    outfile.write(zip.read(each))
                    outfile.flush()
                    outfile.close()
            # load stored database filename
            tmp_config = config.Config(file=os.path.join(tmp_dir,'griffith.conf'))
            filename = os.path.join(tmp_dir, tmp_config('name', 'griffith', section='database') + '.db')
            zip.close()

        # check if file needs conversion
        if filename.lower().endswith(".gri"):
            if os.path.isfile(filename) and  open(filename).readline()[:47] == "** This file contains an SQLite 2.1 database **":
                log.info("MERGE: SQLite2 database format detected. Converting...")
                if not self.db.convert_from_sqlite2(filename, os.path.join(tmp_dir, self.config.get('file', 'griffith.db', section='database'))):
                    log.info("MERGE: Can't convert database, aborting.")
                    return False
        tmp_dir, tmp_file = os.path.split(filename)
        self.config.get('file', tmp_file, section='database') 

        tmp_db = sql.GriffithSQL(tmp_config, tmp_dir, self.locations)

        merged=0
        movies = tmp_db.Movie.count()
        for movie in tmp_db.Movie.query.all():
            if self.db.Movie.query.filter_by(o_title=movie.o_title).first() is not None:
                continue
            t_movies = {}
            for column in movie.mapper.c.keys():
                t_movies[column] = eval("movie.%s"%column)

            # replace number with new one
            t_movies["number"] = gutils.find_next_available(self.db)

            # don't restore volume/collection/tag/language/loan data (it's dangerous)
            t_movies.pop('movie_id')
            t_movies.pop('loaned')
            t_movies.pop('volume_id')
            t_movies.pop('collection_id')

            if self.db.add_movie(t_movies):
                print t_movies

            if movie.image is not None:
                dest_file = os.path.join(self.locations['posters'], movie.image+'.jpg')
                if not os.path.isfile(dest_file):
                    src_file = os.path.join(tmp_dir, movie.image+'.jpg')
                    if os.path.isfile(src_file):
                        move(src_file, dest_file)
            merged+=1
        rmtree(tmp_dir)

        from initialize    import dictionaries, people_treeview
        dictionaries(self)
        people_treeview(self)
        # let's refresh the treeview
        self.clear_details()
        self.populate_treeview(self.db.Movie.query.all())
        #gutils.info(_("Databases merged!\n\nProcessed movies: %s\nMerged movies: %s"%(movies, merged)), self.widgets['window'])

