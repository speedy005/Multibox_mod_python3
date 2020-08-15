from __future__ import print_function
#######################################################################
#
#    Renderer for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#    Please respect my work and don't delete/change name of the renderer author
#
#    Nie zgadzam sie na wykorzystywanie tego renderera w projektach platnych jak np. Graterlia!!!
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    To use it do the following:
#       - download package of animated picons, for example from my opkg
#       - write them in the animatedPicons folder on mounted device or in /usr/share/enigma2/
#             NOTE:if you want to use any other folder, you need to specify it in widget definition. E.g. pixmaps="animatedPicons/Flara/"
#       - include J00zekPiconAnimation widget in the infobar skin definition.
#             E.g. <widget source="session.CurrentService" render="j00zekPiconAnimation" position="30,30" size="220,132" zPosition="5" transparent="1" alphatest="blend" />
#             NOTE:
#                  -  position="X,Y" should be the same like position of a picon in skin definition
#                  -  size="X,Y" should be the same like size of a picon in skin definition
#                  -  zPosition="Z" should be bigger than zPosition of a picon in skin definition, to display animation over the picon.
#
#    OPTIONAL animations control:
#       - to set speed put '.ctrl' file  in the pngs folder containing 'delay=TIME' where TIME is miliseconds to wait between frames
#       - to overwrite skin setting use config attributes from your own plugin or use UserSkin which has GUI to present them
#       - to disable user settings (see above) put lockpath="True" attribute in widget definition
#       - to randomize animations put all in the subfolders of main empy animations folder
#                 Example:
#                         create /usr/shareenigma2/animatedPicons/ EMPTY folder
#                         create /usr/shareenigma2/animatedPicons/Flara subfolder with animation png's
#                         create /usr/shareenigma2/animatedPicons/OldMovie subfolder with second animation png's
#
#######################################################################
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigDirectory
from Components.Harddisk import harddiskmanager
from random import randint
import os

config.plugins.j00zekPiconAnimation = ConfigSubsection()
config.plugins.j00zekPiconAnimation.UserPathEnabled = ConfigYesNo(default = False)
config.plugins.j00zekPiconAnimation.UserPath = ConfigDirectory(default = "")
##### write log in /tmp folder #####
DBG = False
try:
    from Components.j00zekComponents import j00zekDEBUG
except Exception:
    def j00zekDEBUG(myText=None):
        if not myText is None:
            try: print(myText)
            except Exception: pass
#####

searchPaths = ('/usr/share/enigma2/', '/media/sde1/', '/media/cf/', '/media/sdd1/', '/media/usb/', '/media/ba/', '/mnt/ba/', '/media/sda/', '/etc/')

def initPiconPaths():
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[initPiconPaths] >>>')
    for part in harddiskmanager.getMountedPartitions():
        addPiconPath(part.mountpoint)
    if os.path.exists("/proc/mounts"):
        with open("/proc/mounts", "r") as f:
            for line in f:
                if line.startswith('/dev/sd'):
                    mountpoint = line.split(' ')[1]
                    addPiconPath(mountpoint)

def addPiconPath(mountpoint):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] >>> mountpoint=' + mountpoint)
    if mountpoint == '/':
        return
    global searchPaths
    try:
        if mountpoint not in searchPaths:
            if DBG: j00zekDEBUG('j00zekPiconAnimation]:[addPiconPath] mountpoint not in searchPaths')
            for pp in os.listdir(mountpoint):
                lpp = os.path.join(mountpoint, pp) + '/'
                if pp.find('picon') >= 0 and os.path.isdir(lpp): #any folder *picon*
                    for pf in os.listdir(lpp):
                        if pf.endswith('.png') and mountpoint not in searchPaths: #if containf *.png
                            if mountpoint.endswith('/'):
                                searchPaths.append(mountpoint)
                            else:
                                searchPaths.append(mountpoint + '/')
                            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] mountpoint appended to searchPaths')
                            break
                    else:
                        continue
                    break
    except Exception as e:
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] Exception:' + str(e))

def onPartitionChange(why, part):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[onPartitionChange] >>>')
    global searchPaths
    if why == 'add' and part.mountpoint not in searchPaths:
        addPiconPath(part.mountpoint)
    elif why == 'remove' and part.mountpoint in searchPaths:
        searchPaths.remove(part.mountpoint)

class AMB_j00zekPiconAnimation(Renderer):
    __module__ = __name__

    def __init__(self):
        Renderer.__init__(self)
        self.pixmaps = 'animatedPicons'
        self.pixdelay = 50
        self.doAnim = False
        self.doLockPath = False
        self.animCounter = 0
        self.count = 0
        self.slideIcon = 0
        self.pixstep = 1
        self.pics = []
        self.picsFolder = []
        self.animTimer = eTimer()
        self.animTimer.callback.append(self.timerEvent)
        self.what = ['CHANGED_DEFAULT', 'CHANGED_ALL', 'CHANGED_CLEAR', 'CHANGED_SPECIFIC', 'CHANGED_POLL']

    def applySkin(self, desktop, parent):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] >>>')
        #Load attribs
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'pixmaps':
                self.pixmaps = value
            elif attrib == 'lockpath':
                if value == 'True':
                    self.doLockPath = True
            elif attrib == 'pixdelay':
                self.pixdelay = int(value)
                if self.pixdelay < 40:
                    self.pixdelay = 50
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        #Load animation into memory
        try:
            if config.plugins.j00zekPiconAnimation.UserPathEnabled.value == True and self.doLockPath == False:
                if os.path.exists(config.plugins.j00zekPiconAnimation.UserPath.value):
                    self.loadPNGsAnim(config.plugins.j00zekPiconAnimation.UserPath.value)
                    self.loadPNGsSubFolders(config.plugins.j00zekPiconAnimation.UserPath.value)
                elif DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] User path "%s" selected but does NOT exist' % config.plugins.j00zekPiconAnimation.UserPath.value)
            else:
                for path in searchPaths:
                    if self.loadPNGsAnim(os.path.join(path, self.pixmaps)) == True:
                        break
                self.loadPNGsSubFolders(os.path.join(path, self.pixmaps))
        except Exception as e:
            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] Exception %s' % str(e))
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[postWidgetCreate] >>>')
#self.changed((self.CHANGED_DEFAULT,))
        return

    def preWidgetRemove(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[preWidgetRemove] >>>')
        if not self.animTimer is None:
            self.animTimer.stop()
            self.animTimer.callback.remove(self.timerEvent)
            self.animTimer = None

    def connect(self, source):
        Renderer.connect(self, source)

    def doSuspend(self, suspended):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[doSuspend] >>> suspended=%s' % suspended)
        if suspended:
            self.changed((self.CHANGED_CLEAR,))
        else:
            self.changed((self.CHANGED_DEFAULT,))

    def loadPNGsSubFolders(self, animPath):
        self.picsFolder = []
        if len(self.pics) == 0 and os.path.exists(animPath):
            picsFolder = [f for f in os.listdir(animPath) if os.path.isdir(os.path.join(animPath, f))]
            for x in picsFolder:
                for f in os.listdir(os.path.join(animPath, x)):
                    if f.endswith(".png"):
                        self.picsFolder.append(os.path.join(animPath, x))
                        if DBG: j00zekDEBUG('[j00zekPiconAnimation]]:[loadPNGsSubFolders] found *.png in subfolder "%s"' % os.path.join(animPath, x))
                        break

    def loadPNGsAnim(self, animPath):
        if animPath == self.pixmaps: return False
        if os.path.exists(animPath):
            self.pixmaps = animPath
            pngfiles = sorted([f for f in os.listdir(self.pixmaps) if (os.path.isfile(os.path.join(self.pixmaps, f)) and f.endswith(".png"))])
            self.pics = []
            self.doAnim = False
            for x in pngfiles:
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]]:[loadPNGsAnim] read image %s' % os.path.join(self.pixmaps, x))
                self.pics.append(LoadPixmap(os.path.join(self.pixmaps, x)))
            if len(self.pics) > 0:
                self.count = len(self.pics)
                self.doAnim = True
                if os.path.exists(os.path.join(animPath, '.ctrl')):
                    with open(os.path.join(animPath, '.ctrl')) as cf:
                        try:
                            myDelay=cf.readline().strip()
                            cf.close()
                            self.pixdelay = int(myDelay.split('=')[1])
                            if self.pixdelay < 40: self.pixdelay = 40
                        except Exception as e:
                            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Exception "%s" loading .ctrl' % str(e))
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Loaded from path=%s, pics=%s, pixdelay=%s, step=%s' % (self.pixmaps, self.count, self.pixdelay, self.pixstep))
                return True
            else:
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] No *.png in given path "%s".' % (animPath))
        else:
            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[loadPNGsAnim] Path "%s" does NOT exist.' % (animPath))
        return False


    def changed(self, what):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[changed] >>>')
        if self.instance:
            self.instance.setScale(1)
            if DBG: j00zekDEBUG('\t\t what[0]=%s(%s), self.doAnim=%s' % (self.what[int(what[0])], what[0], self.doAnim))
            if what[0] == self.CHANGED_CLEAR:
                if not self.animTimer is None: self.animTimer.stop()
                self.instance.hide()
                self.slideIcon = 0
                self.doAnim = True
            elif self.doAnim == True:
                self.doAnim = False
                self.slideIcon = 0
                self.instance.show()
                self.animTimer.start(self.pixdelay, True)

    def timerEvent(self):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] >>> self.slideIcon=%s' % self.slideIcon)
        self.animTimer.stop()
        if self.slideIcon < self.count:
            self.instance.setPixmap(self.pics[self.slideIcon])
            self.slideIcon = self.slideIcon + self.pixstep
            if self.slideIcon > self.count: self.slideIcon = self.count
            self.animTimer.start(self.pixdelay, True)
        elif self.slideIcon == self.count: #Note last frame does NOT exists
            if DBG: j00zekDEBUG('\t\t stop animation')
            self.instance.hide()
            self.doAnim = True
            self.animCounter = self.animCounter + 1
            if len(self.picsFolder) > 1:
                if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] change animation')
                self.loadPNGsAnim(self.picsFolder[randint(0, len(self.picsFolder)-1)])
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] <<<')

harddiskmanager.on_partition_list_change.append(onPartitionChange)
initPiconPaths()
