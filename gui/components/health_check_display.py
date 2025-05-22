# air_defense_project/gui/components/health_check_display.py
"""
QWidget for displaying system health status indicators.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt # Required for Qt.AlignCenter

class HealthCheckDisplay(QWidget):
    """
    Displays status (OK/Error) for various system components.
    """
    _COLOR_OK = "#a6e3a1"  # Green
    _COLOR_ERROR = "#f38ba8" # Red

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()
        # Initialize with an "inactive" or "unknown" status
        self.update_all_statuses(False, False, False, False)

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        health_frame = QFrame(self)
        frame_layout = QVBoxLayout(health_frame)

        title_label = QLabel("System Health Check", health_frame)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        statuses_layout = QVBoxLayout()
        self.esp32_status_label = QLabel(health_frame)
        self.laser_status_label = QLabel(health_frame)
        self.motors_status_label = QLabel(health_frame)
        self.movement_status_label = QLabel(health_frame)

        statuses_layout.addWidget(self.esp32_status_label)
        statuses_layout.addWidget(self.laser_status_label)
        statuses_layout.addWidget(self.motors_status_label)
        statuses_layout.addWidget(self.movement_status_label)
        frame_layout.addLayout(statuses_layout)

        layout.addWidget(health_frame)

    def _set_status_label(self, label: QLabel, component_name: str, is_ok: bool, ok_text: str = "OK", error_text: str = "Error"):
        """Helper to set text and color for a status label."""
        text = f"✓ {component_name}: {ok_text}" if is_ok else f"✗ {component_name}: {error_text}"
        color = self._COLOR_OK if is_ok else self._COLOR_ERROR
        label.setText(text)
        label.setStyleSheet(f"color: {color};")

    def update_all_statuses(self, esp32_ok: bool, laser_ok: bool, motors_ok: bool, movement_ok: bool):
        """Updates all health status indicators."""
        self._set_status_label(self.esp32_status_label, "ESP32", esp32_ok, "Connected", "Disconnected")
        self._set_status_label(self.laser_status_label, "Laser", laser_ok, "Ready", "Offline/Error")
        self._set_status_label(self.motors_status_label, "Motors", motors_ok, "Operational", "Inactive/Error")
        self._set_status_label(self.movement_status_label, "Movement", movement_ok, "System OK", "System Issue")