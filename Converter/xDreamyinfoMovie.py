# -*- coding: utf-8 -*-
#geht in Py2 und Py3
# by digiteng...02.2020
#    <widget source="session.Event_Now" render="Label" position="210,166" size="679,100" font="Regular; 14" backgroundColor="tb" zPosition="2" transparent="1" halign="left" valign="top">
#      <convert type="infoMovie">INFO</convert>
#    </widget>
#    <ePixmap pixmap="LiteHD2/star_b.png" position="0,277" size="200,20" alphatest="blend" zPosition="0" transparent="1" />
#    <widget source="session.Event_Now" render="Progress" pixmap="LiteHD2/star.png" position="0,277" size="200,20" alphatest="blend" zPosition="1" transparent="1">
#      <convert type="infoMovie">STARS</convert>
#    </widget>
from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import os
import sys

import urllib.request
from urllib.error import URLError

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile



########################### log file loeschen ##################################

myfile="/tmp/Kitte888InfoMovie.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"


# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start")


api = 'b1538d0b'
ablauf = "1234"

#PY3 = (sys.version_info[0] == 3)
if sys.version_info[0] >= 3:
    import urllib.request, urllib.error, urllib.parse
    #open("/tmp/infomovie_py3.txt", "w").write(ablauf)
else:
    import urllib2
    #open("/tmp/infomovie_py2.txt", "w").write(ablauf)





class xDreamyinfoMovie(Converter, object):

    def __init__(self, type):
        logout(data="init")
        Converter.__init__(self, type)
        self.type = type

    @cached
    def getText(self):
        logout(data="getText")
        event = self.source.event
        logout(data="event")
        logout(data=str(event))
        if event:
            logout(data="if event")
            if self.type == 'INFO':
                logout(data="if self type")
                try:
                    logout(data="evnt")
                    evnt = event.getEventName()
                    logout(data=str(evnt))
                    try:
                        p = '((.*?))[;=:-].*?(.*?)'
                        e1 = re.search(p, evnt)
                        ffilm = re.sub('\W+','&', e1.group(1))
                    except:
                        w = re.sub("([\(\[]).*?([\)\]])", " ", evnt)
                        ffilm = re.sub('\W+','&', w)

                    url = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(api, ffilm.lower())
                    logout(data=str(url))
                    if sys.version_info[0] >= 3:
                        data = json.load(urllib.request.urlopen(url))
                    else:
                        data = json.load(urllib2.urlopen(url))
                    #open("/tmp/infomovie_url.txt", "w").write(url)

                    title = data['Title']
                    rtng = data['imdbRating']
                    country = data['Country']
                    year = data['Year']
                    rate = data['Rated']
                    genre = data['Genre']
                    award = data['Awards']
                    #open("/tmp/infomovie_rate.txt", "w").write(rate)

                    if title:
                        return "Title : %s"%str(title) + "\nImdb : %s"%str(rtng) + "\nYear : %s, %s"%(str(country), str(year.encode('utf-8'))) + "\nRate : %s"%str(rate) + "\nGenre : %s"%str(genre) + "\nAwards : %s" %str(award)

                except:
                    return ""
        else:
            return ""

    text = property(getText)


    @cached
    def getValue(self):
        logout(data="getValue-start")
        event = self.source.event
        logout(data="event")
        logout(data=str(event))
        if event:
            logout(data="if event")

            if self.type == 'STARS':
                logout(data="if stars")
                try:
                    logout(data="evnt")
                    evnt = event.getEventName()
                    logout(data=str(evnt))
                    try:
                        p = '((.*?))[;=:-].*?(.*?)'
                        e1 = re.search(p, evnt)
                        ffilm = re.sub('\W+','&', e1.group(1))
                    except:
                        w = re.sub("([\(\[]).*?([\)\]])", " ", evnt)
                        ffilm = re.sub('\W+','&', w)

                    url = 'https://www.omdbapi.com/?apikey=%s&t=%s' %(api, ffilm.lower())
                    logout(data="url")
                    logout(data=str(url))

                    if sys.version_info[0] >= 3:
                        logout(data="data json")
                        #data = json.load(urllib.request.urlopen(url))
                        response = urllib.request.urlopen(url, timeout=10)
                    else:
                        logout(data="data json 2")
                        #data = json.load(urllib2.urlopen(url))
                        response = urllib2.urlopen(url, timeout=10)
                    data = json.load(response)

                    logout(data="data json imdbRating holen")
                    rtng = data['imdbRating']
                    logout(data=str(rtng))

                    if rtng == "N/A" or  rtng == "":
                        return 0
                    else:
                        logout(data="mal 10")
                        return int(10*(float(rtng)))

                except urllib.error.URLError as e:
                    print("Fehler beim Abrufen der Daten:", e)
                    rating_value = 0
                except json.JSONDecodeError as e:
                    print("Fehler beim Verarbeiten der JSON-Daten:", e)
                    rating_value = 0
                except Exception as e:
                    print("Unbekannter Fehler:", e)
                    rating_value = 0


                #except:
                #    return 0
        else:
            return 0

    logout(data="ende")
    value = property(getValue)
    range = 100
