from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QStackedWidget, QFrame)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

# Harvst Palette
HARVST_CREAM = QColor("#F5F2E9")
HARVST_CORAL = QColor("#F15937")
HARVST_DARK_GREEN = QColor("#0D2B24")
HARVST_MUTED_GREEN = QColor("#4A675D")
HARVST_TAN = QColor("#E5DDC8")

class IllustrationWidget(QWidget):
    def __init__(self, draw_func):
        super().__init__()
        self.draw_func = draw_func
        self.setMinimumSize(400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_func(painter, self.width(), self.height())
        painter.end()

def draw_merge(p, w, h):
    # Monitor
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(13, 43, 36, 25))) # DarkGreen alpha
    p.drawRoundedRect(QRectF(w*0.15, h*0.2, w*0.7, h*0.45), 20, 20)
    p.drawRect(QRectF(w*0.45, h*0.65, w*0.1, h*0.08))
    p.drawRect(QRectF(w*0.35, h*0.73, w*0.3, h*0.02))

    # Phone
    p.setBrush(QBrush(HARVST_DARK_GREEN))
    p.drawRoundedRect(QRectF(w*0.55, h*0.35, w*0.25, h*0.45), 24, 24)

    # Glow
    p.setBrush(QBrush(QColor(241, 89, 55, 150)))
    p.drawEllipse(QPointF(w*0.62, h*0.45), w*0.08, w*0.08)

def draw_control(p, w, h):
    # Keys
    p.setBrush(QBrush(HARVST_DARK_GREEN))
    p.drawRoundedRect(QRectF(w*0.2, h*0.3, w*0.15, w*0.15), 10, 10)
    p.setBrush(QBrush(QColor(255, 255, 255, 100)))
    p.drawRoundedRect(QRectF(w*0.4, h*0.25, w*0.15, w*0.15), 10, 10)

    # Mouse
    path = QPainterPath()
    path.moveTo(w*0.6, h*0.5)
    path.quadTo(w*0.8, h*0.4, w*0.85, h*0.6)
    path.quadTo(w*0.9, h*0.8, w*0.7, h*0.85)
    path.quadTo(w*0.5, h*0.8, w*0.6, h*0.5)
    p.setBrush(QBrush(HARVST_TAN))
    p.drawPath(path)

    # Cursor
    p.setBrush(QBrush(HARVST_CORAL))
    cursor = QPainterPath()
    cursor.moveTo(w*0.35, h*0.65)
    cursor.lineTo(w*0.45, h*0.75)
    cursor.lineTo(w*0.4, h*0.75)
    cursor.lineTo(w*0.45, h*0.85)
    cursor.lineTo(w*0.42, h*0.87)
    cursor.lineTo(w*0.37, h*0.77)
    cursor.lineTo(w*0.32, h*0.82)
    cursor.closeSubpath()
    p.drawPath(cursor)

def draw_sync(p, w, h):
    # Waves
    pen = QPen(QColor(255, 255, 255, 150), 6)
    p.setPen(pen)
    for i in range(3):
        y = h * (0.4 + i*0.1)
        path = QPainterPath()
        path.moveTo(w*0.2, y)
        path.cubicTo(w*0.4, y-30, w*0.6, y+30, w*0.8, y)
        p.drawPath(path)

    # Icons
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(HARVST_DARK_GREEN))
    p.drawEllipse(QPointF(w*0.3, h*0.35), w*0.05, w*0.05)
    p.setBrush(QBrush(HARVST_TAN))
    p.drawRect(QRectF(w*0.6, h*0.55, w*0.08, w*0.08))

def draw_view(p, w, h):
    # Back Monitor
    p.setPen(Qt.NoPen)
    p.setBrush(QBrush(QColor(13, 43, 36, 30)))
    p.drawRoundedRect(QRectF(w*0.1, h*0.15, w*0.6, h*0.4), 15, 15)

    # Phone Front
    p.setBrush(QBrush(HARVST_DARK_GREEN))
    p.drawRoundedRect(QRectF(w*0.45, h*0.3, w*0.4, h*0.6), 24, 24)

    # Screen items
    p.setBrush(QBrush(HARVST_CORAL))
    p.drawRect(QRectF(w*0.5, h*0.35, w*0.3, h*0.1))
    p.setBrush(QBrush(QColor(229, 221, 200, 150))) # Tan alpha
    p.drawRect(QRectF(w*0.5, h*0.5, w*0.2, h*0.3))

class OnboardingPage(QWidget):
    def __init__(self, title, desc, draw_func, bg_color, text_color):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)

        self.setStyleSheet(f"background-color: {bg_color.name()}; color: {text_color.name()};")

        ill = IllustrationWidget(draw_func)
        layout.addWidget(ill, alignment=Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 48px; font-weight: 900; line-height: 50px;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        desc_label = QLabel(desc)
        desc_label.setStyleSheet(f"font-size: 18px; color: {text_color.name()}aa;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        layout.addStretch()

class OnboardingView(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        pages = [
            ("One\nWorkspace.", "Turn your phone into a native extension of your Windows PC. Seamlessly integrated.", draw_merge, HARVST_CREAM, HARVST_DARK_GREEN),
            ("Total\nControl.", "Use your mouse and keyboard to interact with Android applications directly from your desktop.", draw_control, HARVST_CORAL, Qt.white),
            ("Seamless\nSync.", "Synchronize your clipboard and transfer files with a simple drag and drop. No cloud required.", draw_sync, HARVST_CORAL, Qt.white),
            ("Double\nthe View.", "Transform your Android device into a secondary high-resolution display for your PC.", draw_view, HARVST_CREAM, HARVST_DARK_GREEN)
        ]

        for title, desc, func, bg, text in pages:
            self.stack.addWidget(OnboardingPage(title, desc, func, bg, text))

        self.bottom_bar = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_layout.setContentsMargins(60, 0, 60, 40)

        self.next_btn = QPushButton("CONTINUE")
        self.next_btn.setMinimumHeight(60)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_page)

        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setStyleSheet("background: transparent; border: none; font-weight: bold;")
        self.skip_btn.setCursor(Qt.PointingHandCursor)
        self.skip_btn.clicked.connect(self.finished.emit)

        self.bottom_layout.addWidget(self.skip_btn)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.next_btn, 1)
        self.layout.addWidget(self.bottom_bar)

        self.update_ui()

    def next_page(self):
        idx = self.stack.currentIndex()
        if idx < self.stack.count() - 1:
            self.stack.setCurrentIndex(idx + 1)
            self.update_ui()
        else:
            self.finished.emit()

    def update_ui(self):
        idx = self.stack.currentIndex()
        page = self.stack.currentWidget()
        bg = page.palette().color(page.backgroundRole())
        text = page.palette().color(page.foregroundRole())

        self.bottom_bar.setStyleSheet(f"background-color: {bg.name()};")

        btn_bg = HARVST_DARK_GREEN if bg == HARVST_CREAM else HARVST_CREAM
        btn_text = Qt.white if bg == HARVST_CREAM else HARVST_DARK_GREEN

        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg.name()};
                color: {btn_text.name()};
                border-radius: 15px;
                font-weight: 900;
                padding: 0 40px;
            }}
        """)
        self.skip_btn.setStyleSheet(f"color: {text.name()}88; background: transparent; border: none; font-weight: bold;")

        if idx == self.stack.count() - 1:
            self.next_btn.setText("GET STARTED")
        else:
            self.next_btn.setText("CONTINUE")
