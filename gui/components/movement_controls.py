# air_defense_project/gui/components/movement_controls.py
"""
QWidget for manual movement controls (up, down, left, right, shoot).
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal

class MovementControls(QWidget):
    """
    Provides directional and shoot buttons for manual system operation.
    Emits signals for movement and shoot commands.
    """
    movement_command_signal = pyqtSignal(str) # Direction: "UP", "DOWN", "LEFT", "RIGHT"
    shoot_command_signal = pyqtSignal()

    _BUTTON_FIXED_HEIGHT = 40
    _BUTTON_FIXED_WIDTH = 80

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        controls_frame = QFrame(self)
        frame_layout = QVBoxLayout(controls_frame)

        title_label = QLabel("Movement Controls", controls_frame)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        buttons_grid = QGridLayout() # For D-pad like arrangement
        buttons = { # Store buttons for easier iteration and connection
            "UP": QPushButton("↑", controls_frame),
            "DOWN": QPushButton("↓", controls_frame),
            "LEFT": QPushButton("←", controls_frame),
            "RIGHT": QPushButton("→", controls_frame),
            "SHOOT": QPushButton("SHOOT", controls_frame)
        }

        buttons["SHOOT"].setStyleSheet("background-color: #f38ba8; color: #11111b;")

        for direction, button in buttons.items():
            button.setFixedHeight(self._BUTTON_FIXED_HEIGHT)
            button.setFixedWidth(self._BUTTON_FIXED_WIDTH)
            if direction == "SHOOT":
                button.clicked.connect(self.shoot_command_signal.emit)
            else:
                # Use a lambda that captures the current value of 'direction'
                button.clicked.connect(lambda checked=False, d=direction: self.movement_command_signal.emit(d))


        buttons_grid.addWidget(buttons["UP"], 0, 1)
        buttons_grid.addWidget(buttons["LEFT"], 1, 0)
        buttons_grid.addWidget(buttons["SHOOT"], 1, 1)
        buttons_grid.addWidget(buttons["RIGHT"], 1, 2)
        buttons_grid.addWidget(buttons["DOWN"], 2, 1)
        buttons_grid.setAlignment(Qt.AlignCenter) # Attempt to center grid content

        frame_layout.addLayout(buttons_grid)
        layout.addWidget(controls_frame)