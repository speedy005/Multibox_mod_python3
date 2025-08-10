# -*- coding: utf-8 -*-
# by digiteng...02.2020, improved for Py2 & Py3 compatibility 2025

from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import re
import sys
from datetime import datetime
from os.path import isfile
from os import remove

try:
    # Python 3 imports
    import urllib.request as urllib_request
    import urllib.parse as urllib_parse
    from urllib.error import URLError
except ImportError:
    # Python 2 imports
    import urllib2 as urllib_request
    import urllib
    URLError = urllib_request.URLError

myfile = "/tmp/Kitte888InfoMovie.log"
logstatus = "on"

# Logfile löschen, falls vorhanden
if isfile(myfile):
    remove(myfile)

def write_log(msg):
    if logstatus == 'on':
        # Python 2 und 3 kompatibel öffnen
        import io
        with io.open(myfile, "a", encoding="utf-8") as log:
            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

def logout(data):
    if logstatus == 'on':
        write_log(data)

logout("start")

API_KEY = 'b1538d0b'

def sanitize_title(title):
    # Erlaubt nur Buchstaben, Zahlen, Leerzeichen; andere durch '&' ersetzen
    # Python2 & 3 kompatibel
    if sys.version_info[0] < 3:
        if isinstance(title, unicode):
            cleaned = re.sub(r'[^\w\s]', '&', title)
        else:
            cleaned = re.sub(r'[^\w\s]', '&', title.decode('utf-8'))
    else:
        cleaned = re.sub(r'[^\w\s]', '&', title)
    return cleaned.strip()

def fetch_movie_data(title):
    """Hole Daten von OMDb API, Titel muss bereits gesäubert sein."""
    try:
        if sys.version_info[0] >= 3:
            encoded_title = urllib_parse.quote(title.lower())
        else:
            encoded_title = urllib.quote(title.lower())
        url = 'https://www.omdbapi.com/?apikey={}&t={}'.format(API_KEY, encoded_title)
        logout("Fetching URL: {}".format(url))

        if sys.version_info[0] >= 3:
            with urllib_request.urlopen(url, timeout=10) as response:
                data = json.load(response)
        else:
            response = urllib_request.urlopen(url, timeout=10)
            data = json.load(response)

        return data
    except URLError as e:
        logout("URLError: {}".format(e))
    except ValueError as e:  # json.JSONDecodeError gibt es nur in Py3.5+, in Py2 ValueError
        logout("JSON Error: {}".format(e))
    except Exception as e:
        logout("Unexpected error: {}".format(e))
    return None

class Luka_FHD_infoMovie(Converter):

    def __init__(self, type):
        logout("init")
        Converter.__init__(self, type)
        self.type = type

    @cached
    def getText(self):
        logout("getText")
        event = self.source.event
        if not event:
            return ""
        try:
            evnt_name = event.getEventName()
            logout("Event name: {}".format(evnt_name))

            # Regex um Titelteile zu extrahieren
            match = re.search(r'((.*?))[;=:-].*?(.*?)', evnt_name)
            if match:
                title_raw = match.group(1)
            else:
                title_raw = re.sub(r"[\(\[].*?[\)\]]", " ", evnt_name)

            title_clean = sanitize_title(title_raw)
            logout("Clean title: {}".format(title_clean))

            data = fetch_movie_data(title_clean)
            if not data or data.get('Response') == 'False':
                return ""

            title = data.get('Title', '')
            rtng = data.get('imdbRating', 'N/A')
            country = data.get('Country', '')
            year = data.get('Year', '')
            rate = data.get('Rated', '')
            genre = data.get('Genre', '')
            award = data.get('Awards', '')

            if title:
                # In Python2/3 sicher formatieren (unicode Probleme vermeiden)
                return u"Title : {}\nImdb : {}\nYear : {}, {}\nRate : {}\nGenre : {}\nAwards : {}".format(
                    title, rtng, year, country, rate, genre, award
                )
        except Exception as e:
            logout("Error in getText: {}".format(e))
        return ""

    text = property(getText)

    @cached
    def getValue(self):
        logout("getValue")
        event = self.source.event
        if not event or self.type != 'STARS':
            return 0
        try:
            evnt_name = event.getEventName()
            logout("Event name: {}".format(evnt_name))

            match = re.search(r'((.*?))[;=:-].*?(.*?)', evnt_name)
            if match:
                title_raw = match.group(1)
            else:
                title_raw = re.sub(r"[\(\[].*?[\)\]]", " ", evnt_name)

            title_clean = sanitize_title(title_raw)
            logout("Clean title: {}".format(title_clean))

            data = fetch_movie_data(title_clean)
            if not data or data.get('Response') == 'False':
                return 0

            rtng = data.get('imdbRating', 'N/A')
            if rtng in ("N/A", ""):
                return 0
            rating_float = float(rtng)
            return int(rating_float * 10)
        except Exception as e:
            logout("Error in getValue: {}".format(e))
            return 0

    value = property(getValue)
    range = 100
