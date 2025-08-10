# by digiteng...11.2020, 04.2022, 08.2024
# <widget render="xtraTMDBratingCircleProgress" source="session.FrontendStatus" position="1260,760" size="60,60" backgroundColor="#15202b" mode="TMDBrating" scale="2" pixmapCircle="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/circleProgress/prgrs150blue1.png" pixmapCircleBack="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/circleProgress/prgrs150back.png" zPosition="3" transparent="1" />

from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, ePoint, eWidget, eLabel, eSize, loadPNG, gFont
from skin import parseColor
import os
import re
import json
from Components.Converter.Poll import Poll
from Components.config import config
import NavigationInstance
from Tools.xtraTool import REGEX, pathLoc
pathLoc = config.plugins.xtrvnt.loc.value

class xtraTMDBratingCircleProgress(Poll, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		Poll.__init__(self)
		self.scale = 0
		self.poll_interval = 1000
		self.poll_enabled = True
		
	GUI_WIDGET = eWidget

	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for (attrib, value) in self.skinAttributes:
			if attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'backgroundColor':
				self.backgroundColor = value
			elif attrib == 'mode':
				self.mode = value
			elif attrib == 'scale':
				self.scale = int(value)
			elif attrib == 'pixmapCircle':
				self.pixmapCirclex = value
			elif attrib == 'pixmapCircleBack':
				self.pixmapCircleBack = value
		self.skinAttributes = attribs
		
		
		self.prgrsPxmp.setScale(self.scale)
		self.prgrsPxmp.setBackgroundColor(parseColor(self.backgroundColor))
		self.prgrsPxmp.resize(eSize(self.szX, self.szY))
		self.prgrsPxmp.setZPosition(2)
		self.prgrsPxmp.setTransparent(1)
		self.prgrsPxmp.setAlphatest(2)

		
		self.prgrsPxmpBack.setScale(self.scale)
		self.prgrsPxmpBack.setBackgroundColor(parseColor(self.backgroundColor))
		self.prgrsPxmpBack.resize(eSize(self.szX, self.szY))
		self.prgrsPxmpBack.setTransparent(1)
		self.prgrsPxmpBack.setAlphatest(2)
		self.prgrsPxmpBack.setZPosition(5)
		
		self.prgrsBack.setBackgroundColor(parseColor(self.backgroundColor))
		self.prgrsBack.resize(eSize(self.szX, self.szY))
		self.prgrsBack.move(ePoint(0, 0))
		self.prgrsBack.setTransparent(0)
		self.prgrsBack.setZPosition(0)
		
		self.prgrsText.setBackgroundColor(parseColor(self.backgroundColor))
		self.prgrsVal.setBackgroundColor(parseColor(self.backgroundColor))
		self.prgrsValR.setBackgroundColor(parseColor(self.backgroundColor))
		ret = Renderer.applySkin(self, desktop, screen)
		return ret

	def changed(self, what):
		# if what[0] == self.CHANGED_CLEAR:
			# return
		# if self.instance:
		try:
			self.prgrsPxmp.setPixmap(loadPNG("{}".format(self.pixmapCirclex)))
			self.prgrsPxmpBack.setPixmap(loadPNG("{}".format(self.pixmapCircleBack)))
			val = None
			eventName="n/a"
			if config.plugins.xtrvnt.xtraInfoSource.value == "TMDB":
				ref=""
				event = None
				title = ""
				read_json = {}
				try:
					# ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
					event = self.source.event

				except: return
				# if ref is not "":
					# event = epgcache.lookupEvent(['IBDCTSERN', (ref.toString(), 1, -1, 1)])
				if event is not None:
					event_name = event.getEventName()
					title = REGEX.sub('', event_name).strip()
					rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, title)
					if os.path.exists(rating_json):
						with open(rating_json) as f:
							read_json = json.load(f)
						val = read_json["tmdbRating"] * 10

			if val is not None :
				val = int(val)
				x, y = 0, 0
				if val >= 0 and val <= 50:
					x = 0
					y = (float(50) / float(self.szY) ) * 100
					y = ((float(val) / float(self.szY)) * float(self.szY)) / y * 100
					y = int(-y)
					
					p = (self.szY / 2 - self.szY / 4) + (self.szY / 20)
					s = (self.szY / 4) + (self.szY / 10)
					f = (self.szY / 3)

					self.prgrsText.setText(str(val))
					self.prgrsText.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsText.resize(eSize(self.szX, int(s)))
					self.prgrsText.move(ePoint(0, int(p)))
					self.prgrsText.setFont(gFont("Regular", int(f)))
					self.prgrsText.setHAlign(eLabel.alignCenter)
					self.prgrsText.setTransparent(1)
					self.prgrsText.setZPosition(99)
					self.prgrsText.show()
					
					self.prgrsVal.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsVal.resize(eSize(int(self.szX / 2), self.szY))
					self.prgrsVal.move(ePoint(x, y))
					self.prgrsVal.setTransparent(0)
					self.prgrsVal.setZPosition(3)
					self.prgrsVal.show()
					
					self.prgrsValR.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsValR.resize(eSize(int(self.szX / 2), self.szY))
					self.prgrsValR.move(ePoint(int(self.szX / 2), 0))
					self.prgrsValR.setTransparent(0)
					self.prgrsValR.setZPosition(3)
					self.prgrsValR.show()
					self.prgrsPxmp.show()
					self.prgrsPxmpBack.show()
				elif val >= 51 and val <= 100:
					x = self.szX // 2
					y = (float(50) / float(self.szY) ) * 100
					y = (float(val) / float(self.szY) * float(self.szY)) / y * 100
					y = y - self.szY + self.szY / 10
					y = int(y)

					p = (self.szY / 2-self.szY / 4)+(self.szY / 20)
					s = (self.szY / 4)+(self.szY / 10)
					f = (self.szY / 3)

					self.prgrsText.setText(str(val))
					self.prgrsText.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsText.resize(eSize(self.szX, int(s)))
					self.prgrsText.move(ePoint(0, int(p)))
					self.prgrsText.setFont(gFont("Regular", int(f)))
					self.prgrsText.setHAlign(eLabel.alignCenter)
					self.prgrsText.setTransparent(1)
					self.prgrsText.setZPosition(99)
					self.prgrsText.show()
					
					self.prgrsValR.clearBackgroundColor()
					self.prgrsValR.hide()
					self.prgrsVal.clearBackgroundColor()
					self.prgrsVal.setBackgroundColor(parseColor(self.backgroundColor))
					self.prgrsVal.resize(eSize(x, self.szY))
					self.prgrsVal.move(ePoint(x, y))
					self.prgrsVal.setTransparent(0)
					self.prgrsVal.setZPosition(3)
					self.prgrsVal.show()
					self.prgrsPxmp.show()
					self.prgrsPxmpBack.show()
				else:
					return
			else:
				self.prgrsText.hide()
				self.prgrsVal.hide()
				self.prgrsValR.hide()
				self.prgrsPxmp.hide()
				self.prgrsPxmpBack.hide()
				self.prgrsVal.resize(eSize(self.szX, self.szY))
				self.prgrsVal.move(ePoint(0,0))
				self.prgrsVal.setTransparent(0)
				self.prgrsVal.setZPosition(3)
				self.prgrsVal.show()
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.prgrsVal = eLabel(self.instance)
		self.prgrsValR = eLabel(self.instance)
		self.prgrsText = eLabel(self.instance)
		self.prgrsBack = eLabel(self.instance)
		self.prgrsPxmp = ePixmap(self.instance)
		self.prgrsPxmpBack = ePixmap(self.instance)

	def GUIdelete(self):
		self.prgrsVal = None
		self.prgrsValR = None
		self.prgrsText = None
		self.prgrsBack = None
		self.prgrsPxmp = None
		self.prgrsPxmpBack = None
