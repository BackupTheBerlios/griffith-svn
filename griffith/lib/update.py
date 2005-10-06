# -*- coding: UTF-8 -*-

__revision__ = '$Id: update.py,v 1.19 2005/10/01 15:46:14 iznogoud Exp $'

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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import os
import gdebug

def update(self):
	movie_id = self.e_number.get_text()
	self.db.cursor.execute("SELECT loaned, volume_id, collection_id FROM movies WHERE number='%s'"%movie_id)
	loaned, volume_id, collection_id = self.db.cursor.fetchall()[0]
	new_volume_id = self.e_volume_combo.get_active()
	new_collection_id = self.e_collection_combo.get_active()
	if loaned:
		if collection_id>0 and collection_id != new_collection_id:
			gutils.error(self, msg=_("You can't change collection while it is loaned!"))
			return False
		if volume_id>0 and volume_id != new_volume_id:
			gutils.error(self, msg=_("You can't change volume while it is loaned!"))
			return False
	plot_buffer = self.e_plot.get_buffer()
	with_buffer = self.e_with.get_buffer()
	obs_buffer = self.e_obs.get_buffer()
	seen = '0'
	if self.e_seen.get_active():
		seen = '1'
	if (self.e_original_title.get_text()<>''):
		self.db.cursor.execute(
			"UPDATE movies SET original_title = '"
			+gutils.gescape(self.e_original_title.get_text())+"', title ='"
			+gutils.gescape(self.e_title.get_text())+"', director='"
			+gutils.gescape(self.e_director.get_text())+"', plot ='"
			+gutils.gescape(plot_buffer.get_text(plot_buffer.get_start_iter(),plot_buffer.get_end_iter()))+"', year='"
			+self.e_year.get_text()+"', runtime ='"
			+self.e_runtime.get_text()+"',actors = '"
			+gutils.gescape(with_buffer.get_text(with_buffer.get_start_iter(),with_buffer.get_end_iter()))+"', country='"
			+self.e_country.get_text()+"', genre ='"
			+self.e_genre.get_text()+"', rating ='"
			+str(int(self.rating_slider.get_value()))+"', classification ='"
			+self.e_classification.get_text()+"', studio = '"
			+self.e_studio.get_text()+"', site ='"
			+self.e_site.get_text()+"', condition ="
		
			+str(self.e_condition.get_active())+", color ="
			+str(self.e_color.get_active())+", region ="
			+str(self.e_region.get_active())+", layers ="
			+str(self.e_layers.get_active())+", imdb ='"
			
			+self.e_imdb.get_text()+"', seen ='"
			+seen+"', obs ='"
			+gutils.gescape(obs_buffer.get_text(obs_buffer.get_start_iter(),obs_buffer.get_end_iter()))+"', trailer='"
			+self.e_trailer.get_text()+"', media ='"
			+gutils.on_combo_box_entry_changed(self.e_media)
			+"', num_media ='" + self.e_discs.get_text()
			+"', volume_id='" + str(new_volume_id)
			+"', collection_id='" + str(new_collection_id)
		
			+"' WHERE number = '" + self.e_number.get_text() +"'"
		)
		self.update_statusbar(_("Movie information has been updated"))
		# update main treelist
		treeselection = self.main_treeview.get_selection()
		(tmp_model, tmp_iter) = treeselection.get_selected()
		tmp_model.set_value(tmp_iter,3,self.e_original_title.get_text())
		tmp_model.set_value(tmp_iter,4,self.e_title.get_text())
		tmp_model.set_value(tmp_iter,5,self.e_director.get_text())
	else:
		gutils.error(self.w_results,_("You should fill the original title"))

def update_image(self,image,id):
	self.db.cursor.execute(
		"UPDATE movies SET image = '"
		+"t_"+os.path.splitext(image)[0]+"' WHERE number = '"+id+"'")
	self.db.con.commit()
	self.update_statusbar(_("Image has been updated"))
	
def clear_image(self,id):
	self.db.cursor.execute(
		"UPDATE movies SET image = '' WHERE number = '"+id+"'")
	self.db.con.commit()
	self.update_statusbar(_("Image has been updated"))

def update_collection(self, id, name=None, volume_id=None, loaned=None):
	if name!=None:
		try:
			self.db.cursor.execute("UPDATE collections SET name = '%s' WHERE id = '%s';"%(name,id))
		except:
			gdebug.debug("ERROR during updating collection's name!")
			return False
	if loaned==1:
		try:
			self.db.cursor.execute("""
				UPDATE collections SET loaned='1' WHERE id='%s';
				UPDATE movies SET loaned='1' WHERE collection_id='%s';
			""" % (id, id))
		except:
			gdebug.debug("ERROR during updating collection's loan data!")
			return False
		if volume_id:
			try:
				self.db.cursor.execute("UPDATE volumes SET loaned='1' WHERE id='%s';"%volume_id)
			except:
				gdebug.debug("ERROR during updating volume's loan data!")
				return False
	elif loaned==0:
		try:
			self.db.cursor.execute("""
				UPDATE collections SET loaned='0' WHERE id='%s';
				UPDATE movies SET loaned='0' WHERE collection_id='%s';
			""" %( id, id))
		except:
			gdebug.debug("ERROR during updating collection's loan data!")
			return False
		if volume_id:
			try:
				self.db.cursor.execute("UPDATE volumes SET loaned='0' WHERE id='%s';"%volume_id)
			except:
				gdebug.debug("ERROR during updating volume's loan data!")
				return False

def update_volume(self, id, name=None, loaned=None):
	if name!=None:
		try:
			self.db.cursor.execute("UPDATE volumes SET name = '%s' WHERE id = '%s';"%(name,id))
		except:
			gdebug.debug("ERROR during updating volume's name!")
			return False
	if loaned==1:
		try:
			self.db.cursor.execute("""
				UPDATE volumes SET loaned=1 WHERE id='%s';
				UPDATE movies SET loaned=1 WHERE volume_id='%s';
			"""%(id, id))
		except:
			gdebug.debug("ERROR during updating volume's loan data!")
			return False
	elif loaned==0:
		try:
			self.db.cursor.execute("""
				UPDATE volumes SET loaned=0 WHERE id='%s';
				UPDATE movies SET loaned=0 WHERE volume_id='%s';
			"""%(id, id))
		except:
			gdebug.debug("ERROR during updating volume's loan data!")
			return False
