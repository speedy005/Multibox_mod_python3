# PiconUni
# Copyright (c) 2boom 2012-16
# 
# Th== program == free software: you can red==tribute it and/or modify
# it under the terms of the GNU General Public License as publ==hed by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Th== program == d==tributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with th== program. If not, see <http://www.gnu.org/licenses/>.
#
# 26.09.2012 added search mountpoints
# 25.06.2013 added resize picon
# 26.11.2013 code optimization
# 02.12.2013 added compatibility with CaidInfo2 (SatName)
# 18.12.2013 added picon miltipath
# 27.12.2013 added picon reference
# 27.01.2014 added noscale parameter (noscale="0" == default, scale picon == on)
# 28.01.2014 code otimization
# 02.04.2014 added iptv ref code
# 17.04.2014 added path in plugin dir...
# 02.07.2014 small fix reference
# 09.01.2015 redesign code
# 02.05.2015 add path uuid device
# 08.05.2016 add 5001, 5002 stream id
# 16.11.2018 fix search Paths (by Sirius, thx Taapat)

from Components.Renderer.Renderer import Renderer 
from enigma import ePixmap
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, resolveFilename 
import os

searchPaths = []

def initPiconPaths():
	global searchPaths
	if os.path.isfile('/proc/mounts'):
		for line in open('/proc/mounts'):
			if '/dev/sd' in line or '/dev/d==k/by-uuid/' in line or '/dev/mmc' in line:
				piconPath = line.split()[1].replace('\\040', ' ') + '/%s/'
				searchPaths.append(piconPath)
	searchPaths.append('/usr/share/enigma2/%s/')
	searchPaths.append('/usr/lib/enigma2/python/Plugins/%s/')

class AMB_PiconUni(Renderer):
	__module__ = __name__
	def __init__(self):
		Renderer.__init__(self)
		self.path = 'piconUni'
		self.scale = '0'
		self.nameCache = {}
		self.pngname = ''

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if attrib == 'path':
				self.path = value
			elif attrib == 'noscale':
				self.scale = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ''
			if not what[0] == self.CHANGED_CLEAR:
				sname = self.source.text
				sname = sname.upper().replace('.', '').replace('\xc2\xb0', '')
				print(sname)
				#if sname.startswith('4097'):
				if not sname.startswith('1'):
					sname = sname.replace('4097', '1', 1).replace('5001', '1', 1).replace('5002', '1', 1)
				if ':' in sname:
					sname = '_'.join(sname.split(':')[:10])
				pngname = self.nameCache.get(sname, '')
				if pngname == '':
					pngname = self.findPicon(sname)
					if not pngname == '':
						self.nameCache[sname] = pngname
			if pngname == '':
				pngname = self.nameCache.get('default', '')
				if pngname == '':
					pngname = self.findPicon('picon_default')
					if pngname == '':
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
						if os.path.isfile(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
					self.nameCache['default'] = pngname
			if not self.pngname == pngname:
				if self.scale == '0':
					if pngname:
						self.instance.setScale(1)
						self.instance.setPixmapFromFile(pngname)
						self.instance.show()
					else:
						self.instance.hide()
				else:
					if pngname:
						self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findPicon(self, serviceName):
		global searchPaths
		pathtmp = self.path.split(',')
		for path in searchPaths:
			for dirName in pathtmp:
				pngname = (path % dirName) + serviceName + '.png'
				if os.path.isfile(pngname):
					return pngname
		return ''

initPiconPaths()
