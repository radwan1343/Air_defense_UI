## File: gui/components/no_fire_zone.py
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFormLayout, QLineEdit
from PyQt5.QtCore import pyqtSignal

class NoFireZoneWidget(QWidget):
    # Signal emitted when zone is defined/cleared
    # Emits dict with x_min and x_max
    zoneDefined = pyqtSignal(dict)
    zoneCleared = pyqtSignal()

    def __init__(self, parent=None):
        super(NoFireZoneWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        # Group box container
        group = QGroupBox("No-Fire Zone (X-axis)")
        layout = QVBoxLayout()

        # Instruction label
        self.label = QLabel(
            "Define a no-fire limit along X-axis:\n"
            "• Enter positive limit value below\n"
            "• Zone will be set from -X to +X"
        )
        layout.addWidget(self.label)

        # Input for X limit
        form_layout = QFormLayout()
        self.input_limit = QLineEdit()
        self.input_limit.setPlaceholderText("Enter X limit")
        form_layout.addRow("X Limit:", self.input_limit)
        layout.addLayout(form_layout)

        # Buttons row
        btn_layout = QHBoxLayout()
        self.btn_set = QPushButton("Set Zone")
        self.btn_clear = QPushButton("Clear Zone")
        btn_layout.addWidget(self.btn_set)
        btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        # Feedback
        self.status = QLabel("Zone: None")
        layout.addWidget(self.status)

        group.setLayout(layout)

        # Main widget layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # Connect signals
        self.btn_set.clicked.connect(self.on_set_zone)
        self.btn_clear.clicked.connect(self.on_clear_zone)

    def on_set_zone(self):
        # Read user input for limit
        try:
            limit = float(self.input_limit.text())
        except ValueError:
            self.status.setText("Invalid input: limit must be a number.")
            return
        x_min = -abs(limit)
        x_max = abs(limit)
        zone = {'x_min': x_min, 'x_max': x_max}
        self.status.setText(f"Zone: {x_min} to {x_max}")
        self.zoneDefined.emit(zone)

    def on_clear_zone(self):
        self.input_limit.clear()
        self.status.setText("Zone: None")
        self.zoneCleared.emit()
