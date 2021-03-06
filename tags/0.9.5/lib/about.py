# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes, Piotr Ożarowski
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
import gtk
import version
import os
import sys

class AboutDialog:
	"""Shows a gtk about dialog"""
	def __init__(self, images_dir):
		dialog = gtk.AboutDialog()
		dialog.set_name(version.pname)
		dialog.set_version(version.pversion)
		dialog.set_copyright("Copyright © 2005-2007 Vasco Nunes. Piotr Ożarowski")
		dialog.set_website(version.pwebsite)
		dialog.set_authors([
			_("Main Authors") + ':',
			version.pauthor.replace(', ', '\n') + "\n",
			_("Programmers") + ':',
			'Jessica Katharina Parth <Jessica.K.P@women-at-work.org>',
			'Michael Jahn <mikej06@hotmail.com>\n',
			_('Contributors:'), # FIXME: remove ":"
			'Christian Sagmueller <christian@sagmueller.net>\n' \
			'Arjen Schwarz <arjen.schwarz@gmail.com>'
		])
		dialog.set_artists([_("Logo, icon and general artwork " + \
			"by Peek <peekpt@gmail.com>." + \
			"\nPlease visit http://www.peekmambo.com/\n"),
			'seen / unseen icons by dragonskulle <dragonskulle@gmail.com>'
		])
		dialog.set_translator_credits(\
			_("Brasilian Portuguese") + ":\n\t" + \
				"Fábio Nogueira <deb-user-ba@ubuntu.com>\n\t" + \
				"Alan A. Dantas <alan.arsolto@gmail.com>\n\t" + \
				"Augusta Carla Klug <augusta_klug@yahoo.com.br>\n\t" + \
				"alexandrers <alexandrenescau@gmail.com>\n" + \
			_("Bulgarian") + ":\n\t" + \
				"Luchezar P. Petkov <luchezar.petkov@gmail.com>\n" + \
			_("Catalan") + ":\n\t" + \
				"el_libre <el.libre@gmail.com>\n" + \
			_("Czech") + ":\n\t" + \
				"Blondak <blondak@neser.cz>,\n\t" + \
				"Ondra 'Kepi' Kudlík <kepi@igloonet.cz>\n\t" + \
				"Kamil Páral <ripper42@gmail.com>\n" + \
			_("Danish") + ":\n\t" + \
				"Joe Dalton <joedalton2@yahoo.dk>\n" + \
			_("Dutch") + ":\n\t" + \
				"Marcel Dijkstra <mdtje@hotmail.com>\n\t" + \
				"Tominator <lambik+launchpad@gmail.com>\n\t" + \
				"warddr <ward.ubuntu@gmail.com>\n" + \
			_("French") + ":\n\t" + \
				"Guillaume Pratte <guillaume@guillaumepratte.net>\n\t" + \
				"Pierre-Luc Lévy <pllevy@free.fr>\n\t" + \
				"antou <antoou+inscriptions@gmail.com>\n\t" + \
				"Rémi Preghenella <remi.pregh@gmail.com>\n\t" + \
				"sd2310 <sd2310@gmail.com>\n" + \
			_("German") + ":\n\t" + \
				"Jessica Katharina Parth <Jessica.K.P@women-at-work.org>,\n\t" + \
				"Sebastian Wallroth <sebastian@wallroth.de>\n\t" + \
				"Christian Sagmueller <christian@sagmueller.net>,\n\t" + \
				"Malte Wiemann <ryan2057@gmx.de>\n" + \
			_("Greek") + ":\n\t" + \
				"Ioannis Koniaris <ikoniari@csd.auth.gr>\n\t" + \
				"Athanasia Tziola <erynies@gmail.com>\n\t" + \
				"linuxangel <chraniotis@gmail.com>\n" + \
			_("Italian") + ":\n\t" + \
				"Diego Porcelli <diego.p77@gmail.com>\n\t" + \
				"Simone Vendemia <simonevendemia@gmail.com>\n" + \
			_("Japanese") + ":\n\t" + \
				"Jack Nihil <jnihil@gmail.com>\n" + \
			_("Norwegian Bokmal") + ":\n\t" + \
				"Anders Oftedal <anders.oftedal@gmail.com>\n" + \
			_("Polish") + ":\n\t" + \
				"Piotr Ozarowski <ozarow+griffith@gmail.com>\n" + \
			_("Portuguese") + ":\n\t" + \
				"Vasco Nunes <vasco.m.nunes@gmail.com>\n" + \
			_("Russian") + ":\n\t" + \
				"Pavel V. Kulikov <kulikovpv8256@yandex.ru>\n\t" + \
				"Nkolay Parukhin <nik@sevpinro.ru>\n" + \
			_("Simplified Chinese") + ":\n\t" + \
				"kempson <kempson.chen@gmail.com>\n" + \
			_("Spanish") + ":\n\t" + \
				"Daniel Ucero <escaranbujo@gmail.com>\n" + \
			_("Swedish") + ":\n\t" + \
				"Daniel Nylander <po@danielnylander.se>\n" + \
			_("Turkish") + ":\n\t" + \
				"transorlate <iloveshorts@hotmail.com>\n" \
		)
		logo_file = os.path.abspath(os.path.join(images_dir, 'griffith.png'))
		logo = gtk.gdk.pixbuf_new_from_file(logo_file)
		dialog.set_logo(logo)
		if os.path.isfile('/usr/share/common-licenses/GPL-2'):
			dialog.set_license(open('/usr/share/common-licenses/GPL-2').read())
		else:
			dialog.set_license(_("This program is released under the GNU" + \
				"General Public License.\n" + \
				"Please visit http://www.gnu.org/copyleft/gpl.html for details."))
		dialog.set_comments(version.pdescription)
		dialog.run()
		dialog.destroy()
