# -*- coding: utf-8 -*-
# by digiteng
# 11.2021
# for channellist
# <widget source="ServiceEvent" render="xtraStar" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
# or
# <widget source="ServiceEvent" render="xtraStar" pixmap="xtra/star.png" position="750,390" size="200,20" alphatest="blend" transparent="1" zPosition="3" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
# from Components.VariableValue import VariableValue
from enigma import ePoint, eWidget, eSize, eSlider, loadPNG
from Components.config import config
# import re
import json
import os
from Tools.xtraTool import REGEX, pathLoc
pathLoc = config.plugins.xtrvnt.loc.value
star = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star.png"
starBackgrund = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star_back.png"

class xtraStar2(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		# VariableValue.__init__(self)
		# self.instance = None
		# self.pxmp = None

	# def applySkin(self, desktop, screen):
		# attribs = self.skinAttributes[:]
		# for attrib, value in self.skinAttributes:
			# if attrib == 'size':
				# self.szX = int(value.split(',')[0])
				# self.szY = int(value.split(',')[1])
			# elif attrib == 'pixmap':
				# self.pxmp = value

		# self.skinAttributes = attribs
		# return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = eSlider
	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				rating = None
				rtng = 0
				event = self.source.event
				if event:
					evnt = event.getEventName()
					try:
						evntNm = REGEX.sub('', evnt).strip()
						rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
						if os.path.exists(rating_json):
							with open(rating_json) as f:
								rating = json.load(f)['imdbRating']
							if rating:
								rtng = int(10*(float(rating)))
								self.instance.setValue(rtng)
								# if self.pxmp is None or self.pxmp == "":
								self.instance.setPixmap(loadPNG(star))
								self.instance.setBackgroundPixmap(loadPNG(starBackgrund))
								# else:
									# self.instance.setPixmap(loadPNG(self.pxmp))
								# self.instance.move(ePoint(0, 0))
								# self.instance.resize(eSize(self.szX, self.szY))
								# self.instance.setAlphatest(2)
								self.instance.setRange(0, 100)
								self.instance.show()
							else:
								self.instance.hide()
						else:
							self.instance.hide()
					except:
						self.instance.hide()
						return
				else:
					self.instance.hide()
			else:
				self.instance.hide()

	# def GUIcreate(self, parent):
		# self.instance = eWidget(parent)
		# self.instance = eSlider(self.instance)

