# based on version by areq 2015-12-13 http://areq.eu.org/
# mod by Fhroma version 12.10.2018

from __future__ import absolute_import #zmiana strategii ladowanie modulow w py2 z relative na absolute jak w py3
from enigma import eConsoleAppContainer, eTimer, iServiceInformation, iPlayableService
from Components.Console import Console
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.PremiumComponents import isImageType, isPY2
import os

DBG = False
if DBG: from Components.PremiumComponents import PremiumDEBUG

class PremiumBitrate(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)        
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
        self.myConsole.ePopen('chmod 755 /usr/bin/bitrate')
    @cached
    def getText(self):
        if DBG: PremiumDEBUG("[PremiumBitrate:getText] vcur %s" % self.vcur)
        if self.vcur > 0:
            return '%d Kb/s' % self.vcur
        else:
            return ''

    text = property(getText)

    def doSuspend(self, suspended):
        if DBG: PremiumDEBUG("[PremiumBitrate:suspended] >>> self.isSuspended=%s, suspended=%s" % (self.isSuspended,suspended))
        if suspended == 0:
            self.isSuspended = False
            self.StartTimer.start(100, True)
        else:
            self.StartTimer.stop()
            self.isSuspended = True
            self.myConsole.ePopen('killall -9 bitrate', self.clearValues )

    def start(self):
        if self.isRunning == False:
            if self.source.service:
                if DBG: PremiumDEBUG("[PremiumBitrate:start] initiate runTimer")
                self.isRunning = True
                self.runTimer.start(100, True)
            else:
                if DBG: PremiumDEBUG("[PremiumBitrate:start] wait 100ms for self.source.service")
                self.StartTimer.start(100, True)
        else:
            if DBG: PremiumDEBUG("[PremiumBitrate:start] runBitrate in progress, nothing to do")

    def runBitrate(self):
        if DBG: PremiumDEBUG("[PremiumBitrate:runBitrate] >>>")
        if isImageType('vti'):
            demux = 2
        else:
            adapter = 0
            demux = 0
        try:
            stream = self.source.service.stream()
            if stream:
                if DBG: PremiumDEBUG("[PremiumBitrate:runBitrate] Collecting stream data...")
                streamdata = stream.getStreamingData()
                if streamdata:
                    if 'demux' in streamdata:
                        demux = streamdata['demux']
                        if demux < 0: demux = 0
                    if 'adapter' in streamdata:
                        adapter = streamdata["adapter"]
                        if adapter < 0: adapter = 0
        except Exception as e:
            if DBG: PremiumDEBUG("[PremiumBitrate:runBitrate] Exception collecting stream data: %s" % str(e))
        try:
            info = self.source.service.info()
            vpid = info.getInfo(iServiceInformation.sVideoPID)
            apid = info.getInfo(iServiceInformation.sAudioPID)
        except Exception as e:
            if DBG: PremiumDEBUG("[PremiumBitrate:runBitrate] Exception collecting service info: %s" % str(e))
            return #bitrate cannot be run without vpid and apid
        if vpid >= 0 and apid >= 0:
            if isImageType('vti'):
                cmd = 'killall -9 bitrate > /dev/null 2>&1; nice bitrate %i %i %i' % ( demux, vpid, vpid )
            else:
                cmd = 'killall -9 bitrate > /dev/null 2>&1;nice bitrate %i %i %i %i' % ( adapter, demux, vpid, vpid )
            if DBG: PremiumDEBUG('[PremiumBitrate:runBitrate] starting "%s"' % cmd)
            self.container.execute(cmd)
    
    def clearValues(self, *args): #invoked by appClosed & kill from suspend
        if DBG: PremiumDEBUG("[PremiumBitrate:clearValues] >>>")
        self.isRunning = False
        self.vmin = self.vmax = self.vavg = self.vcur = 0
        self.amin = self.amax = self.aavg = self.acur = 0
        self.remainingdata = ''
        self.datalines = []
        Converter.changed(self, (self.CHANGED_POLL,))

    def appClosed(self, retval):
        if DBG: PremiumDEBUG("[PremiumBitrate:appClosed] >>> retval=%s, isSuspended=%s" % (retval, self.isSuspended))
        if self.isSuspended == True:
            self.clearValues()
        else:
            self.runTimer.start(100, True)

    def dataAvail(self, conStr):
        if DBG: PremiumDEBUG("[PremiumBitrate:dataAvail] >>> conStr '%s'\n\tself.remainingdata='%s'" % (conStr,self.remainingdata))
        if isPY2():
            conStr = self.remainingdata + str(conStr)
        else:
            conStr = self.remainingdata + str(conStr, 'utf-8', 'ignore')
        newlines = conStr.split('\n')
        if len(newlines[-1]): #checks if last line contains any data, it will be used next time if so
            self.remainingdata = newlines[-1]
            newlines = newlines[0:-1]
        else:
            self.remainingdata = ''
        for line in newlines:
            if len(line):
                self.datalines.append(line)

        if len(self.datalines) >= 2:
            try:
                self.vmin, self.vmax, self.vavg, self.vcur = [int(x) for x in self.datalines[0].split(' ')]
                self.amin, self.amax, self.aavg, self.acur = [int(x) for x in self.datalines[1].split(' ')]
            except Exception:
                pass
            self.datalines = []
            Converter.changed(self, (self.CHANGED_POLL,))
