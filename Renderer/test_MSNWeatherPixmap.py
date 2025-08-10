# -*- coding: utf-8 -*-
# WeatherPlugin E2 (Updated for Python 3.12)
# Coded by Dr.Best (c) 2012-2013, Updated by OpenAI (2025)
# Support: www.dreambox-tools.info
# E-Mail: dr.best@dreambox-tools.info
#
# This plugin is open source but it is NOT free software.
#
# This plugin may only be distributed to and executed on hardware which
# is licensed by Dream Multimedia GmbH.
#

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Components.AVSwitch import AVSwitch
from enigma import eEnv, ePicLoad, eRect, eSize, gPixmapPtr

class test_MSNWeatherPixmap(Renderer):
    def __init__(self):
        super().__init__()
        self.picload = ePicLoad()
        self.picload.PictureData.get().connect(self.paintIconPixmapCB)
        self.iconFileName = ""

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        for attrib, value in self.skinAttributes:
            if attrib == "size":
                try:
                    x, y = map(int, value.split(','))
                    self._scaleSize = eSize(x, y)
                except ValueError:
                    self._scaleSize = eSize(100, 100)  # Default fallback
                break
        sc = AVSwitch().getFramebufferScale()
        self._aspectRatio = eSize(sc[0], sc[1])
        self.picload.setPara((self._scaleSize.width(), self._scaleSize.height(), sc[0], sc[1], True, 2, '#ff000000'))

    def disconnectAll(self):
        self.picload.PictureData.get().disconnect(self.paintIconPixmapCB)
        self.picload = None
        super().disconnectAll()

    def paintIconPixmapCB(self, picInfo=None):
        ptr = self.picload.getData()
        if ptr is not None:
            pic_scale_size = eSize()
            if hasattr(ptr, 'size') and self._scaleSize.isValid() and self._aspectRatio.isValid():
                pic_scale_size = ptr.size().scaled(self._scaleSize, self._aspectRatio)

            if pic_scale_size.isValid():
                self.instance.setScale(1)
                self.instance.setScaleDest(eRect(0, 0, pic_scale_size.width(), pic_scale_size.height()))
            else:
                self.instance.setScale(0)
            self.instance.setPixmap(ptr)
        else:
            self.instance.setPixmap(None)

    def doSuspend(self, suspended):
        self.changed((self.CHANGED_CLEAR if suspended else self.CHANGED_DEFAULT,))

    def updateIcon(self, filename):
        if self.iconFileName != filename:
            self.iconFileName = filename
            self.picload.startDecode(self.iconFileName)

    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR and self.instance:
            self.updateIcon(self.source.iconfilename)
        else:
            self.picload.startDecode("")