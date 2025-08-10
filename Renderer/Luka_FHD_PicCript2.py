
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import iServiceInformation
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN, resolveFilename
from Components.Element import cached
from Components.Converter.Poll import Poll
import os
import datetime
from os import remove
from os.path import isfile

myfile = "/tmp/XDreamy_PicCript2.log"
logstatus = "on"

if isfile(myfile):
    remove(myfile)

def write_log(msg):
    if logstatus == 'on':
        with open(myfile, "a") as log:
            log.write(datetime.date.today().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

def logout(data):
    if logstatus == 'off':
        write_log(data)

logout(data="start")

class Luka_FHD_PicCript2(Renderer):
    __module__ = __name__
    if fileExists('/usr/lib64'):
        searchPaths = (
            '/usr/share/enigma2/%s/',
            '/data/%s/',
            '/usr/lib64/enigma2/python/Plugins/Extensions/%s/',
            '/media/sde1/%s/',
            '/media/cf/%s/',
            '/media/sdd1/%s/',
            '/media/hdd/%s/',
            '/media/usb/%s/',
            '/media/ba/%s/',
            '/mnt/ba/%s/',
            '/media/sda/%s/',
            '/etc/%s/',
        )
    else:
        searchPaths = (
            '/usr/share/enigma2/%s/',
            '/data/%s/',
            '/usr/lib/enigma2/python/Plugins/Extensions/%s/',
            '/media/sde1/%s/',
            '/media/cf/%s/',
            '/media/sdd1/%s/',
            '/media/hdd/%s/',
            '/media/usb/%s/',
            '/media/ba/%s/',
            '/mnt/ba/%s/',
            '/media/sda/%s/',
            '/etc/%s/',
        )

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'cript'
        self.nameCache = {}
        self.pngname = ' '
        self.picon_default = 'fta.png'

    def applySkin(self, desktop, parent):
        attribs = []
        for (attrib, value) in self.skinAttributes:
            if attrib == 'path':
                self.path = value
                config_file = "/etc/enigma2/settings"
                with open(config_file, 'r') as f:
                    config = f.readlines()
                for line in config:
                    if line.startswith("config.skin.primary_skin="):
                        skin_path = line.split("=")[1].strip()
                        skin_dir = skin_path.split("/")[0]
                        skinpath = "/usr/share/enigma2/{}/".format(skin_dir)
                        self.pathnew = '/usr/share/enigma2/{}/%s/'.format(skin_dir)
            elif attrib == 'picon_default':
                self.picon_default = value
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        self.changed([self.CHANGED_DEFAULT])
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ' '
            if what[0] is not self.CHANGED_CLEAR:
                sname = 'none'
                service = self.source.service
                if service:
                    info = service and service.info()
                    if info:
                        caids = info.getInfoObject(iServiceInformation.sCAIDs)
                        if caids and len(caids) > 0:
                            for caid in caids:
                                caid = self.int2hex(caid)
                                if len(caid) == 3:
                                    caid = '0%s' % caid
                                caid = caid[:2].upper()
                                sname = {
                                    '26': 'BiSS',
                                    '01': 'SEC',
                                    '06': 'IRD',
                                    '17': 'BET',
                                    '05': 'VIA',
                                    '18': 'NAG',
                                    '09': 'NDS',
                                    '0B': 'CONN',
                                    '0D': 'CRW',
                                    '4A': 'DRE',
                                    '0E': 'PowerVU',
                                    '22': 'Codicrypt',
                                    '07': 'DigiCipher',
                                    'A1': 'Rosscrypt',
                                    '56': 'Verimatrix'
                                }.get(caid, 'FTA')
                        else:
                            sname = 'FTA'  # <-- Für unverschlüsselte Sender

                pngname = self.nameCache.get(sname, '')
                if pngname == '':
                    pngname = self.findPicon(sname)
                    if pngname != '':
                        self.nameCache[sname] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon(self.picon_default.replace('.png', ''))
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'fta.png')
                        if fileExists(tmp):
                            pngname = tmp
                        self.nameCache['default'] = pngname

            if self.pngname != pngname:
                self.pngname = pngname
                self.instance.setPixmapFromFile(self.pngname)

    def int2hex(self, int_val):
        return '%x' % int_val

    def findPicon(self, serviceName):
        searchPaths1 = list(self.searchPaths) + [self.pathnew]
        self.searchPaths = searchPaths1
        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname
        return ''
