# air_defense_project/gui/components/pid_tuning_panel.py
"""
QWidget for tuning PID parameters for Pan and Tilt motors.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
                             QFormLayout, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal

class PidTuningPanel(QWidget):
    """
    Provides input fields for Pan/Tilt PID values and an Apply button.
    Emits signals for applying settings, logging, or terminal messages.
    """
    # Emits all PID values as strings upon successful validation and apply.
    pid_settings_applied_signal = pyqtSignal(str, str, str, str, str, str)
    log_message_requested = pyqtSignal(str, bool) # msg, is_warning
    terminal_message_requested = pyqtSignal(str)  # msg for terminal

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        pid_frame = QFrame(self)
        frame_layout = QVBoxLayout(pid_frame)

        title_label = QLabel("PID Tuning (Pan/Tilt)", pid_frame)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        form_layout = QFormLayout() # Ideal for label-input pairs

        # Pan Motor PID
        pan_title = QLabel("Pan Motor:", pid_frame)
        pan_title.setStyleSheet("font-weight: bold; color: #fab387;") # Orange
        form_layout.addRow(pan_title) # Span or just add as a row item
        self.pan_p_input = QLineEdit("1.0", pid_frame)
        self.pan_i_input = QLineEdit("0.1", pid_frame)
        self.pan_d_input = QLineEdit("0.01", pid_frame)
        form_layout.addRow("P:", self.pan_p_input)
        form_layout.addRow("I:", self.pan_i_input)
        form_layout.addRow("D:", self.pan_d_input)

        # Tilt Motor PID
        tilt_title = QLabel("Tilt Motor:", pid_frame)
        tilt_title.setStyleSheet("font-weight: bold; color: #89b4fa;") # Blue
        form_layout.addRow(tilt_title)
        self.tilt_p_input = QLineEdit("1.0", pid_frame)
        self.tilt_i_input = QLineEdit("0.1", pid_frame)
        self.tilt_d_input = QLineEdit("0.01", pid_frame)
        form_layout.addRow("P:", self.tilt_p_input)
        form_layout.addRow("I:", self.tilt_i_input)
        form_layout.addRow("D:", self.tilt_d_input)

        frame_layout.addLayout(form_layout)

        apply_button = QPushButton("Apply PID Settings", pid_frame)
        apply_button.clicked.connect(self._on_apply_settings_clicked)
        frame_layout.addWidget(apply_button)

        layout.addWidget(pid_frame)

    def _on_apply_settings_clicked(self):
        """Validates PID inputs and emits signal if valid."""
        pid_values_str = self.get_pid_values_as_strings_tuple()
        try:
            # Validate that all can be converted to float
            for val_str in pid_values_str:
                float(val_str)
            self.pid_settings_applied_signal.emit(*pid_values_str)
        except ValueError:
            error_msg = "Invalid PID: All P,I,D values must be numbers."
            self.log_message_requested.emit(error_msg, True)
            self.terminal_message_requested.emit(f"ERROR: {error_msg}")

    def get_pid_values_as_strings_tuple(self) -> tuple:
        """Returns current PID input values as a tuple of strings."""
        return (
            self.pan_p_input.text(), self.pan_i_input.text(), self.pan_d_input.text(),
            self.tilt_p_input.text(), self.tilt_i_input.text(), self.tilt_d_input.text()
        )

    def get_pid_values_as_dict(self) -> dict:
        """Returns current PID input values as a dictionary."""
        return {
            "pan": {"p": self.pan_p_input.text(), "i": self.pan_i_input.text(), "d": self.pan_d_input.text()},
            "tilt": {"p": self.tilt_p_input.text(), "i": self.tilt_i_input.text(), "d": self.tilt_d_input.text()}
        }

    def update_pid_input_fields(self, motor_type: str, p_val: float, i_val: float, d_val: float):
        """Updates PID input fields from external source (e.g., ROS)."""
        p_str, i_str, d_str = f"{p_val:.3f}", f"{i_val:.3f}", f"{d_val:.3f}" # Format for display

        if motor_type.lower() == "pan":
            self.pan_p_input.setText(p_str)
            self.pan_i_input.setText(i_str)
            self.pan_d_input.setText(d_str)
        elif motor_type.lower() == "tilt":
            self.tilt_p_input.setText(p_str)
            self.tilt_i_input.setText(i_str)
            self.tilt_d_input.setText(d_str)
        else:
            self.log_message_requested.emit(f"PID Update: Unknown motor type '{motor_type}'.", True)