# -*- coding: utf-8 -*-
# by digiteng...
# v1 04.2020
# <widget render="parentalEvent" source="session.Event_Now" position="0,0" size="60,60" alphatest="blend" zPosition="2" transparent="1" />
from Renderer import Renderer
from enigma import ePixmap, eTimer, loadPNG
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
import re
import os

pratePath = resolveFilename(SCOPE_CURRENT_SKIN, 'parental')

class AMB_parentalEvent(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.rateNm = ''

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				self.delay()
		except:
			pass

	def showPoster(self):
		event = self.source.event
		if event:
			fd = event.getShortDescription() + "\n" + event.getExtendedDescription()
			try:
				ppr = ["[aA]b ((\d+))", "[+]((\d+))", "Od lat: ((\d+))"]
				for i in ppr:
					prr = re.search(i, fd)
					if prr:
						parentName = prr.group(1)
						parentName = parentName.replace("7", "6")
						break
				else:
					if os.path.exists("/tmp/rating"):
						with open("/tmp/rating") as f:
							prate = f.readlines()[1]
						if prate == "TV-Y7":
							rate = "6"
						elif prate == "TV-14":
							rate = "12"
						elif prate == "TV-PG":
							rate = "16"
						elif prate == "TV-G":
							rate = "0"
						elif prate == "TV-MA":
							rate = "18"
						elif prate == "PG-13":
							rate = "16"
						elif prate == "R":
							rate = "18"
						elif prate == "G":
							rate = "0"
						else:
							pass
						if rate:	
							parentName = str(rate)

				if parentName:
					rateNm = pratePath + "FSK_{}.png".format(parentName)
					self.instance.setPixmap(loadPNG(rateNm))
					self.instance.show()
				else:
					self.instance.hide()
			except:
				self.instance.hide()
				return
		else:
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showPoster)
		self.timer.start(100, True)
