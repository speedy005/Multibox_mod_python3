#================ ECMInfo =============
# by MyFriendVTI
# Edit by Bueb
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Poll import Poll
from Tools.Directories import resolveFilename, SCOPE_SYSETC
import NavigationInstance

class xDreamy_ECMInfo(Poll, Converter, object):
	
	def __init__(self, args):
		Poll.__init__(self)
		Converter.__init__(self, args)
		self.poll_interval = 2000
		self.poll_enabled = True
		
		self.showFTA = False
		self.inputStr = ""
		
		argarr = args.split(",")
		
		self.inputStr = argarr[0]
		if len(argarr) > 1 and "showFTA" in argarr[1]:
			self.showFTA = True

	@cached
	def getText(self):
		output = ""
		isIPTV = False
		service = self.source.service
		
		if service:
			info = service and service.info()
			if not info:
				return "No service available"
			
			#IPTV-Check
			if self.showFTA:
				isIPTV = self.isIPTV()
				
			#FTA-Check
			if not info.getInfo(iServiceInformation.sIsCrypted) == 1 and self.showFTA == True:
				if isIPTV == False:
					hdmiIN = False
					try:
						if "HDMI IN" in info.getName():
							hdmiIN = True
					except:
						pass
					if not hdmiIN:
						return "Channel is Free-TV "
					else:
						return "HDMI IN"
				else:
					return "IPTV-Stream"
		
			#ECM-Info
			output_ecmInfo = ""
			if "#ECM" in self.inputStr and info.getInfoObject(iServiceInformation.sCAIDs):
				ecm_info = self.ecmfile()
				if ecm_info:
					
					#--------------- CAID -----------------
					caid_val = ecm_info.get('caid', '')
					caid_val = caid_val.lstrip('0x')
					caid_val = caid_val.upper()
					caid_val = caid_val.zfill(4)
					caid = "CAID: " + str(caid_val)
					
					#--------------- system -----------------
					system = ""
					if ((caid_val>='1800') and (caid_val<='18FF')):
						system = "NAGRA"
					elif ((caid_val>='1700') and (caid_val<='17FF')):
						system = "BETA"
					elif ((caid_val>='0E00') and (caid_val<='0EFF')):
						system = "POWERVU"
					elif ((caid_val>='0D00') and (caid_val<='0DFF')):
						system = "CWORKS"
					elif ((caid_val>='0B00') and (caid_val<='0BFF')):
						system = "CONAX"
					elif ((caid_val>='0900') and (caid_val<='09FF')):
						system = "NDS"
					elif ((caid_val>='0600') and (caid_val<='06FF')):
						system = "IRDETO"
					elif ((caid_val>='0500') and (caid_val<='05FF')):
						system = "VIACCESS"
					elif ((caid_val>='0100') and (caid_val<='01FF')):
						system = "SECA"
					elif ((caid_val>='2600') and (caid_val<='26FF')):
						system = "BISS"

					#--------------- hops -----------------
					hops = ecm_info.get('hops', "")
					if hops: hops = 'HOPS: %s' % hops
						
					#--------------- ecm_time -----------------
					ecm_time = ecm_info.get('ecm time', "")
					if ecm_time:
						if not 'msec' in ecm_time and "." in ecm_time:
							ecm_time = 'TIME: %s s' % ecm_time
						else:
							ecm_time = 'TIME: %s ms' % ecm_time
							
					#--------------- address -----------------
					address = str(ecm_info.get('address',""))
					if address == "/dev/sci0":
						address = "Slot #1"
					if address == "/dev/sci1":
						address = "Slot #2"
					#--------------- source -----------------
					source = str(ecm_info.get('source',""))
					#--------------- reader -----------------
					reader = str(ecm_info.get('reader',""))
					#--------------- oscsource -----------------
					oscsource = ecm_info.get('from', "")
					#--------------- decode -----------------
					decode = str(ecm_info.get('decode',""))
					#--------------- using -----------------
					using = str(ecm_info.get('using', ""))
					
					#--------------- provInfo -----------------
					paddress = slot = level = dist = ""
					prov_info = None
					prov = ecm_info.get("prov", "")
					if prov: 
						prov = prov[0:4]
						prov_info = self.provfile(prov, caid_val)
					if prov_info:
						paddress = prov_info.get("paddress", "")
						slot = prov_info.get("slot", "")
						level = prov_info.get("level", "")
						dist = prov_info.get("distance", "")
					if prov: prov = "Prov: " + str(prov)
					if slot: slot = "SL: " + str(slot)
					if level: level = "Lev: " + str(level)
					if dist: dist = "Dist: " + str(dist)
					
					#+++++++++++++++++ ecmInfo_list +++++++++++++++++
					ecmInfo_list = []
					if source == 'emu':
						ecmInfo_list = [caid,system]
					
					elif using:
						if using == 'emu':
							ecmInfo_list = [caid,system,ecm_time]
						elif using == 'CCcam-s2s':
							ecmInfo_list = [caid,system,address,hops,ecm_time]
						else:
							ecmInfo_list = [caid,system,address,hops,ecm_time]
							
					elif oscsource:
						ecmInfo_list = [caid,system,reader,address,hops,ecm_time]
					
					elif decode:
						if decode == "Network":
							ecmInfo_list = [caid,system,decode,ecm_time, prov,slot,level,dist]
						else:
							ecmInfo_list = [caid,system, decode, ecm_time]
							
					else:
						ecmInfo_list = [caid,system,ecm_time]
					
					#+++++++++++++++++ output_ecmInfo +++++++++++++++++	
					if len(ecmInfo_list) > 0:
						output_ecmInfo = " - ".join(x for x in ecmInfo_list if x)	
									
					
			#CAM-Info
			output_camInfo = ""
			if "#CAM" in self.inputStr:
				camInfo = self.getCamInfo()
				if camInfo:
					output_camInfo = camInfo
					
			#output
			if "#ECM" in self.inputStr and "#CAM" in self.inputStr:
				if output_ecmInfo and output_camInfo:
					output = self.inputStr
					output = output.replace("#ECM",output_ecmInfo)
					output = output.replace("#CAM",output_camInfo)
				elif output_ecmInfo:
					output = output_ecmInfo
				#elif output_camInfo:
					#output = output_camInfo
			elif "#ECM" in self.inputStr:
				output = output_ecmInfo
			elif "#CAM" in self.inputStr:
				output = output_camInfo
				
				
			#No ECM/CAM-Info
			if self.showFTA and not output:
				if not isIPTV:
					output = "Channel is crypted"
				else:
					output = "IPTV-Stream is crypted"
				
		return output

	text = property(getText)


	def ecmfile(self):
		ecm = None
		info = {}
		service = self.source.service
		if service:
			try:
				ecmopenfile = open('/tmp/ecm.info', 'rb')
				ecm = ecmopenfile.readlines()
				ecmopenfile.close()
			except:
				return info

			if ecm:
				for line in ecm:
					#ecm time
					x = line.lower().find('msec')
					if x != -1:
						info['ecm time'] = line[0:x + 4]
					elif line.lower().find("response:") != -1:
						y = line.lower().find("response:")
						if y != -1:
							info["ecm time"] = line[y+9:].strip("\n\r")
					#caid
					else:
						item = line.split(':', 1)
						if len(item) > 1:
							info[item[0].strip().lower()] = item[1].strip()
						elif not info.has_key('caid'):
							x = line.lower().find('caid')
							if x != -1:
								y = line.find(',')
								if y != -1:
									info['caid'] = line[x + 5:y]

		return info
		
	def provfile(self, prov, caid):
		provider = None
		pinfo = {}
		try:
			provider = open("/tmp/share.info", "rb").readlines()
		except: pass
		
		if provider:
			for line in provider:
				x = line.lower().find("id:")
				y = line.lower().find("card ")
				if x != -1 and y != -1:
					if caid != "0500":
						if line[x+3:].strip("\n\r") == prov.strip("\n\r") and line[y+5:y+9] == caid:
							x = line.lower().find("at ")
							if x != -1:
								y = line.lower().find("card ")
								if y != -1:
									pinfo["paddress"] = line[x+3:y-1]
								x = line.lower().find("sl:")
								if x != -1:
									y = line.lower().find("lev:")
									if y != -1:
										pinfo["slot"] = line[x+3:y-1]
										x = line.lower().find("dist:")
										if x != -1:
											pinfo["level"] = line[y+4:x-1]
											y = line.lower().find("id:")
											if y != -1:
												pinfo["distance"] = line[x+5:y-1]
					elif line[x+3:].strip("\n\r") == prov.strip("\n\r") and line[y+5:y+8] == caid[:-1]:
							x = line.lower().find("at ")
							if x != -1:
								y = line.lower().find("card ")
								if y != -1:
									pinfo["paddress"] = line[x+3:y-1]
								x = line.lower().find("sl:")
								if x != -1:
									y = line.lower().find("lev:")
									if y != -1:
										pinfo["slot"] = line[x+3:y-1]
										x = line.lower().find("dist:")
										if x != -1:
											pinfo["level"] = line[y+4:x-1]
											y = line.lower().find("id:")
											if y != -1:
												pinfo["distance"] = line[x+5:y-1]
		return pinfo
		
	def getCamInfo(self):
		ret = ""
		try:
			file = open(resolveFilename(SCOPE_SYSETC, '/tmp/.emu.info'), 'r')
			emuversion = file.readline()
			file.close()
			ret = emuversion.replace("\n","")
		except:
			pass
			
		return ret
		
	def isIPTV(self):
		ref = ""
		try:
			if NavigationInstance.instance:
				navref = NavigationInstance.instance.getCurrentlyPlayingServiceReference()
				if navref:
					ref = navref.toString()
		except:
			pass

		if "http" in ref:
			return True
		else:
			return False


	def changed(self, what):
		if (what[0] == self.CHANGED_SPECIFIC and (what[1] == iPlayableService.evUpdatedInfo or what[1] == iPlayableService.evVideoSizeChanged)) or what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)