#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2020
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################
from Components.Renderer.Renderer import Renderer 
from enigma import ePixmap, eTimer, eActionMap
from Components.config import config
import os
import re
import json
import urllib.request, urllib.error, urllib.parse
try:
	from urllib.parse import quote_plus
except ImportError as ie:
	from urllib.parse import quote_plus

from enigma import loadJPG
ENA = True
	
PATH = "/media/usb"
PATH = '%s/poster' % PATH
if not os.path.isdir(PATH):
	os.mkdir(PATH)
FULLPATH = PATH + '/%s.jpg'
try:
	folder_size=sum([sum([os.path.getsize(os.path.join(path_folder, fname)) for fname in files]) for path_folder, folders, files in os.walk(path_folder)])
	posters_sz = "%0.f" % (folder_size/(1024*1024.0))
	if posters_sz >= "10":    # folder remove size(10MB)...
		import shutil
		shutil.rmtree(path_folder)
except:
	pass

class AMB_Poster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.last = "None"
		self.__isInst = True
		self.__isHide = True
		self.__delayInitTimer = eTimer()
		try:
			self.__delayInitTimer_conn = self.__delayInitTimer.timeout.connect(self.searchPoster)
		except AttributeError:
			self.__delayInitTimer.timeout.get().append(self.searchPoster)
 		self.enaExc = False
	GUI_WIDGET = ePixmap

	def doRC(self, key, flag):
		if key == 352 and flag == 3 and self.last != "None":
			try:
				dest = FULLPATH % self.image
				if os.path.isfile(dest):
					os.system("rm -rf " + dest)
					ff = PATH + '/_exceptions.txt'
					all = ""
					if os.path.isfile(ff):
						f = open(ff,"r")
						for i in f.readlines():
							if not self.image in i:
								all += i
						f.close()
					all += self.image + "\n"
					f = open(ff,"w")
					f.write(all)
					f.close()
					self.showPoster(None)
			except: pass
		return 0

	def changed(self, what):
		if self.instance and self.__isInst:
			self.instance.setScale(1)
			self.__isInst = False
		event = self.source.event
		image = None
		if ENA and event is not None:
			try:
				name = event.getEventName()
				if name == self.last:
					return
				if self.__delayInitTimer.isActive():
					self.__delayInitTimer.stop()
				self.last = name
				p = '((.*?)) \([T](\d+)\)'
				f = re.search(p,name)
				if f:
					name = f.group(1)
				image = name.replace(':',' ').replace('.',' ').replace('(',' ').replace(')',' ')
				if ' -' in image:
					image = image.split(' -')[0]
				if '"' in image:
					image = (image.split('"')[1]).replace('"','')
				image = image.strip()
				image = re.sub('\s+', '+', image)
				dest = FULLPATH % image
				self.image = image
				if self.enaExc:
					ff = PATH + '/_exceptions.txt'
					if os.path.isfile(ff):
						f = open(ff,"r").read()
						if f.find(self.image) != -1:
							self.showPoster(None)
							return
				if os.path.isfile(dest):
					if os.path.getsize(dest) < 150:
						os.system("rm -rf " + dest)
				if not os.path.isfile(dest):					
					self.showPoster(None)
					delay = 1
					self.__delayInitTimer.startLongTimer(delay)
				else:
					self.showPoster(dest)
			except: pass
		elif image is None:
			self.showPoster(None)
			self.last = "None"		

	def showPoster(self, dest):
		try:
			if self.instance:
				if dest is not None:
					if self.image in dest:
						self.instance.setPixmap(loadJPG(dest))
						self.instance.show()
						self.__isHide = False
				elif not self.__isHide:
					self.instance.hide()
					self.__isHide = True
		except: pass

	def searchPoster(self):
		self.__delayInitTimer.stop()
		image = self.image
		dest = FULLPATH % image
		def chckUrl(d):
			mask = re.compile('<div class="poster">.*?<img .*?src=\"(http.*?)\"', re.S)
			u = mask.search(d)
			if u and u.group(1).find("jpg") > 0:
				u = u.group(1)
				return u
			return None
		def downNow(w):
			try:
				f = open(dest,'wb')
				f.write(urllib.request.urlopen(w).read())
				f.close()
				if os.path.isfile(dest):
					if os.path.getsize(dest) > 50:
						return True
					else:
						os.system("rm -rf %s,%s" % dest)
			except: pass
			return None
		imdb = "a"
		try:
				data = ""
				info = ""
				url = None
				if imdb in ("a","i"):
					infomask = re.compile(
							'<h1 class="(?:long|)">(?P<title>.*?)<.*?/h1>*'
							'(?:.*?<div class="originalTitle">(?P<originaltitle>.*?)\s*\((?P<g_originaltitle>original title))*'
							'(?:.*?<h4 class="inline">\s*(?P<g_director>Directors?):\s*</h4>.*?<a.*?>(?P<director>.*?)(?:\d+ more|</div>))*'
							'(?:.*?<h4 class="inline">\s*(?P<g_creator>Creators?):\s*</h4>.*?<a.*?>(?P<creator>.*?)(?:\d+ more|</div>))*'
							'(?:.*?<h4 class="inline">\s*(?P<g_writer>Writers?):\s*</h4>.*?<a.*?>(?P<writer>.*?)(?:\d+ more|</div>))*'
							'(?:.*?<h4 class="float-left">(?P<g_seasons>Seasons?)\s*</h4>.*?<a.*?>(?P<seasons>(?:\d+|unknown)?)</a>)*'
							'(?:.*?<h4 class="inline">\s*(?P<g_country>Country):\s*</h4>.*?<a.*?>(?P<country>.*?)</a>)*'
							'(?:.*?<h4 class="inline">\s*(?P<g_premiere>Release Date).*?</h4>\s+(?P<premiere>.*?)\D+\s+<span)*'
							'(?:.*?<h4 class="inline">(?P<g_runtime>Runtime):</h4>\s*(?P<runtime>.*?)</div>)*'
							, re.S)
					htmlmask = re.compile('<.*?>')
					resultmask = re.compile('<tr class=\"findResult (?:odd|even)\">.*?<td class=\"result_text\"> <a href=\"/title/(tt\d{7,7})/.*?\"\s?>(.*?)</a>.*?</td>', re.S)
					data = urllib.request.urlopen("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + quote_plus(image, safe='+') + "&s=all").read()
					info = infomask.search(data)
					if info:
						url = chckUrl(data)
					else:
						if not re.search('class="findHeader">No results found for', data):
							a = data.find("<table class=\"findList\">")
							b = data.find("</table>",a)
							all = data[a:b]
							all_res = resultmask.finditer(all)
							res = [(htmlmask.sub('',x.group(2)), x.group(1)) for x in all_res]
							if len(res) > 0:
								data = urllib.request.urlopen("https://www.imdb.com/title/" + res[0][1]).read()
								info = infomask.search(data)
								if info:
									url = chckUrl(data)
					if url:
						url = downNow(url)
				if imdb in ("a","m") and url is None:
					for x in ("multi","tv"):
						data = json.load(urllib.request.urlopen("https://api.themoviedb.org/3/search/%s?api_key=87241fc3a18a22a33f8ce28edf4e796a&query=%s&language=de-DE" % (x, image)))
						if 'results' in data and len(data['results']) != 0 and data['total_results'] != 0:
							url = downNow("https://image.tmdb.org/t/p/w185_and_h278_bestv2%s" % data['results'][0]['poster_path'])
							if url is not None:
								break
				del data
				del info
		except: pass
		if not os.path.isfile(dest):
			dest = None
		self.showPoster(dest)
		
		
