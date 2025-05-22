# air_defense_project/gui/components/command_terminal.py
"""
QWidget for the command terminal, including output display and input line.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QFrame, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal

class CommandTerminal(QWidget):
    """
    A terminal-like widget with an output area and an input line.
    Emits `command_entered` signal when the user submits a command.
    """
    command_entered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Component fills its allocated space

        terminal_frame = QFrame(self) # Frame provides border and padding via QSS
        terminal_frame.setObjectName("TerminalFrame")
        terminal_inner_layout = QVBoxLayout(terminal_frame)

        title_label = QLabel("Command Terminal", terminal_frame)
        title_label.setAlignment(Qt.AlignCenter)
        terminal_inner_layout.addWidget(title_label)

        self.terminal_output = QTextEdit(terminal_frame)
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setObjectName("TerminalOutput") # For specific styling if needed
        self.terminal_output.setText("$ System booted\n$ GUI initialized\n$ Ready for commands...")
        terminal_inner_layout.addWidget(self.terminal_output)

        input_layout = QHBoxLayout() # For prompt and input line
        prompt_label = QLabel("$", terminal_frame)
        prompt_label.setFixedWidth(15)
        self.terminal_input_line = QLineEdit(terminal_frame)
        self.terminal_input_line.returnPressed.connect(self._submit_input) # Handle Enter key

        input_layout.addWidget(prompt_label)
        input_layout.addWidget(self.terminal_input_line)
        terminal_inner_layout.addLayout(input_layout)

        layout.addWidget(terminal_frame)

    def _submit_input(self):
        """Processes command submission from the input line."""
        command_text = self.terminal_input_line.text().strip()
        if command_text:
            self.append_to_terminal(f"$ {command_text}") # Echo command
            self.command_entered.emit(command_text)
        self.terminal_input_line.clear()

    def append_to_terminal(self, text: str):
        """Appends text to the terminal output area and scrolls down."""
        self.terminal_output.append(text)
        self.terminal_output.verticalScrollBar().setValue(
            self.terminal_output.verticalScrollBar().maximum()
        )

    def clear_terminal(self):
        """Clears the terminal output and shows a ready prompt."""
        self.terminal_output.clear()
        self.append_to_terminal("$ Terminal cleared. Ready for commands...")