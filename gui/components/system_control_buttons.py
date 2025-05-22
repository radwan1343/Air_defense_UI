# air_defense_project/gui/components/system_control_buttons.py
"""
QWidget for system start and stop/disable buttons.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal

class SystemControlButtons(QWidget):
    """
    Provides "START SYSTEM" and "DISABLE SYSTEM" buttons.
    Emits signals when these buttons are clicked.
    """
    system_start_requested = pyqtSignal()
    system_stop_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        control_frame = QFrame(self)
        control_frame_layout = QVBoxLayout(control_frame)

        title_label = QLabel("System Control", control_frame)
        title_label.setAlignment(Qt.AlignCenter)
        control_frame_layout.addWidget(title_label)

        buttons_hbox = QHBoxLayout()
        self.start_button = QPushButton("START SYSTEM", control_frame)
        self.start_button.setStyleSheet("background-color: #a6e3a1; color: #11111b; font-weight: bold;")
        self.start_button.clicked.connect(self.system_start_requested.emit)
        buttons_hbox.addWidget(self.start_button)

        self.stop_button = QPushButton("DISABLE SYSTEM", control_frame)
        self.stop_button.setStyleSheet("background-color: #f38ba8; color: #11111b; font-weight: bold;")
        self.stop_button.clicked.connect(self.system_stop_requested.emit)
        self.stop_button.setEnabled(False) # System is initially off
        buttons_hbox.addWidget(self.stop_button)

        control_frame_layout.addLayout(buttons_hbox)
        layout.addWidget(control_frame)

    def set_buttons_state(self, is_system_active: bool):
        """Updates button enabled states based on system activity."""
        self.start_button.setEnabled(not is_system_active)
        self.stop_button.setEnabled(is_system_active)