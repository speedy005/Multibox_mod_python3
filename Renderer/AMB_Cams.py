# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/blueCams.py
from Renderer import Renderer
from enigma import ePixmap, ePicLoad, iServiceInformation
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.Converter.Poll import Poll

class AMB_Cams(Renderer, Poll):

    def __init__(self):
        Poll.__init__(self)
        Renderer.__init__(self)
        self.nameCache = {}
        self.pngname = ''
        self.path = 'usr/share/enigma2/name_skin/test/crypt/'

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        self.poll_interval = 2000
        self.poll_enabled = True
        sname = 'Unknown'
        caid = ''
        cfgfile = '/tmp/ecm.info'
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                if service:
                    info = service and service.info()
                    if info:
                        caids = info.getInfoObject(iServiceInformation.sCAIDs)
                        try:
                            f = open(cfgfile, 'r')
                            content = f.read()
                            f.close()
                        except:
                            content = ''

                        if len(caids) > 0 and content == '':
                            for caid in caids:
                                if ('%0.4X' % int(caid))[:2] == '26':
                                    sname = 'BISS'
                                elif ('%0.4X' % int(caid))[:2] == '01':
                                    sname = 'SECA MEDIAGUARD'
                                elif ('%0.4X' % int(caid))[:2] == '06':
                                    sname = 'IRDETO'
                                elif ('%0.4X' % int(caid))[:2] == '17':
                                    sname = 'BETACRYPT'
                                elif ('%0.4X' % int(caid))[:2] == '05':
                                    sname = 'Viacces'
                                elif ('%0.4X' % int(caid))[:2] == '18':
                                    sname = 'NAGRAVISION'
                                elif ('%0.4X' % int(caid))[:2] == '09':
                                    sname = 'NDS-VIDEOGUARD'
                                elif ('%0.4X' % int(caid))[:2] == '0B':
                                    sname = 'CONAX'
                                elif ('%0.4X' % int(caid))[:2] == '0D':
                                    sname = 'CRYPTOWORKS'
                                elif ('%0.4X' % int(caid))[:2] == '4A':
                                    sname = 'DRE-Crypt'
                                elif ('%0.4X' % int(caid))[:2] == '7B':
                                    sname = 'DRE-Crypt'
                                elif ('%0.4X' % int(caid))[:2] == '27':
                                    sname = 'EXSET'
                                elif ('%0.4X' % int(caid))[:2] == '10':
                                    sname = 'TANDBERG'
                                elif ('%0.4X' % int(caid))[:2] == '56':
                                    sname = 'VERIMATRIX'

                        elif len(caids) > 0 and content != '':
                            contentInfo = content.split('\n')
                            for line in contentInfo:
                                if line.startswith('caid:'):
                                    caid = self.parseEcmInfoLine(line)
                                    if caid.__contains__('x'):
                                        idx = caid.index('x')
                                        caid = caid[idx + 1:]
                                        if len(caid) == 3:
                                            caid = '0%s' % caid
                                        caid = caid[:2]
                                        caid = caid.upper()
                                        if caid == '26':
                                            sname = 'BISS'
                                        elif caid == '01':
                                            sname = 'SECA MEDIAGUARD'
                                        elif caid == '06':
                                            sname = 'IRDETO'
                                        elif caid == '17':
                                            sname = 'BETACRYPT'
                                        elif caid == '05':
                                            sname = 'Viacces'
                                        elif caid == '18':
                                            sname = 'NAGRAVISION'
                                        elif caid == '09':
                                            sname = 'NDS-VIDEOGUARD'
                                        elif caid == '0B':
                                            sname = 'CONAX'
                                        elif caid == '0D':
                                            sname = 'CRYPTOWORKS'
                                        elif caid == '4A' or caid == '7B':
                                            sname = 'DRE-Crypt'
                                        elif caid == '27':
                                            sname = 'EXSET'
                                        elif caid == '0E':
                                            sname = 'POWERVU'
                                        elif caid == '10':
                                            sname = 'TANDBERG'
                                        elif caid == '56':
                                            sname = 'VERIMATRIX'
                                elif line.startswith('=====') or line.startswith('CAID') or line.startswith('***'):
                                    caid = self.parseInfoLine(line)
                                    if caid.__contains__('x'):
                                        idx = caid.index('x')
                                        caid = caid[idx + 1:]
                                        caid = caid[:2]
                                        caid = caid.upper()
                                        if caid == '26':
                                            sname = 'BISS'
                                        elif caid == '01':
                                            sname = 'SECA MEDIAGUARD'
                                        elif caid == '06':
                                            sname = 'IRDETO'
                                        elif caid == '17':
                                            sname = 'BETACRYPT'
                                        elif caid == '05':
                                            sname = 'Viacces'
                                        elif caid == '18':
                                            sname = 'NAGRAVISION'
                                        elif caid == '09':
                                            sname = 'NDS-VIDEOGUARD'
                                        elif caid == '0B':
                                            sname = 'CONAX'
                                        elif caid == '0D':
                                            sname = 'CRYPTOWORKS'
                                        elif caid == '4A' or caid == '7B':
                                            sname = 'DRE-Crypt'
                                        elif caid == '27':
                                            sname = 'EXSET'
                                        elif caid == '0E':
                                            sname = 'POWERVU'
                                        elif caid == '10':
                                            sname = 'TANDBERG'
                                        elif caid == '56':
                                            sname = 'VERIMATRIX'

                        elif caids is None and content != '':
                            sname = 'Fta'
                        else:
                            sname = 'Fta'
                    works = True
                    if works == True:
                        pngname = self.nameCache.get(sname, '')
                        if pngname == '':
                            pngname = self.findPicon(sname)
                            if pngname != '':
                                self.nameCache[sname] = pngname
                        if pngname == '':
                            pngname = self.nameCache.get(sname, '')
                            if pngname == '':
                                pngname = self.findPicon(sname)
                                if pngname == '':
                                    tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'Crypt.png')
                                    if fileExists(tmp):
                                        pngname = tmp
                                    else:
                                        pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'usr/share/enigma2/Multibox/test/crypt/Crypt.png')
                                self.nameCache['default'] = pngname
                        if self.pngname != pngname:
                            self.pngname = pngname
                            self.instance.setScale(1)
                            self.instance.setPixmapFromFile(pngname)
        return

    def parseEcmInfoLine(self, line):
        if line.__contains__(':'):
            idx = line.index(':')
            line = line[idx + 1:]
            line = line.replace('\n', '')
            while line.startswith(' '):
                line = line[1:]

            while line.endswith(' '):
                line = line[:-1]

            return line
        else:
            return ''

    def parseInfoLine(self, line):
        if line.__contains__('CaID') or line.__contains__('CAID'):
            idx = line.index('D')
            line = line[idx + 1:]
            line = line.replace('\n', '')
            while line.startswith(' '):
                line = line[1:]

            while line.endswith(' '):
                line = line[:-1]

            return line
        else:
            return ''

    def findPicon(self, serviceName):
        if serviceName:
            pngname = self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname
        return ''