# -*- coding: utf-8 -*-
# by digiteng...11.2021
# for channellist, fhd skin, 300x170 backdrops
# <widget source="ServiceEvent" render="xtraBackdropWidget" position="980,113" size="920,863" cornerRadius="20" backgroundColor="background" zPosition="99" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePoint, eWidget, eSlider, eLabel, eSize, gFont, ePixmap, loadJPG, loadPNG, eEPGCache, eServiceReference
from Components.Converter.xtraEventGenre import getGenreStringSub
from Components.config import config
from skin import parseColor
from time import localtime, mktime, time
from datetime import datetime, timedelta
import re
import os
import json
from Tools.xtraTool import REGEX, pathLoc, pRating
pathLoc = config.plugins.xtrvnt.loc.value
NoImage = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
pratePath = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/parental/"
imgNo="/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film.jpg"
star = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star.png"
starBackgrund = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/star/star_back.png"

class xtraBackdropWidget(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.epgcache = eEPGCache.getInstance()
		self.fontSizeNow = 20
		self.fontSizeNexts = 18
		self.cornerRadius = 20
		
	def applySkin(self, desktop, screen):
		attribs = self.skinAttributes[:]
		for attrib, value in self.skinAttributes:
			if attrib == 'position':
				self.px = int(value.split(',')[0])
				self.py = int(value.split(',')[1])
			elif attrib == 'size':
				self.szX = int(value.split(',')[0])
				self.szY = int(value.split(',')[1])
			elif attrib == 'backgroundColor':
				self.backgroundColor = value
			elif attrib == 'fontSizeNow':
				self.fontSizeNow = int(value)
			elif attrib == 'fontSizeNexts':
				self.fontSizeNexts = int(value)
			elif attrib == 'cornerRadius':
				self.cornerRadius = int(value)
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, screen)

	GUI_WIDGET = eWidget
	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				
				evnt = ''
				pstrNm = ''
				evntNm = ''
				service = ''
				event = None
				fd = ''
				ed = ''
				desc = ''
				rtd = ''
				imdbRtng = ''
				imdbRating = ''
				events = None
				rate = ''
				prate = ''
				service = self.source.service
				event = self.source.event
				if event:
					self.instance.show()
					evnt = event.getEventName()
					evntNm = REGEX.sub('', evnt).strip()
					read_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
					if os.path.exists(read_json):
						with open(read_json) as f:
							read_json = json.load(f)
					fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
					ed = event.getExtendedDescription()

					try:
						prate = read_json["rated"]
						if prate is not None:
							rtd = prate
						elif prate is None:
							parentName = ''
							prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
							for i in prs:
								prr = re.search(i, fd)
								if prr:
									parentName = prr.group(1)
									parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
									rtd = parentName
									break
						else:
							try:
								age = ''
								rating = event.getParentalData()
								if rating:
									age = rating.getRating()
									rtd = age
							except: pass
					except:
						parentName = ''
						prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
						for i in prs:
							prr = re.search(i, fd)
							if prr:
								parentName = prr.group(1)
								parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
								rtd = parentName
								break
					rtd = pRating(rtd)
					try:
						if rtd:
							rateNm = "{}FSK_{}.png".format(pratePath, rtd.replace("+", ""))
							self.parentPxmp.setPixmapFromFile(rateNm)
							self.parentPxmp.resize(eSize(60, 60))
							self.parentPxmp.move(ePoint(240, 110))
							self.parentPxmp.setZPosition(10)
							self.parentPxmp.setAlphatest(2)
							self.parentPxmp.setScale(1)
							self.parentPxmp.show()
						else:
							self.parentPxmp.hide()
					except: pass
					try:
						rating = None
						rating = read_json['imdbRating']
						if rating is not None:
							try:
								rtng = int(10 * float(rating))
								self.ratingPxmp.setPixmap(loadPNG(star))
								self.ratingPxmp.setBackgroundPixmap(loadPNG(starBackgrund))
								self.ratingPxmp.setRange(0, 100)
								self.ratingPxmp.setValue(rtng)
								self.ratingPxmp.move(ePoint(20, 220))
								self.ratingPxmp.resize(eSize(200,20))
								self.ratingPxmp.setAlphatest(2)
								self.ratingPxmp.show()
							except Exception as err:
								from Tools.xtraTool import errorlog
								errorlog(err, __file__)
							self.ratingLabel.setText("IMDB : {}".format(rating))
							self.ratingLabel.setBackgroundColor(parseColor(self.backgroundColor))
							self.ratingLabel.resize(eSize(400, 30))
							self.ratingLabel.move(ePoint(20, 250))
							self.ratingLabel.setFont(gFont("Regular", self.fontSizeNow))
							self.ratingLabel.setHAlign(eLabel.alignLeft)
							self.ratingLabel.show()
						else:
							self.ratingPxmp.hide()
							self.ratingLabel.hide()
					except:
						self.ratingPxmp.hide()
						self.ratingLabel.hide()
					d=[]
					try:
						dir = read_json["director"]
						d.append("Director : {}".format(dir))
					except: pass
					try:
						actr = read_json["actors"]
						n=0
						d.append("\nActors : ")
						for i in actr:
							d.append("{}, ".format(i))
							n += 1
							if n == 3: break
					except: pass
					try:
						des = read_json["desc"]
						d.append("\nDescription : {}".format(des))
					except:
						d.append("Description : {}".format(fd))
					descr = "".join(d)
					description =	'{}'.format(descr)
					# description = "\n".join(["-"*500, description, "-"*500])
					events = self.epgcache.lookupEvent(['IBDCT', (service.toString(), 0, -1, 480)])
					if self.epgcache is not None and events:
						try:
							# event 0
							evnt = events[0][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[0][1])
							evntNm0 = "%02d:%02d - %s\n%s"%(bt[3], bt[4], evnt, self.info())
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp0.setPixmap(loadJPG(pstrNm))
								self.eventPxmp0.resize(eSize(300, 170))
								self.eventPxmp0.move(ePoint(20,20))
								self.eventPxmp0.setTransparent(0)
								self.eventPxmp0.setZPosition(9)
								self.eventPxmp0.setScale(1)
								self.eventPxmp0.setCornerRadius(self.cornerRadius,15)
								self.eventPxmp0.show()
							else:
								self.eventPxmp0.setPixmap(loadJPG(NoImage))
								self.eventName0.hide()
							self.eventName0.setText(str(evntNm0))
							self.eventName0.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName0.resize(eSize(440, 170))
							self.eventName0.move(ePoint(330, 20))
							self.eventName0.setFont(gFont("Regular", self.fontSizeNow))
							self.eventName0.setHAlign(eLabel.alignLeft)
							self.eventName0.show()
						except:
							self.eventPxmp0.hide()
							self.eventName0.hide()
						try:
							self.eventDesc.setText(description)
							self.eventDesc.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventDesc.resize(eSize(750, 400))
							self.eventDesc.move(ePoint(20, 250))
							self.eventDesc.setFont(gFont("Regular", self.fontSizeNow))
							self.eventDesc.setHAlign(eLabel.alignLeft)
							self.eventDesc.setVAlign(eLabel.alignCenter)
							self.eventDesc.show()
						except:
							self.eventPxmp0.hide()
							self.eventName0.hide()
						try:
							# event 1
							evnt = events[1][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[1][1])
							evntNm1 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp1.setPixmap(loadJPG(pstrNm))
								self.eventPxmp1.resize(eSize(300, 170))
								self.eventPxmp1.move(ePoint(20, 700))
								self.eventPxmp1.setTransparent(0)
								self.eventPxmp1.setZPosition(9)
								self.eventPxmp1.setScale(1)
								self.eventPxmp1.setCornerRadius(self.cornerRadius,15)
								self.eventPxmp1.show()
							else:
								self.eventPxmp1.setPixmap(loadJPG(NoImage))
								self.eventPxmp1.setCornerRadius(self.cornerRadius,15)
								self.eventName1.hide()
							self.eventName1.setText(str(evntNm1))
							self.eventName1.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName1.resize(eSize(300, 100))
							self.eventName1.move(ePoint(20, 880))
							self.eventName1.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName1.setHAlign(eLabel.alignLeft)
							self.eventName1.show()
						except:
							self.eventPxmp1.hide()
							self.eventName1.hide()
						try:
							# event 2
							evnt = events[2][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[2][1])
							evntNm2 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp2.setPixmap(loadJPG(pstrNm))
								self.eventPxmp2.resize(eSize(300, 170))
								self.eventPxmp2.move(ePoint(400, 700))
								self.eventPxmp2.setTransparent(0)
								self.eventPxmp2.setZPosition(3)
								self.eventPxmp2.setScale(1)
								self.eventPxmp2.setCornerRadius(self.cornerRadius,15)
								self.eventPxmp2.show()
							else:
								self.eventPxmp2.setPixmap(loadJPG(NoImage))
								self.eventPxmp2.setCornerRadius(self.cornerRadius,15)
								self.eventName2.hide()
							self.eventName2.setText(str(evntNm2))
							self.eventName2.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName2.resize(eSize(300, 100))
							self.eventName2.move(ePoint(400, 880))
							self.eventName2.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName2.setHAlign(eLabel.alignLeft)
							self.eventName2.show()
						except:
							self.eventPxmp2.hide()
							self.eventName2.hide()
						try:
							# event 3
							evnt = events[3][4]
							evntNm = REGEX.sub('', evnt).strip()
							bt = localtime(events[3][1])
							evntNm3 = "%02d:%02d - %s\n"%(bt[3], bt[4], evnt)
							pstrNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							if os.path.exists(pstrNm):
								self.eventPxmp3.setPixmap(loadJPG(pstrNm))
								self.eventPxmp3.resize(eSize(300, 170))
								self.eventPxmp3.move(ePoint(780, 700))
								self.eventPxmp3.setTransparent(0)
								self.eventPxmp3.setZPosition(3)
								self.eventPxmp3.setScale(1)
								self.eventPxmp3.setCornerRadius(self.cornerRadius,15)
								self.eventPxmp3.show()
							else:
								self.eventPxmp3.setPixmap(loadJPG(NoImage))
								self.eventPxmp3.setCornerRadius(self.cornerRadius,15)
								self.eventName3.hide()
							self.eventName3.setText(str(evntNm3))
							self.eventName3.setBackgroundColor(parseColor(self.backgroundColor))
							self.eventName3.resize(eSize(300, 100))
							self.eventName3.move(ePoint(780, 880))
							self.eventName3.setFont(gFont("Regular", self.fontSizeNexts))
							self.eventName3.setHAlign(eLabel.alignLeft)
							self.eventName3.show()
						except:
							self.eventPxmp3.hide()
							self.eventName3.hide()
						# prime time ##################################################################################################################
						primetime = "N/A"
						text = "N/A"
						try:
							prime_hour = config.epgselection.graph_primetimehour.value
							prime_minute = config.epgselection.graph_primetimemins.value
						except:
							prime_hour = 20
							prime_minute = 15
						now = localtime(time())
						dt = datetime(now.tm_year, now.tm_mon, now.tm_mday, prime_hour, prime_minute)
						pt = int(mktime(dt.timetuple()))
						self.epgcache.startTimeQuery(eServiceReference(service.toString()), pt)
						event = self.epgcache.getNextTimeEntry()
						if event and (now.tm_hour <= prime_hour):
							bt = event.getBeginTime()
							duration = round(event.getDuration())
							et = event.getBeginTime() + duration
							eNm = event.getEventName()
							evntNm = REGEX.sub('', eNm).strip()
							bcdrpNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							text = "\c0000????Prime Time\n\c00aaaaaa%02d:%02d \n%smin\c00??????\n%s"%(localtime(bt)[3], localtime(bt)[4], duration//60, evntNm)
							nowx = int(time())
							if nowx > et:
								text = "\c00444445Prime Time (End)\n\c00444445%02d:%02d \n%smin\c00444445\n%s"%(localtime(bt)[3], localtime(bt)[4], duration//60, evntNm)
							self.primeTimeNowLabel.setText(text)
							self.primeTimeNowLabel.resize(eSize(300, 100))
							self.primeTimeNowLabel.move(ePoint(780, 200))
							self.primeTimeNowLabel.setFont(gFont("Regular", self.fontSizeNow))
							self.primeTimeNowLabel.setBackgroundColor(parseColor(self.backgroundColor))
							self.primeTimeNowLabel.show()
							if os.path.exists(bcdrpNm):
								self.primeTimeNowPxmp.setPixmapFromFile(bcdrpNm)
							else:
								self.primeTimeNowPxmp.setPixmapFromFile(imgNo)
						else:
							self.primeTimeNowPxmp.setPixmapFromFile(imgNo)
							self.primeTimeNowLabel.setText(text)
						self.primeTimeNowPxmp.setScale(1)
						self.primeTimeNowPxmp.setBackgroundColor(parseColor(self.backgroundColor))
						self.primeTimeNowPxmp.resize(eSize(300, 170))
						self.primeTimeNowPxmp.move(ePoint(780, 20))
						self.primeTimeNowPxmp.setCornerRadius(self.cornerRadius,15)
						self.primeTimeNowPxmp.show()
						#############################################################################
						# PrimeTime Next
						pt = dt + timedelta(1)
						pt = int(mktime(pt.timetuple()))
						self.epgcache.startTimeQuery(eServiceReference(service.toString()), pt)
						event = self.epgcache.getNextTimeEntry()
						if event:
							bt = event.getBeginTime()
							duration = round(event.getDuration())
							et = event.getBeginTime() + duration
							eNm = event.getEventName()
							evntNm = REGEX.sub('', eNm).strip()
							bcdrpNm = "{}xtraEvent/backdrop/{}.jpg".format(pathLoc, evntNm)
							text = "\c0000????Prime Time Next\n\c00aaaaaa%02d:%02d \n%smin\c00??????\n%s"%(localtime(bt)[3], localtime(bt)[4], duration//60, evntNm)
							self.primeTimeNextLabel.setText(text)
							self.primeTimeNextLabel.resize(eSize(300, 100))
							self.primeTimeNextLabel.move(ePoint(780, 530))
							self.primeTimeNextLabel.setBackgroundColor(parseColor(self.backgroundColor))
							self.primeTimeNextLabel.show()
							if os.path.exists(bcdrpNm):
								self.primeTimeNextPxmp.setPixmapFromFile(bcdrpNm)
							else:
								self.primeTimeNextPxmp.setPixmapFromFile(imgNo)
						else:
							self.primeTimeNextPxmp.setPixmapFromFile(imgNo)
							self.primeTimeNowLabel.setText(text)
						self.primeTimeNextPxmp.setBackgroundColor(parseColor(self.backgroundColor))
						self.primeTimeNextPxmp.setScale(1)
						self.primeTimeNextPxmp.resize(eSize(300, 170))
						self.primeTimeNextPxmp.move(ePoint(780, 350))
						self.primeTimeNextPxmp.setCornerRadius(self.cornerRadius,15)
						self.primeTimeNextPxmp.show()
					else:
						self.eventPxmp1.hide()
						self.eventPxmp2.hide()
						self.eventPxmp3.hide()
						self.eventName1.hide()
						self.eventName2.hide()
						self.eventName3.hide()
						self.eventDesc.hide()
				else:
					self.instance.hide()
			else:
				self.instance.hide()

	def GUIcreate(self, parent):
		self.instance = eWidget(parent)
		self.eventDesc = eLabel(self.instance)
		self.eventName0 = eLabel(self.instance)
		self.eventName1 = eLabel(self.instance)
		self.eventName2 = eLabel(self.instance)
		self.eventName3 = eLabel(self.instance)
		self.eventPxmp0 = ePixmap(self.instance)
		self.eventPxmp1 = ePixmap(self.instance)
		self.eventPxmp2 = ePixmap(self.instance)
		self.eventPxmp3 = ePixmap(self.instance)
		self.parentPxmp = ePixmap(self.instance)
		self.primeTimeNowLabel = eLabel(self.instance)
		self.primeTimeNextLabel = eLabel(self.instance)
		self.primeTimeNowPxmp = ePixmap(self.instance)
		self.primeTimeNextPxmp = ePixmap(self.instance)
		self.ratingPxmp = eSlider(self.instance)
		self.ratingLabel = eLabel(self.instance)

	def info(self):
		event = ""
		tc = ""
		try:
			event = self.source.event
			if event:
				evnt = event.getEventName()
				evntNm = REGEX.sub('', evnt).strip()
				read_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
				fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
				if os.path.exists(read_json):
					with open(read_json) as f:
						read_json = json.load(f)
				evnt = []
				try:
					year = ''
					fd = fd.replace(',', '').replace('(', '').replace(')', '')
					fdl = ['\d{4} [A-Z]+', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
					for i in fdl:
						year = re.findall(i, fd)
						if year:
							year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
							evnt.append("Year : {}".format(year))
							break
				except:
					year = read_json["release_date"]
					if year:
						evnt.append("Year : {}".format(year))
				try:
					imdbRating = read_json["imdbRating"]
					if imdbRating:
						evnt.append("IMDB : {}".format(imdbRating))
				except:
					pass
				try:
					Rated = read_json["rated"]
					pRated = read_json["parentalRating"]
					if Rated is not None:
						evnt.append("Rated : {}+".format(Rated))
					elif pRated is not None:
						evnt.append("Rated : {}".format(Rated))
					else:
						parentName = ''
						prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
						for i in prs:
							prr = re.search(i, fd)
							if prr:
								parentName = prr.group(1)
								parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
								evnt.append("Rated : {}+".format(parentName))
								break
							else:
								try:
									age = ''
									rating = event.getParentalData()
									if rating:
										age = rating.getRating()
										evnt.append("Rated : {}+".format(age))
								except:
									pass
				except: pass
				try:
					Genre = read_json["genre"]
					evnt.append("Genre : {}".format(Genre))
				except:
					genres = event.getGenreDataList()
					if genres:
						genre = genres[0]
						evnt.append("Genre : {}".format(getGenreStringSub(genre[0], genre[1])))
				try:
					Countries = read_json["countries"]
					evnt.append("Countries : {}".format(Countries))
				except: pass
				try:
					duration = read_json["duration"]
					evnt.append("Duration : {}min".format(duration))
				except: pass

				tc = "\n".join(evnt)
				return tc
			else:
				return tc
		except:
			pass
