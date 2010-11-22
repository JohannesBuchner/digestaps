#! /usr/bin/python

# This file is Copyright 2005 Mario Zoppetti, and was added by
# Darryl A. Dixon <esrever_otua@pythonhacker.is-a-geek.net> to 
# 'NTLM Authorization Proxy Server',
# Copyright 2001 Dmitry A. Rozmanov <dima@xenon.spb.ru>
#
# NTLM APS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# NTLM APS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the sofware; see the file COPYING. If not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# setup.py
from distutils.core import setup
import sys, re, string, os

try:
    import py2exe 
    sys.argv.append("py2exe")
    use_py2exe=True
except:
    use_py2exe=False


if use_py2exe:
    serverCfgDir=''
else:
    serverCfgDir='/etc/ntlmaps'

setup(name='ntlmaps',
      version='1.0',
      description='NTLM Authorization Proxy Server',
      url='http://ntlmaps.sourceforge.net/',
      packages=['ntlmaps'],
      scripts=['scripts/ntlmaps', 'scripts/ntlmaps-hashes'],
      data_files=[(serverCfgDir, ['server.cfg']),
                  ('/etc/rc.d/init.d', ['init/ntlmaps'])],
      options = {"py2exe": {"packages": ["encodings", "win32console"],
                            "optimize": 2}},
      )
