# air_defense_project/gui/components/log_display.py
"""
QWidget for displaying timestamped log messages.
"""
import time
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFrame
from PyQt5.QtCore import Qt # Qt is used for Qt.AlignCenter

class LogDisplay(QWidget):
    """
    Displays log messages with timestamps and INFO/WARN prefixes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        log_frame = QFrame(self)
        log_frame.setObjectName("LogFrame")
        log_inner_layout = QVBoxLayout(log_frame)

        title_label = QLabel("System Log", log_frame)
        title_label.setAlignment(Qt.AlignCenter) # Qt.AlignCenter requires Qt import
        log_inner_layout.addWidget(title_label)

        self.log_text_area = QTextEdit(log_frame)
        self.log_text_area.setReadOnly(True)
        log_inner_layout.addWidget(self.log_text_area)

        layout.addWidget(log_frame)

    def add_log_entry(self, message: str, is_warning: bool = False):
        """Adds a formatted log entry (timestamp, prefix, message)."""
        prefix = "[WARN]" if is_warning else "[INFO]"
        timestamp = time.strftime("%H:%M:%S")
        log_entry_text = f"{prefix} {timestamp} - {message}"
        self.log_text_area.append(log_entry_text)
        self.log_text_area.verticalScrollBar().setValue(
            self.log_text_area.verticalScrollBar().maximum()
        )

    def add_initial_logs(self, log_entries: list): # Ensure this method exists and is named correctly
        """Adds a list of pre-formatted log entries at startup."""
        for entry in log_entries:
            self.log_text_area.append(entry)
        if log_entries: # Only scroll if there were entries
            self.log_text_area.verticalScrollBar().setValue(
                self.log_text_area.verticalScrollBar().maximum()
            )

    def add_random_log_entry(self):
        """Generates and adds a random log entry for simulation."""
        info_logs = [
            "System status: Nominal.", "Network latency: OK.",
            "Tracking params updated.", "Battery: Charging."
        ]
        warn_logs = ["High CPU load.", "Unusual movement Sector 4.", "Laser temp elevated."]
        is_warning_event = random.choices([True, False], weights=[0.2, 0.8], k=1)[0]

        log_message = random.choice(warn_logs if is_warning_event else info_logs)
        self.add_log_entry(log_message, is_warning=is_warning_event)