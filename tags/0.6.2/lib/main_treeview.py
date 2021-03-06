# -*- coding: UTF-8 -*-

__revision__ = '$Id: main_treeview.py 264 2006-03-04 22:03:52Z iznogoud $'

# Copyright (c) 2005 Vasco Nunes
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
import os
import gtk

def treeview_clicked(self):
	try:
		tmp = self.initialized # if Griffith is not initialized, return false
	except:
		return
	if self.total:
		self.clear_details()
		treeselection = self.main_treeview.get_selection()
		(tmp_model, tmp_iter) = treeselection.get_selected()
		id = tmp_model.get_value(tmp_iter,1)
		row = self.db.select_movie_by_num(id)[0]

		plot_buffer = self.e_plot.get_buffer()
		obs_buffer = self.e_obs.get_buffer()
		with_buffer = self.e_with.get_buffer()
		with_iter = with_buffer.get_start_iter()

		self.e_movie_id.set_text(str(row['id']))
		self.e_number.set_text(str(row['number']))
		self.e_original_title.set_text(str(row['original_title']))
		self.e_title.set_text(str(row['title']))
		self.e_director.set_text(str(row['director']))
		plot_buffer.set_text(str(row['plot']))
		self.e_discs.set_value(int(row['num_media']))
		if str(row['year']) != "0":
			self.e_year.set_text(str(row['year']))
		if str(row['runtime']) != "0":
			self.e_runtime.set_text(str(row['runtime']))

		with_buffer.set_text(str(row['actors']))

		self.e_country.set_text(str(row['country']))
		self.e_genre.set_text(str(row['genre']))
		if row['condition'] != "":
			self.e_condition.set_active(int(row['condition']))
		if row['region'] != "":
			self.e_region.set_active(int(row['region']))
		if row['layers'] != "":
			self.e_layers.set_active(int(row['layers']))
		if row['color'] != "":
			self.e_color.set_active(int(row['color']))
		self.e_classification.set_text(str(row['classification']))
		self.e_studio.set_text(str(row['studio']))
		self.e_site.set_text(str(row['site']))
		self.e_imdb.set_text(str(row['imdb']))
		if row['seen']:
			self.e_seen.set_active(True)
		else:
			self.e_seen.set_active(False)
		if row['rating']:
			self.image_rating.show()
			self.rating_slider.set_value(int(row['rating']))
		else:
			self.image_rating.hide()
		self.e_trailer.set_text(str(row['trailer']))
		if row['obs']<>None:
			obs_buffer.set_text(str(row['obs']))
		self.e_media.set_active(int(row['media']))
		
		# check loan status and adjust buttons and history box
		if row['loaned']:
			self.popup_loan.set_sensitive(False)
			self.popup_email.set_sensitive(True)
			self.popup_return.set_sensitive(True)
			self.loan_button.set_sensitive(False)
			self.b_email_reminder.set_sensitive(True)
			self.return_button.set_sensitive(True)
		else:
			self.popup_loan.set_sensitive(True)
			self.popup_email.set_sensitive(False)
			self.popup_return.set_sensitive(False)
			self.return_button.set_sensitive(False)
			self.b_email_reminder.set_sensitive(False)
			self.loan_button.set_sensitive(True)

		# poster
		tmp_dest = os.path.join(self.griffith_dir, "posters")
		tmp_img = os.path.join(tmp_dest, "m_%s.jpg"%row['image'])
		tmp_img2 = os.path.join(tmp_dest, "%s.jpg"%row['image'])

		if len(row['image']) and os.path.isfile(tmp_img2):
			image_path = tmp_img
			self.delete_poster.set_sensitive(True)
			self.zoom_poster.set_sensitive(True)
		else:
			image_path = os.path.join(self.locations['images'], "default.png")
			self.delete_poster.set_sensitive(False)
			self.zoom_poster.set_sensitive(False)
		# lets see if we have a scaled down medium image already created
		if os.path.isfile(image_path):
			pass
		else:
			# if not, lets make one for future use :D
			original_image = os.path.join(tmp_dest, "%s.jpg"%row['image'])
			if os.path.isfile(original_image):
				gutils.make_medium_image(self, "%s.jpg"%row['image'])
			else:
				self.Image.set_from_file(os.path.join(self.locations['images'], "default.png"))
				pixbuf = self.Image.get_pixbuf()
		handler = self.e_picture.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image_path))
		if row['loaned']:
			if row['collection_id'] > 0 and self.db.is_collection_loaned(row['collection_id']) == 1:
				data_loan = self.db.get_loan_info(collection_id=row['collection_id'])
			elif row['volume_id'] > 0 and self.db.is_volume_loaned(row['volume_id']) == 1:
				data_loan = self.db.get_loan_info(volume_id=row['volume_id'])
			else:
				data_loan = self.db.get_loan_info(movie_id=row['number'])
			data_person = self.db.select_person_by_id(data_loan[0]['person_id'])
			self.person_name = data_person[0]['name']
			self.person_email = data_person[0]['email']
			self.loan_date = str(data_loan[0]['date'])
			self.loan_info.set_label(self._("This movie has been loaned to ") + self.person_name + self._(" on ") + self.loan_date[:10])
		else:
			self.loan_info.set_label(self._("Movie not loaned"))

		#loan history	
		self.loans_treemodel.clear()						
		loans = self.db.get_loan_history(collection_id=row['collection_id'], volume_id=row['volume_id'], movie_id=row['number'])
		for loan_row in loans:
			myiter = self.loans_treemodel.append(None)
			self.loans_treemodel.set_value(myiter, 0,'%s' % str(loan_row['date'])[:10])
			if loan_row['return_date'] != '':
				self.loans_treemodel.set_value(myiter, 1, str(loan_row['return_date'])[:10])
			else:
				self.loans_treemodel.set_value(myiter, 1, "---")
			person = self.db.select_person_by_id(loan_row['person_id'])
			self.loans_treemodel.set_value(myiter, 2, person[0]['name'])

		#volumes/collections
		i = gutils.findKey(row['volume_id'], self.volume_combo_ids)
		self.e_volume_combo.set_active(i)
		i = gutils.findKey(row['collection_id'], self.collection_combo_ids)
		self.e_collection_combo.set_active(i)
		self.e_volume_id.set_text(str(row['volume_id']))
		self.e_collection_id.set_text(str(row['collection_id']))
		self.e_volume_id.hide()
		self.e_collection_id.hide()

		#languages
		languages = self.db.get_all_data("movie_lang", where="movie_id='%s'" % row['id'])
		self.e_languages = []	# language widgets
		if len(languages) > 0:
			from initialize import create_language_hbox
			for i in languages:
				create_language_hbox(self, widget=self.e_lang_vbox, tab=self.e_languages, default=i['lang_id'], type=i['type'])

		#tags
		for tag in self.db.get_all_data("movie_tag", where="movie_id='%s'" % row['id'], what="tag_id"):
			i = gutils.findKey(tag['tag_id'], self.tags_ids)
			self.e_tags[i].set_active(True)

def populate(self, data):
	self.treemodel.clear()
	for row in data:
		myiter = self.treemodel.append(None)
		self.treemodel.set_value(myiter,1,'%004d' % int(row['number']))

		# check preferences to hide or show columns
		if (self.config.get('view_otitle') == 'True'):
			self.otitle_column.set_visible(True)
		else:
			self.otitle_column.set_visible(False)
		if (self.config.get('view_title') == 'True'):
			self.title_column.set_visible(True)
		else:
			self.title_column.set_visible(False)
		if (self.config.get('view_director') == 'True'):
			self.director_column.set_visible(True)
		else:
			self.director_column.set_visible(False)
		if (self.config.get('view_image') == 'True'):
			self.image_column.set_visible(True)
			tmp_dest = os.path.join(self.griffith_dir, "posters")
			tmp_img = os.path.join(tmp_dest, "t_"+row['image']+".jpg")
			if len(row['image']) and os.path.isfile(tmp_img):
				image_path = tmp_img
			else:
				image_path = self.locations['images'] + "/default_thumbnail.png"
			# lets see if we have a scaled down thumbnail already created
			if os.path.isfile(os.path.join(tmp_dest, "t_"+row['image']+".jpg")):
				pass
			else:
				# if not, lets make one for future use :D
				original_image = os.path.join(tmp_dest, "%s.jpg"%row['image'])
				if os.path.isfile(original_image):
					gutils.make_thumbnail(self, "%s.jpg"%row['image'])
				else:
					self.Image.set_from_file("%s/default_thumbnail.png"%self.locations['images'])
					pixbuf = self.Image.get_pixbuf()
			self.Image.set_from_file(image_path)
			pixbuf = self.Image.get_pixbuf()
			self.treemodel.set_value(myiter, 2, pixbuf)

		else:
			# let's hide image column from main treeview since we don't want it to be visible
			self.image_column.set_visible(False)
		self.treemodel.set_value(myiter,3,str(row['original_title']))
		self.treemodel.set_value(myiter,4,str(row['title']))
		self.treemodel.set_value(myiter,5,str(row['director']))
