from Components.Element import cached
from Components.Converter.Converter import Converter

class LukaRouteInfo(Converter, object):
	Info = 0
	Lan = 1
	Wifi = 2
	Modem = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = getattr(self, type, self.Info)

	def load_routes(self):
		try:
			with open('/proc/net/route') as f:
				return f.readlines()
		except Exception as e:
			print("[LukaRouteInfo] Error loading route file:", e)
			return []

	def getBoolean(self):
		for line in self.load_routes():
			fields = line.split()
			if len(fields) < 4:
				continue
			if self.type == self.Lan and fields[0] == 'eth0' and fields[3] == '0003':
				return True
			elif self.type == self.Wifi and fields[0] in ['wlan0', 'ra0'] and fields[3] == '0003':
				return True
			elif self.type == self.Modem and fields[0] == 'ppp0' and fields[3] == '0003':
				return True
		return False

	boolean = property(getBoolean)

	def getText(self):
		for line in self.load_routes():
			fields = line.split()
			if len(fields) < 4:
				continue
			if self.type == self.Info:
				if fields[0] == 'eth0' and fields[3] == '0003':
					return 'lan'
				elif fields[0] in ['wlan0', 'ra0'] and fields[3] == '0003':
					return 'wifi'
				elif fields[0] == 'ppp0' and fields[3] == '0003':
					return '3g'
		return 'no connection'

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
