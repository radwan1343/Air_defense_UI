# air_defense_project/gui/components/system_modes_panel.py
"""
QWidget for selecting the system's operational mode using radio buttons.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal

class SystemModesPanel(QWidget):
    """
    Provides radio buttons for selecting system modes.
    Emits `mode_changed_signal` with the name of the selected mode.
    """
    mode_changed_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        modes_frame = QFrame(self)
        modes_frame_layout = QVBoxLayout(modes_frame)

        title_label = QLabel("System Modes", modes_frame)
        title_label.setAlignment(Qt.AlignCenter)
        modes_frame_layout.addWidget(title_label)

        radios_layout = QHBoxLayout()
        self.manual_radio = QRadioButton("Manual", modes_frame)
        self.manual_radio.setChecked(True) # Default mode

        self.phase_one_radio = QRadioButton("Phase One", modes_frame)
        self.phase_two_radio = QRadioButton("Phase Two", modes_frame)
        self.phase_three_radio = QRadioButton("Phase Three", modes_frame)

        # Connect toggled signal (emitted when state changes, including becoming unchecked)
        # The lambda checks 'is_checked' to only act when a radio button becomes selected.
        self.manual_radio.toggled.connect(
            lambda is_checked: self._on_mode_selected("Manual") if is_checked else None)
        self.phase_one_radio.toggled.connect(
            lambda is_checked: self._on_mode_selected("Phase One") if is_checked else None)
        self.phase_two_radio.toggled.connect(
            lambda is_checked: self._on_mode_selected("Phase Two") if is_checked else None)
        self.phase_three_radio.toggled.connect(
            lambda is_checked: self._on_mode_selected("Phase Three") if is_checked else None)

        radios_layout.addWidget(self.manual_radio)
        radios_layout.addWidget(self.phase_one_radio)
        radios_layout.addWidget(self.phase_two_radio)
        radios_layout.addWidget(self.phase_three_radio)
        modes_frame_layout.addLayout(radios_layout)

        layout.addWidget(modes_frame)

    def _on_mode_selected(self, mode_name: str):
        """Emits signal when a mode is selected."""
        self.mode_changed_signal.emit(mode_name)