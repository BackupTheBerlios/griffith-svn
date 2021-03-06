# -*- coding: UTF-8 -*-

__revision__ = '$Id: gdebug.py 179 2006-02-01 22:24:24Z iznogoud $'

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

class GriffithDebug:
	debug_mode = None
	
	def __init__(self):
		self.debug_mode = False

	def set_debug(self):
		self.debug_mode = True

	def show(self, txt):
		if self.debug_mode:
			print txt.encode('utf8')
