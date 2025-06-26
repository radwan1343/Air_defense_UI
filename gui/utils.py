from PyQt5.QtWidgets import QGroupBox, QLayout

def make_group(title: str, layout: QLayout, parent=None) -> QGroupBox:
    """
    Wraps a QLayout into a QGroupBox with the given title.
    """
    group = QGroupBox(title, parent)
    group.setLayout(layout)
    return group
