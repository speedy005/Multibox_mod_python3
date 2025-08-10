# 2boom 2011-14
#  CamdRAED - Converter
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#       <convert type="iCamdRAED">Camd</convert>
# </widget>
# Edit By RAED 16-04-2013
# Updated By RAED 20-04-2014 Added TS-Panel
# Updated By RAED 07-06-2014 Added DE-OpenBlackHole
# Updated By RAED 08-06-2014 Added BlackHole OE1.6
# Updated By RAED 10-08-2014 Added BlackHole OE2.0
# Updated By RAED 13-02-2015 Edit VTI
# Updated By RAED 15-06-2015 Added Newnigma2 OE2.0
# Updated By RAED 07-01-2016 Fixed Some Bugs
# Updated By RAED 12-07-2019 Fixed OpenATV detect name of emu
# Updated By RAED 26-07-2020 Fixed name for some images and support python3
# Updated By RAED 23-03-2021 More Fixed OpenATV/Openpli detect name of emu
# Updated By RAED 09-01-2022 Added Puer2 support
# Updated By RAED 25-12-2022 Update some codes for py3 images

from Components.Converter.Converter import Converter
from Components.config import config
from Components.Element import cached
from Components.Converter.Poll import Poll
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import os

BRANDPLI = '/usr/share/enigma2/hw_info/hw_info.cfg'  # OpenPLI


def checkclist():
    if os.path.exists("/etc/clist.list"):
        for line in open("/etc/clist.list", "r"):
            if 'no' in line:
                return False
            else:
                return True


def ncam_oscam_ver():
    camdlist = ""
    if os.path.exists("/tmp/.ncam/ncam.version"):
        for line in open("/tmp/.ncam/ncam.version"):
            if line.startswith("Version:"):
                camdlist = "%s" % line.split(':')[1].replace(" ", "")
    elif os.path.exists("/tmp/.oscam/oscam.version"):
        for line in open("/tmp/.oscam/oscam.version"):
            if line.startswith("Version:"):
                camdlist = "%s" % line.split(':')[1].replace(" ", "")
    return camdlist


class iCamdRAED(Poll, Converter, object):
    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 2000
        self.poll_enabled = True

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        if not service:
            return None
        camd = ""
        serlist = None
        camdlist = None
        camdlist2 = None
        nameemu = []
        nameser = []
        if not info:
            return ""
        if ncam_oscam_ver() != None:
            camdlist2 = ncam_oscam_ver()
        # PurE2
        elif os.path.exists("/etc/clist.list") and os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.py") or os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.pyo") or os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/pManager/camrestart.pyc"):
            try:
                camdlist = open("/etc/clist.list", "r")
            except:
                return None
        # Merlin 2 & 3 And DreamOSatEmumanager
        elif os.path.exists("/etc/clist.list") and checkclist() is True:
            try:
                camdlist = open("/etc/clist.list", "r")
            except:
                return None
        # Alternative SoftCam Manager
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/plugin.py")):
            if config.plugins.AltSoftcam.actcam.value != "none":
                return config.plugins.AltSoftcam.actcam.value
            else:
                return None
        # VIX
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "SystemPlugins/ViX/SoftcamManager.pyo")) or os.path.exists(resolveFilename(SCOPE_PLUGINS, "SystemPlugins/ViX/SoftcamManager.pyc")):
            try:
                self.autostartcams = config.softcammanager.softcams_autostart.value
                for softcamcheck in self.autostartcams:
                    softcamcheck = softcamcheck.replace("/usr/softcams/", "")
                    softcamcheck = softcamcheck.replace("\n", "")
                    return softcamcheck
            except:
                return None
        #  GlassSysUtil
        elif os.path.exists("/tmp/ucm_cam.info"):
            return open("/tmp/ucm_cam.info").read()
        # egami
        elif os.path.exists("/etc/egami/emuname"):
            try:
                camdlist = open("/etc/egami/emuname", "r")
            except:
                return None
        # elif os.path.exists("/tmp/egami.inf"):
        #        for line in open("/tmp/egami.inf"):
        #                if 'Current emulator:' in line:
        #                        return line.split(':')[-1].lstrip().strip('\n')
        # egami #other code
        # elif os.path.exists("/tmp/egami.inf","r"):
        #        for line in open("/tmp/egami.inf"):
        #                item = line.split(":",1)
        #                if item[0] == "Current emulator":
        #                        return item[1].strip()
        # TS-Panel & Ts images
        elif os.path.exists("/etc/startcam.sh"):
            try:
                for line in open("/etc/startcam.sh"):
                    if "script" in line:
                        return "%s" % line.split("/")[-1].split()[0][:-3]
            except:
                camdlist = None
        # domica 8
        elif os.path.exists("/etc/init.d/cam"):
            if config.plugins.emuman.cam.value:
                return config.plugins.emuman.cam.value
        # PKT
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "Extensions/PKT/plugin.pyo")) or os.path.exists(resolveFilename(SCOPE_PLUGINS, "Extensions/PKT/plugin.pyc")):
            if config.plugins.emuman.cam.value:
                return config.plugins.emuman.cam.value
        # HDMU
        elif os.path.exists("/etc/.emustart") and os.path.exists("/etc/image-version"):
            try:
                for line in open("/etc/.emustart"):
                    return line.split()[0].split('/')[-1]
            except:
                return None
        # Domica
        elif os.path.exists("/etc/active_emu.list"):
            try:
                camdlist = open("/etc/active_emu.list", "r")
            except:
                return None
        # OpenSPA
        elif os.path.exists("/etc/.ActiveCamd"):
            try:
                camdlist = open("/etc/.ActiveCamd", "r")
            except:
                return None
        # OoZooN
        elif os.path.exists("/tmp/cam.info"):
            try:
                camdlist = open("/tmp/cam.info", "r")
            except:
                return None
        # ItalySat
        elif os.path.exists("/etc/CurrentItalyCamName"):
            try:
                camdlist = open("/etc/CurrentItalyCamName", "r")
            except:
                return None
        # BlackHole OE2.0
        elif os.path.exists("/etc/CurrentBhCamName"):
            try:
                camdlist = open("/etc/CurrentBhCamName", "r")
            except:
                return None
        # BlackHole OE1.6
        elif os.path.exists("/etc/CurrentDelCamName"):
            try:
                camdlist = open("/etc/CurrentDelCamName", "r")
            except:
                return None
        # DE-OpenBlackHole
        elif os.path.exists("/etc/BhFpConf"):
            try:
                camdlist = open("/etc/BhCamConf", "r")
            except:
                return None
        # Newnigma2
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "newnigma2/eCamdCtrl/eCamdctrl.pyo")) or os.path.exists(resolveFilename(SCOPE_PLUGINS, "newnigma2/eCamdCtrl/eCamdctrl.pyc")):
            try:
                from Plugins.newnigma2.eCamdCtrl.eCamdctrl import runningcamd
                if config.plugins.camdname.skin.value:
                    return runningcamd.getCamdCurrent()
            except:
                return None
        # Newnigma2 OE2.5
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "newnigma2/camdctrl/camdctrl.pyo")) or os.path.exists(resolveFilename(SCOPE_PLUGINS, "newnigma2/camdctrl/camdctrl.pyc")):
            if config.plugins.camdname.skin.value:
                return config.usage.emu_name.value
            return None
        # GP3 OE2.0
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "Bp/geminimain/lib/libgeminimain.so")):
            try:
                from Plugins.Bp.geminimain.plugin import GETCAMDLIST
                from Plugins.Bp.geminimain.lib import libgeminimain
                camdl = libgeminimain.getPyList(GETCAMDLIST)
                cam = None
                for x in camdl:
                    if x[1] == 1:
                        cam = x[2]
                return cam
            except:
                return None
        # GP4 OE2.5
        elif os.path.exists(resolveFilename(SCOPE_PLUGINS, "GP4/geminicamswitch/gscamScreen.pyo")) or os.path.exists(resolveFilename(SCOPE_PLUGINS, "GP4/geminicamswitch/gscamScreen.pyc")):
            # from Plugins.GP4.geminicamswitch.gscamScreen import Camswitch
            from Plugins.GP4.geminicamswitch.gscamtools import gpconfset
            if gpconfset.gcammanager.currentbinary.value:
                return gpconfset.gcammanager.currentbinary.value
            return None
        # Dream Elite
        elif os.path.exists("/usr/lib/enigma2/python/DE/DEPanel.so"):
            try:
                from DE.DELibrary import Tool
                t = Tool()
                emuname = t.readEmuName(t.readEmuActive()).strip()
                emuactive = emuname != "None" and emuname or t.readEmuName(t.readCrdsrvActive()).strip()
                return emuactive
            except:
                return None
        # ATV for 6.3 and later & Pli
        # elif os.path.exists("/etc/init.d/softcam") and not os.path.exists(BRANDPLI):
        elif os.path.exists("/etc/init.d/softcam") or os.path.exists("/etc/init.d/cardserver"):
            try:
                for line in open("/etc/init.d/softcam"):
                    if "# Short-Description:" in line:
                        return line.split(':')[-1].lstrip().strip('\n')
            except:
                pass
        # Pli/OV
        # elif os.path.exists(BRANDPLI) and os.path.exists("/etc/init.d/softcam") or os.path.exists("/etc/init.d/cardserver"):
                try:
                    for line in open("/etc/init.d/softcam"):
                        if "echo" in line:
                            nameemu.append(line)
                    camdlist = "%s" % nameemu[1].split('"')[1]
                except:
                    pass
                try:
                    for line in open("/etc/init.d/cardserver"):
                        if "echo" in line:
                            nameser.append(line)
                    serlist = "%s" % nameser[1].split('"')[1]
                except:
                    pass
                if serlist is not None and camdlist is not None:
                    return ("%s %s" % (serlist, camdlist))
                elif camdlist is not None:
                    return "%s" % camdlist
                elif serlist is not None:
                    return "%s" % serlist
                return ""
        # AAF & ATV old under 6.2 & VTI
        elif os.path.exists("/etc/image-version") and not os.path.exists("/etc/.emustart"):
            emu = ""
            server = ""
            for line in open("/etc/image-version"):
                if "=AAF" in line or "=openATV" in line or "=opendroid" in line or "=openESI" in line or "=OpenPlus" in line:
                    if config.softcam.actCam.value:
                        emu = config.softcam.actCam.value
                    if config.softcam.actCam2.value:
                        server = config.softcam.actCam2.value
                        if config.softcam.actCam2.value == "no CAM 2 active":
                            server = ""
                elif "=vuplus" in line:
                    if os.path.exists("/tmp/.emu.info"):
                        for line in open("/tmp/.emu.info"):
                            emu = line.strip('\n')
                # BlackHole
                elif "version=" in line and os.path.exists("/etc/CurrentBhCamName"):
                    emu = open("/etc/CurrentBhCamName").read()
            return "%s %s" % (emu, server)
        else:
            return None

        if serlist is not None:
            try:
                cardserver = ""
                for current in serlist.readlines():
                    cardserver = current
                serlist.close()
            except:
                pass
        else:
            cardserver = " "

        if camdlist != None:
            try:
                emu = ""
                for current in camdlist.readlines():
                    emu = current
                camdlist.close()
            except:
                pass
        else:
            emu = " "

        if camdlist2 != None:
            return "%s" % camdlist2
        else:
            return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, what)
