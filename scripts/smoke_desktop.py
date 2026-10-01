#!/usr/bin/env python3
"""Construct the Linux desktop UI and run a short offscreen Qt event loop."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "desktop"))

from main import PhoneDockApp  # noqa: E402  (add the existing app directory first)


def main() -> int:
    application = QApplication([])
    window = PhoneDockApp()
    window.show()
    QTimer.singleShot(250, application.quit)
    result = application.exec()

    window.close()
    window.decoder.quit()
    if not window.decoder.wait(2000):
        raise RuntimeError("The desktop decoder QThread did not stop after the smoke test")
    print("Linux desktop UI constructed and ran in Qt offscreen mode")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
