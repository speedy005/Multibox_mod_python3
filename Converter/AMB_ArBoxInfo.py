
from Poll import Poll
from Components.Converter.Converter import Converter
from Components.config import config
from Components.Element import cached
import os

class AMB_ArBoxInfo(Poll, Converter, object):
	boxtype = 0

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "boxtype":
			self.type = self.boxtype
		self.poll_interval = 1000
		self.poll_enabled = True

	def imageinfo(self):
		imageinfo = ''
		if os.path.isfile("/usr/lib/opkg/status"):
			imageinfo = "/usr/lib/opkg/status"
		elif os.path.isfile("/usr/lib/ipkg/status"):
			imageinfo = "/usr/lib/ipkg/status"
		elif os.path.isfile("/var/lib/opkg/status"):
			imageinfo = "/var/lib/opkg/status"
		elif os.path.isfile("/var/opkg/status"):
			imageinfo = "/var/opkg/status"
		return imageinfo

	def boxinfo(self):
		box = software = ''
		package = 0
		if os.path.isfile(self.imageinfo()):
			for line in open(self.imageinfo()):
					break
		if os.path.isfile("/proc/version"):
			enigma = open("/proc/version").read().split()[2]
		if os.path.isfile("/proc/stb/info/boxtype"):
			box = open("/proc/stb/info/boxtype").read().strip().upper()
		elif os.path.isfile("/proc/stb/info/vumodel"):
			box = "Vu+ " + open("/proc/stb/info/vumodel").read().strip().capitalize()
		elif os.path.isfile("/proc/stb/info/model"):
			box = open("/proc/stb/info/model").read().strip().upper()
		if os.path.isfile("/etc/issue"):
			for line in open("/etc/issue"):
				software += line.capitalize().replace('\n', '').replace('\l', '').replace('\\', '').strip()[:-1]
			software = ' : %s ' % software.strip()
		if os.path.isfile("/etc/vtiversion.info"):
			software = ''
			for line in open("/etc/vtiversion.info"):
				software += line.split()[0].split('-')[0] + ' ' + line.split()[-1].replace('\n', '')
			software = ' : %s ' % software.strip()
		return '%s%s' % (box, software)		

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ''
		elif self.type is self.boxtype:
			return self.boxinfo()

	text = property(getText)

	def changed(self, what):
		if what[0] is self.CHANGED_POLL:
			self.downstream_elements.changed(what)
		elif not what[0] is self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
