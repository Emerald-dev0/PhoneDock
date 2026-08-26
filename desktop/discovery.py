from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
from PySide6.QtCore import QObject, Signal

class PhoneDockListener(ServiceListener):
    def __init__(self, emitter):
        self.emitter = emitter

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.emitter.device_lost.emit(name)

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            address = info.parsed_addresses()[0] if info.addresses else None
            if address:
                self.emitter.device_discovered.emit({
                    "name": name.split('.')[0],
                    "address": address,
                    "port": info.port
                })

class DiscoveryManager(QObject):
    device_discovered = Signal(dict)
    device_lost = Signal(str)

    def __init__(self):
        super().__init__()
        self.zeroconf = Zeroconf()
        self.listener = PhoneDockListener(self)
        self.browser = None

    def start(self):
        self.browser = ServiceBrowser(self.zeroconf, "_phonedock._tcp.local.", self.listener)

    def stop(self):
        if self.browser:
            self.browser.cancel()
        self.zeroconf.close()
