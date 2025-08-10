# -*- coding: utf-8 -*-
# by digiteng...
# 07.2020 - 11.2020 - 11.2021
# <widget render="xtraParental" source="session.Event_Now" position="0,0" size="60,60" alphatest="blend" zPosition="2" transparent="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadPNG
from Components.config import config
import re
import json
import os
from Plugins.Extensions.xtraEvent.skins.xtraSkins import *
from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile

########################### log file loeschen ##################################
dir_path = "/tmp/xtraevent"
try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Verzeichnis wurde erstellt:", dir_path)
    else:
        print("Verzeichnis existiert bereits:", dir_path)
except Exception as e:
    print("Fehler beim Erstellen des Verzeichnisses:", e)

myfile = dir_path + "/parental.log"
## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)

logstatus = "off"
if config.plugins.xtraEvent.logFiles.value == True:
    logstatus = "on"
else:
    logstatus = "off"

def write_log(msg):
    if logstatus == 'on':
        with open(myfile, "a") as log:
            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")
            return
    return

def logout(data):
    if logstatus == 'on':
        write_log(data)
        return
    return

logout(data="start")

try:
    import sys
    if sys.version_info[0] == 3:
        from builtins import str
except:
    pass

pratePath = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/parental/"
try:
    pathLoc = config.plugins.xtraEvent.loc.value
    logout(data="start pathloc")
    logout(data=str(pathLoc))
except:
    pathLoc = ""

REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'
    r'(: odc.\d+)|'
    r'(\d+: odc.\d+)|'
    r'(\d+ odc.\d+)|(:)|'
    r'!|'
    r'/.*|'
    r'\|\s[0-9]+\+|'
    r'[0-9]+\+|'
    r'\s\d{4}\Z|'
    r'([\(\[\|].*?[\)\]\|])|'
    r'(\"|\"\.|\"\,|\.)\s.+|'
    r'\"|:|'
    r'\*|'
    r'Премьера\.\s|'
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
    r'(х|Х|м|М|т|Т|д|Д)/с\s|'
    r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
    r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
    r'\d{1,3}(-я|-й|\sс-н).+|'
    r'\sح\s*\d+|'                # Entfernt Episodennummern in arabischen Serien
    r'\sج\s*\d+|'                # Entfernt Staffelangaben in arabischen Serien
    r'\sم\s*\d+|'                # Entfernt weitere Staffelangaben in arabischen Serien
    r'\d+$', re.DOTALL
)

class xtraParental(Renderer):

    def __init__(self):
        logout(data="init")
        Renderer.__init__(self)
        self.rateNm = ''

    GUI_WIDGET = ePixmap
    def changed(self, what):
        logout(data="changed")
        if not self.instance:
            return
        else:
            logout(data="rate-prate-parentname")
            rate = ""
            prate = ""
            parentName = ""
            event = self.source.event
            if event:
                logout(data="event")
                fd = "{}{}{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())
                ppr = [r"[aA]b ((\d+))", r"[+]((\d+))", r"Od lat: ((\d+))"]
                for i in ppr:
                    logout(data="for i")
                    prr = re.search(i, fd)
                    if prr:
                        logout(data="prr")
                        logout(data=str(prr))
                        try:
                            logout(data="prr1")
                            parentName = prr.group(1)
                            parentName = parentName.replace("7", "6")
                            break
                        except:
                            logout(data="prr2")
                            pass
                else:
                    logout(data="event 2")
                    evnt = event.getEventName()
                    logout(data="event")
                    logout(data=str(evnt))
                    evntNm = REGEX.sub('', evnt).strip()
                    logout(data="evntNm")
                    logout(data=str(evntNm))
                    rating_json = "{}xtraEvent/infosomdb/{}.json".format(pathLoc, evntNm)
                    logout(data="rating json")
                    logout(data=str(rating_json))
                    if os.path.exists(rating_json):
                        logout(data="json path check")
                        try:
                            logout(data="json vorhanden")
                            with open(rating_json) as f:
                                prate = json.load(f)['Rated']
                        except:
                            pass
                    logout(data="prate")
                    logout(data=str(prate))
                    if prate == "TV-Y7":
                        rate = "6"
                    elif prate == "TV-Y":
                        rate = "6"
                    elif prate == "TV-14":
                        rate = "12"
                    elif prate == "TV-PG":
                        rate = "16"
                    elif prate == "TV-G":
                        rate = "0"
                    elif prate == "TV-MA":
                        rate = "18"
                    elif prate == "PG-13":
                        rate = "16"
                    elif prate == "R":
                        rate = "18"
                    elif prate == "G":
                        rate = "0"
                    else:
                        pass
                    if rate:
                        logout(data="rate leer schreibe parentName")
                        parentName = str(rate)

                if parentName:
                    logout(data="parentName")
                    logout(data=str(parentName))
                    rateNm = "{}FSK_{}.png".format(pratePath, parentName)
                    logout(data="rateNm")
                    logout(data=str(rateNm))
                    # Sicherstellen, dass das Bild existiert, bevor es geladen wird
                    if os.path.exists(rateNm):
                        self.instance.setPixmap(loadPNG(rateNm))
                    else:
                        logout(data="Bild {} nicht gefunden, Fallback auf FSK_NA.png".format(rateNm))
                        self.instance.setPixmap(loadPNG("{}FSK_NA.png".format(pratePath)))
                    self.instance.setScale(1)
                    self.instance.show()
                else:
                    logout(data="parentName-NA")
                    # Sicherstellen, dass das FSK_NA.png Bild existiert
                    if os.path.exists("{}FSK_NA.png".format(pratePath)):
                        self.instance.setPixmap(loadPNG("{}FSK_NA.png".format(pratePath)))
                    else:
                        logout(data="FSK_NA.png nicht gefunden!")
                    self.instance.setScale(1)
                    self.instance.show()
            else:
                logout(data="parentName-NA-2")
                # Sicherstellen, dass das FSK_NA.png Bild existiert
                if os.path.exists("{}FSK_NA.png".format(pratePath)):
                    self.instance.setPixmap(loadPNG("{}FSK_NA.png".format(pratePath)))
                else:
                    logout(data="FSK_NA.png nicht gefunden!")
                self.instance.setScale(1)
                self.instance.show()
            return
