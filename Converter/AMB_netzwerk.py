from Components.Converter.Converter import Converter
from Components.Element import cached
from Screens.InfoBar import InfoBar
from Tools.Directories import fileExists
from enigma import eTimer
from enigma import iServiceInformation
from Components.ConfigList import ConfigListScreen
from Components.Converter.Poll import Poll
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave

class AMB_netzwerk(Poll, Converter, object):
    IP = 0
    NETMASK = 1
    GATEWAY = 2
    MEMTOTAL = 3
    MEMFREE = 4
    STB = 5
    VIDEOMODE = 6
    SKIN = 7
    PROV = 8
    CW0 = 9
    CW1 = 10
    SOURCE = 11
    TMP = 12
    INFO0 = 13
    ALL = 14
    IMAGE = 15

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 1000
        self.poll_enabled = True
        self.type = {'ip': self.IP,
         'netmask': self.NETMASK,
         'gateway': self.GATEWAY,
         'memtotal': self.MEMTOTAL,
         'memfree': self.MEMFREE,
         'stb': self.STB,
         'videomode': self.VIDEOMODE,
         'skin': self.SKIN,
         'prov': self.PROV,
         'cw0': self.CW0,
         'cw1': self.CW1,
         'source': self.SOURCE,
         'tmp': self.TMP,
         'info0': self.INFO0,
         'all': self.ALL,
         'image': self.IMAGE}[type]

    @cached
    def getText(self):
        if self.type == self.NETMASK:
            if fileExists('/etc/network/interfaces'):
                try:
                    for line in open('/etc/network/interfaces'):
                        if 'netmask' in line:
                            return line.split(' ')[1]

                except:
                    return

        elif self.type == self.IP:
            if fileExists('/etc/network/interfaces'):
                try:
                    for line in open('/etc/network/interfaces'):
                        if 'address' in line:
                            return line.split(' ')[1]

                except:
                    return

        elif self.type == self.GATEWAY:
            if fileExists('/etc/network/interfaces'):
                try:
                    for line in open('/etc/network/interfaces'):
                        if 'gateway' in line:
                            return line.split(' ')[1]

                except:
                    return

        elif self.type == self.MEMTOTAL:
            if fileExists('/proc/meminfo'):
                try:
                    for line in open('/proc/meminfo'):
                        if 'MemTotal' in line:
                            return line.split(':')[1]

                except:
                    return

        elif self.type == self.MEMFREE:
            if fileExists('/proc/meminfo'):
                try:
                    for line in open('/proc/meminfo'):
                        if 'MemFree' in line:
                            return line.split(':')[1]

                except:
                    return

        elif self.type == self.STB:
            if fileExists('/etc/image-version'):
                try:
                    for line in open('/etc/image-version'):
                        if 'version' in line:
                            return 'Version_' + line.split('=')[1]

                except:
                    return
        elif self.type == self.VIDEOMODE:
            if fileExists('/etc/videomode'):
                return open('/etc/videomode').read()
        elif self.type == self.SKIN:
            if fileExists('/etc/enigma2/settings'):
                try:
                    for line in open('/etc/enigma2/settings'):
                        if 'config.skin.primary_skin' in line:
                            return line.replace('/skin.xml', ' ').split('=')[1]

                except:
                    return

        elif self.type == self.PROV:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if 'prov' in line:
                        return line.split(':')[1]

        elif self.type == self.CW0:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if 'cw0' in line:
                        return line.split(':')[1]

        elif self.type == self.CW1:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if 'cw1' in line:
                        return line.split(':')[1]

        elif self.type == self.SOURCE:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if 'source' in line:
                        return line.replace('source:', ' ')

        elif self.type == self.TMP:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if 'msec' in line:
                        return 'tmp ' + line.split(' ')[0]

        elif self.type == self.INFO0:
            if fileExists('/tmp/ecm.info'):
                for line in open('/tmp/ecm.info'):
                    if '=' in line:
                        return line.replace('=', '')
        elif self.type == self.ALL:
            if fileExists('/tmp/ecm.info'):
                return open('/tmp/ecm.info').read()
        elif self.type == self.IMAGE:
            if fileExists('/etc/image-version'):
                try:
                    for line in open('/etc/image-version'):
                        if 'creator' in line:
                            return line.split('=')[1]

                except:
                    return

    text = property(getText)
