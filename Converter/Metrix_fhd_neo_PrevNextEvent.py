"""
=====================================================
 WIDGETS FÜR SKIN.XML (Lesehilfe)
=====================================================

<!-- Vorheriges Event anzeigen -->
<widget source="ServiceEvent" render="Label"
    position="50,50" size="600,30" font="Regular;20">
    <convert type="PrevNextEvent">PrevEvent</convert>
</widget>

<!-- Nächstes Event anzeigen -->
<widget source="ServiceEvent" render="Label"
    position="50,90" size="600,30" font="Regular;20">
    <convert type="PrevNextEvent">NextEvent</convert>
</widget>

<!-- Seite zurück -->
<widget source="ServiceEvent" render="Label"
    position="50,130" size="600,30" font="Regular;20">
    <convert type="PrevNextEvent">PagePrev</convert>
</widget>

<!-- Seite vor -->
<widget source="ServiceEvent" render="Label"
    position="50,170" size="600,30" font="Regular;20">
    <convert type="PrevNextEvent">PageNext</convert>
</widget>

=====================================================
"""

from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eEPGCache
from Screens.ChannelSelection import ChannelSelection

class Metrix_fhd_neo_PrevNextEvent(Converter):
    PREV_EVENT = 0
    NEXT_EVENT = 1
    PAGE_PREV = 2
    PAGE_NEXT = 3

    # Speichert die letzte Aktion global
    last_action = None

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {
            "PrevEvent": self.PREV_EVENT,
            "NextEvent": self.NEXT_EVENT,
            "PagePrev": self.PAGE_PREV,
            "PageNext": self.PAGE_NEXT,
        }.get(type, self.PREV_EVENT)

        # Hook nur einmal einbauen
        if not hasattr(ChannelSelection, "_prevnextevent_hooked"):
            self._patch_ChannelSelection()
            ChannelSelection._prevnextevent_hooked = True

    def _patch_ChannelSelection(self):
        """
        Hooked die ChannelSelection-Methoden, damit Widgets
        sofort aktualisiert werden, wenn seekBack/seekFwd usw. gedrückt werden.
        """
        orig_prev = ChannelSelection.setPrevEvent
        orig_next = ChannelSelection.setNextEvent
        orig_pageprev = ChannelSelection.setPrevPage
        orig_pagenext = ChannelSelection.setNextPage

        def new_prev(self_):
            PrevNextEvent.last_action = "PrevEvent"
            orig_prev(self_)
            if "ServiceEvent" in self_:
                self_["ServiceEvent"].changed()

        def new_next(self_):
            PrevNextEvent.last_action = "NextEvent"
            orig_next(self_)
            if "ServiceEvent" in self_:
                self_["ServiceEvent"].changed()

        def new_pageprev(self_):
            PrevNextEvent.last_action = "PagePrev"
            orig_pageprev(self_)
            if "ServiceEvent" in self_:
                self_["ServiceEvent"].changed()

        def new_pagenext(self_):
            PrevNextEvent.last_action = "PageNext"
            orig_pagenext(self_)
            if "ServiceEvent" in self_:
                self_["ServiceEvent"].changed()

        ChannelSelection.setPrevEvent = new_prev
        ChannelSelection.setNextEvent = new_next
        ChannelSelection.setPrevPage = new_pageprev
        ChannelSelection.setNextPage = new_pagenext

    @cached
    def getText(self):
        """
        Gibt den passenden Text oder Eventtitel zurück
        """
        service = self.source.service
        epg = eEPGCache.getInstance()

        if not service:
            return ""

        if self.type == self.PREV_EVENT:
            ev = epg.lookupEventTime(service, -1)
            return ev and ev.getEventName() or "<< Vorheriges Event"
        elif self.type == self.NEXT_EVENT:
            ev = epg.lookupEventTime(service, -1, 1)
            return ev and ev.getEventName() or "Nächstes Event >>"
        elif self.type == self.PAGE_PREV:
            return "<< Seite zurück"
        elif self.type == self.PAGE_NEXT:
            return "Seite vor >>"

        return ""

    text = property(getText)
