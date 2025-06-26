## File: gui/components/no_fire_zone.py
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFormLayout, QLineEdit
from PyQt5.QtCore import pyqtSignal

class NoFireZoneWidget(QWidget):
    """
    Widget to define a no-fire zone along the X axis with lower and upper limits.
    Emits:
      - zoneDefined(dict) with {'x_lower': float, 'x_upper': float}
      - zoneCleared()
    """
    zoneDefined = pyqtSignal(dict)
    zoneCleared = pyqtSignal()

    def __init__(self, parent=None):
        super(NoFireZoneWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        group = QGroupBox("No-Fire Zone (X-axis Limits)")
        layout = QVBoxLayout()

        # Instruction
        self.label = QLabel(
            "Enter lower and upper X-axis limits for no-fire zone:\n"
            "• Lower limit: the minimum X coordinate\n"
            "• Upper limit: the maximum X coordinate"
        )
        layout.addWidget(self.label)

        # Input fields
        form_layout = QFormLayout()
        self.input_lower = QLineEdit()
        self.input_lower.setPlaceholderText("Lower limit (float)")
        self.input_upper = QLineEdit()
        self.input_upper.setPlaceholderText("Upper limit (float)")
        form_layout.addRow("Lower X:", self.input_lower)
        form_layout.addRow("Upper X:", self.input_upper)
        layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_set = QPushButton("Set Zone")
        self.btn_clear = QPushButton("Clear Zone")
        btn_layout.addWidget(self.btn_set)
        btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        # Status
        self.status = QLabel("Zone: None")
        layout.addWidget(self.status)

        group.setLayout(layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # Connections
        self.btn_set.clicked.connect(self.on_set_zone)
        self.btn_clear.clicked.connect(self.on_clear_zone)

    def on_set_zone(self):
        try:
            lower = float(self.input_lower.text())
            upper = float(self.input_upper.text())
        except ValueError:
            self.status.setText("Invalid input: please enter numeric limits.")
            return
        if lower > upper:
            self.status.setText("Lower limit must be <= upper limit.")
            return
        zone = {'x_lower': lower, 'x_upper': upper}
        self.status.setText(f"Zone: [{lower}, {upper}]")
        self.zoneDefined.emit(zone)

    def on_clear_zone(self):
        self.input_lower.clear()
        self.input_upper.clear()
        self.status.setText("Zone: None")
        self.zoneCleared.emit()
