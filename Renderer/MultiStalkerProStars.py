# by digiteng
# v1 07.2020

# <ePixmap pixmap="xtra/star_b.png" position="560,367" size="200,20" alphatest="blend" zPosition="2" transparent="1" />
# <widget render="xtraStar" source="session.Event_Now" pixmap="xtra/star.png" position="560,367" size="200,20" alphatest="blend" transparent="1" zPosition="3" />

from Components.VariableValue import VariableValue
from Components.Renderer.Renderer import Renderer
from enigma import eSlider


class MultiStalkerProStars(VariableValue, Renderer):
    def __init__(self):
        Renderer.__init__(self)
        VariableValue.__init__(self)
        self.__start = 0
        self.__end = 100

    GUI_WIDGET = eSlider

    def changed(self, what):
        rtng = 0
        if what[0] == self.CHANGED_CLEAR:
            (self.range, self.value) = ((0, 1), 0)
            return
        elif self.source:
            if hasattr(self.source, "text"):
                film_rating = self.source.text
                try:
                    rtng = int(10 * (float(film_rating)))
                except BaseException:
                    pass
        range = 100
        value = rtng

        (self.range, self.value) = ((0, range), value)

    def postWidgetCreate(self, instance):
        instance.setRange(self.__start, self.__end)

    def setRange(self, range):
        (self.__start, self.__end) = range
        if self.instance is not None:
            self.instance.setRange(self.__start, self.__end)

    def getRange(self):
        return self.__start, self.__end

    range = property(getRange, setRange)
