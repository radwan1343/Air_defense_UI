## File: gui/components/image_view.py
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QComboBox, QPushButton, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class ImageView(QWidget):
    """
    Displays live camera feed using OpenCV, with detection layer controls.
    """
    detection_layer_changed = pyqtSignal(str)
    image_successfully_loaded = pyqtSignal(str)  # compatibility
    log_message_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self._init_ui()
        self._init_camera()

    def _init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout(self)

        # Detection Layer Group (no extra padding)
        detect_group = QGroupBox("Detection Layer")
        detect_layout = QHBoxLayout()
        detect_layout.setContentsMargins(0, 0, 0, 0)
        detect_layout.setSpacing(5)
        self.detect_combo = QComboBox()
        self.detect_combo.addItems(["None", "Balloon", "Laser Spot", "Custom"])
        self.load_btn = QPushButton("Apply Layer")
        detect_layout.addWidget(self.detect_combo)
        detect_layout.addWidget(self.load_btn)
        detect_group.setLayout(detect_layout)
        detect_group.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(detect_group)

        # Camera Feed Group (responsive sizing)
        camera_group = QGroupBox("Camera Feed")
        camera_layout = QVBoxLayout()
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(0)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        camera_layout.addWidget(self.label)
        camera_group.setLayout(camera_layout)
        # Expand to fill available space
        camera_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(camera_group, stretch=1)

        # Connect detection layer controls
        self.load_btn.clicked.connect(self._on_apply_layer)

        self.setLayout(main_layout)

    def _init_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.log_message_requested.emit('Unable to access camera')
            return
        # Start timer to grab frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(30)  # approx 33fps
        self.log_message_requested.emit('Camera feed started (OpenCV)')

    def _update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        # Convert BGR to RGB for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.label.setPixmap(pix)

    def _on_apply_layer(self):
        layer = self.detect_combo.currentText()
        self.detection_layer_changed.emit(layer)
        self.log_message_requested.emit(f"Detection layer set to: {layer}")

    def stop_camera_feed(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'cap'):
            self.cap.release()
        self.log_message_requested.emit('Camera feed stopped')

    def cleanup_resources(self):
        self.stop_camera_feed()
