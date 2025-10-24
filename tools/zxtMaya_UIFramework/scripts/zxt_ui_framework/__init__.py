"""Utility helpers for the shared Maya UI framework based on dayu_widgets."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_VENDOR_ROOT = Path(__file__).resolve().parents[1] / 'packages' / 'dayu_widgets_bundle'
if _VENDOR_ROOT.exists():
    resolved = str(_VENDOR_ROOT)
    if resolved not in sys.path:
        sys.path.insert(0, resolved)

from dayu_widgets import dayu_theme  # noqa: E402  (import after sys.path tweak)


_DEFAULT_THEME = dayu_theme

def ensure_qt_binding() -> None:
    """Ensure qtpy binding defaults to PySide2 for the Maya runtime."""
    os.environ.setdefault('QT_API', 'pyside2')

def apply_theme(widget):
    """Apply the shared dayu theme to a widget."""
    ensure_qt_binding()
    _DEFAULT_THEME.apply(widget)


__all__ = ["dayu_theme", "ensure_qt_binding", "apply_theme"]
