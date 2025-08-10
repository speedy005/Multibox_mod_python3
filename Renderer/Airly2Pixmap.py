# -*- coding: utf-8 -*-
#							  Airly
#					Based on http://map.airly.org
#							 2.0-r6
#
#    Copyright (C) 2023  Ampersand
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Components.AVSwitch import AVSwitch
from enigma import eEnv, ePicLoad, eRect, eSize, gPixmapPtr


class Airly2Pixmap(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.picload = ePicLoad()
		self.picload.PictureData.get().append(self.generatePixmap)
		self.iconFileName = ""

	GUI_WIDGET = ePixmap

	def postWidgetCreate(self, instance):
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				x, y = value.split(',')
				self._scaleSize = eSize(int(x), int(y))
				break
		sc = AVSwitch().getFramebufferScale()
		self._aspectRatio = eSize(sc[0], sc[1])
		self.picload.setPara((self._scaleSize.width(), self._scaleSize.height(), sc[0], sc[1], True, 2, '#ff000000'))
		
	def disconnectAll(self):
		self.picload.PictureData.get().remove(self.generatePixmap)
		self.picload = None
		Renderer.disconnectAll(self)
		
	def generatePixmap(self, picInfo=None):
		ptr = self.picload.getData()
		if ptr is not None:
			pic_scale_size = eSize()
			if 'scale' in eSize.__dict__ and self._scaleSize.isValid() and self._aspectRatio.isValid():
				pic_scale_size = ptr.size().scale(self._scaleSize, self._aspectRatio)
			elif 'scaleSize' in gPixmapPtr.__dict__:
				pic_scale_size = ptr.scaleSize()
			if pic_scale_size.isValid():
				pic_scale_width = pic_scale_size.width()
				pic_scale_height = pic_scale_size.height()
				dest_rect = eRect(0, 0, pic_scale_width, pic_scale_height)
				self.instance.setScale(1)
				self.instance.setScaleDest(dest_rect)
			else:
				self.instance.setScale(0)
			self.instance.setPixmap(ptr)
		else:
			self.instance.setPixmap(None)
		
	def doSuspend(self, suspended):
		self.changed((self.CHANGED_DEFAULT,))
			
	def updateIcon(self, filename):
		new_IconFileName = filename
		if (self.iconFileName != new_IconFileName):
			self.iconFileName = new_IconFileName
			self.picload.startDecode(self.iconFileName)

	def changed(self, what):
		if what[0] != self.CHANGED_CLEAR:
			if self.instance:
				self.updateIcon(self.source.iconfilename)
		else:
			self.picload.startDecode("")
