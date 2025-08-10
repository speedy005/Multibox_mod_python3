from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from enigma import eLabel, eTimer
import os
import re
## <widget source="session.CurrentService" render="AglareECMInfoRenderer" position="37,489" size="400,300" font="Regular;18" /> ##
class Metrixfhd_neo_ECMInfoRenderer(Renderer, VariableText):
    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.poll_timer = eTimer()
        self.poll_timer.timeout.get().append(self.poll)
        self.poll_interval = 2000  # 2 seconds
        self.debug = False  # Set to True for debugging
        
    GUI_WIDGET = eLabel
    
    def onShow(self):
        self.poll_timer.start(self.poll_interval)
        self.changed(None)
        
    def onHide(self):
        self.poll_timer.stop()
        
    def poll(self):
        self.changed(None)
        
    def debug_log(self, message):
        if self.debug:
            print(f"[ECMInfoRenderer] {message}")
            
    def get_ecm_data(self):
        ecm_info = {}
        try:
            if not os.path.exists("/tmp/ecm.info"):
                return None  # File doesn't exist
                
            if os.path.getsize("/tmp/ecm.info") <= 0:
                return {}    # File is empty
                
            with open("/tmp/ecm.info", "r") as f:
                for line in f:
                    line = line.strip()
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        # Handle special cases
                        if key == "from":
                            # Extract both server and port from "from" field
                            if ":" in value:
                                server, port = value.split(":", 1)
                                ecm_info["server"] = server.strip()
                                ecm_info["port"] = port.strip()
                            else:
                                ecm_info["server"] = value
                        elif key in ["cw0", "cw1"]:
                            # Keep full CW value but remove extra spaces
                            value = " ".join(value.split())
                        ecm_info[key] = value
        except Exception as e:
            self.debug_log(f"Error reading ecm.info: {str(e)}")
        return ecm_info
    
    def format_hex(self, value):
        try:
            if value.startswith("0x"):
                value = value[2:]
            return "%0.4X" % int(value, 16)
        except:
            return value
            
    def format_provider(self, prov):
        try:
            if prov.startswith("0x"):
                prov = prov[2:]
            return "%0.6X" % int(prov, 16)
        except:
            return prov
            
    def changed(self, what):
        if self.instance:
            ecm_info = self.get_ecm_data()
            lines = []
            
            if ecm_info is None:
                self.text = "Free to Air"
                return
                
            if not ecm_info:  # Empty file
                self.text = "Waiting for ECM data..."
                return
                
            # Required fields in display order
            fields = [
                ("Protocol", "protocol"),
                ("Reader", "reader"),
                ("Address", lambda: ecm_info.get("from", 
                                  f"{ecm_info.get('server','N/A')}:{ecm_info.get('port','')}" 
                                  if ecm_info.get('server') else "N/A")),
                ("CAID", "caid"),
                ("PID", "pid"),
                ("Provider", "prov"),
                ("CHID", "chid"),
                ("Hops", "hops"),
                ("ECM Time", "ecm time"),
                ("CW0", "cw0"),
                ("CW1", "cw1")
            ]
            
            for label, key in fields:
                try:
                    if callable(key):
                        value = key()
                    else:
                        value = ecm_info.get(key, "N/A")
                        if key in ["caid", "pid"]:
                            value = self.format_hex(value)
                        elif key == "prov":
                            value = self.format_provider(value)
                    
                    lines.append(f"{label}: {value}")
                except Exception as e:
                    self.debug_log(f"Error processing {label}: {str(e)}")
                    lines.append(f"{label}: Error")
            
            self.text = "\n".join(lines)