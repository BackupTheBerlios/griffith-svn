# please use current py2app trunk from svn

from distutils.core import setup
import py2app
import glob

            argv_emulation=1,
            optimize=2,
includes="cairo,pangocairo,pysqlite2,pysqlite2.*,cgi,PIL,pysqlite2,pysqlite2.*,pango,atk,gobject,tempfile,csv,xml.dom,xml.dom.ext,xml.dom.minidom,xml.sax,threading,htmlentitydefs,sqlalchemy,sqlalchemy.*,sqlalchemy.mods.*,sqlalchemy.databases.*,sqlalchemy.engine.*,sqlalchemy.ext.*,sqlalchemy.orm.*,zipfile,webbrowser,shutil,reportlab,reportlab.pdfgen,reportlab.pdfgen.canvas,reportlab.platypus,reportlab.pdfbase.ttfonts,smtplib,platform,psycopg2,MySQLdb,pygtk", 