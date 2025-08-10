# -*- coding: utf-8 -*-
# by digiteng...
# <widget render="xtraEvents" source="ServiceEvent" eventNumber="4" position="1265,605" size="600,210" font="Regular; 28" noWrap="1" zPosition="2" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache
from time import localtime

class Skyline_xtraEvents(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.epgcache = eEPGCache.getInstance()
		self.evntNmbr = 1
		
	def applySkin(self, desktop, parent):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'eventNumber':
				self.evntNmbr = int(value)
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = eLabel
	def changed(self, what):
		try:
			event = self.source.event
			if event is None:
				self.text = "N/A"
				return
			if what[0] == self.CHANGED_CLEAR:
				self.text = ""
			else:
				txt = ""
				evnts=""
				service = self.source.service
				events = self.epgcache.lookupEvent(['BDTM', (service.toString(), 0, -1, -1)])
				if self.evntNmbr > len(events):
					n = len(events)
				else:
					n = self.evntNmbr + 1
				if events:
					for i in range(1, n, 1):
						if i == n:
							break
							break
						try:
							evnts = events[i][2]
							bt = localtime(events[i][0])
							txt += "\c0000FF00%02d:%02d \c00FF0000%s\n" % (bt.tm_hour, bt.tm_min, evnts)
						except:
							pass

				self.text = txt
		except Exception as err:
			from Tools.NachtWeatherUpdate import errorlog
			errorlog(err, __file__)
