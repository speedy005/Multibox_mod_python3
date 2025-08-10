# -*- coding: utf-8 -*-
# by digiteng...07.2020, 11.2020, 11.2021, 12.2024
# IMDB or TMDB information...
# options;
# Title,Rated,Duration,Genre,SE,ReleaseDate,AirDate,Revenue,Countries,Actors,Director,Crews,Description,Rating,RatingSimple,RatingProgress
# example;
	# for ch sel...

		# <ePixmap pixmap="xtra/star_b.png" position="990,278" size="200,20" alphatest="blend" zPosition="2" transparent="1" />
		# <widget source="ServiceEvent" render="Progress" pixmap="xtra/star.png" position="990,278" size="200,20" alphatest="blend" transparent="1" zPosition="2" backgroundColor="background">
			# <convert type="xtraInfo">IMDB;RatingProgress</convert>
		# </widget>
		
		# <widget source="ServiceEvent" render="Label" position="990,308" size="800,45" font="Regular; 30" halign="left" transparent="1" zPosition="5" backgroundColor="background" valign="center">
			# <convert type="xtraInfo">IMDB;Rating</convert>
		# </widget>
		
		# <widget source="ServiceEvent" render="Label" position="1283,113" size="600,240" font="Regular; 26" halign="left" transparent="1" zPosition="5" backgroundColor="background" valign="top">
			# <convert type="xtraInfo">TMDB;-;Color:\c00ffff00,\c00??????;Title,Rated,Duration,Genre,SE,AirDate,Countries</convert>
		# </widget>

		# <widget source="ServiceEvent" render="RunningText" options="movetype=running,startdelay=5000,steptime=60,direction=top,startpoint=0,wrap=1,always=0,repeat=2,oneshot=1" size="900,400" position="990,374" font="Regular; 30" halign="left" transparent="1" zPosition="2" backgroundColor="background" valign="top">
			# <convert type="xtraInfo">TMDB;-;Director,Actors,Description</convert>
		# </widget>
from __future__ import absolute_import
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Components.Converter.xtraEventGenre import getGenreStringSub
import re
import json
import os
from Components.Converter.Poll import Poll
tc="n/a"
from Tools.xtraTool import REGEX, pathLoc
keyColorA = "\c0000????"
keyColorB = "\c00ffffff"
imdbRating="IMDB Rating"
tmdbRatingFull="Rating"
imdbRating2="RatingSimple"
tmdbRating="Rating"
Year="AirDate"
Country="Countries"
tmdbRatingValue=imdbRatingValue="RatingProgress"
pathLoc = config.plugins.xtrvnt.loc.value

class xtraInfo(Poll, Converter):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True

	@cached
	def getText(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			evntNm = REGEX.sub('', evnt).strip()
			fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
			evnt = []
			if "Color" in self.type:
				col = self.type.split(";")
				for i in range(len(col)):
					if "Color" in col[i]:
						keyColorA = col[i].split(":")[1].split(",")[0]
						keyColorB = col[i].split(":")[1].split(",")[1]
			else:
				keyColorA = "\c00ff0000"
				keyColorB = "\c0000ff00"

###########################################################################################################################
			if "TMDB" in self.type:
				rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
				if os.path.exists(rating_json):
					with open(rating_json) as f:
						read_json = json.load(f)
				else:
					evnt=[]

			elif "IMDB" in self.type:
				rating_json = "{}xtraEvent/imdb/casts/{}/{}_info.json".format(pathLoc, evntNm, evntNm)
				if os.path.exists(rating_json):
					with open(rating_json) as f:
						read_json = json.load(f)
				else:
					evnt=[]

			else:
				rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
				if os.path.exists(rating_json):
					with open(rating_json) as f:
						read_json = json.load(f)
				else:
					evnt=[]

###########################################################################################################################

			if "Title" in self.type:
				try:
					if "TMDB" in self.type:
						title = read_json['title']
						evnt.append("{}Title : {}{}".format(keyColorA, keyColorB, title))
					elif "IMDB" in self.type:
						title = read_json['orjTitle']
						evnt.append("{}Title : {}{}".format(keyColorA, keyColorB, title))
						
				except:
					evnt.append("{}Title : {}{}".format(keyColorA, keyColorB, event.getEventName()))
			if "Rated" in self.type:
				try:
					Rated = None
					if "title" in str(read_json): 
						Rated = read_json["rated"]
						if Rated != None:
							evnt.append("{}Rated : {}{}".format(keyColorA, keyColorB, Rated))
					if Rated == None:
						parentName = ''
						prs = ['[aA]b ((\d+))', '[+]((\d+))', 'Od lat: ((\d+))', '(\d+)[+]', '(TP)', '[-](\d+)']
						for i in prs:
							prr = re.search(i, fd)
							if prr:
								parentName = prr.group(1)
								parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
								evnt.append("{}Rated : {}{}+".format(keyColorA, keyColorB, parentName))
								break
						if parentName == '':
							try:
								age = ''
								rating = event.getParentalData()
								if rating:
									age = rating.getRating()
									evnt.append("{}Rated : {}{}+".format(keyColorA, keyColorB, age))
							except:
								pass			
				except:
					pass
			if "Duration" in self.type:
				try:
					if "duration" in str(read_json):
						Duration = read_json["duration"]
						evnt.append("{}Duration : {}{} min".format(keyColorA, keyColorB, Duration))
					else:
						drtn = round(event.getDuration()// 60)
						if drtn > 0:
							evnt.append("{}Duration : {}{}min".format(keyColorA, keyColorB, drtn))
						else:
							prs = re.findall(r' \d+ Min', fd)
							if prs:
								drtn = round(prs[0])
								evnt.append("{}Duration : {}{}min".format(keyColorA, keyColorB, drtn))
				except:
					pass
			if "Genre" in self.type:
				try:
					if "genre" in str(read_json):
						Genre = read_json["genre"]
						evnt.append("{}Genre : {}{}".format(keyColorA, keyColorB, Genre))
					else:
						genres = event.getGenreDataList()
						if genres:
							genre = genres[0]
							evnt.append("{}Genre : {}{}".format(keyColorA, keyColorB, getGenreStringSub(genre[0], genre[1])))
				except:
					pass
			if "SE" in self.type:
				try:
					prs = ['(\d+). Staffel, Folge (\d+)', 'T(\d+) Ep.(\d+)', '"Episodio (\d+)" T(\d+)', '(\d+).* \(odc. (\d+).*\)']
					for i in prs:
						seg = re.search(i, fd)
						if seg:
							s = seg.group(1).zfill(2)
							e = seg.group(2).zfill(2)
							evnt.append("{}SE : {}S{}E{}".format(keyColorA, keyColorB, s, e))
				except:
					pass
			if "ReleaseDate" in self.type or "Year" in self.type:
				try:
					if "release_date" in str(read_json):
						rd = read_json["release_date"]
						evnt.append("{}ReleaseDate : {}{}".format(keyColorA, keyColorB, rd))
				except:
					pass
			if "AirDate" in self.type or "Year" in self.type:
				try:
					year = ''
					fd = fd.replace('(', '').replace(')', '')
					fdl = ['\d{4} [A-Z]+','[A-Z]*,.* \d{4}', '[A-Z]+ \d{4}', '[A-Z][a-z]+\s\d{4}', '\+\d+\s\d{4}']
					for i in fdl:
						year = re.findall(i, fd)
						if year:
							year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
							evnt.append("{}AirDate : {}{}".format(keyColorA, keyColorB, year))
							break
				except:
					pass
			if "Budget" in self.type:
				try:
					if "budget" in str(read_json):
						rd = read_json["budget"]
						evnt.append("{}Budget : {}{}".format(keyColorA, keyColorB, rd))
				except:
					pass
			if "Revenue" in self.type:
				try:
					if "revenue" in str(read_json):
						rd = read_json["revenue"]
						evnt.append("{}Revenue : {}{}".format(keyColorA, keyColorB, rd))
				except:
					pass
			if "Countries" in self.type or "Country" in self.type:
				try:
					if "countries" in str(read_json):
						rd = read_json["countries"]
						evnt.append("{}Countries : {}{}".format(keyColorA, keyColorB, rd))
				except:
					pass

			if "Actors" in self.type:
				try:
					for i in range(3):
						actr = list(read_json["actors"].keys())[i]
						evnt.append("{}Actors :{}{}".format(keyColorA, keyColorB, actr))
				except:
					pass
			if "Director" in self.type:
				try:
					if "director" in str(read_json):
						rd = read_json["director"]
						evnt.append("{}Director : {}{}".format(keyColorA, keyColorB, rd))
					elif "creator" in str(read_json):
						rd = read_json["creator"]
						evnt.append("{}Creator : {}{}".format(keyColorA, keyColorB, rd))
				except:
					pass
			if "Crews" in self.type:
				try:
					for i in range(3):
						crw = list(read_json["crews"].keys())[i]
						evnt.append("{}Crews :{}{}".format(keyColorA, keyColorB, crw))
				except:
					pass
			if "Description" in self.type:
				try:
					if "TMDB" in self.type:
						descr = read_json["desc"]
						evnt.append("{}Description :{}{}".format(keyColorA, keyColorB, descr))
					elif "TMDB" in self.type:
						descr = read_json["description"]
						evnt.append("{}Description :{}{}".format(keyColorA, keyColorB, descr))
					else:
						evnt.append("{}Description :{}{}".format(keyColorA, keyColorB, fd))
				except:
					pass
			if "TMDB" in self.type:
				if "Rating" in self.type:
					try:
						TMDBrating = read_json["tmdbRating"] * 10
						TMDBvote = read_json["tmdbVote"]
						evnt.append("{}TMDB : {}{}%({})".format(keyColorA, keyColorB, TMDBrating, TMDBvote))
					except:
						pass
				elif "RatingSimple" in self.type:
					try:
						tmdbRating = read_json["tmdbRating"]
						evnt.append("{}".format(tmdbRating))
					except:
						pass
			elif "IMDB" in self.type and "Rating" in self.type:
					try:
						read_json = {}
						json_imdb = "{}xtraEvent/imdb/casts/{}/{}_info.json".format(pathLoc, evntNm, evntNm)
						json_tmdb = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
						if os.path.exists(json_imdb):
							with open(json_imdb) as f:
								read_json_imdb = json.load(f)
							IMDBrating = read_json_imdb["rating"]
							IMDBvote = read_json_imdb["ratingVote"]
							evnt.append("{}IMDB : {}{}({})".format(keyColorA, keyColorB, IMDBrating, IMDBvote))
						elif os.path.exists(json_tmdb):
							with open(json_tmdb) as f:
								read_json_tmdb = json.load(f)
							IMDBratingg = read_json_tmdb["imdbRating"]
							IMDBvotee = read_json_tmdb["imdbRatingVote"]
							evnt.append("{}IMDB : {}{}({})".format(keyColorA, keyColorB, IMDBratingg, IMDBvotee))
					except Exception as err:
						from Tools.xtraTool import errorlog
						errorlog(err, __file__)
			elif "IMDB" in self.type and "RatingSimple" in self.type:
					try:
						read_json = {}
						json_imdb = "{}xtraEvent/imdb/casts/{}/{}_info.json".format(pathLoc, evntNm, evntNm)
						json_tmdb = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
						if os.path.exists(json_imdb):
							with open(json_imdb) as f:
								read_json_imdb = json.load(f)
							IMDBrating = read_json_imdb["rating"]
							IMDBvote = read_json_imdb["ratingVote"]
							evnt.append("{}\n{}".format(IMDBrating, IMDBvote))
						elif os.path.exists(json_tmdb):
							with open(json_tmdb) as f:
								read_json_tmdb = json.load(f)
							IMDBratingg = read_json_tmdb["imdbRating"]
							IMDBvotee = read_json_tmdb["imdbRatingVote"]
							evnt.append("{}\n{}".format(IMDBratingg, IMDBvotee))
					except:
						pass
			else:
				if self.type == "imdbRating":
					try:
						read_json = {}
						json_imdb = "{}xtraEvent/imdb/casts/{}/{}_info.json".format(pathLoc, evntNm, evntNm)
						json_tmdb = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
						if os.path.exists(json_imdb):
							with open(json_imdb) as f:
								read_json_imdb = json.load(f)
							IMDBrating = read_json_imdb["rating"]
							IMDBvote = read_json_imdb["ratingVote"]
							evnt.append("{}IMDB : {}{}({})".format(keyColorA, keyColorB, IMDBrating, IMDBvote))
						elif os.path.exists(json_tmdb):
							with open(json_tmdb) as f:
								read_json_tmdb = json.load(f)
							IMDBratingg = read_json_tmdb["imdbRating"]
							IMDBvotee = read_json_tmdb["imdbRatingVote"]
							evnt.append("{}IMDB : {}{}({})".format(keyColorA, keyColorB, IMDBratingg, IMDBvotee))
					except Exception as err:
						from Tools.xtraTool import errorlog
						errorlog(err, __file__)
				elif "Rating" in self.type:
					try:
						TMDBrating = int(read_json["tmdbRating"]) * 10
						TMDBvote = read_json["tmdbVote"]
						evnt.append("{}TMDB : {}{}%({})".format(keyColorA, keyColorB, TMDBrating, TMDBvote))
					except:
						pass
				elif "RatingSimple" in self.type:
					try:
						tmdbRating = read_json["tmdbRating"]
						evnt.append("{}".format(tmdbRating))
					except:
						pass
					
					
			# tc = '\c0000??00 '
			# tc += '\c00??????'
			# tc = tc.join(evnt)
			if " " in self.type:
				tc = "\n".join(evnt)
			elif "•" in self.type:
				tc = " • ".join(evnt)
			else:
				tc = "\n".join(evnt)
			return tc
	text = property(getText)

	@cached
	def getValue(self):
		event = self.source.event
		if event:
			evnt = event.getEventName()
			evntNm = REGEX.sub('', evnt).strip()
			try:
				if "RatingProgress" in self.type:
					if "IMDB" in self.type:
						try:
							rating_json = "{}xtraEvent/imdb/casts/{}/{}_info.json".format(pathLoc, evntNm, evntNm)
							if os.path.exists(rating_json):
								with open(rating_json) as f:
									read_json = json.load(f)
								imdbRatingValue = read_json["rating"]
								if imdbRatingValue:
									return int(10*(float(imdbRatingValue)))
								else:
									return 0
							else:
								rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
								if os.path.exists(rating_json):
									with open(rating_json) as f:
										read_json = json.load(f)
									imdbRatingValue = read_json["imdbRating"]
									if imdbRatingValue:
										return int(10*(float(imdbRatingValue)))
									else:
										return 0
						except:
							return 0
					elif "TMDB" in self.type:
						try:
							rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
							try:
								if os.path.exists(rating_json):
									with open(rating_json) as f:
										read_json = json.load(f)
								else:
									return
							except:
								return
							tmdbRatingValue = read_json["tmdbRating"]
							if tmdbRatingValue:
								return int(10*(float(tmdbRatingValue)))
							else:
								return 0
						except:
							return 0
			except:
				return 0
		else:
			return 0

	value = property(getValue)
	range = 100
	
	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)
