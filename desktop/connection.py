import socket
import struct
import threading
from PySide6.QtCore import QObject, Signal

class ConnectionManager(QObject):
    frame_received = Signal(bytes)
    disconnected = Signal()

    def __init__(self, address, port):
        super().__init__()
        self.address = address
        self.port = port
        self.socket = None
        self.running = False
        self.thread = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0) # 5 second timeout for initial connection
            self.socket.connect((self.address, self.port))
            self.socket.settimeout(None) # Back to blocking for the thread
            self.running = True
            self.thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.thread.start()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()
        if self.thread:
            self.thread.join(timeout=1)

    def _receive_loop(self):
        buffer = b""
        try:
            while self.running:
                data = self.socket.recv(4096)
                if not data:
                    break
                buffer += data

                while len(buffer) >= 5:
                    size, type_ = struct.unpack(">IB", buffer[:5])
                    if len(buffer) >= 5 + size:
                        payload = buffer[5:5+size]
                        if type_ == 1 or type_ == 0: # Video Frame
                            self.frame_received.emit(payload)
                        buffer = buffer[5+size:]
                    else:
                        break
        except Exception as e:
            print(f"Socket loop error: {e}")
        finally:
            self.running = False
            self.disconnected.emit()

    def send_input(self, input_data: bytes):
        if self.socket:
            try:
                header = struct.pack(">IB", len(input_data), 2)
                self.socket.sendall(header + input_data)
            except Exception as e:
                print(f"Failed to send input: {e}")
