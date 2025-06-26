## File: gui/main_window.py
"""
Main window for the Air Defense GUI.
Responsive layout with 3 columns: left 25%, center 50%, right 25%.
"""
import time
import random
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer

from gui.utils import make_group
from .styles import STYLESHEET
from .ros_connector import ROSConnector
from .components import (
    LogDisplay,
    SystemControlButtons,
    NoFireZoneWidget,
    ImageView,
    SystemModesPanel,
    MovementControls,
    HealthCheckDisplay,
    LaserPowerController,
    LaserLensController,
    PidTuningPanel
)

class AirDefenseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system_active = False
        self.initial_log_entries = [
            "[CORE] GUI Initialized.",
            "[CORE] Style applied..."
        ]
        self.ros_connector = ROSConnector(self)

        # Instantiate UI components before layout
        self.no_fire_zone = NoFireZoneWidget()
        self.system_modes_panel = SystemModesPanel()
        self.log_display = LogDisplay()
        self.system_control_buttons = SystemControlButtons()
        self.image_view = ImageView()
        # Constrain camera feed size
        self.image_view.setMaximumWidth(750)
        self.image_view.setMaximumHeight(750)
        self.movement_controls = MovementControls()
        self.health_check_display = HealthCheckDisplay()
        self.laser_power_controller = LaserPowerController()
        self.laser_lens_controller = LaserLensController()
        self.pid_tuning_panel = PidTuningPanel()

        self.setStyleSheet(STYLESHEET)
        self._initUI()
        self._connect_signals_slots()
        self._setup_timers()

    def _initUI(self):
        self.setWindowTitle('Air Defense GUI v3.2')
        # Allow free resizing, initial size 1100x800
        self.resize(1100, 800)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # --- Assemble Panels ---
        # Left panel (25%)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.no_fire_zone)
        left_layout.addWidget(self.system_modes_panel)
        left_layout.addWidget(self.log_display, stretch=1)
        main_layout.addLayout(left_layout, stretch=1)

        # Center panel (50%)
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.system_control_buttons, stretch=3)
        center_layout.addWidget(self.image_view, stretch=3)
        center_layout.addWidget(self.movement_controls, stretch=4)
        main_layout.addLayout(center_layout, stretch=2)

        # Right panel (25%)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.health_check_display)
        right_layout.addWidget(self.laser_power_controller)
        right_layout.addWidget(self.laser_lens_controller)
        right_layout.addWidget(self.pid_tuning_panel)
        right_layout.addStretch(1)
        main_layout.addLayout(right_layout, stretch=1)

        # Load initial logs
        self.log_display.add_initial_logs(self.initial_log_entries)




    def _setup_timers(self):
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.log_display.add_random_log_entry)
        self.log_timer.start(8000)

        self.power_simulation_timer = QTimer(self)
        self.power_simulation_timer.timeout.connect(
            lambda: self.laser_power_controller.update_current_power_display(self.system_active)
        )
        self.power_simulation_timer.start(2500)

    def _connect_signals_slots(self):
        # System Controls
        self.system_control_buttons.system_start_requested.connect(self._start_system)
        self.system_control_buttons.system_stop_requested.connect(self._stop_system)
        # Image View
        # Image View
        self.image_view.detection_layer_changed.connect(self._handle_detection_layer_change)
        self.image_view.log_message_requested.connect(self.log_display.add_log_entry)
        # No-Fire Zone
        self.no_fire_zone.zoneDefined.connect(self._handle_no_fire_zone)
        self.no_fire_zone.zoneCleared.connect(self._handle_clear_no_fire_zone)
        # System Modes
        self.system_modes_panel.mode_changed_signal.connect(self._handle_mode_change)
        # Movement
        self.movement_controls.movement_command_signal.connect(self._handle_movement_command)
        self.movement_controls.shoot_command_signal.connect(self._handle_shoot_command)
        # Laser Power/Lens
        self.laser_power_controller.target_power_changed.connect(self._handle_laser_target_power_change)
        self.laser_lens_controller.lens_value_changed.connect(self._handle_laser_lens_change)
        self.laser_lens_controller.log_message_requested.connect(self.log_display.add_log_entry)
        # PID Tuning
        self.pid_tuning_panel.pid_settings_applied_signal.connect(self._handle_pid_settings_applied)
        self.pid_tuning_panel.log_message_requested.connect(self.log_display.add_log_entry)
        # ROS Connector
        self.ros_connector.ros_log_received.connect(
            lambda m: self.log_display.add_log_entry(m, False)
        )
        self.ros_connector.pid_values_received.connect(self._update_pid_from_ros)
        self.ros_connector.system_status_updated.connect(self._update_health_from_ros)

    # --- System State Handlers ---
    def _start_system(self):
        if self.system_active:
            return
        self.log_display.add_log_entry("SYSTEM STARTING...", is_warning=True)
        self.system_active = True
        self.system_control_buttons.set_buttons_state(self.system_active)

    def _stop_system(self):
        if not self.system_active:
            return
        self.log_display.add_log_entry("SYSTEM STOPPING...", is_warning=True)
        self.system_active = False
        self.system_control_buttons.set_buttons_state(self.system_active)

    # --- Component Signal Handlers ---
    def _handle_detection_layer_change(self, layer_name: str):
        self.log_display.add_log_entry(f"View layer changed to: {layer_name}", False)

    def _handle_no_fire_zone(self, zone: dict):
        self.log_display.add_log_entry(f"No-Fire Zone set: {zone}", False)
        self.ros_connector.publish_no_fire_zone(zone)

    def _handle_clear_no_fire_zone(self):
        self.log_display.add_log_entry("No-Fire Zone cleared.", False)
        self.ros_connector.publish_clear_no_fire_zone()

    def _handle_mode_change(self, mode_name: str):
        self.log_display.add_log_entry(f"Mode: {mode_name}", False)

    def _handle_movement_command(self, direction: str):
        self.log_display.add_log_entry(f"Move: {direction}", False)

    def _handle_shoot_command(self):
        if not self.system_active:
            self.log_display.add_log_entry("Cannot SHOOT: System INACTIVE.", True)
            return
        self.log_display.add_log_entry("ACTION: FIRING LASER (Simulated)", True)

    def _handle_laser_target_power_change(self, power: int):
        self.log_display.add_log_entry(f"Laser Target: {power}%", False)

    def _handle_laser_lens_change(self, value: int):
        self.log_display.add_log_entry(f"Laser Lens: {value}mm", False)

    def _handle_pid_settings_applied(self, pP_s, pI_s, pD_s, tP_s, tI_s, tD_s):
        self.log_display.add_log_entry(f"Pan PID set: P={pP_s}, I={pI_s}, D={pD_s}", False)
        self.log_display.add_log_entry(f"Tilt PID set: P={tP_s}, I={tI_s}, D={tD_s}", False)

    # --- ROS Connector Signal Handlers ---
    def _update_pid_from_ros(self, motor: str, p: float, i: float, d: float):
        self.log_display.add_log_entry(
            f"ROS PID Update for {motor}: P{p:.2f} I{i:.2f} D{d:.2f}", False
        )

    def _update_health_from_ros(self, status: dict):
        self.log_display.add_log_entry(f"ROS Health Update: {status}", False)

    def closeEvent(self, event):
        self.log_display.add_log_entry("GUI Shutting down...", False)
        self.log_timer.stop()
        self.power_simulation_timer.stop()
        self.ros_connector.shutdown()
        event.accept()
