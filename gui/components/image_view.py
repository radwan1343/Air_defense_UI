import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QComboBox, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel

class ImageView(QWidget):
    """
    Displays live camera feed using OpenCV with an integrated 'View' selector.
    Emits:
      - detection_layer_changed(str): on view selection change
      - log_message_requested(str): for status updates
    """
    detection_layer_changed = pyqtSignal(str)
    log_message_requested      = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._init_camera()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        # Group: View selector + camera feed
        group = QGroupBox("Camera View")
        group_layout = QVBoxLayout(group)
        group_layout.setContentsMargins(4,4,4,4)

            # View selection with label
        view_header = QHBoxLayout()
        view_label  = QLabel("View:", self)
        view_header.addWidget(view_label)
        self.view_combo = QComboBox(self)
        self.view_combo.addItems(["Raw image", "Tracking"])
        self.view_combo.currentTextChanged.connect(self.detection_layer_changed)
        view_header.addWidget(self.view_combo)
        group_layout.addLayout(view_header)


        # Camera display label
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        # Let it expand to fill available space
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_layout.addWidget(self.label)

        main_layout.addWidget(group, stretch=1)
        self.setLayout(main_layout)

    def _init_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.log_message_requested.emit("Unable to access camera")
            return
        # Timer for updating frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(30)  # ~33 FPS
        self.log_message_requested.emit("Camera feed started")

    def _update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        # BGR→RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.label.setPixmap(pix)

    def stop_camera_feed(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'cap'):
            self.cap.release()
        self.log_message_requested.emit("Camera feed stopped")

    def cleanup_resources(self):
        self.stop_camera_feed()
