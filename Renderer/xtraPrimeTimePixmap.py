# -*- coding: utf-8 -*-
# by digiteng, 03.10.2024, 01.2025
# for ch
  # <widget render="xtraPrimeTimeLabel" source="ServiceEvent" mode="now" position="1550,232" size="300,70" font="Regular;14" backgroundColor="#50000000" noWrap="1" zPosition="9" transparent="1" halign="center" valign="center" />
  # <widget render="xtraPrimeTimePixmap" source="ServiceEvent" img="backdrop" mode="now" position="1550,53" size="300,170" zPosition="2" transparent="1" cornerRadius="20" />
  # <widget render="xtraPrimeTimeLabel" source="ServiceEvent" mode="next" position="1550,517" size="300,70" font="Regular;14" backgroundColor="#50000000" noWrap="1" zPosition="9" transparent="1" halign="center" valign="center" />
  # <widget render="xtraPrimeTimePixmap" source="ServiceEvent" img="backdrop" mode="next" position="1550,339" size="300,170" zPosition="2" transparent="1" cornerRadius="20" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import eEPGCache, eServiceReference, ePixmap
from time import localtime, mktime, time
from datetime import datetime, timedelta
from Components.config import config
import os
from Tools.xtraTool import REGEX, pathLoc
imgNo="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
pathLoc = config.plugins.xtrvnt.loc.value

class xtraPrimeTimePixmap(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.epgCache = eEPGCache.getInstance()

	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.px = int(value.split(',')[0])
				self.py = int(value.split(',')[1])
			elif attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'backgroundColor':
				self.backgroundColor = value
			elif attrib == 'mode':
				self.mode = value
			elif attrib == 'img':
				self.imgs = value
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		if not self.instance:
			return
		if what[0] != self.CHANGED_CLEAR:
			try:
				# event = self.source.event
				# if event is None:
					# self.instance.setPixmapFromFile(imgNo)
					# self.instance.setScale(1)
					# self.instance.show()
					# return
				try:
					ref = self.source.service
				except:
					import NavigationInstance
					ref = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
				case=""

				try:
					prime_hour = config.epgselection.graph_primetimehour.value
					prime_minute = config.epgselection.graph_primetimemins.value
				except:
					prime_hour = 20
					prime_minute = 15
				now = localtime(time())
				dt = datetime(now.tm_year, now.tm_mon, now.tm_mday, prime_hour, prime_minute)
				pt = int(mktime(dt.timetuple()))
				if self.mode == "next":
					pt = dt + timedelta(1)
					pt = int(mktime(pt.timetuple()))
				self.epgCache.startTimeQuery(eServiceReference(ref.toString()), pt)
				event = self.epgCache.getNextTimeEntry()
				bt = event.getBeginTime()
				duration = round(event.getDuration())
				et = event.getBeginTime() + duration
				eNm = event.getEventName()
				evntNm = REGEX.sub('', eNm).strip()
				bcdrpNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
				pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
				if self.mode == "now":
					nowx = int(time())
					if event and not (now.tm_hour <= prime_hour):
						self.instance.setPixmapFromFile(imgNo)
						self.instance.show()
						return

				if self.imgs == "backdrop":
					if os.path.exists(bcdrpNm):
						self.instance.setPixmapFromFile(bcdrpNm)
					else:
						self.instance.setPixmapFromFile(imgNo)
				elif self.imgs == "poster":
					if os.path.exists(pstrNm):
						self.instance.setPixmapFromFile(pstrNm)
					else:
						self.instance.setPixmapFromFile(imgNo)
				else:
					self.instance.setPixmapFromFile(imgNo)

				self.instance.setScale(1)
				self.instance.show()
			except Exception as err:
				from Tools.xtraTool import errorlog
				errorlog(err, __file__)
