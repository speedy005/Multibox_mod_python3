# iVpn Converter by speedy005
# This converter is free to use and modify, but the copyright notice must not be removed.
# Compatible with all Python 3 and Python 2 images.

from os import path, listdir
from os.path import exists
from subprocess import run, CalledProcessError, Popen, PIPE
from Components.Converter.Converter import Converter
from Components.Element import cached

class xDreamy_iVpn(Converter):
    VPNLOAD = 0

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'vpn':
            self.type = self.VPNLOAD
        self.has_wireguard = exists("/usr/bin/wg")
        self.has_openvpn = exists("/var/run/openvpn")

    @cached
    def getBoolean(self):
        # Check for OpenVPN
        if self.has_openvpn and self.is_openvpn_active():
            return True

        # Check for WireGuard
        if self.has_wireguard and self.is_wireguard_active():
            return True

        return False

    def is_openvpn_active(self):
        try:
            # Nutzt die run_command Funktion, die Python 2 und 3 unterstützt
            result = self.run_command(['ip', 'link', 'show', 'tun0'])
            return result and "tun0" in result
        except (CalledProcessError, OSError, IOError):
            return False

    def is_wireguard_active(self):
        try:
            # Nutzt die run_command Funktion, die Python 2 und 3 unterstützt
            result = self.run_command(['ip', 'link', 'show', 'wg0'])
            return result and "wg0" in result
        except (CalledProcessError, OSError, IOError):
            return False

    def run_command(self, command):
        """
        Führt einen Shell-Befehl aus und gibt dessen Ausgabe zurück.
        Hier wird Kompatibilität zu Python 2 und Python 3 hergestellt:
        
        - In Python 3 kann man subprocess.run() verwenden.
        - In Python 2 gibt es subprocess.run() nicht, daher wird Popen mit communicate() genutzt.
        - Außerdem wird die Ausgabe von bytes in einen String dekodiert (nur relevant für Python 3).
        """
        try:
            # Prüfen, ob Popen.communicate verfügbar ist (ja, in Python 2 und 3)
            if hasattr(Popen, 'communicate'):
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                output, _ = process.communicate()
                # Falls output bytes sind (Python 3), in String umwandeln
                return output.decode('utf-8') if isinstance(output, bytes) else output
            else:
                # Fallback (theoretisch nie nötig, da communicate fast immer da ist)
                # Hier wird run() verwendet (nur Python 3)
                return "".join(run(command, capture_output=True, text=True).stdout)
        except (CalledProcessError, OSError, IOError):
            # Fehlerbehandlung für Python 2 und 3
            return ""

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
