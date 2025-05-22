# air_defense_project/gui/components/laser_lens_controller.py
"""
QWidget for controlling the laser lens setting.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

class LaserLensController(QWidget):
    """
    Provides a QSpinBox and buttons to control the laser lens value.
    Emits `lens_value_changed` and `log_message_requested` signals.
    """
    lens_value_changed = pyqtSignal(int) # New lens value in mm
    log_message_requested = pyqtSignal(str, bool) # msg, is_warning

    _LENS_STEP_FINE = 1 # For spinbox arrows
    _LENS_STEP_COARSE = 5 # For dedicated buttons

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        lens_frame = QFrame(self)
        frame_layout = QVBoxLayout(lens_frame)

        title_label = QLabel("Laser Lens Controller", lens_frame)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Lens:", lens_frame))

        self.lens_spinbox = QSpinBox(lens_frame)
        self.lens_spinbox.setRange(30, 100) # Example range
        self.lens_spinbox.setSuffix(" mm")
        self.lens_spinbox.setValue(50)    # Default
        self.lens_spinbox.setSingleStep(self._LENS_STEP_FINE)
        self.lens_spinbox.valueChanged.connect(self._on_spinbox_value_changed)
        controls_layout.addWidget(self.lens_spinbox, 1) # Allow spinbox to stretch a bit

        buttons_vbox = QVBoxLayout() # Vertical buttons for up/down
        up_btn = QPushButton("▲", lens_frame)
        up_btn.setFixedWidth(40)
        up_btn.clicked.connect(self._increment_lens_coarse)
        down_btn = QPushButton("▼", lens_frame)
        down_btn.setFixedWidth(40)
        down_btn.clicked.connect(self._decrement_lens_coarse)
        buttons_vbox.addWidget(up_btn)
        buttons_vbox.addWidget(down_btn)
        controls_layout.addLayout(buttons_vbox)

        frame_layout.addLayout(controls_layout)
        layout.addWidget(lens_frame)

    def _on_spinbox_value_changed(self, value: int):
        """Handles spinbox value change and emits signals."""
        self.lens_value_changed.emit(value)
        self.log_message_requested.emit(f"Laser lens set to: {value} mm", False)

    def _increment_lens_coarse(self):
        """Increments lens value by a coarse step using the button."""
        self.lens_spinbox.setValue(self.lens_spinbox.value() + self._LENS_STEP_COARSE)

    def _decrement_lens_coarse(self):
        """Decrements lens value by a coarse step using the button."""
        self.lens_spinbox.setValue(self.lens_spinbox.value() - self._LENS_STEP_COARSE)

    def get_lens_value(self) -> int:
        """Returns the current lens value."""
        return self.lens_spinbox.value()