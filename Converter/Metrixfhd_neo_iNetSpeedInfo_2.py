# -*- coding: utf-8 -*-
# This plugin is free software, you are allowed to
# modify it (if you keep the license),
# but you are not allowed to distribute/publish
# it without source code (this version and your modifications).
# This means you also have to distribute
# source code of your modifications.
#
#
#######################################################################
#
# NetSpeedInfo for VU+
# Coded by markusw (c) 2013
# www.vuplus-support.org
#
#######################################################################
# -*- coding: utf-8 -*-
# This plugin is free software, you are allowed to
# modify it (if you keep the license),
# but you are not allowed to distribute/publish
# it without source code (this version and your modifications).
# This means you also have to distribute
# source code of your modifications.
#
#
#######################################################################
#
# NetSpeedInfo for VU+
# Coded by markusw (c) 2013
# www.vuplus-support.org
#
#######################################################################
# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll


class Metrixfhd_neo_iNetSpeedInfo_2(Poll, Converter, object):
    RCL = 0
    TML = 1
    RCW = 2
    TMW = 3
    RCLT = 4
    TMLT = 5
    RCWT = 6
    TMWT = 7
    RCL_MB = 8
    TML_MB = 9
    RCW_MB = 10
    TMW_MB = 11
    RC = 12
    TM = 13
    RCT = 14
    TMT = 15
    RC_MB = 16
    TM_MB = 17
    NET_TYP = 18
    ERR_RCL = 19
    ERR_TML = 20
    DRO_RCL = 21
    DRO_TML = 22
    ERR_RCW = 23
    ERR_TMW = 24
    DRO_RCW = 25
    DRO_TMW = 26
    COMPACT = 27  # Neu: Kompakter Gesamtstatus

    def __init__(self, type, update_interval=1000):
        Poll.__init__(self)
        self.poll_interval = 1000
        self.poll_enabled = True
        self.lanreceivetotal = 0
        self.lanreceivetotalout = 0
        self.lanreceive = 0
        self.lanreceivemb = 0
        self.wlanreceivetotal = 0
        self.wlanreceivetotalout = 0
        self.wlanreceive = 0
        self.wlanreceivemb = 0
        self.lantransmittotal = 0
        self.lantransmittotalout = 0
        self.lantransmit = 0
        self.lantransmitmb = 0
        self.wlantransmittotal = 0
        self.wlantransmittotalout = 0
        self.wlantransmit = 0
        self.wlantransmitmb = 0
        self.receivetotal = 0
        self.receive = 0
        self.transmittotal = 0
        self.transmit = 0
        self.receivemb = 0
        self.transmitmb = 0
        self.nettyp = "NONE"
        self.error_lanreceive = 0
        self.drop_lanreceive = 0
        self.error_lantransmite = 0
        self.drop_lantransmite = 0
        self.error_wlanreceive = 0
        self.drop_wlanreceive = 0
        self.error_wlantransmite = 0
        self.drop_wlantransmite = 0

        Converter.__init__(self, type)
        if type == "RCL":
            self.type = self.RCL
        elif type == "TML":
            self.type = self.TML
        elif type == "RCW":
            self.type = self.RCW
        elif type == "TMW":
            self.type = self.TMW
        elif type == "RCLT":
            self.type = self.RCLT
        elif type == "TMLT":
            self.type = self.TMLT
        elif type == "RCWT":
            self.type = self.RCWT
        elif type == "TMWT":
            self.type = self.TMWT
        elif type == "RCL_MB":
            self.type = self.RCL_MB
        elif type == "TML_MB":
            self.type = self.TML_MB
        elif type == "RCW_MB":
            self.type = self.RCW_MB
        elif type == "TMW_MB":
            self.type = self.TMW_MB
        elif type == "RC":
            self.type = self.RC
        elif type == "TM":
            self.type = self.TM
        elif type == "RCT":
            self.type = self.RCT
        elif type == "TMT":
            self.type = self.TMT
        elif type == "RC_MB":
            self.type = self.RC_MB
        elif type == "TM_MB":
            self.type = self.TM_MB
        elif type == "NET_TYP":
            self.type = self.NET_TYP
        elif type == "ERR_RCL":
            self.type = self.ERR_RCL
        elif type == "ERR_TML":
            self.type = self.ERR_TML
        elif type == "DRO_RCL":
            self.type = self.DRO_RCL
        elif type == "DRO_TML":
            self.type = self.DRO_TML
        elif type == "ERR_RCW":
            self.type = self.ERR_RCW
        elif type == "ERR_TMW":
            self.type = self.ERR_TMW
        elif type == "DRO_RCW":
            self.type = self.DRO_RCW
        elif type == "DRO_TMW":
            self.type = self.DRO_TMW
        elif type == "COMPACT":
            self.type = self.COMPACT

    @cached
    def getText(self):
        textvalue = self.updateNetSpeedInfoStatus()
        return textvalue

    text = property(getText)

    def updateNetSpeedInfoStatus(self):
        lan_interface = "eth0"  # Passe hier dein LAN-Interface an

        try:
            with open("/proc/net/dev") as bwm:
                lines = bwm.readlines()
        except Exception:
            return "Fehler beim Lesen von /proc/net/dev"

        lan_speed = None
        # LAN Speed auslesen (in Mbit/s)
        try:
            with open(f"/sys/class/net/{lan_interface}/speed") as f:
                lan_speed = f.read().strip()
                if lan_speed == "-1":
                    lan_speed = None
                else:
                    lan_speed = int(lan_speed)
        except Exception:
            lan_speed = None

        flaglan = 0
        flagwlan = 0
        for bw in lines[2:]:
            while "  " in bw:
                bw = bw.replace("  ", " ")
            if "eth" in bw:
                flaglan = 1
                sp = bw.split(":")[1].strip().split()
                newlanreceive = int(sp[0]) / 1024
                self.error_lanreceive = int(sp[2])
                self.drop_lanreceive = int(sp[3])
                if self.lanreceivetotal > 0:
                    self.lanreceive = (newlanreceive - self.lanreceivetotal) * 8 / 1024
                    self.lanreceivemb = (newlanreceive - self.lanreceivetotal) / 1024
                self.lanreceivetotal = newlanreceive
                self.lanreceivetotalout = newlanreceive / 1024

                newlantransmit = int(sp[8]) / 1024
                self.error_lantransmite = int(sp[10])
                self.drop_lantransmite = int(sp[11])
                if self.lantransmittotal > 0:
                    self.lantransmit = (newlantransmit - self.lantransmittotal) * 8 / 1024
                    self.lantransmitmb = (newlantransmit - self.lantransmittotal) / 1024
                self.lantransmittotal = newlantransmit
                self.lantransmittotalout = newlantransmit / 1024
                if (self.lantransmittotal + self.lanreceivetotal) == 0:
                    flaglan = 0
            elif any(tag in bw for tag in ["ra", "wlan", "wifi"]):
                flagwlan = 1
                sp = bw.split(":")[1].strip().split()
                newwlanreceive = int(sp[0]) / 1024
                self.error_wlanreceive = int(sp[2])
                self.drop_wlanreceive = int(sp[3])
                if self.wlanreceivetotal > 0:
                    self.wlanreceive = (newwlanreceive - self.wlanreceivetotal) * 8 / 1024
                    self.wlanreceivemb = (newwlanreceive - self.wlanreceivetotal) / 1024
                self.wlanreceivetotal = newwlanreceive
                self.wlanreceivetotalout = newwlanreceive / 1024

                newwlantransmit = int(sp[8]) / 1024
                self.error_wlantransmite = int(sp[10])
                self.drop_wlantransmite = int(sp[11])
                if self.wlantransmittotal > 0:
                    self.wlantransmit = (newwlantransmit - self.wlantransmittotal) * 8 / 1024
                    self.wlantransmitmb = (newwlantransmit - self.wlantransmittotal) / 1024
                self.wlantransmittotal = newwlantransmit
                self.wlantransmittotalout = newwlantransmit / 1024

        if flaglan == 1:
            self.receive = self.lanreceive
            self.transmit = self.lantransmit
            self.receivetotal = self.lanreceivetotal / 1024
            self.transmittotal = self.lantransmittotal / 1024
            self.nettyp = "LAN"
        elif flagwlan == 1:
            self.receive = self.wlanreceive
            self.transmit = self.wlantransmit
            self.receivetotal = self.wlanreceivetotal / 1024
            self.transmittotal = self.wlantransmittotal / 1024
            self.nettyp = "WLAN"
        else:
            self.receive = 0
            self.transmit = 0
            self.receivetotal = 0
            self.transmittotal = 0
            self.nettyp = "NONE"

        self.receivemb = self.receive / 8 if (flaglan or flagwlan) else 0
        self.transmitmb = self.transmit / 8 if (flaglan or flagwlan) else 0

        if self.type == self.COMPACT:
            speed_info = ""
            if self.nettyp == "LAN" and lan_speed:
                speed_info = f" ({lan_speed} Mbit/s)"
            return "Netzwerk: %s%s (↓ %3.2f Mbit/s ↑ %3.2f Mbit/s) | Total: ↓ %d MB ↑ %d MB" % (
                self.nettyp,
                speed_info,
                self.receive,
                self.transmit,
                self.receivetotal,
                self.transmittotal
            )
        return "Typ nicht erkannt"

    def changed(self, what):
        if what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)



