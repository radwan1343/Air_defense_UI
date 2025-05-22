# air_defense_project/gui/styles.py
"""
Contains the QSS (Qt StyleSheet) for styling the application.
"""
STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QFrame {
        border: 1px solid #313244;
        border-radius: 8px;
        padding: 5px;
    }
    QFrame#LeftPanelFrame, QFrame#CenterPanelFrame, QFrame#RightPanelFrame {
        /* Specific styling for main panel containers if needed */
    }
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #cdd6f4;
    }
    QPushButton {
        background-color: #45475a;
        color: #cdd6f4;
        border-radius: 4px;
        padding: 8px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #585b70;
    }
    QPushButton:pressed {
        background-color: #7f849c;
    }
    QRadioButton {
        color: #cdd6f4;
        spacing: 8px;
    }
    QRadioButton::indicator {
        width: 15px;
        height: 15px;
    }
    QTextEdit, QLineEdit, QSpinBox {
        background-color: #11111b;
        color: #a6e3a1;
        border: 1px solid #313244;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        padding: 5px;
    }
    QTextEdit { /* Overriding default for general QTextEdit if not for input */
        color: #cdd6f4;
    }
    QTextEdit#TerminalOutput { /* Specific terminal output styling */
        color: #a6e3a1;
    }
    QSlider::groove:horizontal {
        border: 1px solid #313244;
        height: 8px;
        background: #313244;
        margin: 2px 0;
    }
    QSlider::handle:horizontal {
        background: #89b4fa;
        border: 1px solid #74c7ec;
        width: 18px;
        margin: -2px 0;
        border-radius: 9px;
    }
    QComboBox {
        background-color: #11111b;
        color: #cdd6f4;
        border: 1px solid #313244;
        border-radius: 4px;
        padding: 5px;
        selection-background-color: #45475a;
    }
    QComboBox QAbstractItemView {
        background-color: #11111b;
        color: #cdd6f4;
        selection-background-color: #585b70;
        border-radius: 4px;
        border: 1px solid #313244;
    }
    QFormLayout QLabel {
        /* Custom styling for labels within QFormLayout if needed */
    }
"""