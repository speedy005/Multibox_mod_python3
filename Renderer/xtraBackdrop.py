# -*- coding: utf-8 -*-
# by digiteng...04.2020, 11.2020, 11.2021, 05.2025(animation added)
# <widget source="ServiceEvent" render="xtraBackdrop" position="785,75" size="300,170" zPosition="2" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer, loadPNG, ePoint, eSize, loadJPG, eServiceCenter
from Components.config import config
import re
import os
from Tools.xtraTool import REGEX, pathLoc

piconPath = ""
paths = ('/media/hdd/picon/', '/media/usb/picon/', '/media/mmc/picon/', 
'/usr/share/enigma2/picon/', '/picon/', '/media/sda1/picon/', 
'/media/sda2/picon/', '/media/sda3/picon/')
for path in paths:
	if os.path.isdir(path):
		piconPath = path
		break
try:
	pathLoc = config.plugins.xtrvnt.loc.value
except:
	pass
try:
	from _thread import start_new_thread
except:
	try:
		from thread import start_new_thread
	except:
		pass
NoImage = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
backdropImage="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
class xtraBackdrop(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		
		self.animationMode = None
		self.val = 0
		self.valstop = 0
		self.cornerRadius = 10
		self.animationSpeed = 1
		self.timer = eTimer()
		self.timer.callback.append(self.showAnimation)

	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.px = int(value.split(',')[0])
				self.py = int(value.split(',')[1])
			elif attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'animationMode':
				self.animationMode = value
			elif attrib == 'animationSpeed':
				self.animationSpeed = int(value)
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				if self.animationMode is not None:
					start_new_thread(self.showAnimation, ())
				else:
					self.showBackdrop()
			else:
				self.instance.hide()
				return

	def showBackdrop(self):
		evnt = ''
		bckNm = ''
		evntNm = ''
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				bckNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
				bckNmm = "{}xtraEvent/backdropThumbnail/{}.jpg".format(pathLoc, evntNm)
				if os.path.exists(bckNm):
					backdropImage = bckNm
				elif os.path.exists(bckNmm):
					backdropImage = bckNmm
				else:
					self.showPicon()
				self.instance.setPixmap(loadJPG(backdropImage))
				self.instance.setScale(1)
				self.instance.setCornerRadius(self.cornerRadius, 15)
				self.instance.show()
			else:
				self.showPicon()
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)

	def showPicon(self):
		ref = ""
		info = None
		ChNm=""
		try:
			import NavigationInstance
			ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
			ChNm = eServiceCenter.getInstance().info(ref).getName(ref)
			ChNm = ChNm.replace('\xc2\x86', '').replace('\xc2\x87', '')
			ChNm = ChNm.lower().replace('&', 'and').replace('+', 'plus').replace('*', 'star').replace(' ', '').replace('.', '')

			picName = "{}{}.png".format(piconPath, ChNm)
			picName = picName.strip()
			if os.path.exists(picName):
				self.instance.setScale(2)
				self.instance.setPixmapFromFile(picName)
				self.instance.setAlphatest(2)
				self.instance.show()
			elif not os.path.exists(picName):
				picName = "{}{}.png".format(piconPath, str(ref).replace(':', '_'))
				picName = picName.replace('_.png', '.png')
				if os.path.exists(picName):
					self.instance.setScale(2)
					self.instance.setPixmapFromFile(picName)
					self.instance.setAlphatest(2)
					self.instance.show()
				else:
					picName = "/usr/share/enigma2/skin_default/picon_default.png"
					self.instance.setScale(2)
					self.instance.setPixmapFromFile(picName)
					self.instance.setAlphatest(2)
					self.instance.show()
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)

	def showAnimation(self):
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				self.instance.hide()
				self.val += self.animationSpeed
				if "Slide" in self.animationMode:
					self.instance.setScale(0)
				else:
					self.instance.setScale(1)
				bckNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
				bckNmm = "{}xtraEvent/backdropThumbnail/{}.jpg".format(pathLoc, evntNm)
				if os.path.exists(bckNm):
					backdropImage = bckNm
				elif os.path.exists(bckNmm):
					backdropImage = bckNmm
				else:
					self.showPicon()
				self.instance.setPixmap(loadJPG(backdropImage))
				self.instance.move(ePoint(self.px, self.py))
				if "LeftRight" in self.animationMode:
					self.valstop = self.szX
					self.instance.resize(eSize(self.val, self.szY))
				elif "TopBottom" in self.animationMode: 
					self.valstop = self.szY
					self.instance.resize(eSize(self.szX, self.val))
				elif "Grow" in self.animationMode:
					self.valstop = self.szY
					self.instance.resize(eSize(int(self.val*1.8), self.val))
				elif "Popup" in self.animationMode:
					self.valstop = self.szY
					self.instance.resize(eSize(int(self.val*1.8), int(self.val)))
					self.instance.move(ePoint(int(self.px + (self.szX//2-self.szX//4.5))-int(self.val//2), int(self.py + (self.szY//2))-int(self.val//2)))
				else:
					return
				self.instance.show()
				if self.val >= self.valstop:
					self.timer.stop()
					self.val = 0
					self.valstop = 0
					self.instance.setScale(1)
					self.instance.show()
					return
				
				self.timer.start(1, True)

			else:
				self.instance.hide()
				return
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)
