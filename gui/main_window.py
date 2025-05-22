# air_defense_project/gui/main_window.py
"""
Main window for the Air Defense GUI.
Assembles UI components, manages application logic, state, and ROS2 interaction.
"""
import time
import random
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import QTimer

from .styles import STYLESHEET
from .ros_connector import ROSConnector
from .components import (CommandTerminal, LogDisplay, SystemControlButtons, ImageView,
                         SystemModesPanel, MovementControls, HealthCheckDisplay,
                         LaserPowerController, LaserLensController, PidTuningPanel)

class AirDefenseGUI(QMainWindow):
    """
    Main application window. Orchestrates UI components and simulated ROS interactions.
    """
    def __init__(self):
        super().__init__()
        self.system_active = False
        self.initial_log_entries = [
            "[CORE] GUI Initialized.",
            "[CORE] Style applied. Awaiting system start...",
        ]
        self.ros_connector = ROSConnector(self) # ROS interaction layer

        self._initUI()
        self._connect_signals_slots()
        self._setup_timers()

    def _initUI(self):
        """Sets up the main window layout and instantiates UI components."""
        self.setWindowTitle('Air Defense GUI v3.2 (Granular & Refined)')
        self.setGeometry(100, 100, 1360, 920) # Adjusted for comfortable component spacing
        self.setStyleSheet(STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Instantiate all components
        self.command_terminal = CommandTerminal()
        self.log_display = LogDisplay()
        self.system_control_buttons = SystemControlButtons()
        self.image_view = ImageView() # Camera functionality is now within ImageView
        self.system_modes_panel = SystemModesPanel()
        self.movement_controls = MovementControls()
        self.health_check_display = HealthCheckDisplay()
        self.laser_power_controller = LaserPowerController()
        self.laser_lens_controller = LaserLensController()
        self.pid_tuning_panel = PidTuningPanel()

        # --- Assemble Panels ---
        # Left Panel (Terminal, Log)
        left_panel = QFrame()
        left_panel.setObjectName("LeftPanelFrame")
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.command_terminal, 1)
        left_layout.addWidget(self.log_display, 1)
        main_layout.addWidget(left_panel, 1) # Stretch factor 1

        # Center Panel (System Control, Image View, Modes, Movement)
        center_panel = QFrame()
        center_panel.setObjectName("CenterPanelFrame")
        center_layout = QVBoxLayout(center_panel)
        center_layout.addWidget(self.system_control_buttons) # No stretch, compact
        center_layout.addWidget(self.image_view, 4)          # Image view takes most space
        center_layout.addWidget(self.system_modes_panel)     # Compact
        center_layout.addWidget(self.movement_controls, 1)   # Some space for movement
        main_layout.addWidget(center_panel, 2) # Stretch factor 2 (wider)

        # Right Panel (Health, Laser, PID)
        right_panel = QFrame()
        right_panel.setObjectName("RightPanelFrame")
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self.health_check_display)
        right_layout.addWidget(self.laser_power_controller)
        right_layout.addWidget(self.laser_lens_controller)
        right_layout.addWidget(self.pid_tuning_panel)
        right_layout.addStretch(1) # Pushes content up if extra space
        main_layout.addWidget(right_panel, 1) # Stretch factor 1

        self.log_display.add_initial_logs(self.initial_log_entries)

    def _setup_timers(self):
        """Initializes and starts QTimers for periodic updates."""
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.log_display.add_random_log_entry)
        self.log_timer.start(8000) # Random log every 8s

        self.power_simulation_timer = QTimer(self)
        self.power_simulation_timer.timeout.connect(
            lambda: self.laser_power_controller.update_current_power_display(self.system_active)
        )
        self.power_simulation_timer.start(2500) # Simulate power fluctuation every 2.5s

    def _connect_signals_slots(self):
        """Connects signals from components to handler methods."""
        # Terminal
        self.command_terminal.command_entered.connect(self._handle_terminal_command)
        # System Controls
        self.system_control_buttons.system_start_requested.connect(self._start_system)
        self.system_control_buttons.system_stop_requested.connect(self._stop_system)
        # Image View
        self.image_view.detection_layer_changed.connect(self._handle_detection_layer_change)
        self.image_view.log_message_requested.connect(self.log_display.add_log_entry)
        self.image_view.image_successfully_loaded.connect(
            lambda path: self.log_display.add_log_entry(f"Static image loaded: {os.path.basename(path)}", False)
        )
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
        self.pid_tuning_panel.terminal_message_requested.connect(self.command_terminal.append_to_terminal)
        # ROS Connector
        self.ros_connector.ros_log_received.connect(lambda msg: self.log_display.add_log_entry(msg, False)) # msg already prefixed by ROSConnector
        self.ros_connector.pid_values_received.connect(self._update_pid_from_ros)
        self.ros_connector.system_status_updated.connect(self._update_health_from_ros)

    # --- System State Handlers ---
    def _start_system(self):
        if self.system_active: return
        self.log_display.add_log_entry("SYSTEM STARTING...", is_warning=True)
        self.system_active = True
        self.system_control_buttons.set_buttons_state(self.system_active)
        self.command_terminal.append_to_terminal("Attempting system start...")
        # Simplified startup sequence
        QTimer.singleShot(100, lambda: self.command_terminal.append_to_terminal("Core modules initializing..."))
        QTimer.singleShot(300, lambda: self.command_terminal.append_to_terminal("ROS2 link active (simulated)."))
        QTimer.singleShot(500, lambda: (
            self.command_terminal.append_to_terminal("System ACTIVE."),
            self.health_check_display.update_all_statuses(True, True, True, True),
            self.ros_connector.publish_system_command("start")
        ))

    def _stop_system(self):
        if not self.system_active: return
        self.log_display.add_log_entry("SYSTEM STOPPING...", is_warning=True)
        # Stop camera if it's active
        if self.image_view.is_camera_feed_active:
            self.image_view.stop_camera_feed()

        self.system_active = False
        self.system_control_buttons.set_buttons_state(self.system_active)
        self.command_terminal.append_to_terminal("Attempting system stop...")
        QTimer.singleShot(100, lambda: self.command_terminal.append_to_terminal("Powering down modules..."))
        QTimer.singleShot(300, lambda: (
            self.command_terminal.append_to_terminal("System INACTIVE."),
            self.health_check_display.update_all_statuses(False, False, False, False),
            self.ros_connector.publish_system_command("stop")
        ))

    # --- Component Signal Handlers ---
    def _handle_detection_layer_change(self, layer_name: str):
        self.log_display.add_log_entry(f"View layer changed to: {layer_name}", False)
        # ROS call if needed: self.ros_connector.publish_view_layer(layer_name)

    def _handle_mode_change(self, mode_name: str):
        self.log_display.add_log_entry(f"Mode: {mode_name}", False)
        self.command_terminal.append_to_terminal(f"$ Mode set: {mode_name}")
        self.ros_connector.publish_mode_change(mode_name)

    def _handle_movement_command(self, direction: str):
        self.log_display.add_log_entry(f"Move: {direction}", False)
        self.command_terminal.append_to_terminal(f"$ Move: {direction}")
        self.ros_connector.publish_movement_command(direction)

    def _handle_shoot_command(self):
        if not self.system_active:
            msg = "Cannot SHOOT: System INACTIVE."
            self.log_display.add_log_entry(msg, True)
            self.command_terminal.append_to_terminal(f"WARN: {msg}")
            return
        self.log_display.add_log_entry("ACTION: FIRING LASER (Simulated)", True)
        self.command_terminal.append_to_terminal("$ ACTION: FIRING")
        self.ros_connector.publish_laser_action("fire")

    def _handle_laser_target_power_change(self, power: int):
        self.log_display.add_log_entry(f"Laser Target: {power}%", False)
        self.command_terminal.append_to_terminal(f"$ Laser Target Pwr: {power}%")
        self.ros_connector.publish_laser_power(power)

    def _handle_laser_lens_change(self, value: int):
        # Logged by component itself.
        self.command_terminal.append_to_terminal(f"$ Laser Lens: {value}mm")
        self.ros_connector.publish_laser_lens(value)

    def _handle_pid_settings_applied(self, pP_s, pI_s, pD_s, tP_s, tI_s, tD_s):
        # Values are already validated as strings convertible to float by PidTuningPanel
        self.log_display.add_log_entry(f"Pan PID set: P={pP_s}, I={pI_s}, D={pD_s}", False)
        self.log_display.add_log_entry(f"Tilt PID set: P={tP_s}, I={tI_s}, D={tD_s}", False)
        self.command_terminal.append_to_terminal(f"$ Pan PID: P={pP_s} I={pI_s} D={pD_s}")
        self.command_terminal.append_to_terminal(f"$ Tilt PID: P={tP_s} I={tI_s} D={tD_s}")
        self.ros_connector.publish_pid_settings("pan", float(pP_s), float(pI_s), float(pD_s))
        self.ros_connector.publish_pid_settings("tilt", float(tP_s), float(tI_s), float(tD_s))

    # --- ROS Connector Signal Handlers ---
    def _update_pid_from_ros(self, motor: str, p: float, i: float, d: float):
        self.log_display.add_log_entry(f"ROS PID Update for {motor}: P{p:.2f} I{i:.2f} D{d:.2f}", False)
        self.command_terminal.append_to_terminal(f"$ ROS {motor} PID: P{p:.2f} I{i:.2f} D{d:.2f}")
        self.pid_tuning_panel.update_pid_input_fields(motor, p, i, d)

    def _update_health_from_ros(self, status: dict):
        self.log_display.add_log_entry(f"ROS Health Update: {status}", False)
        self.health_check_display.update_all_statuses(
            status.get('esp32', False), status.get('laser', False),
            status.get('motors', False), status.get('movement', False)
        )

    # --- Terminal Command Processor ---
    def _handle_terminal_command(self, command: str):
        cmd_lower = command.lower().strip()
        self.log_display.add_log_entry(f"Terminal: '{command}'", False)

        if not cmd_lower: return

        if cmd_lower == "help":
            self.command_terminal.append_to_terminal(
                "Commands: help, status, clear, start, stop, reboot, calibrate, scan, config, "
                "pid <pan|tilt> <p> <i> <d>, roslog <msg>, rosstatus"
            )
        elif cmd_lower == "status":
            pid_vals = self.pid_tuning_panel.get_pid_values_as_dict()
            self.command_terminal.append_to_terminal(
                f"System: {'ACTIVE' if self.system_active else 'INACTIVE'}\n"
                f"Laser Target: {self.laser_power_controller.get_target_power()}% "
                f"(Sim Current: {self.laser_power_controller.current_power_display_label.text()})\n"
                f"Lens: {self.laser_lens_controller.get_lens_value()}mm\n"
                f"Pan PID: P {pid_vals['pan']['p']}, I {pid_vals['pan']['i']}, D {pid_vals['pan']['d']}\n"
                f"Tilt PID: P {pid_vals['tilt']['p']}, I {pid_vals['tilt']['i']}, D {pid_vals['tilt']['d']}"
            )
        elif cmd_lower == "clear": self.command_terminal.clear_terminal()
        elif cmd_lower == "start": self._start_system()
        elif cmd_lower == "stop": self._stop_system()
        elif cmd_lower == "reboot":
            self.command_terminal.append_to_terminal("Simulating reboot...")
            if self.system_active: self._stop_system()
            QTimer.singleShot(800, self._start_system) # Start after a delay
        elif cmd_lower == "calibrate":
            self.command_terminal.append_to_terminal("Simulating calibration via ROS...")
            self.ros_connector.publish_system_command("calibrate")
            QTimer.singleShot(1000, lambda: self.command_terminal.append_to_terminal("Calibration complete (simulated)."))
        elif cmd_lower == "scan":
            if not self.system_active:
                self.command_terminal.append_to_terminal("System must be ACTIVE to scan.")
                return
            self.command_terminal.append_to_terminal("Simulating target scan via ROS...")
            self.ros_connector.publish_system_command("scan_targets")
            QTimer.singleShot(1500, lambda: self.command_terminal.append_to_terminal(
                f"Scan: {'Target found (simulated)' if random.random() > 0.5 else 'No targets (simulated)'}"
            ))
        elif cmd_lower == "config": # Basic config display
            self.command_terminal.append_to_terminal(f"Build: {time.strftime('%Y-%m-%d')}, System Active: {self.system_active}")
        elif cmd_lower.startswith("pid "):
            parts = command.split()
            if len(parts) == 5:
                motor, p_s, i_s, d_s = parts[1].lower(), parts[2], parts[3], parts[4]
                try:
                    p,i,d = float(p_s), float(i_s), float(d_s)
                    if motor in ["pan", "tilt"]:
                        self.pid_tuning_panel.update_pid_input_fields(motor, p, i, d)
                        self.pid_tuning_panel._on_apply_settings_clicked() # Trigger apply logic
                        self.command_terminal.append_to_terminal(f"Terminal: {motor.capitalize()} PID set and applied.")
                    else: self.command_terminal.append_to_terminal("PID motor must be 'pan' or 'tilt'.")
                except ValueError: self.command_terminal.append_to_terminal("PID values must be numbers.")
            else: self.command_terminal.append_to_terminal("Usage: pid <pan|tilt> <P> <I> <D>")
        elif cmd_lower.startswith("roslog "):
            self.ros_connector._on_incoming_ros_log(command[len("roslog "):].strip())
        elif cmd_lower == "rosstatus":
             self.ros_connector._on_incoming_system_status({
                'esp32': random.choice([True,False]), 'laser': random.choice([True,False]),
                'motors': self.system_active, 'movement': self.system_active and random.choice([True,False])
            })
        else:
            self.command_terminal.append_to_terminal(f"Unknown command: {command}")

    def closeEvent(self, event):
        """Handles window close event, ensuring cleanup."""
        self.log_display.add_log_entry("GUI Shutting down...", False)
        self.log_timer.stop()
        self.power_simulation_timer.stop()
        if hasattr(self, 'image_view'): # Ensure image_view was initialized
            self.image_view.cleanup_resources() # Important for camera release
        self.ros_connector.shutdown()
        event.accept()