import serial
import serial.tools.list_ports
import json

class SerialDevice():
    def __init__(self, *args, **kwargs):
        self.device = {}

    def find_device_port(self):
        ports = {}
        try:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if ("VID:PID=1A86:7523" in port.hwid) or ("VID:PID=2341:0043" in port.hwid):
                    return port.device
        except:
            print("Error buscando puertos serie")

        return ""  

    def open(self, port):
        if not port:
            port = self.find_device_port()
        try:    
            self.device = serial.Serial(port, 115200, timeout=1)
        except:
            return False
        
        return True

    def close(self):
        try:
            self.device.close()
            return True
        except:
            return False

    def is_open(self):
        try:
            return self.device.is_open
        except:
            return False

    def send_cmd(self, msg):
        try:
            if (self.device.is_open == True):
                # Limpiar el buffer de recepcion.
                self.device.flushInput()
                self.device.flushOutput()
                self.device.write(msg.encode(encoding='ascii')) 
        except:
            return False

        return bool(self.device.is_open) 

    def read_answer(self):
        try:
            if (self.device.is_open == True):
                line = self.device.read_until(b'}').decode("utf-8") 
                line = line.replace('\r\n', '')
                return json.loads(line)
        except:
            return {}

        return {}

    def rcv_timeout(self, seconds):
        try:
            self.device.timeout = seconds
        except:
            print("Error setting receive timeout")
        