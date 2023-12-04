import serial
import time
import threading

class Arduino:  
    
    def __init__(self):
        self.serial_port = serial.Serial('COM6', 115200)
        self.latest_data = None
        self.data_lock = threading.Lock()
        self.running = True
        self.read_thread = threading.Thread(target=self.read_data)
        self.read_thread.start()
        
    
    def read_data(self):
        while self.running:
            try:     
                data = self.serial_port.readline().decode('utf-8').strip()    
                if data:
                    self.latest_data = data
            except:
                pass
    
    def stop(self):
        self.running = False
        self.read_thread.join()
    
    def get_latest_data(self):
        with self.data_lock:
            return self.latest_data
    
    def send_data(self, data):
        self.serial_port.write(data.encode('utf-8'))
