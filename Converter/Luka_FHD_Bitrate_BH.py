# based on version by areq 2015-12-13 http://areq.eu.org/
# mod by j00zek version 12.10.2018 mod by fhroma  dzieki j00zek

from enigma import eConsoleAppContainer, eTimer, iServiceInformation, iPlayableService
from Components.Console import Console
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.FhromaComponents import isImageType

import os

DBG = False
if DBG:
    from Components.FhromaComponents import FhromaDEBUG

class Luka_FHD_Bitrate_BH(Converter):

    def __init__(self, type):
        super().__init__(type)
        self.clearValues()
        self.isRunning = False
        self.isSuspended = False
        self.myConsole = Console()
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.appClosed)
        self.container.dataAvail.append(self.dataAvail)
        self.StartTimer = eTimer()
        self.StartTimer.callback.append(self.start)
        self.StartTimer.start(100, True)
        self.runTimer = eTimer()
        self.runTimer.callback.append(self.runBitrate)

    @cached
    def getText(self):
        if DBG:
            FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:getText] vcur {self.vcur}")
        if self.vcur > 0:
            return f"{self.vcur} Kb/s"
        else:
            return ""

    text = property(getText)

    def doSuspend(self, suspended):
        if DBG:
            FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:suspended] >>> self.isSuspended={self.isSuspended}, suspended={suspended}")
        if suspended == 0:
            self.isSuspended = False
            self.StartTimer.start(100, True)
        else:
            self.isSuspended = True
            self.myConsole.ePopen("killall -9 bitrate", self.clearValues)

    def start(self):
        if not self.isRunning:
            if self.source.service:
                if DBG:
                    FhromaDEBUG("[Luka_FHD_Bitrate_BH:start] initiate runTimer")
                self.isRunning = True
                self.runTimer.start(100, True)
            else:
                if DBG:
                    FhromaDEBUG("[Luka_FHD_Bitrate_BH:start] wait 100ms for self.source.service")
                self.StartTimer.start(100, True)
        else:
            if DBG:
                FhromaDEBUG("[Luka_FHD_Bitrate_BH:start] runBitrate in progress, nothing to do")

    def runBitrate(self):
        if DBG:
            FhromaDEBUG("[Luka_FHD_Bitrate_BH:runBitrate] >>>")
        if isImageType("vti"):
            demux = 2
            adapter = 0
        else:
            adapter = 0
            demux = 0
        try:
            stream = self.source.service.stream()
            if stream:
                if DBG:
                    FhromaDEBUG("[Luka_FHD_Bitrate_BH:runBitrate] Collecting stream data...")
                streamdata = stream.getStreamingData()
                if streamdata:
                    demux = max(0, streamdata.get("demux", demux))
                    adapter = max(0, streamdata.get("adapter", adapter))
        except Exception as e:
            if DBG:
                FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:runBitrate] Exception collecting stream data: {e}")
        try:
            info = self.source.service.info()
            vpid = info.getInfo(iServiceInformation.sVideoPID)
            apid = info.getInfo(iServiceInformation.sAudioPID)
        except Exception as e:
            if DBG:
                FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:runBitrate] Exception collecting service info: {e}")
            return  # bitrate cannot be run without vpid and apid
        if vpid >= 0 and apid >= 0:
            if isImageType("vti"):
                cmd = f"killall -9 bitrate > /dev/null 2>&1;chmod 775 /usr/bin/bitrate; nice bitrate {demux} {vpid} {vpid}"
            else:
                cmd = f"killall -9 bitrate > /dev/null 2>&1;chmod 775 /usr/bin/bitrate; nice bitrate {adapter} {demux} {vpid} {vpid}"
            if DBG:
                FhromaDEBUG(f'[Luka_FHD_Bitrate_BH:runBitrate] starting "{cmd}"')
            self.container.execute(cmd)

    def clearValues(self, *args):  # invoked by appClosed & kill from suspend
        if DBG:
            FhromaDEBUG("[Luka_FHD_Bitrate_BH:clearValues] >>>")
        self.isRunning = False
        self.vmin = self.vmax = self.vavg = self.vcur = 0
        self.amin = self.amax = self.aavg = self.acur = 0
        self.remainingdata = ""
        self.datalines = []
        Converter.changed(self, (self.CHANGED_POLL,))

    def appClosed(self, retval):
        if DBG:
            FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:appClosed] >>> retval={retval}, isSuspended={self.isSuspended}")
        if self.isSuspended:
            self.clearValues()
        else:
            self.runTimer.start(100, True)

    def dataAvail(self, data_str):
        if DBG:
            FhromaDEBUG(f"[Luka_FHD_Bitrate_BH:dataAvail] >>> str '{data_str}'\n\tself.remainingdata='{self.remainingdata}'")
        data_str = self.remainingdata + data_str
        newlines = data_str.split("\n")
        if newlines[-1]:
            self.remainingdata = newlines[-1]
            newlines = newlines[:-1]
        else:
            self.remainingdata = ""
        for line in newlines:
            if line:
                self.datalines.append(line)

        if len(self.datalines) >= 2:
            try:
                self.vmin, self.vmax, self.vavg, self.vcur = [int(x) for x in self.datalines[0].split()]
                self.amin, self.amax, self.aavg, self.acur = [int(x) for x in self.datalines[1].split()]
            except Exception:
                pass
            self.datalines = []
            Converter.changed(self, (self.CHANGED_POLL,))
