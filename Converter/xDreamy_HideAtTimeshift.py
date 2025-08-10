#================ ObelixFHD_HideAtTimeshift =============

from Components.Converter.Converter import Converter
from Components.Element import cached
from Screens.InfoBar import InfoBar
import skin

class xDreamy_HideAtTimeshift(Converter, object):
	def __init__(self, args):
		Converter.__init__(self, args)
		self.TimeshiftState = None
		if skin.parameters.get("InfobarHeadBar_HideAtTimeshift", (0,))[0] == 0:
			return
		if InfoBar and InfoBar.instance and InfoBar.instance.pvrStateDialog:
			self.TimeshiftState = InfoBar.instance.pvrStateDialog
			self.TimeshiftState.onShow.append(self.timeShiftStateShow)
			self.TimeshiftState.onHide.append(self.timeShiftStateHide)
			
	@cached
	def getText(self):
		
		return self.source.text
		
	text = property(getText)
	
	@cached
	def getBoolean(self):
		
		return self.source.boolean

	boolean = property(getBoolean)
	
	@cached
	def getPixmap(self):
		
		return self.source.pixmap
	
	pixmap = property(getPixmap)
	
	
	def timeShiftStateShow(self):
		for element in self.downstream_elements:
			element.visible = False
			
	def timeShiftStateHide(self):
		for element in self.downstream_elements:
			element.visible = True

		
	
	
# =========================================================
