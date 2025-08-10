from Components.Converter.Converter import Converter
from Components.Element import cached
from boxbranding import getMachineMake
import socket
import os

class NOVmodel(Converter):
	DECO = 1
	IPDECO = 2
	UP = 3


	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type
		if type == 'deco':
			self.type = self.DECO
		elif type == 'ipdeco':
			self.type = self.IPDECO
		elif type == 'tiempo':
			self.type = self.UP

	@cached
	def getText(self):
		textvalue = ''
		if self.type == self.DECO:
			textvalue = self.mostrardeco()
		elif self.type == self.IPDECO:
			textvalue = self.mostrarip()
		elif self.type == self.UP:
			textvalue = self.mostrarup()
		return textvalue

	text = property(getText)

	def mostrardeco(self):
        		modelodeco = ''
        		modelodeco = getMachineMake()
        		return modelodeco

	def mostrarip(self):
        		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        		s.connect(("8.8.8.8", 80))
        		return s.getsockname()[0]

	def mostrarup(self):
			try:
				with open('/proc/uptime', 'r') as file:
					uptime_info = file.read().split()
			except:
				return ' '
				uptime_info = None
			if uptime_info is not None:
				total_seconds = float(uptime_info[0])
				MINUTE = 60
				HOUR = MINUTE * 60
				DAY = HOUR * 24
				days = int( total_seconds / DAY )
				hours = int( ( total_seconds % DAY ) / HOUR )
				minutes = int( ( total_seconds % HOUR ) / MINUTE )
				seconds = int( total_seconds % MINUTE )
				uptime = ''
				if days > 0:
					uptime += str(days) + ' ' + (days == 1 and _('d') or _('d') ) + ' '
				if len(uptime) > 0 or hours > 0:
					uptime += str(hours) + ' ' + (hours == 1 and _('h') or _('h') ) + ' '
				if len(uptime) > 0 or minutes > 0:
					uptime += str(minutes) + ' ' + (minutes == 1 and _('m') or _('m') )
				return uptime