##############################################################################################################################################
#  Youchie-PLI-FHD Renderer for Enigma2
#  Coded by Youchie SmartCam Tem (c)2025
#  If you use this Renderer for other skins and rename it, please keep the second line adding your credits below
#
##############################################################################################################################################

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists

class Luka_FHD_Cryptedicon(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self.Cryptedicon = {
            "sim_on": "/usr/share/enigma2/Aglare-FHD/icons/sim_on1.png"
        }
        self.default_icon = "/usr/share/enigma2/Aglare-FHD/icons/sim_pffn1.png"
        self.last_status = "not_opened"

    def changed(self, what):
        if not self.instance:
            return

        status = self.source.convert()

        if status != self.last_status:
            self.last_status = status

            if status == "opened":
                icon_path = self.Cryptedicon.get("sim_on", self.default_icon)
            else:
                icon_path = self.default_icon

            try:
                self.instance.setPixmapFromFile(icon_path)
                self.instance.show()
            except Exception as e:
                print(f"Error loading CAM icon: {e}")
                self.instance.hide()
