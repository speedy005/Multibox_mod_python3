# -*- coding: utf-8 -*-
# EvgIPChecker
# Copyright (c) Evg77734 2021
# 

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from os import path, popen
import re
import os, socket
import os.path, time
import sys
import json
import math
import datetime
from datetime import date

try:
    py_version = sys.version_info.major
except:
    py_version = 3
    
if py_version == 2:
	from Poll import Poll
else:
	from Components.Converter.Poll import Poll

def getdata():
	n = []
	if os.path.exists("/tmp/ip.js") == True:
		t = os.path.getmtime("/tmp/ip.js")
		now = time.time()
		t1 = now - t
		if t1 < 3600.0:
			with open("/tmp/ip.js", "r") as data_file:
				data = json.load(data_file)
				n.append(data['status'])
				n.append(data['country'])
				n.append(data['countryCode'])
				n.append(data['region'])
				n.append(data['regionName'])
				n.append(data['city'])
				n.append(data['zip'])
				n.append(data['lat'])
				n.append(data['lon'])
				n.append(data['timezone'])
				n.append(data['isp'])
				n.append(data['org'])
				n.append(data['as'])
				n.append(data['query'])
				n.append(data['offset'])
				
				c = n
		else:
			try:
				os.system("wget -qO- \'http://ip-api.com/json/?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,query,timezone,offset&lang=ger\' -O /tmp/ip.js")
			except:
				pass
						
			if os.path.exists("/tmp/ip.js") == True:
				with open("/tmp/ip.js", "r") as data_file:
					data = json.load(data_file)
					n.append(data['status'])
					n.append(data['country'])
					n.append(data['countryCode'])
					n.append(data['region'])
					n.append(data['regionName'])
					n.append(data['city'])
					n.append(data['zip'])
					n.append(data['lat'])
					n.append(data['lon'])
					n.append(data['timezone'])
					n.append(data['isp'])
					n.append(data['org'])
					n.append(data['as'])
					n.append(data['query'])
					n.append(data['offset'])
					c = n
			else:
				n = ['n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a']
				c = n
						
	else:
		try:
			os.system("wget -qO- \'http://ip-api.com/json/?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,isp,org,as,query,timezone,offset&lang=ger\' -O /tmp/ip.js")
		except:
			pass
				
		if os.path.exists("/tmp/ip.js") == True:
			with open("/tmp/ip.js", "r") as data_file:
				data = json.load(data_file)
				n.append(data['status'])
				n.append(data['country'])
				n.append(data['countryCode'])
				n.append(data['region'])
				n.append(data['regionName'])
				n.append(data['city'])
				n.append(data['zip'])
				n.append(data['lat'])
				n.append(data['lon'])
				n.append(data['timezone'])
				n.append(data['isp'])
				n.append(data['org'])
				n.append(data['as'])
				n.append(data['query'])
				n.append(data['offset'])
				c = n
		else:
			n = ['n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a','n/a']
			c = n
				
	return c

class xDreamy_IPChecker(Poll, Converter, object):
	status = 0
	country = 1
	countryCode = 2
	region = 3
	regionName = 4
	city = 5
	zipp = 6
	lat = 7
	lon = 8
	timezone = 9
	isp = 10
	org = 11
	aas = 12
	query = 13
	Iplocal = 14
	WSCHOD = 15
	ZACHOD = 16
	SZCZYT = 17
	SUNDAY = 18
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 60000
		self.poll_enabled = True
		self.type = {'status': self.status,
		'country': self.country,
		'countryCode': self.countryCode,
		'region': self.region,
		'regionName': self.regionName,
		'city': self.city,
		'zipp': self.zipp,
		'lat': self.lat,
		'lon': self.lon,
		'timezone': self.timezone,
		'isp': self.isp,
		'org': self.org,
		'aas': self.aas,
		'query': self.query,
		'Iplocal': self.Iplocal,
		'WSCHOD': self.WSCHOD,
		'ZACHOD': self.ZACHOD,
		'SZCZYT': self.SZCZYT,
		'SUNDAY': self.SUNDAY
		}[type]		

	@cached	
	def getText(self):
		if self.type == self.status:
			ip = []
			ip = getdata()
			return str(ip[0])

		if self.type == self.country:
			ip = []
			ip = getdata()
			return str(ip[1])

		if self.type == self.countryCode:
			ip = []
			ip = getdata()
			return str(ip[2])

		if self.type == self.region:
			ip = []
			ip = getdata()
			return str(ip[3])
			
		if self.type == self.regionName:
			ip = []
			ip = getdata()
			return str(ip[4])
			
		if self.type == self.city:
			ip = []
			ip = getdata()
			return str(ip[5])
			
		if self.type == self.zipp:
			ip = []
			ip = getdata()
			return str(ip[6])
			
		if self.type == self.lat:
			ip = []
			ip = getdata()
			return str(ip[7])
			
		if self.type == self.lon:
			ip = []
			ip = getdata()
			return str(ip[8])
			
		if self.type == self.timezone:
			ip = []
			ip = getdata()
			return str(ip[9])
			
		if self.type == self.isp:
			ip = []
			ip = getdata()
			return str(ip[10])
			
		if self.type == self.org:
			ip = []
			ip = getdata()
			return str(ip[11])
			
		if self.type == self.aas:
			ip = []
			ip = getdata()
			return str(ip[12])
			
		if self.type == self.query:
			ip = []
			ip = getdata()
			return str(ip[13])												
		
		if self.type == self.Iplocal:
			gw = os.popen("ip -4 route show default").read().split()
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect((gw[2], 0))
			ipaddr = s.getsockname()[0]
			return "%s" % ipaddr

		ip = []
		ip = getdata()
		
		dlu = float(ip[8])
		
		szer = float(ip[7])
		
		ST = float((float(ip[14])/3600)-1)
		
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
		if self.type == self.SUNDAY:
			time_1 = datetime.timedelta(hours= Wh , minutes=Wm)
			time_2 = datetime.timedelta(hours= Zh, minutes=Zm)
			d = (time_2 - time_1)
			dd = datetime.datetime.strptime(str(d), "%H:%M:%S")
			ddd = dd.strftime('%H:%M')
			return str(ddd)
		
			
	text = property(getText)
