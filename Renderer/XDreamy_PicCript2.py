#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import iServiceInformation
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_SKIN,resolveFilename
from Components.Element import cached
from Components.Converter.Poll import Poll
import os
ablauf = " 1234 "
#open("/tmp/PicCript2", "w").write(ablauf)

# --------------------------- Logfile -------------------------------
from os import system, path, popen, remove
import datetime
import codecs
from shutil import copyfile
from os import remove
from os.path import isfile
########################### log file loeschen ##################################

myfile="/tmp/XDreamy_PicCript2.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################


###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"

# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.date.today().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('off'):
        write_log(data)
        return
    return


# so muss das commando aussehen , um in den file zu schreiben
logout(data="start")

class XDreamy_PicCript2(Renderer):


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
        self.nameCache = { }
        self.pngname = ' '
        self.picon_default = 'fta.png'

    def applySkin(self, desktop, parent):
        attribs = [ ]
        #open("/tmp/PicEmuattribs", "w").write(attribs)
        for (attrib, value) in self.skinAttributes:
            if attrib == 'path':
                self.path = value
                logout(data="path")
                logout(data=str(self.path))

                # Pfad zur Enigma2-Konfigurationsdatei
                config_file = "/etc/enigma2/settings"

                # Konfiguration laden
                with open(config_file, 'r') as f:
                    config = f.readlines()
                for line in config:
                    if line.startswith("config.skin.primary_skin="):
                        skin_path = line.split("=")[1].strip()
                        skin_dir = skin_path.split("/")[0]
                        skinpath = "/usr/share/enigma2/{}/".format(skin_dir)
                        logout(data=str(skinpath))
                        self.pathnew=skinpath+self.path
                        self.pathnew = '/usr/share/enigma2/{}/%s/'.format(skin_dir)
                        logout(data="path")
                        logout(data=str(self.pathnew))


            elif attrib == 'picon_default':
                self.picon_default = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        triggerChanged = [self.CHANGED_DEFAULT]
        self.changed(triggerChanged)
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ' '
            if what[0] is not self.CHANGED_CLEAR:
                sname = 'none'
                #open("/tmp/PicCriptsname", "w").write(sname)
                service = self.source.service
                if service:
                    info = service and service.info()
                    if info:
                        caids = \
                            info.getInfoObject(iServiceInformation.sCAIDs)
                        if caids:
                            if len(caids) > 0:
                                for caid in caids:
                                    caid = self.int2hex(caid)
                                    if len(caid) is 3:
                                        caid = '0%s' % caid
                                        caid = caid[:2]
                                        caid = caid.upper()
                                        if caid == '26':
                                            sname = 'BiSS'
                                        elif caid == '01':
                                            sname = 'SEC'
                                        elif caid == '06':
                                            sname = 'IRD'
                                        elif caid == '17':
                                            sname = 'BET'
                                        elif caid == '05':
                                            sname = 'VIA'
                                        elif caid == '18':
                                            sname = 'NAG'
                                        elif caid == '09':
                                            sname = 'NDS'
                                        elif caid == '0B':
                                            sname = 'CONN'
                                        elif caid == '0D':
                                            sname = 'CRW'
                                        elif caid == '4A':
                                            sname = 'DRE'
                                        elif caid == '0E':
                                            sname = 'PowerVU'
                                        elif caid == '22':
                                            sname = 'Codicrypt'
                                        elif caid == '07':
                                            sname = 'DigiCipher'
                                        elif caid == 'A1':
                                            sname = 'Rosscrypt'
                                        elif caid == '56':
                                            sname = 'Verimatrix'

                pngname = self.nameCache.get(sname, '')
                if pngname is '':
                    pngname = self.findPicon(sname)
                    if pngname is not '':
                        self.nameCache[sname] = pngname
            if pngname is '':
                pngname = self.nameCache.get('default', '')
                if pngname is '':
                    pngname = self.findPicon('picon_default')
                    if pngname is '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN,
                                'fta.png')
                        if fileExists(tmp):
                            pngname = tmp
                        self.nameCache['default'] = pngname

            if self.pngname is not pngname:
                self.pngname = pngname
                self.instance.setPixmapFromFile(self.pngname)

    def int2hex(self, int):
        return '%x' % int

    def findPicon(self, serviceName):
        searchPaths1 = list(self.searchPaths) + [self.pathnew]
        self.searchPaths = searchPaths1
        for path in self.searchPaths:
            logout(data="path")
            logout(data=str(path))
            #logout(data="pathnew")
            #logout(data=str(self.pathnew))
            pngname = path % self.path + serviceName + '.png'
            logout(data=str(pngname))

            if fileExists(pngname):
                return pngname
        return ''