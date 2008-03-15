#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Mar  5 15:24:35 2008

__revision__ = '$Id: $'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski

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

# ================================
# Note: indentations with 4 spaces. This is how wxGlade likes to generate files...
# ================================

# set the PATH
import sys, os.path
lib = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'lib'))
if os.path.isdir(lib):
    sys.path.append(lib)
del lib

# check dependencies
from gutils import get_dependencies
(required, extra) = get_dependencies()
missing = []
for i in required:
    if i['version'] is False or (i['version'] is not True and i['version'][0] == '-'):
        missing.append(i)
if len(missing) > 0:
    print 'Error: missing modules:'
    for i in missing:
        print "%(module)s" % i,
        if i.has_key('module_req'):
            print "\t:: required version: %(module_req)s" % i,
            if i['version'] is not False and i['version'][0] == '-':
                print "\t:: detected: %(version)s" % i
        print "\n",
    sys.exit(1)
del missing

# other imports
import wx
import add, config, gconsole, gutils, gdebug, initialize, main_treeview, quick_filter

# begin wxGlade: extracode
# end wxGlade

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
    
        # debug object
        global debug
        debug = self.debug = gdebug.GriffithDebug()

        gconsole.check_args(self)
        initialize.locations(self)
        initialize.i18n(self, self.locations['i18n'])
        self.posix = (os.name == 'posix')
        
        # Configuration
        if self._tmp_config.find('/') >=0 or self._tmp_config.find('\\') >=0:
            configFileName = self._tmp_config
        else:
            configFileName = os.path.join(self.locations['home'], self._tmp_config)
        self.config = config.Config(file=configFileName)
        initialize.location_posters(self.locations, self.config)
        
        # convert old database
        filename = os.path.join(self.locations['home'], self.config.get('file', 'griffith.db', section='database'))
        if self.config.get('file', 'griffith.db', section='database').lower().endswith('.gri'):
            debug.show('Old database format detected. Converting...')
            from dbupgrade import convert_from_old_db
            if convert_from_old_db(self, filename, os.path.join(self.locations['home'], 'griffith.db')):
                self.config.save()
                initialize.location_posters(self.locations, self.config)
            else:
                print 'Cant convert old database, exiting.'
                sys.exit(4)     
        
        # create/connect db
        from sql import GriffithSQL
        self.db = GriffithSQL(self.config, self.debug, self.locations['home'])
        
        # let's check any console arguments to parse
        gconsole.check_args_with_db(self)
        
        self.filter_l = False
        
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_2 = wx.Panel(self.window_1, -1)
        self.notebook_1 = wx.Notebook(self.window_1_pane_2, -1, style=0)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1)
        
        # Menu Bar
        self.main_frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.new = wx.MenuItem(wxglade_tmp_menu, 1, _("New"), _("Start a blank database"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.new)
        self.save_as = wx.MenuItem(wxglade_tmp_menu, 2, _("Save as..."), _("Make a backup of the database"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.save_as)
        self.revert = wx.MenuItem(wxglade_tmp_menu, 3, _("Revert"), _("Revert to a previous database backup"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.revert)
        wxglade_tmp_menu.AppendSeparator()
        self.import_data = wx.MenuItem(wxglade_tmp_menu, 4, _("Import"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.import_data)
        self.export_data = wx.MenuItem(wxglade_tmp_menu, 5, _("Export"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.export_data)
        wxglade_tmp_menu.AppendSeparator()
        self.exit = wx.MenuItem(wxglade_tmp_menu, wx.ID_EXIT, _("Exit"), _("Terminate the program"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.exit)
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("File"))
        wxglade_tmp_menu = wx.Menu()
        self.add = wx.MenuItem(wxglade_tmp_menu, 7, _("Add"), _("Add a new record"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.add)
        self.delete = wx.MenuItem(wxglade_tmp_menu, 8, _("Delete"), _("Deletes a record"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.delete)
        self.edit = wx.MenuItem(wxglade_tmp_menu, 9, _("Edit"), _("Edit a record"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.edit)
        self.duplicate = wx.MenuItem(wxglade_tmp_menu, 10, _("Duplicate"), _("Duplicates a record"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.duplicate)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu_sub = wx.Menu()
        self.open = wx.MenuItem(wxglade_tmp_menu_sub, 11, _("Open"), _("Opens the poster viewer"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.AppendItem(self.open)
        self.fetch = wx.MenuItem(wxglade_tmp_menu_sub, 12, _("Fetch from Amazon"), _("Fetches a poster using Amazon service"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.AppendItem(self.fetch)
        self.erase = wx.MenuItem(wxglade_tmp_menu_sub, 13, _("Erase"), _("Erase the current poster"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.AppendItem(self.erase)
        wxglade_tmp_menu.AppendMenu(wx.NewId(), _("Poster image"), wxglade_tmp_menu_sub, "")
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("Edit"))
        wxglade_tmp_menu = wx.Menu()
        self.view_toolbar = wx.MenuItem(wxglade_tmp_menu, 14, _("Toolbar"), _("Toggles toolbar visibility"), wx.ITEM_CHECK)
        wxglade_tmp_menu.AppendItem(self.view_toolbar)
        wxglade_tmp_menu.AppendSeparator()
        self.view_not_seen = wx.MenuItem(wxglade_tmp_menu, 15, _("Not seen"), _("View only not seen"), wx.ITEM_RADIO)
        wxglade_tmp_menu.AppendItem(self.view_not_seen)
        self.view_loaned = wx.MenuItem(wxglade_tmp_menu, 16, _("Loaned"), _("View only loaned"), wx.ITEM_RADIO)
        wxglade_tmp_menu.AppendItem(self.view_loaned)
        self.view_all = wx.MenuItem(wxglade_tmp_menu, 17, _("All"), _("View all records"), wx.ITEM_RADIO)
        wxglade_tmp_menu.AppendItem(self.view_all)
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("View"))
        wxglade_tmp_menu = wx.Menu()
        self.suggest = wx.MenuItem(wxglade_tmp_menu, 18, _("Suggest"), _("Suggest an unseen film"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.suggest)
        wxglade_tmp_menu_sub = wx.Menu()
        self.print_cover_builtin = wx.MenuItem(wxglade_tmp_menu_sub, 19, _("Built-in"), _("Prints a cover with record data"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.AppendItem(self.print_cover_builtin)
        self.prints_cover_custom = wx.MenuItem(wxglade_tmp_menu_sub, 20, _("Custom"), _("Prints a cover with a custom image"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.AppendItem(self.prints_cover_custom)
        wxglade_tmp_menu.AppendMenu(wx.NewId(), _("Print cover"), wxglade_tmp_menu_sub, "")
        wxglade_tmp_menu.AppendSeparator()
        self.preferences = wx.MenuItem(wxglade_tmp_menu, wx.ID_PREFERENCES, _("Preferences"), _("Define the preferences"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.preferences)
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("Tools"))
        wxglade_tmp_menu = wx.Menu()
        self.loan_film = wx.MenuItem(wxglade_tmp_menu, 22, _("Loan"), _("Loans a film"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.loan_film)
        self.return_film = wx.MenuItem(wxglade_tmp_menu, 23, _("Return"), _("Returns a previously loaned film"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.return_film)
        self.email_reminder = wx.MenuItem(wxglade_tmp_menu, 24, _("E-mail reminder"), _("Sends an automatic loan reminder e-mail message "), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.email_reminder)
        wxglade_tmp_menu.AppendSeparator()
        self.people = wx.MenuItem(wxglade_tmp_menu, 25, _("People"), _("Manages people information"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.people)
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("Loans"))
        wxglade_tmp_menu = wx.Menu()
        self.homepage = wx.MenuItem(wxglade_tmp_menu, 26, _("Homepage"), _("Visit Griffith's homepage"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.homepage)
        self.forum = wx.MenuItem(wxglade_tmp_menu, 27, _("Forum"), _("Visit Griffith's community forum"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.forum)
        self.reportbug = wx.MenuItem(wxglade_tmp_menu, 28, _("Reportbug"), _("Report a new bug"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.reportbug)
        wxglade_tmp_menu.AppendSeparator()
        self.about = wx.MenuItem(wxglade_tmp_menu, wx.ID_ABOUT, _("About"), _("Display information about this program"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.about)
        self.main_frame_menubar.Append(wxglade_tmp_menu, _("Help"))
        self.SetMenuBar(self.main_frame_menubar)
        # Menu Bar end
        self.main_frame_statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.main_frame_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_DOCKABLE|wx.TB_TEXT)
        self.SetToolBar(self.main_frame_toolbar)
        self.main_frame_toolbar.AddLabelTool(1004, _("First"), wx.Bitmap("images/go-first.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.main_frame_toolbar.AddLabelTool(1003, _("Previous"), wx.Bitmap("images/go-previous.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.main_frame_toolbar.AddLabelTool(1004, _("Next"), wx.Bitmap("images/go-next.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.main_frame_toolbar.AddLabelTool(1005, _("Last"), wx.Bitmap("images/go-last.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.main_frame_toolbar.AddSeparator()
        self.main_frame_toolbar.AddLabelTool(1006, _("Add"), wx.Bitmap("images/document-new.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Add a new film"), _("Add a new film to the collection"))
        self.main_frame_toolbar.AddLabelTool(1008, _("Delete"), wx.Bitmap("images/user-trash.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Delete this film"), _("Deletes this film from collection"))
        self.main_frame_toolbar.AddLabelTool(1009, _("Edit"), wx.Bitmap("images/edit-select-all.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Edit film details"), _("Edit film details"))
        self.main_frame_toolbar.AddSeparator()
        self.main_frame_toolbar.AddLabelTool(1010, _("Webpage"), wx.Bitmap("images/applications-internet.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Go to the film webpage"), _("Go to the film webpage"))
        self.main_frame_toolbar.AddSeparator()
        self.main_frame_toolbar.AddLabelTool(1013, _("Amazon Poster"), wx.Bitmap("images/applications-graphics.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Add Poster From Amazon"), _("Try to find a poster using the Amazon Services on the web"))
        self.main_frame_toolbar.AddSeparator()
        self.main_frame_toolbar.AddLabelTool(1014, _("People"), wx.Bitmap("images/system-users.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        # Tool Bar end
        self.label_1 = wx.StaticText(self, -1, _("Filter"))
        self.tc_filter = wx.TextCtrl(self, -1, "")
        self.bt_clear_filter = wx.Button(self, -1, _("clear"))
        self.cb_criteria = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.main_listcontrol = wx.ListCtrl(self.window_1_pane_1, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.number = wx.StaticText(self.window_1_pane_2, -1, _("label_2"))
        self.o_title = wx.StaticText(self.window_1_pane_2, -1, _("label_2"))
        self.title = wx.StaticText(self.window_1_pane_2, -1, _("label_2"))
        self.poster = wx.BitmapButton(self.window_1_pane_2, -1, wx.NullBitmap, style=wx.BU_AUTODRAW)
        self.plot = wx.TextCtrl(self.notebook_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_AUTO_URL|wx.TE_LINEWRAP|wx.TE_WORDWRAP)
        self.cast = wx.TextCtrl(self.notebook_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_AUTO_URL|wx.TE_LINEWRAP|wx.TE_WORDWRAP)
        self.notes = wx.TextCtrl(self.notebook_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_AUTO_URL|wx.TE_LINEWRAP|wx.TE_WORDWRAP)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnNew, self.new)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.save_as)
        self.Bind(wx.EVT_MENU, self.OnRevert, self.revert)
        self.Bind(wx.EVT_MENU, self.OnImport, self.import_data)
        self.Bind(wx.EVT_MENU, self.OnExport, self.export_data)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit)
        self.Bind(wx.EVT_MENU, self.OnAdd, self.add)
        self.Bind(wx.EVT_MENU, self.OnDelete, self.delete)
        self.Bind(wx.EVT_MENU, self.OnEdit, self.edit)
        self.Bind(wx.EVT_MENU, self.onDuplicate, self.duplicate)
        self.Bind(wx.EVT_MENU, self.OnPosterOpen, self.open)
        self.Bind(wx.EVT_MENU, self.OnPosterFromAmazon, self.fetch)
        self.Bind(wx.EVT_MENU, self.OnPosterErase, self.erase)
        self.Bind(wx.EVT_MENU, self.OnViewToolbar, self.view_toolbar)
        self.Bind(wx.EVT_MENU, self.OnViewNotSeen, self.view_not_seen)
        self.Bind(wx.EVT_MENU, self.OnViewLoaned, self.view_loaned)
        self.Bind(wx.EVT_MENU, self.OnViewAll, self.view_all)
        self.Bind(wx.EVT_MENU, self.OnSuggest, self.suggest)
        self.Bind(wx.EVT_MENU, self.OnPrintCoverBuiltin, self.print_cover_builtin)
        self.Bind(wx.EVT_MENU, self.OnPrintCoverCustom, self.prints_cover_custom)
        self.Bind(wx.EVT_MENU, self.OnPreferences, self.preferences)
        self.Bind(wx.EVT_MENU, self.OnLoanFilm, self.loan_film)
        self.Bind(wx.EVT_MENU, self.OnReturnFilm, self.return_film)
        self.Bind(wx.EVT_MENU, self.OnEmailReminder, self.email_reminder)
        self.Bind(wx.EVT_MENU, self.OnPeople, self.people)
        self.Bind(wx.EVT_MENU, self.OnHomepage, self.homepage)
        self.Bind(wx.EVT_MENU, self.OnForum, self.forum)
        self.Bind(wx.EVT_MENU, self.OnReportBug, self.reportbug)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.about)
        self.Bind(wx.EVT_TOOL, self.OnFirst, id=1004)
        self.Bind(wx.EVT_TOOL, self.OnPrevious, id=1003)
        self.Bind(wx.EVT_TOOL, self.OnNext, id=1004)
        self.Bind(wx.EVT_TOOL, self.OnLast, id=1005)
        self.Bind(wx.EVT_TOOL, self.OnAdd, id=1006)
        self.Bind(wx.EVT_TOOL, self.OnDelete, id=1008)
        self.Bind(wx.EVT_TOOL, self.OnEdit, id=1009)
        self.Bind(wx.EVT_TOOL, self.OnWebpage, id=1010)
        self.Bind(wx.EVT_TOOL, self.OnAddAmazonPoster, id=1013)
        self.Bind(wx.EVT_TOOL, self.OnPeople, id=1014)
        self.Bind(wx.EVT_TEXT, self.OnFilterChange, self.tc_filter)
        self.Bind(wx.EVT_BUTTON, self.OnClearFilter, self.bt_clear_filter)
        self.Bind(wx.EVT_TEXT, self.OnChangeCriteria, self.cb_criteria)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnMainListDelete, self.main_listcontrol)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnMainListSelected, self.main_listcontrol)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnMainLColumnClicked, self.main_listcontrol)
        # end wxGlade
        
        initialize.locations_misc(self)
        #initialize.toolbar(self)
        initialize.treeview(self)
        #initialize.loans_treeview(self)
        #initialize.lang_treeview(self)
        initialize.dictionaries(self)
        initialize.combos(self)
        #initialize.preferences(self)
        #initialize.movie_plugins(self)
        #initialize.export_plugins(self)
        #initialize.people_treeview(self)
        #initialize.web_results(self)
        self.initialized = True
        #self.restore_state()
        #self.clear_details()
        self.populate_treeview()

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle(_("Griffith"))
        self.SetSize((684, 706))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.main_frame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        main_frame_statusbar_fields = [_("Ready")]
        for i in range(len(main_frame_statusbar_fields)):
            self.main_frame_statusbar.SetStatusText(main_frame_statusbar_fields[i], i)
        self.main_frame_toolbar.Realize()
        self.tc_filter.SetMinSize((200, -1))
        self.number.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 1, ""))
        self.o_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.title.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL, 0, ""))
        self.poster.SetMinSize((150, 200))
        self.plot.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.cast.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.notes.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_1, 0, 0, 0)
        sizer_5.Add(self.tc_filter, 0, 0, 0)
        sizer_5.Add(self.bt_clear_filter, 0, 0, 0)
        sizer_5.Add(self.cb_criteria, 0, 0, 0)
        sizer_1.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_2.Add(self.main_listcontrol, 1, wx.EXPAND, 0)
        self.window_1_pane_1.SetSizer(sizer_2)
        sizer_4.Add(self.number, 0, wx.ALL, 0)
        sizer_4.Add(self.o_title, 0, 0, 0)
        sizer_4.Add(self.title, 0, 0, 0)
        sizer_4.Add(self.poster, 0, wx.ALL, 1)
        self.notebook_1.AddPage(self.plot, _("Plot"))
        self.notebook_1.AddPage(self.cast, _("Actors"))
        self.notebook_1.AddPage(self.notes, _("Notes"))
        sizer_4.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        self.window_1_pane_2.SetSizer(sizer_3)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnNew(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnNew' not implemented"
        event.Skip()

    def OnSaveAs(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnSaveAs' not implemented"
        event.Skip()

    def OnRevert(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnRevert' not implemented"
        event.Skip()

    def OnImport(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnImport' not implemented"
        event.Skip()

    def OnExport(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnExport' not implemented"
        event.Skip()

    def OnExit(self, event): # wxGlade: MainFrame.<event_handler>
        self.Close(True)

    def OnAdd(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnAdd' not implemented"
        event.Skip()

    def OnDelete(self, event): # wxGlade: MainFrame.<event_handler>
        from delete import delete_movie
        response = gutils.question(self, _("Are you sure you want to delete these entries?"), \
            _("Delete entries"))
        if response == wx.ID_YES:
            delete_movie(self)

    def OnEdit(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnEdit' not implemented"
        event.Skip()

    def onDuplicate(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `onDuplicate' not implemented"
        event.Skip()

    def OnPosterOpen(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPosterOpen' not implemented"
        event.Skip()

    def OnPosterFromAmazon(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPosterFromAmazon' not implemented"
        event.Skip()

    def OnPosterErase(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPosterErase' not implemented"
        event.Skip()

    def OnViewToolbar(self, event): # wxGlade: MainFrame.<event_handler>
        self.main_frame_toolbar.Show(False)

    def OnViewNotSeen(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnViewNotSeen' not implemented"
        event.Skip()

    def OnViewLoaned(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnViewLoaned' not implemented"
        event.Skip()

    def OnViewAll(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnViewAll' not implemented"
        event.Skip()

    def OnSuggest(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnSuggest' not implemented"
        event.Skip()

    def OnPrintCoverBuiltin(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPrintCoverBuiltin' not implemented"
        event.Skip()

    def OnPrintCoverCustom(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPrintCoverCustom' not implemented"
        event.Skip()

    def OnPreferencies(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPreferencies' not implemented"
        event.Skip()

    def OnLoan(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnLoan' not implemented"
        event.Skip()

    def OnReturn(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnReturn' not implemented"
        event.Skip()

    def OnEmailReminder(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnEmailReminder' not implemented"
        event.Skip()

    def OnPeople(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPeople' not implemented"
        event.Skip()

    def OnHomepage(self, event): # wxGlade: MainFrame.<event_handler>
        gutils.run_browser(version.pwebsite)

    def OnForum(self, event): # wxGlade: MainFrame.<event_handler>
        gutils.run_browser(version.pforum)

    def OnReportBug(self, event): # wxGlade: MainFrame.<event_handler>
        gutils.run_browser(version.pbugtracker)

    def OnAbout(self, event): # wxGlade: MainFrame.<event_handler>
        from about import display_about
        display_about()

    def OnLoanFilm(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnLoanFilm' not implemented"
        event.Skip()

    def OnReturnFilm(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnReturnFilm' not implemented"
        event.Skip()

    def OnFirst(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnFirst' not implemented"
        event.Skip()

    def OnMainListSelected(self, event): # wxGlade: MainFrame.<event_handler>
        index = self.main_listcontrol.GetFirstSelected()
        item = self.main_listcontrol.GetItem(index)
        main_treeview.treeview_clicked(self,item.GetText())
            
    def populate_treeview(self, statement=None, where=None):
        main_treeview.populate(self, statement, where)

    def OnMainListDelete(self, event): # wxGlade: MainFrame.<event_handler>
        from delete import delete_movie
        delete_movie(self)

    def OnPreferences(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPreferences' not implemented"
        event.Skip()

    def OnPrevious(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnPrevious' not implemented"
        event.Skip()

    def OnNext(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnNext' not implemented"
        event.Skip()

    def OnLast(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnLast' not implemented"
        event.Skip()

    def OnWebpage(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnWebpage' not implemented"
        event.Skip()

    def OnAddLocalPoster(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnAddLocalPoster' not implemented"
        event.Skip()

    def OnRemovePoster(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnRemovePoster' not implemented"
        event.Skip()

    def OnAddAmazonPoster(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `OnAddAmazonPoster' not implemented"
        event.Skip()

    def OnFilterChange(self, event): # wxGlade: MainFrame.<event_handler>
        quick_filter.change_filter(self)

    def OnClearFilter(self, event): # wxGlade: MainFrame.<event_handler>
        self.tc_filter.Clear()
        main_treeview.populate(self)

    def OnChangeCriteria(self, event): # wxGlade: MainFrame.<event_handler>
        selected_criteria = self.cb_criteria.GetValue()
        self.config.set('criteria', selected_criteria, section='mainlist')
        quick_filter.change_filter(self)

    def OnMainLColumnClicked(self, event): # wxGlade: MainFrame.<event_handler>
        print "not implemented"

# end of class MainFrame

class GriffithApp(wx.App):
    def OnInit(self):
        # show a splashscreen
        image = wx.Image("images/splash.bmp", wx.BITMAP_TYPE_BMP)
        bmp = image.ConvertToBitmap()
        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN |
            wx.SPLASH_TIMEOUT, 2000, None, -1)
        wx.Yield()
        wx.InitAllImageHandlers()
        main_frame = MainFrame(None, -1, "")
        self.SetTopWindow(main_frame)
        main_frame.Show()
        return 1

# end of class GriffithApp

if __name__ == "__main__":
    import gettext
    gettext.install("griffith") # replace with the appropriate catalog name

    griffith = GriffithApp(0)
    griffith.MainLoop()