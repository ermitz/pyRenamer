# -*- coding: utf-8 -*-

"""
Copyright (C) 2006-07 Adolfo González Blázquez <code@infinicode.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

If you find any bugs or have any suggestions email: code@infinicode.org
"""

from gettext import gettext as _
import os.path
import user

import build_info

have_hachoir = True
have_eyed3 = False

# Check for hachoir_metadata
try:
    import hachoir_metadata
except ImportError, e:
    if str(e).find("hachoir_metadata") >= 0:
          have_hachoir = False
          print "WARNING: python-hachoir-metadata not found."
except:
    have_hachoir = False
    print "WARNING: python-hachoir-metadata not found."

# Check for eyed3
if not have_hachoir:

	# Check for eyeD3
	have_eyed3 = True
	try:
	    import eyeD3
	except ImportError, e:
	    if str(e).find("eyeD3") >= 0:
	          have_eyed3 = False
	          print "WARNING: python-eyed3 not found."
	except:
	    have_eyed3 = False
	    print "WARNING: python-eyed3 not found."

if not (have_hachoir or have_eyed3):
	print "WARNING: Music rename disabled!"

pixmaps_dir = build_info.RESOURCE_DIR
resources_dir = build_info.RESOURCE_DIR
locale_dir = build_info.LOCALE_DIR
home_dir = user.home
config_dir = os.path.join(user.home, '.' + "pyrenamer2")

name = "pyrenamer"
name_long = "pyRenamer"
copyright = 'Copyright © 2006-08 Adolfo González Blázquez'
authors = ["Adolfo González Blázquez <code@infinicode.org>", "Eric Sagnard"]
artists = ["Adolfo González Blázquez <code@infinicode.org>"]
website = "http://www.infinicode.org/code/pyrenamer/"
version = "0.6.1"
description = _("Mass file renamer for GNOME")
icon = pixmaps_dir + "/pyrenamer.png"
gladefile = resources_dir + "/pyrenamer.glade"

if os.path.isfile('/usr/share/common-licenses/GPL-2'):
	license = open('/usr/share/common-licenses/GPL-2').read()
else:
	license = "This program is free software; you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation; either version 2 of the License, or \
(at your option) any later version. \n\n\
This program is distributed in the hope that it will be useful, but \
WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \
See the GNU General Public License for more details. \n\n\
You should have received a copy of the GNU General Public License \
along with this program; if not, write to the Free Software Foundation, Inc., \
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA."
