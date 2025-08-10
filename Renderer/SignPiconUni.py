# PiconUni
# Copyright (c) 2boom 2012-15
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# 26.09.2012 added search mountpoints
# 25.06.2013 added resize picon
# 26.11.2013 code optimization
# 02.12.2013 added compatibility with CaidInfo2 (SatName)
# 18.12.2013 added picon miltipath
# 27.12.2013 added picon reference
# 27.01.2014 added noscale parameter (noscale="0" is default, scale picon is on)
# 28.01.2014 code otimization
# 02.04.2014 added iptv ref code
# 17.04.2014 added path in plugin dir...
# 02.07.2014 small fix reference
# 09.01.2015 redesign code

from Renderer import Renderer 
from enigma import ePixmap, ePicLoad
from Components.AVSwitch import AVSwitch
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, resolveFilename 
import os

try:
    from Components.Converter.Poll import PollConverter as Poll
    dreamos=True
except:
    from Components.Converter.Poll import Poll
    dreamos=False

        
class SignPiconUni(Renderer, Poll):
	__module__ = __name__
	searchPaths = ('/data/%s/', '/usr/share/enigma2/%s/', '/usr/lib/enigma2/python/Plugins/Extensions/%s/', '/media/sde1/%s/', '/media/cf/%s/', '/media/sdd1/%s/', '/media/hdd/%s/', '/media/usb/%s/', '/media/ba/%s/', '/mnt/ba/%s/', '/media/sda/%s/', '/etc/%s/')

	def __init__(self):
		Renderer.__init__(self)
		if dreamos:
		   Poll.__init__(self,type)
		else:
                   Poll.__init__(self)
		self.path = 'piconUni'
		self.scale = '0'
		self.nameCache = {}
		self.pngname = ''
		self.picon_default = "picon_default.png"

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if (attrib == 'path'):
				self.path = value
			elif (attrib == 'picon_default'):
				self.picon_default = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
	        self.poll_interval = 50
	        self.poll_enabled = True
		if self.instance:
                        print("raedwhat2",str(what),"**",str(self.CHANGED_CLEAR))
			pngname = ''
			if not what[0] is self.CHANGED_CLEAR:
				sname = self.source.text
				sname = sname.upper().replace('.', '').replace('\xc2\xb0', '')
				if sname.startswith('4097'):
					sname = sname.replace('4097', '1', 1)
				if ':' in sname:
					sname = '_'.join(sname.split(':')[:10])
				pngname = self.nameCache.get(sname, '')
				print("raedpngname",str(pngname))
				if pngname is '':
					pngname = self.findPicon(sname)
					if not pngname is '':
						self.nameCache[sname] = pngname
			if pngname is '':
				pngname = self.nameCache.get('default', '')
				if pngname is '':
					pngname = self.findPicon('picon_default')
					if pngname is '':
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
						if os.path.isfile(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/picon_default.png')
					self.nameCache['default'] = pngname

			print("raedpngnameself.pngname",str(pngname),"**",self.pngname)	
			if not self.pngname is pngname:
                                print("raedpngnameself.pngname2",str(pngname),"**",self.pngname)
				self.picload = ePicLoad()
				try:
				        self.picload.PictureData.get().append(self.piconShow)
				except:
				        self.picload_conn = self.picload.PictureData.connect(self.piconShow)
				scale = AVSwitch().getFramebufferScale()
				self.picload.setPara((self.instance.size().width(), self.instance.size().height(), scale[0], scale[1], False, 1, "#00000000"))
				self.picload.startDecode(pngname)
				self.pngname = pngname

	def piconShow(self, picInfo = None):
		ptr = self.picload.getData()
		if not ptr is None:
			self.instance.setPixmap(ptr.__deref__())
		return

	def findPicon(self, serviceName):
		#global searchPaths
		for path in self.searchPaths:
                        pngname = (((path % self.path) + serviceName) + '.png')
                        if fileExists(pngname):
                                return pngname
                return ''


