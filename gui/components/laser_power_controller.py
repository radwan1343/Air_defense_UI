# air_defense_project/gui/components/laser_power_controller.py
"""
QWidget for controlling and displaying laser power.
"""
import random # For simulating current power fluctuations
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
                             QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

class LaserPowerController(QWidget):
    """
    Provides slider for target laser power, displays current/target values.
    Emits `target_power_changed` signal.
    """
    target_power_changed = pyqtSignal(int) # New target power percentage

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        power_frame = QFrame(self)
        frame_layout = QVBoxLayout(power_frame)

        title_label = QLabel("Laser Power Controller", power_frame)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        # Current (actual) power display
        current_power_layout = QHBoxLayout()
        current_power_layout.addWidget(QLabel("Current:", power_frame))
        self.current_power_display_label = QLabel("0%", power_frame)
        self.current_power_display_label.setStyleSheet(f"color: {self._get_power_color(0)};")
        current_power_layout.addWidget(self.current_power_display_label)
        current_power_layout.addStretch() # Align left
        frame_layout.addLayout(current_power_layout)

        # Target power controls
        frame_layout.addWidget(QLabel("Target Power:", power_frame))
        self.target_power_slider = QSlider(Qt.Horizontal, power_frame)
        self.target_power_slider.setRange(0, 100)
        self.target_power_slider.setValue(50) # Default target
        self.target_power_slider.setTickPosition(QSlider.TicksBelow)
        self.target_power_slider.setTickInterval(10)
        self.target_power_slider.valueChanged.connect(self._on_slider_value_changed)
        frame_layout.addWidget(self.target_power_slider)

        self.target_power_display_label = QLabel(f"{self.target_power_slider.value()}%", power_frame)
        self.target_power_display_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.target_power_display_label)

        # Fine-tune buttons
        buttons_layout = QHBoxLayout()
        decrease_btn = QPushButton("Decrease (-5%)", power_frame)
        decrease_btn.clicked.connect(lambda: self.target_power_slider.setValue(self.target_power_slider.value() - 5))
        decrease_btn.setStyleSheet("background-color: #89b4fa; color: #11111b;")
        increase_btn = QPushButton("Increase (+5%)", power_frame)
        increase_btn.clicked.connect(lambda: self.target_power_slider.setValue(self.target_power_slider.value() + 5))
        increase_btn.setStyleSheet("background-color: #fab387; color: #11111b;")
        buttons_layout.addWidget(decrease_btn)
        buttons_layout.addWidget(increase_btn)
        frame_layout.addLayout(buttons_layout)

        layout.addWidget(power_frame)

    def _on_slider_value_changed(self, value: int):
        """Handles slider value change, updates label and emits signal."""
        self.target_power_display_label.setText(f"{value}%")
        self.target_power_changed.emit(value)

    def get_target_power(self) -> int:
        """Returns the current target power set by the slider."""
        return self.target_power_slider.value()

    def _get_power_color(self, power_value: int) -> str:
        """Determines display color based on power value."""
        if power_value > 75: return "#f38ba8"  # Red (High)
        if power_value < 25: return "#89b4fa"  # Blue (Low)
        return "#a6e3a1"  # Green (Mid)

    def update_current_power_display(self, is_system_active: bool):
        """Simulates and updates the 'current' laser power display value and color."""
        try:
            current_val = int(self.current_power_display_label.text().replace('%', ''))
        except ValueError:
            current_val = 0

        target_val = self.get_target_power()
        new_simulated_val = current_val

        if is_system_active: # Simulate adjustment towards target
            diff = target_val - current_val
            if abs(diff) > 2:
                adjustment = int(diff / 5) or (1 if diff > 0 else -1)
                new_simulated_val += adjustment
            else: # Close to target, add small fluctuation
                new_simulated_val += random.randint(-1, 1)
        else: # Simulate power decay or low fluctuation if inactive
            new_simulated_val = max(0, current_val - random.randint(1, 3)) + random.randint(-1, 1)

        new_simulated_val = max(0, min(100, new_simulated_val)) # Clamp 0-100

        self.current_power_display_label.setText(f"{new_simulated_val}%")
        self.current_power_display_label.setStyleSheet(f"color: {self._get_power_color(new_simulated_val)};")