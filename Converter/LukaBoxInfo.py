# -*- coding: utf-8 -*-
# Luka-BoxInfo
# Copyright (c) speedy005 2025
# v.1.0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# mod by speedy005
# LukaBoxInfo - Enhanced system information converter for Enigma2
# Copyright (c) speedy005 2025, Updated 2025
# License: GNU GPL v3
# LukaBoxInfo – System Converter for Enigma2
# Updated 2025 – includes CPU usage, speed in GHz, skin and uptime fixes

from __future__ import print_function  # Python 2/3 print compatibility
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.config import config
from Components.Element import cached
from os.path import isfile
from os import popen
import time
import sys

class LukaBoxInfo(Poll, Converter, object):
    Boxtype, CpuInfo, HddTemp, TempInfo, FanInfo, Upinfo, CpuLoad, CpuSpeed, CpuUsage, SkinInfo, TimeInfo, TimeInfo2, TimeInfo3, TimeInfo4, PythonVersion = range(15)

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 2000
        self.poll_enabled = True
        self.last_idle = 0
        self.last_total = 0

        type_map = {
            "Boxtype": self.Boxtype,
            "CpuInfo": self.CpuInfo,
            "HddTemp": self.HddTemp,
            "TempInfo": self.TempInfo,
            "FanInfo": self.FanInfo,
            "Upinfo": self.Upinfo,
            "CpuLoad": self.CpuLoad,
            "CpuSpeed": self.CpuSpeed,
            "CpuUsage": self.CpuUsage,
            "SkinInfo": self.SkinInfo,
            "TimeInfo": self.TimeInfo,
            "TimeInfo2": self.TimeInfo2,
            "TimeInfo3": self.TimeInfo3,
            "TimeInfo4": self.TimeInfo4,
            "PythonVersion": self.PythonVersion,
        }

        self.type = type_map.get(type, self.Boxtype)

    @cached
    def getText(self):
        if self.type == self.Boxtype:
            try:
                from Components.SystemInfo import BoxInfo
                brand = BoxInfo.getItem("displaybrand") or ""
                model = BoxInfo.getItem("displaymodel") or ""
                return "{} {}".format(brand, model).strip()
            except Exception:
                return popen("head -n1 /etc/hostname").read().strip()

        elif self.type == self.CpuInfo:
            if isfile("/proc/cpuinfo"):
                model = ""
                cores = 0
                try:
                    for line in open("/proc/cpuinfo"):
                        if line.lower().startswith("model name"):
                            model = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("processor"):
                            cores += 1
                    return "{} ({} cores)".format(model, cores)
                except Exception:
                    return "Keine CPU-Info"
            return "Keine CPU-Info"

        elif self.type == self.HddTemp:
            try:
                temp = popen("hddtemp -n -q /dev/sda").read().strip()
                if temp:
                    return "HDD Temp: {}°C".format(temp)
                return "Keine HDD-Temp"
            except Exception:
                return "Keine HDD-Temp"

        elif self.type == self.TempInfo:
            paths = [
                "/sys/class/thermal/thermal_zone0/temp",
                "/proc/stb/fp/temp_sensor",
                "/proc/stb/fp/temp_sensor0",
            ]
            for path in paths:
                if isfile(path):
                    try:
                        val = open(path).read().strip()
                        temp = int(val)
                        if temp > 1000:
                            temp //= 1000
                        return "Box-Temp: {}°C".format(temp)
                    except Exception:
                        continue
            return "Keine Temperaturinfo"

        elif self.type == self.FanInfo:
            path = "/proc/stb/fp/fan_speed"
            if isfile(path):
                try:
                    speed = open(path).read().strip()
                    return "{} RPM".format(speed)
                except Exception:
                    return "Fehler bei Lüfterdaten"
            return "Keine Lüfterinfo"

        elif self.type == self.Upinfo:
            try:
                with open('/proc/uptime', 'r') as file:
                    uptime_info = file.read().split()
            except Exception:
                return ' '
            if uptime_info:
                total_seconds = float(uptime_info[0])
                MINUTE = 60
                HOUR = MINUTE * 60
                DAY = HOUR * 24
                days = int(total_seconds / DAY)
                hours = int((total_seconds % DAY) / HOUR)
                minutes = int((total_seconds % HOUR) / MINUTE)
                uptime = ""
                uptime += "{} {}".format(days, "Tag" if days == 1 else "Tage") + " "
                uptime += "{:02d} std ".format(hours)
                uptime += "{:02d} min".format(minutes)
                return "Uptime: {}".format(uptime.strip())
            return "Uptime: 0 Tage 00 std 00 min"

        elif self.type == self.CpuLoad:
            try:
                load = float(open('/proc/loadavg').read().split()[0])
                return "{:.2f}".format(load)
            except Exception:
                return "Keine CPU-Lastinfo"

        elif self.type == self.CpuSpeed:
            try:
                if isfile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"):
                    khz = int(open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").read().strip())
                    return "{:.2f} GHz".format(khz / 1_000_000.0)
                else:
                    for line in open("/proc/cpuinfo"):
                        if line.lower().startswith("cpu mhz"):
                            mhz = float(line.split(":",1)[1].strip())
                            return "{:.2f} GHz".format(mhz / 1000.0)
            except Exception:
                return "Keine CPU-Geschwindigkeit"

        elif self.type == self.CpuUsage:
            try:
                parts = open("/proc/stat").readline().split()[1:]
                vals = list(map(int, parts))
                idle = vals[3] + vals[4]
                total = sum(vals)
                if self.last_total:
                    d_idle = idle - self.last_idle
                    d_total = total - self.last_total
                    usage = (1 - float(d_idle) / d_total) * 100 if d_total else 0.0
                else:
                    usage = 0.0
                self.last_idle, self.last_total = idle, total
                return "CPU: {:.1f}%".format(usage)
            except Exception:
                return "Keine CPU-Auslastung"

        elif self.type == self.SkinInfo:
            try:
                name = config.skin.primary_skin.value if hasattr(config.skin, "primary_skin") else config.skin.value
                if name.endswith("/skin.xml"):
                    name = name[:-9]
                elif name.endswith(".xml"):
                    name = name[:-4]
                if "/" in name:
                    name = name.split("/")[-1]
                return name
            except Exception:
                return "Kein Skin gesetzt"

        elif self.type == self.TimeInfo:
            return time.strftime("%H:%M:%S")

        elif self.type == self.TimeInfo2:
            return time.strftime("%d.%m.%Y")

        elif self.type == self.TimeInfo3:
            return time.strftime("%H:%M")

        elif self.type == self.TimeInfo4:
            return time.strftime("%Y-%m-%d %H:%M:%S")

        elif self.type == self.PythonVersion:
            try:
                from Screens.About import about
                return "Python {}".format(about.getPythonVersionString())
            except Exception:
                v = sys.version_info
                return "Python {}.{}.{}".format(v[0], v[1], v[2])

        return ""

    text = property(getText)
