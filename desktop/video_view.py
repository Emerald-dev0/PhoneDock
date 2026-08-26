import av
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QThread
from PySide6.QtGui import QImage, QPainter, QPalette

class VideoDecoderThread(QThread):
    new_image = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.codec = av.CodecContext.create('h264', 'r')
        self.running = True

    @Slot(bytes)
    def decode_frame(self, data):
        try:
            packets = self.codec.parse(data)
            for packet in packets:
                frames = self.codec.decode(packet)
                for frame in frames:
                    array = frame.to_rgb().to_ndarray()
                    height, width, channel = array.shape
                    bytes_per_line = 3 * width
                    q_img = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    self.new_image.emit(q_img.copy())
        except Exception as e:
            print(f"Decoding error: {e}")

    def stop(self):
        self.running = False

class VideoView(QWidget):
    mouse_event = Signal(int, float, float) # type, x, y

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image = None
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    @Slot(QImage)
    def update_image(self, image):
        self.current_image = image
        self.update()

    def paintEvent(self, event):
        if self.current_image:
            painter = QPainter(self)
            scaled_img = self.current_image.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled_img.width()) // 2
            y = (self.height() - scaled_img.height()) // 2
            painter.drawImage(x, y, scaled_img)
            painter.end()

    def _send_mouse_event(self, type_id, event):
        if not self.current_image:
            return
        w, h = self.width(), self.height()
        iw, ih = self.current_image.width(), self.current_image.height()
        aspect = iw / ih
        if w / h > aspect:
            render_h = h
            render_w = h * aspect
        else:
            render_w = w
            render_h = w / aspect
        ox = (w - render_w) / 2
        oy = (h - render_h) / 2
        rel_x = (event.position().x() - ox) / render_w
        rel_y = (event.position().y() - oy) / render_h
        if 0 <= rel_x <= 1 and 0 <= rel_y <= 1:
            self.mouse_event.emit(type_id, rel_x, rel_y)

    def mousePressEvent(self, event):
        self._send_mouse_event(1, event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._send_mouse_event(2, event)

    def mouseReleaseEvent(self, event):
        self._send_mouse_event(3, event)
