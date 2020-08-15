# YanRouteInfo by 2boom 2012 v.0.7
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="50,20" valign="center" halign="center" font="Regular;14" foregroundColor="foreground" transparent="1"  backgroundColor="background">
#	<convert type="YanRouteInfo">Info</convert>
# </widget>
#<widget source="session.CurrentService" render="Pixmap" pixmap="750HD/icons/ico_lan_on.png" position="1103,35" zPosition="1" size="28,15" transparent="1" alphatest="blend">
#    <convert type="YanRouteInfo">Lan  | Wifi | Modem</convert>
#    <convert type="ConditionalShowHide" />
#  </widget>



from Components.Converter.Converter import Converter
from Components.Element import cached



class AMB_RouteInfo(Converter, object):
	Info = 0
	Lan = 1
	Wifi = 2
	Modem = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "Info":
			self.type = self.Info
		elif type == "Lan":
			self.type = self.Lan
		elif type == "Wifi":
			self.type = self.Wifi
		elif type == "Modem":
			self.type = self.Modem

	@cached
	def getBoolean(self):
		info = False
		for line in open("/proc/net/route"):
			if self.type == self.Lan and line.split()[0] == "eth0" and line.split()[3] == "0003":
				info = True
			elif self.type == self.Wifi and (line.split()[0] == "wlan0" or line.split()[0] == "ra0") and line.split()[3] == "0003":
				info = True
			elif self.type == self.Modem and line.split()[0] == "ppp0" and line.split()[3] == "0003":
				info = True
		return info
		
	boolean = property(getBoolean)
	
	@cached
	def getText(self):
		info = ""
		for line in open("/proc/net/route"):
			if self.type == self.Info and line.split()[0] == "eth0" and line.split()[3] == "0003":
				info = "lan"
			elif self.type == self.Info and  (line.split()[0] == "wlan0" or line.split()[0] == "ra0") and line.split()[3] == "0003":
				info = "wifi"
			elif self.type == self.Info and line.split()[0] == "ppp0" and line.split()[3] == "0003":
				info = "3g"
		return info

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
