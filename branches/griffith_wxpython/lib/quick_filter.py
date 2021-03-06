# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

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

from gettext import gettext as _
import gutils

def change_filter(self):
    x = 0
    text = gutils.gescape(self.tc_filter.GetValue())
    
    from sqlalchemy import select
    statement = select(self.db.Movie.c)
    
    if text:
        criteria = self.search_criteria[self.cb_criteria.GetSelection()]
        if criteria in ('year', 'runtime', 'media_num', 'rating'):
            statement.append_whereclause(self.db.Movie.c[criteria]==text)
        else:
            statement.append_whereclause(self.db.Movie.c[criteria].like('%'+text+'%'))
            
    self.populate_treeview(statement)