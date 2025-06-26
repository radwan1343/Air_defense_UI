## File: gui/components/system_modes_panel.py
"""
QWidget for selecting the system's operational mode using vertical radio buttons.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal

class SystemModesPanel(QWidget):
    """
    Provides vertical radio buttons for selecting system modes.
    Emits `mode_changed_signal` with the name of the selected mode.
    """
    mode_changed_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        title = QLabel("System Modes", self)
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        # Button group for radio buttons
        self.btn_group = QButtonGroup(self)

        # Modes list
        modes = ["Manual", "Phase One", "Phase Two", "Phase Three"]
        for idx, mode in enumerate(modes):
            rb = QRadioButton(mode, self)
            # Default select first
            if idx == 0:
                rb.setChecked(True)
            self.btn_group.addButton(rb, id=idx)
            layout.addWidget(rb)

        # Connect signal: button toggled
        self.btn_group.buttonToggled.connect(self._on_button_toggled)

        self.setLayout(layout)

    def _on_button_toggled(self, button, checked):
        if checked:
            self.mode_changed_signal.emit(button.text())
