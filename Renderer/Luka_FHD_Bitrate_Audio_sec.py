# -*- coding: utf-8 -*-
# by digiteng...12.2020
# <widget render="Bitrate" source="session.CurrentService" position="0,0" size="500,40" font="Regular; 30" zPosition="2" transparent="1" />
from Renderer import Renderer
from enigma import eLabel, eConsoleAppContainer, iServiceInformation
from Components.VariableText import VariableText
import platform
import os

class Luka_FHD_Bitrate_Audio_sec(Renderer, VariableText):
    GUI_WIDGET = eLabel

    def __init__(self):
        super().__init__()
        self.v = 0
        self.a = 0
        self.text = "0 kbit/s"
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.stopBitrate)
        self.container.dataAvail.append(self.getBitrate)

    def changed(self, what):
        print(f"[Luka_FHD_Bitrate_Audio_sec] changed called with: {what}")
        self.text = "0 kbit/s"

        if what and what[0] != self.CHANGED_CLEAR:
            service = self.source.getCurrentService()
            if service:
                info = service.info()
                vpid = info.getInfo(iServiceInformation.sVideoPID)
                apid = info.getInfo(iServiceInformation.sAudioPID)
                print(f"[Luka_FHD_Bitrate_Audio_sec] Service info: vpid={vpid}, apid={apid}")

                based = platform.machine()
                print(f"[Luka_FHD_Bitrate_Audio_sec] Platform detected: {based}")

                # Erst versuchen /tmp, dann Fallback /var/tmp
                wrote_file = False
                for path in ["/tmp/based.txt", "/var/tmp/based.txt"]:
                    try:
                        with open(path, "w") as f:
                            f.write(str(based))
                        print(f"[Luka_FHD_Bitrate_Audio_sec] Successfully wrote {path}")
                        wrote_file = True
                        break
                    except Exception as e:
                        print(f"[Luka_FHD_Bitrate_Audio_sec] Error writing {path}: {e}")
                
                if not wrote_file:
                    print("[Luka_FHD_Bitrate_Audio_sec] WARNING: Could not write platform file!")

                # Kommando auswählen je nach Architektur
                if based == "sh4":
                    btrt = f"bitrate_sh4 0 0 {vpid} {apid}"
                elif based == "mips":
                    btrt = f"bitrate_mips 0 0 {vpid} {apid}"
                elif based in ("aarch64", "armv7l"):
                    btrt = f"bitrate_arm 0 0 {vpid} {apid}"
                else:
                    btrt = f"bitrate_mips 0 0 {vpid} {apid}"

                print(f"[Luka_FHD_Bitrate_Audio_sec] Executing command: {btrt}")
                self.container.execute(btrt)
            else:
                print("[Luka_FHD_Bitrate_Audio_sec] No current service available")

    def getBitrate(self, bt):
        print(f"[Luka_FHD_Bitrate_Audio_sec] Raw bitrate output:\n{bt}")
        try:
            bt_lines = bt.strip().split("\n")
            if len(bt_lines) > 1 and len(bt_lines[1].split(" ")) > 3:
                self.a = bt_lines[1].split(" ")[3]
                self.text = f"{self.a} kbit/s"
                print(f"[Luka_FHD_Bitrate_Audio_sec] Audio bitrate parsed: {self.a} kbit/s")
            else:
                print(f"[Luka_FHD_Bitrate_Audio_sec] Unexpected bitrate output format: {bt_lines}")
        except Exception as e:
            print(f"[Luka_FHD_Bitrate_Audio_sec] getBitrate error: {e}")

    def stopBitrate(self, retval):
        print(f"[Luka_FHD_Bitrate_Audio_sec] stopBitrate called with retval: {retval}")
        self.v = 0
        self.a = 0
        self.text = "0 kbit/s"
        if self.container.running():
            print("[Luka_FHD_Bitrate_Audio_sec] Killing container process")
            self.container.kill()
