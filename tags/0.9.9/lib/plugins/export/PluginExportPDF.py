# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes
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

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.rl_config import defaultPageSize
from reportlab.rl_config import defaultEncoding
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax import saxutils
import os, gtk
import version
import gutils
import string
import sys
import config
from locale import getdefaultlocale
from sqlalchemy import Select, desc

exec_location = os.path.abspath(os.path.dirname(sys.argv[0]))

plugin_name = "PDF"
plugin_description = _("PDF export plugin")
plugin_author = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.4"

class ExportPlugin:
    def __init__(self, database, locations, parent_window, debug, **kwargs):
        self.db = database
        self.locations = locations
        self.parent = parent_window
        self.config = kwargs['config']
        self.styles = getSampleStyleSheet()
        self.export_simple_pdf()
        self.fontName = ""

    def export_simple_pdf(self):
        """exports a simple movie list to a pdf file"""
        
        if self.config.get('font', '') != '':
                self.fontName = 'custom_font'
                pdfmetrics.registerFont(TTFont(self.fontName, self.config.get('font', '')))
        else:
                self.fontName = "Helvetica"

        basedir = None
        if not self.config is None:
            basedir = self.config.get('export_dir', None, section='export-pdf')
        if basedir is None:
            filename = gutils.file_chooser(_("Export a PDF"), action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK),name="griffith_simple_list.pdf")
        else:
            filename = gutils.file_chooser(_("Export a PDF"), action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK),name="griffith_simple_list.pdf",folder=basedir)
        if filename is not False and filename[0]:
            if not self.config is None and filename[1]:
                self.config.set('export_dir', filename[1], section='export-pdf')
                self.config.save()
            overwrite = None
            pdffilename = filename[0].decode('utf-8')
            if os.path.isfile(pdffilename):
                response = gutils.question(self,_("File exists. Do you want to overwrite it?"),1,self.parent)
                if response==-8:
                    overwrite = True
                else:
                    overwrite = False
                    
            if overwrite == True or overwrite is None:
                # filename encoding
                defaultLang, defaultEnc = getdefaultlocale()
                if defaultEnc is None:
                    defaultEnc = 'UTF-8'
                c = SimpleDocTemplate(pdffilename.encode(defaultEnc))
                # data encoding
                #if defaultEncoding == 'WinAnsiEncoding':
                #    defaultEnc = 'cp1252'
                #else:
                defaultEnc = 'utf-8'
                style = self.styles["Normal"]
                Story = [Spacer(1,2*inch)]
                # define some custom stylesheetfont
                total = self.db.Movie.count()
                p = Paragraph("<font name='" + self.fontName +"' size=\"18\">" + saxutils.escape((_("List of films")).encode('utf-8')) + '</font>', self.styles["Heading1"] )
                Story.append(p)
                Story.append(Paragraph(" ",style))
                p = Paragraph("<font name='" + self.fontName +"' size=\"10\">" + saxutils.escape((_("Total Movies: %s") % str(total)).encode('utf-8'))  + '</font>', self.styles["Heading3"])
                Story.append(p)
                Story.append(Paragraph(" ",style))
                movies = Select(self.db.Movie.c)
                # select sort column
                sort_column_name = self.config.get('sortby', 'number', section='mainlist')
                sort_reverse = self.config.get('sortby_reverse', False, section='mainlist')
                do_grouping = True
                for i in sort_column_name.split(','):
                    if i != 'title' and i != 'o_title':
                        do_grouping = False
                    if self.db.Movie.c.has_key(i):
                        if sort_reverse:
                            movies.order_by_clause.append(desc(self.db.Movie.c[i]))
                        else:
                            movies.order_by_clause.append(self.db.Movie.c[i])
                movies = movies.execute().fetchall()
                first_letter = '0'
                for movie in movies:
                    number = movie.number
                    original_title = str(movie.o_title).encode(defaultEnc)
                    title = str(movie.title).encode(defaultEnc)
                    grouping_title = movie.title
                    if grouping_title is None:
                        grouping_title = u'None'
                    if movie.director:
                        director = ' - ' + str(movie.director).encode(defaultEnc)
                    else:
                        director = ""
                    # group by first letter
                    # use movie.title/grouping_title for grouping because of encoding problems !!!
                    if do_grouping and grouping_title[0] != first_letter:
                        if grouping_title[0] in '0123456789':
                            # Group Numbers
                            if first_letter != '0-9':
                                first_letter = '0-9'
                                paragraph_text = '<font name=' + self.fontName + ' size="15">' + saxutils.escape(first_letter) + '</fonts>'
                                p = Paragraph(paragraph_text.decode(defaultEnc), self.styles['Heading2'])
                                Story.append(p)
                        else:
                            first_letter = grouping_title[0]
                            paragraph_text = '<font name=' + self.fontName + ' size="15">' + saxutils.escape(first_letter) + '</fonts>'
                            p = Paragraph(paragraph_text.decode(defaultEnc), self.styles['Heading2'])
                            Story.append(p)
                    # add movie title
                    paragraph_text = '<font name=' + self.fontName + ' size="7">' + \
                        '<b>'+ saxutils.escape(title) + '</b>' + \
                        saxutils.escape(' (' + original_title + '), ' + director + ' | ' + str(number)) + \
                        '</font>'
                    p = Paragraph(paragraph_text.decode(defaultEnc), self.styles['Normal'])
                    Story.append(p)
                    if not movie.genre is None:
                        paragraph_text = '<font name=' + self.fontName + ' size="5">' + \
                        '<b>' + _('Genre') + ': </b>' + saxutils.escape(str(movie.genre).encode(defaultEnc)) + \
                        '</font>'
                        p = Paragraph(paragraph_text.decode(defaultEnc), self.styles['Normal'])
                        Story.append(p)
                    if not movie.cast is None:
                        paragraph_text = '<i><font name=' + self.fontName + ' size="5">' + \
                        '<b>' + _('Cast') + ': </b>' + saxutils.escape('; '.join(str(movie.cast).encode(defaultEnc).split("\n")[0:2])) + \
                            '</font></i>'
                        p = Paragraph(paragraph_text.decode(defaultEnc), self.styles['Normal'])
                        Story.append(p)
                c.build(Story, onFirstPage=self.page_template, onLaterPages=self.page_template)
                gutils.info(self, _('PDF has been created.'), self.parent)
            
    def page_template(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.fontName,7)
        canvas.drawCentredString(defaultPageSize[0]/2, 40,_("Page %d") % doc.page)
        canvas.setFont(self.fontName,5)
        canvas.drawCentredString(defaultPageSize[0]/2, 20, (_("Document generated by Griffith v")+
            version.pversion+" - Copyright (C) "+version.pyear+" "+
            version.pauthor+" - " + _("Released Under the GNU/GPL License")).encode('utf-8'))
        canvas.restoreState()
