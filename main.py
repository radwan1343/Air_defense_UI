# air_defense_project/main.py
"""
Main entry point for the Air Defense GUI application.
Initializes the QApplication and the main GUI window.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication

# Ensure the 'gui' directory is in the Python path for correct module imports.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from gui.main_window import AirDefenseGUI

# Common workaround for Qt platform plugin issues.
if "QT_QPA_PLATFORM_PLUGIN_PATH" not in os.environ or not os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"]:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AirDefenseGUI()
    ex.show()
    sys.exit(app.exec_())