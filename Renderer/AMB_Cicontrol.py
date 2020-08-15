#!/usr/bin/python
# -*- coding: utf-8 -*-
# by Nikolasi

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eDVBCI_UI, eDVBCIInterfaces, eEnv
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, \
    SCOPE_CURRENT_SKIN, resolveFilename
from Components.Converter.Poll import Poll


class AMB_Cicontrol(Renderer, Poll):

    searchPaths = (eEnv.resolve('${datadir}/enigma2/%s/'),
                   '/media/hdd/%s/', '/media/usb/%s/')

    def __init__(self):
        Poll.__init__(self)
        Renderer.__init__(self)
        self.path = 'emu'
        self.slot = 0
        self.nameCache = {}
        self.pngname = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for (attrib, value) in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            elif attrib == 'slot':
                self.slot = int(value)
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        self.poll_interval = 1000
        self.poll_enabled = True
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                if service:
                    NUM_CI = \
                        eDVBCIInterfaces.getInstance().getNumOfSlots()
                    if NUM_CI > 0:
                        state = \
                            eDVBCI_UI.getInstance().getState(self.slot)
                        if state != -1:
                            if state == 0:
                                text = 'nomodule'
                            elif state == 1:
                                text = 'initmodule'
                            elif state == 2:
                                text = 'ready'
                        else:
                            text = 'nomodule'
                    else:
                        text = 'nomodule'
                    pngname = self.nameCache.get(text, '')
                    if pngname == '':
                        pngname = self.findPicon(text)
                        if pngname != '':
                            self.nameCache[text] = pngname
            if pngname == '':  # no picon for service found
                pngname = self.nameCache.get('default', '')
                if pngname == '':  # no default yet in cache..
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN,
                                'picon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE,
                                    'skin_default/picon_default.png')
                    self.nameCache['default'] = pngname
            if self.pngname != pngname:
                self.instance.setPixmapFromFile(pngname)
                self.pngname = pngname

    def findPicon(self, serviceName):
        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname
        return ''