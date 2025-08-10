from Components.VariableText import VariableText
from Components.Renderer.Renderer import Renderer
from enigma import (
    eLabel, ePoint, eSize,
    RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_HALIGN_BLOCK,
    RT_VALIGN_TOP, RT_VALIGN_CENTER, RT_VALIGN_BOTTOM,
    RT_WRAP
)
from skin import parseColor, parseFont


class MetrixCurveFHDLabel(VariableText, Renderer):
    GUI_WIDGET = eLabel

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.test_label = None
        self.txtflags = 0
        self.W = self.H = 0
        self.txfont = None
        self.fcolor = None
        self.bcolor = None
        self.halign = eLabel.alignLeft

    def connect(self, source):
        if source:
            Renderer.connect(self, source)
            self.changed((self.CHANGED_DEFAULT,))
        else:
            self.text = '<no-source>'
            print('SKINERROR: render label has no source')

    def changed(self, what):
        if not self.instance:
            return

        if what[0] == self.CHANGED_CLEAR:
            self.text = ''
        elif self.source and hasattr(self.source, 'text'):
            title = str(self.source.text)

            if self.test_label:
                self.test_label.setText(title)
                text_size = self.test_label.calculateSize()

                if text_size.width() > self.W:
                    i = -1
                    while True:
                        truncated = f"{title[:i]}..."
                        self.test_label.setText(truncated)
                        if self.test_label.calculateSize().width() < self.W or abs(i) > len(title):
                            title = truncated
                            break
                        i -= 1

            self.text = title
        else:
            self.text = '<no-source>'
            print('SKINERROR: render label has no source')

    def postWidgetCreate(self, instance):
        self.test_label = eLabel(instance)

    def applySkin(self, desktop, screen):
        self.halign = eLabel.alignLeft
        valign = eLabel.alignTop

        if self.skinAttributes:
            attribs = []
            for attrib, value in self.skinAttributes:
                match attrib:
                    case 'size':
                        x, y = map(int, value.split(','))
                        self.W, self.H = x, y
                    case 'font':
                        self.txfont = parseFont(value, ((1, 1), (1, 1)))
                    case 'foregroundColor':
                        self.fcolor = parseColor(value)
                    case 'backgroundColor':
                        self.bcolor = parseColor(value)
                    case 'valign' if value in ('top', 'center', 'bottom'):
                        valign_map = {
                            'top': (eLabel.alignTop, RT_VALIGN_TOP),
                            'center': (eLabel.alignCenter, RT_VALIGN_CENTER),
                            'bottom': (eLabel.alignBottom, RT_VALIGN_BOTTOM),
                        }
                        valign, flag = valign_map[value]
                        self.txtflags |= flag
                    case 'halign' if value in ('left', 'center', 'right', 'block'):
                        halign_map = {
                            'left': (eLabel.alignLeft, RT_HALIGN_LEFT),
                            'center': (eLabel.alignCenter, RT_HALIGN_CENTER),
                            'right': (eLabel.alignRight, RT_HALIGN_RIGHT),
                            'block': (eLabel.alignBlock, RT_HALIGN_BLOCK),
                        }
                        self.halign, flag = halign_map[value]
                        self.txtflags |= flag
                    case 'noWrap':
                        if value == '0':
                            self.txtflags |= RT_WRAP
                        else:
                            self.txtflags &= ~RT_WRAP

                if attrib != 'animated':
                    attribs.append((attrib, value))
            self.skinAttributes = attribs

        ret = Renderer.applySkin(self, desktop, screen)

        if self.test_label and self.txfont:
            self.test_label.setFont(self.txfont)
        if self.test_label:
            if not self.txtflags & RT_WRAP:
                self.test_label.setNoWrap(1)
            self.test_label.setVAlign(valign)
            self.test_label.setHAlign(self.halign)
            self.test_label.move(ePoint(self.W, self.H))
            self.test_label.resize(eSize(self.W, self.H))
            self.test_label.hide()

        return ret

    def onShow(self):
        self.suspended = False

    def onHide(self):
        self.suspended = True

    def preWidgetRemove(self, instance):
        self.test_label = None
