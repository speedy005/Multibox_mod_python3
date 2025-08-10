from Renderer import Renderer
from enigma import eLabel, eServiceCenter
from Components.VariableText import VariableText


class Skyline_Pids(VariableText, Renderer):
    GUI_WIDGET = eLabel

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))

    def getServiceRef(self):
        # Versucht, die Service-Referenz zu bekommen
        service = None
        if hasattr(self.source, "service"):
            service = self.source.service
        elif hasattr(self.source, "getCurrentService"):
            # z.B. bei ServiceEvent
            svc = self.source.getCurrentService()
            if svc:
                service = svc
        return service

    def changed(self, what):
        if not self.instance:
            return

        if what[0] == self.CHANGED_CLEAR:
            self.text = " "
            return

        service = self.getServiceRef()
        if not service:
            self.text = "[kein Service]"
            return

        info = eServiceCenter.getInstance().info(service)
        if not info:
            self.text = "[kein Info]"
            return

        refstr = str(service.toString())
        curref = refstr.replace("%3a", ":")

        try:
            if curref.startswith("1:7:"):
                self.text = ""
                return
            if "%3a/" in refstr:
                self.text = "[keine Daten]"
                return

            ids = refstr.split(":")
            if len(ids) < 6:
                self.text = "[unvollständig]"
                return

            sid = f"SID:{int(ids[3], 16)} ({ids[3]})"
            tsid = f"TSID:{int(ids[4], 16)} ({ids[4]})"
            onid = f"ONID:{int(ids[5], 16)} ({ids[5]})"
            self.text = f"{sid} {tsid} {onid}"

        except Exception as e:
            self.text = f"[Fehler: {e}]"
