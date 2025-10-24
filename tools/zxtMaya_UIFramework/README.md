# zxtMaya_UIFramework

Shared UI framework bundle for the zxtMaya suite. Packages `dayu_widgets`, `qtpy`, and utility helpers so
all tools can reuse a consistent widget set. The module exposes a Python path located at `scripts/` which is
registered through `suite_manifest.json`.

## Usage

```python
from zxt_ui_framework import apply_theme, ensure_qt_binding
from dayu_widgets.button import MPushButton

ensure_qt_binding()
button = MPushButton("Submit")
apply_theme(button)
```

The bundle keeps the upstream wheel layout under `scripts/packages/dayu_widgets_bundle/`. Upgrading the
framework simply requires replacing that directory with a newer wheel install (and updating this README).
