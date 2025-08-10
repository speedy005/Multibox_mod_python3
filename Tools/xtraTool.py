# -*- coding: utf-8 -*-
# by digiteng...03.2024

from __future__ import absolute_import
from time import strftime
import socket
from Components.config import config
import re

# REGEX mit auskommentierten Altersangaben (16+, 12+ etc. bleiben erhalten)
REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'         # Klammerinhalte
    r'(: odc.\d+)|'                 # : odc.x
    r'(\d+: odc.\d+)|'              # x: odc.x
    r'(\d+ odc.\d+)|'               # x odc.x
    r'(\d+.* \(odc. \d+.*\))|'      # x (odc. x)
    r'!|\?|/|\\|\(|\)|='            # Sonderzeichen
    r'\*|"|%|@|#|'                  
    # r'\|\s[0-9]+\+|'             # auskommentiert, damit Altersangaben bleiben
    # r'[0-9]+\+|'                 # auskommentiert
    r'\s\d{4}\Z|'                   # Jahreszahlen am Ende
    r'([\(\[\|].*?[\)\]\|])|'       
    r'\"|:|'                        
    r'Премьера\.\s|'                
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
    r'(х|Х|м|М|т|Т|д|Д)/с\s|'
    r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
    r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
    r'\d{1,3}(-я|-й|\sс-н).+|',
    re.DOTALL
)

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

try:
    pathLoc = config.plugins.xtrvnt.loc.value
except:
    pathLoc = "/tmp/"

def pathLocation():
    try:
        return config.plugins.xtrvnt.loc.value
    except:
        return "/"

def errorlog(err, filex):
    tm = strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/xtraError.log", "a+") as f:
        f.write("File : {}, {}, \nERROR:{}, \nLine:{}\n\n".format(filex, tm, err, err.__traceback__.tb_lineno))

def eventlog(filex):
    tm = strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/xtraEvent.log", "a+") as f:
        f.write("[{}], {}\n".format(tm, filex))

def intCheck():
    try:
        socket.setdefaulttimeout(2)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except:
        return False

def getLanguage():
    lang = "en"
    try:
        from Components.Language import language
        lang = language.getLanguage()
    except:
        try:
            lang = config.osd.language.value
        except:
            lang = "en"
    return lang[:2]

def version():
    ver = "N/A"
    with open("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/version", "r") as f:
        ver = f.read()
    return ver

def pRating(rate):
    if rate in ["G", "TV-G", "PG", "TV-Y", "TV-PG", "E"]:
        rate = "0"
    elif rate in ["4", "6", "6+", "7", "7A", "7+", "9", "9+", "TV-Y7"]:
        rate = "6"
    elif rate in ["TV-14", "PG-13", "E10+", "T", "T+", "12", "12+", "12A", "13", "13+", "13A", "14", "14+", "14A", "10+"]:
        rate = "12"
    elif rate in ["R", "TV-MA", "M", "16", "16+", "15", "15+"]:
        rate = "16"
    elif rate in ["NC-17", "AO", "MAX", "18", "18+"]:
        rate = "18"
    else:
        rate = "NA"
    return rate

# NEU: Altersfreigabe (z.B. "16+") extrahieren
def extractAgeRating(title):
    match = re.search(r'\b(6|12|16|18)\+', title)
    if match:
        return match.group(0)
    return None

# NEU: Titel bereinigen und Altersfreigabe extrahieren
def cleanTitle(raw_title):
    age = extractAgeRating(raw_title)
    if age:
        raw_title = raw_title.replace(age, "")
    clean = REGEX.sub('', raw_title)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean, age

# Beispiel zur Selbstkontrolle
if __name__ == "__main__":
    test_titles = [
        "Tatort 16+ (Staffel 3)",
        "Lenßen hilft / oder SAT.1: Bayern-Magazin 12+",
        "Filmname 2023 !",
        "М/ф Смешарики 1-я серия",
        "Show 18+ [HD]"
    ]

    for t in test_titles:
        title_clean, age_rating = cleanTitle(t)
        print(f"Original: {t}")
        print(f"Bereinigt: {title_clean}")
        print(f"Altersfreigabe: {age_rating or 'Keine'}")
        print("---")
