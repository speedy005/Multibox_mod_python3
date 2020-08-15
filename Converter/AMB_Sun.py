# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Sun.py
from Components.Converter.Converter import Converter
from Components.Element import cached
import math
import datetime
from datetime import date

class AMB_Sun(Converter, object):
    WSCHOD = 0
    ZACHOD = 1
    SZCZYT = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'wschod':
            self.type = self.WSCHOD
        elif type == 'zachod':
            self.type = self.ZACHOD
        elif type == 'szczyt':
            self.type = self.SZCZYT

    @cached
    def getDane(self):
        import linecache
        wer2 = linecache.getline('/etc/pozycjageo', 2)
        dlu = float(wer2[5:])
        wer3 = linecache.getline('/etc/pozycjageo', 3)
        szer = float(wer3[5:])
        wer4 = linecache.getline('/etc/pozycjageo', 4)
        ST = float(wer4[8:])
        rok = datetime.date.today().year
        miesiac = datetime.date.today().month
        dzien = datetime.date.today().day
        pi = 3.14159265359
        N3 = pi / 180
        D5 = rok
        D6 = miesiac
        D7 = dzien
        if D6 <= 2:
            E6 = D6 + 12
            E7 = D5 - 1
        else:
            E6 = D6
            E7 = D5
        L5 = int(D5 / 100)
        L6 = 2 - L5 + int(L5 / 4)
        L7 = int(365.25 * (E7 + 4716)) + int(30.6001 * (E6 + 1)) + D7 + L6 - 1524.5
        M3 = (L7 - 2451545) / 36525
        M4 = 280.46646 + 36000.76983 * M3 + 0.0003032 * M3 * M3
        O3 = 57.29577951
        M5 = 357.52911 + 35999.05029 * M3 - 0.0001537 * M3 * M3
        N5 = M5 / 360
        O5 = (N5 - int(N5)) * 360
        M6 = (1.914602 - 0.004817 * M3 - 1.4e-05 * M3 * M3) * math.sin(O5 * N3)
        M7 = (0.019993 - 0.000101 * M3) * math.sin(2 * O5 * N3)
        M8 = 0.000289 * math.sin(3 * O5 * N3)
        M9 = M6 + M7 + M8
        N4 = M4 / 360
        O4 = (N4 - int(N4)) * 360
        N6 = O4 + M9
        N7 = 125.04 - 1934.136 * M3
        if N7 < 0:
            N9 = N7 + 360
        else:
            N9 = N7
        N10 = N6 - 0.00569 - 0.00478 * math.sin(N9 * N3)
        M11 = 23.43930278 - 0.0130042 * M3 - 1.63e-07 * M3 * M3
        N11 = math.sin(M11 * N3) * math.sin(N10 * N3)
        N12 = math.asin(N11) * 180 / pi
        N15 = dlu / 15
        O15 = szer
        M13 = (7.7 * math.sin((O4 + 78) * N3) - 9.5 * math.sin(2 * O4 * N3)) / 60
        O16 = math.cos(N12 * N3) * math.cos(O15 * N3)
        N16 = -0.01483 - math.sin(N12 * N3) * math.sin(O15 * N3)
        P15 = 2 * (math.acos(N16 / O16) * O3) / 15
        P17 = 13 - N15 + M13 - P15 / 2
        Wh = int(P17 + ST)
        Wm = int(round((P17 + ST - Wh) * 60))
        if Wm == 60:
            Wm = 0
            Wh = Wh + 1
        if Wm < 10:
            Wa = '0'
        else:
            Wa = ''
        R18 = 13 - N15 + M13
        Gh = int(R18 + ST)
        Gm = int(round((R18 + ST - Gh) * 60))
        if Gm == 60:
            Gm = 0
            Gh = Gh + 1
        if Gm < 10:
            Ga = '0'
        else:
            Ga = ''
        Q17 = 13 - N15 + M13 + P15 / 2
        Zh = int(Q17 + ST)
        Zm = int(round((Q17 + ST - Zh) * 60))
        if Zm == 60:
            Zm = 0
            Zh = Zh + 1
        if Zm < 10:
            Za = '0'
        else:
            Za = ''
        if self.type == self.WSCHOD:
            return str(Wh) + ':' + Wa + str(Wm)
        if self.type == self.ZACHOD:
            return str(Zh) + ':' + Za + str(Zm)
        if self.type == self.SZCZYT:
            return str(Gh) + ':' + Ga + str(Gm)

    text = property(getDane)