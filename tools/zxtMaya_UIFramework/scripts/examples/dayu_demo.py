"""Simple Maya demo window using dayu_widgets."""

from __future__ import annotations

from dayu_widgets.qt import QtWidgets
from zxt_ui_framework import apply_theme, ensure_qt_binding
from dayu_widgets.button import MPushButton

try:  # Maya runtime imports (skip when running unit tests)
    from maya import OpenMayaUI as omui  # type: ignore
    import maya.utils  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover - maya unavailable during tests
    omui = None  # type: ignore


def show_demo() -> QtWidgets.QWidget:
    """Create a simple Dayu themed window bound to the Maya main window."""
    ensure_qt_binding()

    parent = None
    if omui is not None:
        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            parent = QtWidgets.QWidget.find(ptr)

    window = QtWidgets.QWidget(parent)
    window.setWindowTitle("Dayu Widgets Demo")
    layout = QtWidgets.QVBoxLayout(window)

    button = MPushButton("Submit")
    layout.addWidget(button)

    apply_theme(window)
    window.resize(320, 160)
    window.show()
    return window


if __name__ == "__main__":
    show_demo()
