#Mod by Maggy Ultra Transparent FHD
from Renderer import Renderer
from enigma import ePixmap, eServiceCenter, eServiceReference
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.Alternatives import GetWithAlternative
from Components.config import config

class test_Picon(Renderer):
	searchPaths = ('/usr/share/enigma2/%s/', '/media/usb/%s/')

	def __init__(self):
		Renderer.__init__(self)
		self.path = "picon"
		self.size = None
		self.nameCache = { }
		self.pngname = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
			if attrib == "size":
				value = value.split(',')
				if len(value) == 2:
					self.size = value[0] + "x" + value[1]
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				s_name = sname
				if sname.startswith("1:134"):
					sname = GetWithAlternative(self.source.text)
				for protocol in ("http", "rtmp", "rtsp", "mms", "rtp"):
					pos = sname.rfind(':' + protocol )
					if pos != -1:
						sname = sname.split(protocol)[0]
						break
				
				pos = sname.rfind(':')
				if pos != -1:
					sname = sname[:pos].rstrip(':').replace(':','_')
				pngname = self.nameCache.get(sname, "")
				if pngname == "":
					pngname = self.findPicon(sname)
					if pngname == "":
						serviceHandler = eServiceCenter.getInstance()
						service = eServiceReference(s_name)
						if service and service is not None:
							info = serviceHandler.info(service)
							if info and info is not None:
								service_name = info.getName(service).replace('\xc2\x86','').replace('\xc2\x87', '').replace('/', '_')
								pngname = self.findPicon(service_name)
					if pngname == "" and sname.startswith("5002_"):
						pngname = self.findPicon(sname.replace("5002_", "1_", 1))
					if pngname != "":
						self.nameCache[sname] = pngname
			if pngname == "": 
				self.instance.hide()
			else:
				self.instance.show()
			if pngname != "" and self.pngname != pngname:
				if config.usage.picon_scale.value:
					self.instance.setScale(2)
				else:
					self.instance.setScale(0)
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findPicon(self, serviceName):
		if self.path == "picon":
			path_normal = config.usage.picon_dir.value + "/"
			path_size = config.usage.picon_dir.value + "_" + self.size + "/"
			for path in (path_size, path_normal):
				pngname = path + serviceName + ".png"
				if fileExists(pngname):
					return pngname
		for path in self.searchPaths:
			if self.size:
				mypath = self.path + "_" + self.size
				pngname = (path % mypath) + serviceName + ".png"
				if fileExists(pngname):
					return pngname
			pngname = (path % self.path) + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		return ""
