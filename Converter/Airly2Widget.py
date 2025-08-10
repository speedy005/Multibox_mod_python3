# -*- coding: utf-8 -*-
#							  Airly
#					Based on http://map.airly.org
#							 2.0-r6
#
#    Copyright (C) 2023  Ampersand
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.config import config
from Components.Element import cached
from Tools.Directories import fileExists
from enigma import eTimer
import os
import datetime

if os.path.exists("/tmp/Airly") is False:
	try:
		os.makedirs("/tmp/Airly", 755)
	except:
		pass

TMP_PATH = "/tmp/Airly"


class Airly2Widget(Poll, Converter, object):
	PM1 = 1
	PM25 = 2
	PM10 = 3
	PRES = 4
	HUM = 5
	TEMP = 6
	CAQI = 7
	INDEXBACKPNG = 8
	SCHTIME = 9
	HOMEID = 10
	CITY = 11
	STREET = 12
	PLEVEL = 13
	NO2 = 14
	O3 = 15
	SO2 = 16
	CO = 17
	WIND = 18
	WINDBEARING = 19
	

	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = {
			"pm1": self.PM1,
			"pm25": self.PM25,
			"pm10": self.PM10,
			"pres": self.PRES,
			"hum": self.HUM,
			"temp": self.TEMP,
			"caqi": self.CAQI,
			"indexBackPNG": self.INDEXBACKPNG,
			"schtime": self.SCHTIME,
			"homeid": self.HOMEID,
			"city": self.CITY,
			"street": self.STREET,
			"ldesc": self.PLEVEL,
			"no2": self.NO2,
			"o3": self.O3,
			"so2": self.SO2,
			"co": self.CO,
			"wind": self.WIND,
			"windbearing": self.WINDBEARING
		}[type]
		self.pmunits = ' µg/m³'
		self.DynamicTimer = eTimer()
		self.DynamicTimer.callback.append(self.doSwitch)

	def getPm1Value(self):
		pm1 = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm1 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"PM1:" in item:
						pm1 = item.strip().split(b':')[1].decode()
						pm11 = pm1.split('.')[0]
						pm12 = pm1.split('.')[1]
						if int(pm12[0]) >= 5:
							pm1 = int(float(pm1))
							pm1 += 1
							pm1 = 'PM1: ' + str(pm1) + self.pmunits
						else:
							pm1 = pm11
							pm1 = 'PM1: ' + str(pm1) + self.pmunits
			except:
				pm1 = ''
		else:
			pm1 = ''
		return pm1
		
	def getPm25Value(self):
		pm25 = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm25 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"PM25:" in item:
						pm25 = item.strip().split(b':')[1].decode()
						pm251 = pm25.split('.')[0]
						pm252 = pm25.split('.')[1]
						if int(pm252[0]) >= 5:
							pm25 = int(float(pm25))
							pm25 += 1
							pm25 = 'PM2.5: ' + str(pm25) + self.pmunits
						else:
							pm25 = pm251
							pm25 = 'PM2.5: ' + str(pm25) + self.pmunits
			except:
				pm25 = ''
		else:
			pm25 = ''
		return pm25
		
	def getPm10Value(self):
		pm10 = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pm10 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"PM10:" in item:
						pm10 = item.strip().split(b':')[1].decode()
						pm101 = pm10.split('.')[0]
						pm102 = pm10.split('.')[1]
						if int(pm102[0]) >= 5:
							pm10 = int(float(pm10))
							pm10 += 1
							pm10 = 'PM10: ' + str(pm10) + self.pmunits
						else:
							pm10 = pm101
							pm10 = 'PM10: ' + str(pm10) + self.pmunits
			except:
				pm10 = ''
		else:
			pm10 = ''
		return pm10
		
	def getTempValue(self):
		temp = ''
		tempunits = ' °C'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			temp = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"TEMPERATURE:" in item:
						temp = item.strip().split(b':')[1].decode()
						temp1 = temp.split('.')[0]
						temp2 = temp.split('.')[1]
						if int(temp2[0]) >= 5:
							if temp.startswith('-'):
								temp = int(float(temp))
								temp -= 1
								temp = str(temp) + tempunits
							else:
								temp = int(float(temp))
								temp += 1
								temp = str(temp) + tempunits
						else:
							if temp.startswith('-0'):
								temp = temp1[1]
								temp = str(temp) + tempunits
							else:
								temp = temp1
								temp = str(temp) + tempunits
			except:
				temp = ''	
		else:
			temp = ''
		return temp
		
	def getPresValue(self):
		pres = ''
		preunits = ' hPa'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			pres = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"PRESSURE:" in item:
						pres = item.strip().split(b':')[1].decode()
						pres1 = pres.split('.')[0]
						pres2 = pres.split('.')[1]
						if int(pres2[0]) >= 5:
							pres = int(float(pres))
							pres += 1
							pres = str(pres) + preunits
						else:
							pres = pres1
							pres = str(pres) + preunits
			except:
				pres = ''
		else:
			pres = ''
		return pres
		
	def getHumValue(self):
		hum = ''
		huunits = ' %'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			hum = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"HUMIDITY:" in item:
						hum = item.strip().split(b':')[1].decode()
						hum1 = hum.split('.')[0]
						hum2 = hum.split('.')[1]
						if int(hum2[0]) >= 5:
							hum = int(float(hum))
							hum += 1
							hum = str(hum) + huunits
						else:
							hum = hum1
							hum = str(hum) + huunits
			except:
				hum = ''
		else:
			hum = ''
		return hum

	def getWindBearingValue(self):
		windbearing = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			windbearing = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"WIND_BEARING:" in item:
						windbearing = item.split(b':')[1].decode()
						if int(float(windbearing)) >= 0.00 and int(float(windbearing)) < 22.50:
							windbearing = _('N')
						elif int(float(windbearing)) >= 22.50 and int(float(windbearing)) < 45.00:
							windbearing = _('NE')
						elif int(float(windbearing)) >= 45.00 and int(float(windbearing)) < 67.50:
							windbearing = _('EN')
						elif int(float(windbearing)) >= 67.50 and int(float(windbearing)) < 112.50:
							windbearing = _('E')
						elif int(float(windbearing)) >= 112.50 and int(float(windbearing)) < 135.00:
							windbearing = _('ES')
						elif int(float(windbearing)) >= 135.00 and int(float(windbearing)) < 157.50:
							windbearing = _('SE')
						elif int(float(windbearing)) >= 157.50 and int(float(windbearing)) < 202.50:
							windbearing = _('S')
						elif int(float(windbearing)) >= 202.50 and int(float(windbearing)) < 225.00:
							windbearing = _('SW')
						elif int(float(windbearing)) >= 225.00 and int(float(windbearing)) < 247.50:
							windbearing = _('WS')
						elif int(float(windbearing)) >= 247.50 and int(float(windbearing)) < 270.00:
							windbearing = _('W')
						elif int(float(windbearing)) >= 270.00 and int(float(windbearing)) < 315.00:
							windbearing = _('WN')
						elif int(float(windbearing)) >= 315.00 and int(float(windbearing)) < 337.50:
							windbearing = _('NW')
						elif int(float(windbearing)) >= 337.50 and int(float(windbearing)) < 360.00:
							windbearing = _('N')
						else:
							windbearing = ''
						windbearing = ' (' + str(windbearing) + ')'
			except:
				windbearing = ''
		else:
			windbearing = ''
		return windbearing

	def getWindValue(self):
		wind = ''
		windkmunits = ' km/h'
		windmunits = ' m/s'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			wind = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"WIND_SPEED:" in item:
						wind = item.strip().split(b':')[1].decode()
						wind1 = wind.split('.')[0]
						wind2 = wind.split('.')[1]
						if int(wind2[0]) >= 5:
							wind = int(float(wind))
							wind += 1
							if config.plugins.airly.windspeedunits.value == 'km':
								wind = str(wind) + windkmunits
							else:
								wind = int(wind) * 1000/3600
								wind = str(int(float(wind))) + windmunits
						else:
							wind = wind1
							if config.plugins.airly.windspeedunits.value == 'km':
								wind = str(wind) + windkmunits
							else:
								wind = int(wind) * 1000/3600
								wind = str(int(float(wind))) + windmunits
			except:
				wind = ''
		else:
			wind = ''
		return wind
		
	def getCaqiValue(self):
		caqi = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			caqi = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"AIRLY_CAQI:" in item:
						caqi = item.strip().split(b':')[1].decode()
						caqi1 = caqi.split('.')[0]
						caqi2 = caqi.split('.')[1]
						if int(caqi2[0]) >= 5:
							caqi = int(float(caqi))
							caqi += 1
							caqi = str(caqi)
						else:
							caqi = caqi1
							caqi = str(caqi)
			except:
				caqi = ''
		else:
			caqi = ''
		return caqi
		
	def getIndexBackPNGValue(self):
		level = ''
		indexBackPNG = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/0.png'
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"level:" in item:
						level = item.strip().split(b':')[1].decode()
				if level == 'VERY_LOW':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/1.png'
				elif level == 'LOW':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/2.png'
				elif level == 'MEDIUM':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/3.png'
				elif level == 'HIGH':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/4.png'
				elif level == 'VERY_HIGH':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/5.png'
				elif level == 'EXTREME':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/6.png'
				elif level == 'AIRMAGEDDON':
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/7.png'
				else:
					indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/0.png'
			except:
				pass
		else:
			indexBackPNG = '/usr/lib/enigma2/python/Plugins/Extensions/Airly/gfx/indexbacks/0.png'
		return indexBackPNG
			
	def getSchTime(self):
		if fileExists(TMP_PATH + '/airly.sch'):
			TIME_FORMAT = '%Y-%m-%d  %H:%M'
			t = os.path.getmtime(TMP_PATH + '/airly.sch')
			return str(datetime.datetime.fromtimestamp(t).strftime(TIME_FORMAT))
			
	def getIDValue(self):
		homeid = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			homeid = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"id:" in item:
						homeid = item.strip().split(b':')[1].decode()
						homeid = 'ID: ' + str(homeid)
				for item in output:
					if "mode:" in item:
						homeid = 'ID:Pomiar interpolowany'
				homeid = str(homeid)
			except:
				homeid = ''
		else:
			homeid = ''
		return homeid
		
	def getCityValue(self):
		city = ''
		title = 'Airly'
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			city = title
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"city:" in item:
						city = item.strip().split(b':')[1].decode()
			except:
				city = ''
		else:
			city = title
		return city
		
	def getStreetValue(self):
		street = ''
		number = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			street = ''
			number = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"street:" in item:
						street = item.strip().split(b':')[1].decode()
				for item in output:
					if b"number:" in item:
						number = item.strip().split(b':')[1].decode()
				street = str(street) + ' ' + str(number)
			except:
				street = ''
		else:
			street = ''
		return street

	def getPollutionValue(self):
		plevel = ''
		ldesc = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			plevel = ''
			ldesc = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"level:" in item:
						plevel = item.strip().split(b':')[1].decode()
				if plevel == 'VERY_LOW':
					ldesc = 'Idealny dzień na aktywność na świeżym powietrzu.'
				elif plevel == 'LOW':
					ldesc = 'Dobre powietrze. Możesz bez obaw wyjść na zewnątrz i cieszyć się dniem.'
				elif plevel == 'MEDIUM':
					ldesc = 'Bywało lepiej. To nie jest najlepszy dzień na aktywność poza domem.'
				elif plevel == 'HIGH':
					ldesc = 'Zła jakość powietrza. Lepiej zostań dzisiaj w domu.'
				elif plevel == 'VERY_HIGH':
					ldesc = 'Bardzo zła jakość powietrza. Chroń swoje płuca.'
				elif plevel == 'EXTREME':
					ldesc = 'Ekstremalnie zła jakość powietrza. Nie wychodź bez maseczki.'
				elif plevel == 'AIRMAGEDDON':
					ldesc = 'AIRMAGEDDON. Nie oddychaj...'
				else:
					ldesc = ''
			except:
				pass
		return ldesc
		
	def getNO2Value(self):
		no2 = ''
		subscript_two = chr(0x2082)
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			no2 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"NO2:" in item:
						no2 = item.strip().split(b':')[1].decode()
						no21 = no2.split('.')[0]
						no22 = no2.split('.')[1]
						if int(no22[0]) >= 5:
							no2 = int(float(no2))
							no2 += 1
							no2 = 'NO' + str(subscript_two) + ': ' + str(no2) + self.pmunits
						else:
							no2 = no21
							no2 = 'NO' + str(subscript_two) + ': ' + str(no2) + self.pmunits
			except:
				no2 = ''
		else:
			no2 = ''
		return no2
		
	def getO3Value(self):
		o3 = ''
		subscript_three = chr(0x2083)
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			o3 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"O3:" in item:
						o3 = item.strip().split(b':')[1].decode()
						o31 = o3.split('.')[0]
						o32 = o3.split('.')[1]
						if int(o32[0]) >= 5:
							o3 = int(float(o3))
							o3 += 1
							o3 = 'O' + str(subscript_three) + ': ' + str(o3) + self.pmunits
						else:
							o3 = o31
							o3 = 'O' + str(subscript_three) + ': ' + str(o3) + self.pmunits
			except:
				o3 = ''
		else:
			o3 = ''
		return o3
		
	def getSO2Value(self):
		so2 = ''
		subscript_two = chr(0x2082)
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			so2 = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if "SO2:" in item:
						so2 = item.strip().split(b':')[1].decode()
						so21 = so2.split('.')[0]
						so22 = so2.split('.')[1]
						if int(so22[0]) >= 5:
							so2 = int(float(so2))
							so2 += 1
							so2 = 'SO' + str(subscript_two) + ': ' + str(so2) + self.pmunits
						else:
							so2 = so21
							so2 = 'SO' + str(subscript_two) + ': ' + str(so2) + self.pmunits
			except:
				so2 = ''
		else:
			so2 = ''
		return so2

	def getCOValue(self):
		co = ''
		if fileExists(TMP_PATH + '/airly.sch') and os.stat(TMP_PATH + '/airly.sch').st_size == 0:
			co = ''
		elif fileExists(TMP_PATH + '/airly.sch'):
			try:
				with open(TMP_PATH + '/airly.sch', 'rb') as f:
					output = f.readlines()
				for item in output:
					if b"CO:" in item:
						co = item.strip().split(b':')[1].decode()
						co1 = co.split('.')[0]
						co2 = co.split('.')[1]
						if int(co2[0]) >= 5:
							co = int(float(co))
							co += 1
							co = 'CO: ' + str(co) + self.pmunits
						else:
							co = co1
							co = 'CO: ' + str(co) + self.pmunits
			except:
				co = ''
		else:
			co = ''
		return co

	@cached
	def getText(self):
		self.DynamicTimer.start(500)
		
		if self.type == self.PM1:
			return self.getPm1Value()
		elif self.type == self.PM25:
			return self.getPm25Value()
		elif self.type == self.PM10:
			return self.getPm10Value()
		elif self.type == self.TEMP:
			return self.getTempValue()
		elif self.type == self.PRES:
			return self.getPresValue()
		elif self.type == self.HUM:
			return self.getHumValue()
		elif self.type == self.CAQI:
			return self.getCaqiValue()
		elif self.type == self.SCHTIME:
			return self.getSchTime()
		elif self.type == self.HOMEID:
			return self.getIDValue()
		elif self.type == self.CITY:
			return self.getCityValue()
		elif self.type == self.STREET:
			return self.getStreetValue()
		elif self.type == self.PLEVEL:
			return self.getPollutionValue()
		elif self.type == self.NO2:
			return self.getNO2Value()
		elif self.type == self.O3:
			return self.getO3Value()
		elif self.type == self.SO2:
			return self.getSO2Value()
		elif self.type == self.CO:
			return self.getCOValue()
		elif self.type == self.WIND:
			return self.getWindValue()
		elif self.type == self.WINDBEARING:
			return self.getWindBearingValue()

	text = property(getText)
	
	@cached
	def getIconFilename(self):
		if self.type == self.INDEXBACKPNG:
			return self.getIndexBackPNGValue()
			
	iconfilename = property(getIconFilename)

	def changed(self, what):
		self.what = what
		Converter.changed(self, what)

	def doSwitch(self):
		self.DynamicTimer.stop()
		Converter.changed(self, self.what)
