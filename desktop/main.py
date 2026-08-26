import sys
import struct
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QPushButton, QStackedWidget, QFrame,
                             QListWidget, QListWidgetItem, QMessageBox)
from PySide6.QtCore import Qt, Slot, QSettings, QTimer
from PySide6.QtGui import QIcon, QMovie

from discovery import DiscoveryManager
from connection import ConnectionManager
from video_view import VideoView, VideoDecoderThread
from onboarding_view import OnboardingView
from PySide6.QtCore import Qt, Slot, QSettings

# Harvst Palette

# Harvst Palette
HARVST_CREAM = "#F5F2E9"
HARVST_CORAL = "#F15937"
HARVST_DARK_GREEN = "#0D2B24"
HARVST_MUTED_GREEN = "#4A675D"
HARVST_TAN = "#E5DDC8"

STYLE_SHEET = f"""
QMainWindow {{
    background-color: {HARVST_DARK_GREEN};
}}

QWidget#discovery_page {{
    background-color: {HARVST_CREAM};
}}

QLabel#header_title {{
    color: {HARVST_DARK_GREEN};
    font-size: 32px;
    font-weight: 900;
}}

QFrame#card {{
    background-color: white;
    border-radius: 24px;
    border: 1px solid {HARVST_TAN};
}}

QPushButton#btn_primary {{
    background-color: {HARVST_CORAL};
    color: white;
    border-radius: 12px;
    padding: 16px;
    font-weight: bold;
    font-size: 14px;
}}

QPushButton#btn_primary:hover {{
    background-color: #D14A2B;
}}

QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
}}

QListWidget::item {{
    background-color: white;
    border: 1px solid {HARVST_TAN};
    border-radius: 12px;
    margin-bottom: 8px;
    padding: 12px;
    color: {HARVST_DARK_GREEN};
    font-weight: bold;
}}

QListWidget::item:selected {{
    border: 2px solid {HARVST_CORAL};
    color: {HARVST_CORAL};
}}
"""

class PhoneDockApp(QMainWindow):
    VERSION = "1.1.0"
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PhoneDock v{self.VERSION}")
        self.setMinimumSize(1000, 800)
        self.setStyleSheet(STYLE_SHEET)

        self.settings = QSettings("PhoneDock", "Client")
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)

        self.setup_onboarding_page()
        self.setup_discovery_page()
        self.setup_streaming_page()

        if self.settings.value("onboarding_completed", "false") == "true":
            self.central_stack.setCurrentIndex(1)
        else:
            self.central_stack.setCurrentIndex(0)

        self.discovery_manager = DiscoveryManager()
        self.discovery_manager.device_discovered.connect(self.on_device_found)
        self.discovery_manager.device_lost.connect(self.on_device_lost)
        self.discovery_manager.start()

        self.connection = None
        self.decoder = VideoDecoderThread()
        self.decoder.start()

    def setup_onboarding_page(self):
        self.onboarding = OnboardingView()
        self.onboarding.finished.connect(self.finish_onboarding)
        self.central_stack.addWidget(self.onboarding)

    def finish_onboarding(self):
        self.settings.setValue("onboarding_completed", "true")
        self.central_stack.setCurrentIndex(1)

    def setup_discovery_page(self):
        page = QWidget()
        page.setObjectName("discovery_page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        header = QLabel("PhoneDock")
        header.setObjectName("header_title")
        layout.addWidget(header)

        info_card = QFrame()
        info_card.setObjectName("card")
        card_layout = QVBoxLayout(info_card)
        card_layout.setContentsMargins(40, 40, 40, 40)

        self.status_label = QLabel("Looking for devices...")
        self.status_label.setStyleSheet(f"color: {HARVST_MUTED_GREEN}; font-size: 16px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.status_label)

        # Empty state placeholder
        self.empty_state_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_state_widget)
        empty_icon = QLabel("📡")
        empty_icon.setStyleSheet("font-size: 64px;")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_icon)
        empty_text = QLabel("Make sure PhoneDock is open on your Android device and both are on the same Wi-Fi network.")
        empty_text.setStyleSheet(f"color: {HARVST_MUTED_GREEN};")
        empty_text.setWordWrap(True)
        empty_text.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(empty_text)
        card_layout.addWidget(self.empty_state_widget)

        self.device_list = QListWidget()
        self.device_list.hide() # Hidden by default
        card_layout.addWidget(self.device_list)

        self.connect_btn = QPushButton("CONNECT DEVICE")
        self.connect_btn.setObjectName("btn_primary")
        self.connect_btn.setEnabled(False) # Disabled until device selected
        self.connect_btn.clicked.connect(self.start_connection)
        card_layout.addWidget(self.connect_btn)

        layout.addWidget(info_card)
        self.central_stack.addWidget(page)

    def setup_streaming_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_view = VideoView()
        self.video_view.mouse_event.connect(self.on_mouse_event)
        layout.addWidget(self.video_view)

        controls = QHBoxLayout()
        controls.setContentsMargins(20, 10, 20, 20)

        self.latency_label = QLabel("0 ms")
        self.latency_label.setStyleSheet("color: white; font-weight: bold; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 10px;")
        controls.addWidget(self.latency_label)

        controls.addStretch()

        disconnect_btn = QPushButton("DISCONNECT")
        disconnect_btn.setStyleSheet(f"background: {HARVST_CORAL}; border: none; color: white; padding: 10px 24px; border-radius: 12px; font-weight: 900;")
        disconnect_btn.setCursor(Qt.PointingHandCursor)
        disconnect_btn.clicked.connect(self.stop_connection)
        controls.addWidget(disconnect_btn)

        layout.addLayout(controls)
        self.central_stack.addWidget(page)

    @Slot(dict)
    def on_device_found(self, device):
        # Check if already in list
        for i in range(self.device_list.count()):
            if device['address'] in self.device_list.item(i).text():
                return

        item = QListWidgetItem(f"📱 {device['name']} ({device['address']})")
        item.setData(Qt.UserRole, device)
        self.device_list.addItem(item)

        self.empty_state_widget.hide()
        self.device_list.show()
        self.connect_btn.setEnabled(True)
        self.status_label.setText(f"{self.device_list.count()} device(s) discovered")

    @Slot(str)
    def on_device_lost(self, name):
        for i in range(self.device_list.count()):
            if name in self.device_list.item(i).text():
                self.device_list.takeItem(i)
                break

        if self.device_list.count() == 0:
            self.device_list.hide()
            self.empty_state_widget.show()
            self.connect_btn.setEnabled(False)
            self.status_label.setText("Looking for devices...")
        else:
            self.status_label.setText(f"{self.device_list.count()} device(s) discovered")

    def start_connection(self):
        selected = self.device_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Device", "Please select a device from the list first.")
            return

        device = selected.data(Qt.UserRole)
        self.connect_btn.setText("CONNECTING...")
        self.connect_btn.setEnabled(False)

        # Give UI time to update
        QApplication.processEvents()

        self.connection = ConnectionManager(device['address'], device['port'])
        self.connection.frame_received.connect(self.decoder.decode_frame)
        self.connection.disconnected.connect(self.stop_connection)
        self.decoder.new_image.connect(self.video_view.update_image)

        if self.connection.connect():
            self.central_stack.setCurrentIndex(2)
        else:
            QMessageBox.critical(self, "Connection Failed", f"Could not connect to {device['name']}. Please check your network and try again.")
            self.connect_btn.setText("CONNECT DEVICE")
            self.connect_btn.setEnabled(True)

    def stop_connection(self):
        if self.connection:
            self.connection.disconnect()
            self.connection = None
        self.central_stack.setCurrentIndex(1)
        self.connect_btn.setText("CONNECT DEVICE")
        self.connect_btn.setEnabled(True)

    def on_mouse_event(self, type_id, x, y):
        if self.connection:
            data = struct.pack(">Bff", type_id, x, y)
            self.connection.send_input(data)

    def closeEvent(self, event):
        self.discovery_manager.stop()
        self.decoder.stop()
        self.stop_connection()
        super().closeEvent(event)

    def on_mouse_event(self, type_id, x, y):
        if self.connection:
            data = struct.pack(">Bff", type_id, x, y)
            self.connection.send_input(data)

    def closeEvent(self, event):
        self.discovery_manager.stop()
        self.decoder.stop()
        self.stop_connection()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhoneDockApp()
    window.show()
    sys.exit(app.exec())
