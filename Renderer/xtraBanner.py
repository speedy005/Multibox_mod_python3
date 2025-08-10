# -*- coding: utf-8 -*-
# by digiteng...06.2020, 08.2020, 11.2021, 05.2025(animation added)
# <widget source="session.Event_Now" render="xtraBanner" position="0,0" size="762,141" zPosition="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG, eTimer, ePoint, eSize
from Components.config import config
import os
import re
from Tools.xtraTool import REGEX, pathLoc
pathLoc = config.plugins.xtrvnt.loc.value
try:
	from _thread import start_new_thread
except:
	try:
		from thread import start_new_thread
	except:
		pass

class xtraBanner(Renderer):

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
					self.showBanner()
			else:
				self.instance.hide()
				
	
	def showBanner(self):
		evnt = ''
		pstrNm = ''
		evntNm = ''
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				pstrNm = "{}xtraEvent/banner/{}.jpg".format(pathLoc, evntNm)
				if os.path.exists(pstrNm):
					self.instance.setPixmap(loadJPG(pstrNm))
					self.instance.setScale(1)
					self.instance.show()
				else:
					self.instance.hide()
					return
			else:
				self.instance.hide()
				return
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)

	def showAnimation(self):
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				pstrNm = "{}xtraEvent/banner/{}.jpg".format(pathLoc, evntNm)
				self.instance.hide()
				self.val += self.animationSpeed
				if "Slide" in self.animationMode:
					self.instance.setScale(0)
				else:
					self.instance.setScale(1)
				if os.path.exists(pstrNm):
					self.instance.setPixmap(loadJPG(pstrNm))
					self.instance.move(ePoint(self.px, self.py))
					if "LeftRight" in self.animationMode:
						self.valstop = self.szX
						self.instance.resize(eSize(self.val, self.szY))
					elif "TopBottom" in self.animationMode: 
						self.valstop = self.szY
						self.instance.resize(eSize(self.szX, self.val))
					elif "Grow" in self.animationMode:
						self.valstop = self.szX
						self.instance.resize(eSize(int(self.val*5.4), self.val))
					elif "Popup" in self.animationMode:
						self.valstop = self.szY
						self["banner"].instance.resize(eSize(int(self.val*5.4), int(self.val)))
						self["banner"].move(ePoint(int(self.px + (self.szX//2-self.szX//2.45))-int(self.val//2), int(self.py + (self.szY//2))-int(self.val//2)))
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
			else:
				self.instance.hide()
				return
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)
