# -*- coding: utf-8 -*-
# by digiteng...10.2020, 02.2022, 08.2022, 01.2025

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference, eEPGCache, eServiceCenter
from ServiceReference import resolveAlternate, ServiceReference

class xtraServiceName(Converter):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		try:
			if self.type == "ServiceName":
				service = self.source.service
				info = None
				name = None
				if isinstance(service, eServiceReference):
					info = self.source.info
				elif isinstance(service, iPlayableServicePtr):
					info = service and service.info()
					service = None

				if not info:
					return ""
				name = service and info.getName(service)
				if name is None:
					name = info.getName()
				name = name.replace('\xc2\x86', '').replace('\xc2\x87', '').replace('_', ' ')
				return name
		except Exception as err:
			from Tools.xtraTool import errorlog
			errorlog(err, __file__)
	text = property(getText)

	def changed(self, what):
		if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
			Converter.changed(self, what)

