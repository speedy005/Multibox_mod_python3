from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eEPGCache, eServiceReference
from time import localtime, strftime, mktime, time
from datetime import datetime


class iNextEvents(Converter, object):
    Event1 = 0
    Event2 = 1
    Event3 = 2
    PrimeTime = 3
    noDuration = 10
    onlyDuration = 11
    withDuration = 12
    onlyStart = 13

    def __init__(self, type):
        Converter.__init__(self, type)
        self.epgcache = eEPGCache.getInstance()
        args = type.split(',')
        if len(args) != 2:
            print('type must contain exactly 2 arguments')
        type = args.pop(0)
        showDuration = args.pop(0)
        if type == 'Event2':
            self.type = self.Event2
        elif type == 'Event3':
            self.type = self.Event3
        elif type == 'PrimeTime':
            self.type = self.PrimeTime
        else:
            self.type = self.Event1
        if showDuration == 'noDuration':
            self.showDuration = self.noDuration
        elif showDuration == 'onlyDuration':
            self.showDuration = self.onlyDuration
        elif showDuration == 'onlyStart':
            self.showDuration = self.onlyStart
        else:
            self.showDuration = self.withDuration

    @cached
    def getText(self):
        ref = self.source.service
        info = ref and self.source.info
        if info is None:
            return ''
        else:
            textvalue = ''
            if self.type < self.PrimeTime:
                curEvent = self.source.getCurrentEvent()
                if curEvent:
                    self.epgcache.startTimeQuery(eServiceReference(ref.toString()), curEvent.getBeginTime() + curEvent.getDuration())
                    nextEvents = []
                    for i in range(self.type):
                        self.epgcache.getNextTimeEntry()

                    next = self.epgcache.getNextTimeEntry()
                    if next:
                        textvalue = self.formatEvent(next)
            elif self.type == self.PrimeTime:
                curEvent = self.source.getCurrentEvent()
                if curEvent:
                    now = localtime(time())
                    dt = datetime(now.tm_year, now.tm_mon, now.tm_mday, 21, 15)
                    primeTime = int(mktime(dt.timetuple()))
                    self.epgcache.startTimeQuery(eServiceReference(ref.toString()), primeTime)
                    next = self.epgcache.getNextTimeEntry()
                    if next and next.getBeginTime() <= int(mktime(dt.timetuple())):
                        textvalue = self.formatEvent(next)
            return textvalue

    text = property(getText)

    def formatEvent(self, event):
        begin = strftime('%H:%M', localtime(event.getBeginTime()))
        end = strftime('%H:%M', localtime(event.getBeginTime() + event.getDuration()))
        title = event.getEventName()
        duration = '%d min' % (event.getDuration() / 60)

        if self.showDuration == self.withDuration:
            f = '{begin} - {end} - {title:<} - {duration}'
            return f.format(begin=begin, end=end, title=title, duration=duration)

        elif self.showDuration == self.onlyStart:
            f = '{begin} - {title:<}'
            return f.format(begin=begin, title=title)

        elif self.showDuration == self.noDuration:
            f = '{begin} - {end} - {title:<}'
            return f.format(begin=begin, end=end, title=title)

        elif self.showDuration == self.onlyDuration:
            f = '{title:<} - {duration}'
            return f.format(title=title, duration=duration)

        else:
            return ''
