# Bitrate3.py
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, eServiceReference, eConsoleAppContainer
from Components.Element import cached
from Components.Converter.Poll import Poll


class iBitrate3(Poll, Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 500
        self.poll_enabled = True
        self.container = eConsoleAppContainer()
        self.type = self.retval = type
        self.container.dataAvail.append(self.dataAvail)

    def dataAvail(self, str):
        try:
            str = str.decode()
            print(str)
            video, audio = str.split(' ')
            self.retval = self.type.replace('%A', '%s' % audio[:-1]).replace('%V', '%s' % video)
            print(self.retval)
        except Exception as e:
            print('error converte bitrate3', e)

    @cached
    def getText(self):
        service = self.source.service
        vpid = apid = dvbnamespace = tsid = onid = -1
        if service:
            serviceInfo = service.info()
            vpid = serviceInfo.getInfo(iServiceInformation.sVideoPID)
            apid = serviceInfo.getInfo(iServiceInformation.sAudioPID)
            adapter = 0
            demux = 0
            try:
                stream = service.stream()
                if stream:
                    streamdata = stream.getStreamingData()
                    if streamdata:
                        if 'demux' in streamdata:
                            demux = streamdata['demux']
                        if 'adapter' in streamdata:
                            adapter = streamdata['adapter']
            except:
                pass

            cmd = '/usr/bin/opbitrate ' + str(adapter) + ' ' + str(demux) + ' ' + str(vpid) + ' ' + str(apid)
            print(cmd)
            self.container.execute(cmd)
        return self.retval

    text = property(getText)
