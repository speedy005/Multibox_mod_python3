# PiconUni
# Copyright (c) 2boom 2012-16
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# 26.09.2012 added search mountpoints
# 25.06.2013 added resize picon
# 26.11.2013 code optimization
# 02.12.2013 added compatibility with CaidInfo2 (SatName)
# 18.12.2013 added picon miltipath
# 27.12.2013 added picon reference
# 27.01.2014 added noscale parameter (noscale="0" is default, scale picon is on)
# 28.01.2014 code otimization
# 02.04.2014 added iptv ref code
# 17.04.2014 added path in plugin dir...
# 02.07.2014 small fix reference
# 09.01.2015 redesign code
# 02.05.2015 add path uuid device
# 08.05.2016 add 5001, 5002 stream id
# 16.11.2018 fix search Paths (by Sirius, thx Taapat)

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, resolveFilename 
import os

# --------------------------- Logfile -------------------------------
from os import system, path, popen, remove
import datetime
import codecs
from shutil import copyfile
from os import remove
from os.path import isfile
########################### log file loeschen ##################################

myfile="/tmp/xDreamy_mod_PiconUni_2.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################


###########################  log file anlegen ##################################
# speedy005 logfile anlegen die eingabe in logstatus

logstatus = "on"

# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('off'):
        with open(myfile, "a") as log:

            log.write(datetime.date.today().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# so muss das commando aussehen , um in den file zu schreiben
logout(data="start")


searchPaths = []



def initPiconPaths():
    global searchPaths
    if os.path.isfile('/proc/mounts'):
        for line in open('/proc/mounts'):
            if '/dev/sd' in line or '/dev/disk/by-uuid/' in line or '/dev/mmc' in line:
                piconPath = line.split()[1].replace('\\040', ' ') + '/%s/'
                searchPaths.append(piconPath)
    searchPaths.append('/usr/share/enigma2/%s/')
    searchPaths.append('/usr/lib/enigma2/python/Plugins/%s/')
    #searchPaths.append(full_skin_path)
    #logout(data=str(searchPaths))



class xDreamy_mod_PiconUni_2(Renderer):
    __module__ = __name__
    def __init__(self):
        Renderer.__init__(self)
        self.path = 'piconUni'
        self.scale = '0'
        self.nameCache = {}
        self.pngname = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for (attrib, value,) in self.skinAttributes:
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
                        self.pathnew = skinpath + self.path
                        self.pathnew = '/usr/share/enigma2/{}/%s/'.format(skin_dir)
                        logout(data="path")
                        logout(data=str(self.pathnew))



                wai = resolveFilename(SCOPE_SKIN_IMAGE, self.path)
                logout(data=str(wai))
            elif attrib == 'noscale':
                self.scale = value
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        triggerChanged = [self.CHANGED_DEFAULT]
        self.changed(triggerChanged)
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ''
            if not what[0] is self.CHANGED_CLEAR:
                sname = self.source.text
                sname = sname.upper().replace('.', '').replace('\xc2\xb0', '')
                print(sname)
                if not sname.startswith('1'):
                    sname = sname.replace('4097', '1', 1).replace('5001', '1', 1).replace('5002', '1', 1)
                if ':' in sname:
                    sname = '_'.join(sname.split(':')[:10])
                pngname = self.nameCache.get(sname, '')
                if pngname == '':
                    pngname = self.findPicon(sname)
                    if not pngname != '':
                        self.nameCache[sname] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                        if os.path.isfile(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                    self.nameCache['default'] = pngname
            if not self.pngname is pngname:
                if self.scale == '0':
                    if pngname:
                        self.instance.setScale(1)
                        self.instance.setPixmapFromFile(pngname)
                        self.instance.show()
                    else:
                        self.instance.hide()
                else:
                    if pngname:
                        self.instance.setPixmapFromFile(pngname)
                self.pngname = pngname

    def findPicon(self, serviceName):
        global searchPaths
        pathtmp = self.path.split(',')
        searchPaths1 = list(searchPaths) + [self.pathnew]
        searchPaths = searchPaths1

        for path in searchPaths:
            #logout(data=str(searchPaths))
            for dirName in pathtmp:
                logout(data="path")
                logout(data=str(path))
                pngname = (path % dirName) + serviceName + '.png'
                logout(data=str(pngname))

                if os.path.isfile(pngname):
                    return pngname
        return ''

initPiconPaths()