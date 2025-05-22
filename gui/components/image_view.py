## air_defense_project/gui/components/image_view.py
"""
QWidget for displaying a live camera feed or a static image, with detection layer controls.
Requires opencv-python: pip install opencv-python
"""
import os
import cv2 # OpenCV for camera functionality
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor, QImage

class ImageView(QWidget):
    """
    Displays video from a camera or a static image.
    Includes controls for camera, image loading, and detection layer overlay.
    """
    detection_layer_changed = pyqtSignal(str)
    log_message_requested = pyqtSignal(str, bool) # msg, is_warning
    image_successfully_loaded = pyqtSignal(str) # path of static image

    CAMERA_UPDATE_INTERVAL_MS = 33 # Approx 30 FPS

    def __init__(self, parent=None, camera_index=0):
        super().__init__(parent)
        self.current_static_image_path = None # Path to the displayed static image
        self.camera_capture = None
        self.camera_index = camera_index
        self.is_camera_feed_active = False

        self.camera_update_timer = QTimer(self)
        self.camera_update_timer.timeout.connect(self._update_camera_frame_display)

        self._initUI()

    def _initUI(self):
        """Initializes the UI elements."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        view_frame = QFrame(self)
        view_frame.setObjectName("ImageFrame") # For QSS styling
        frame_layout = QVBoxLayout(view_frame)

        # --- Header with controls ---
        controls_header_layout = QHBoxLayout()
        title_label = QLabel("System View", view_frame)
        controls_header_layout.addWidget(title_label)
        controls_header_layout.addStretch()

        self.start_camera_button = QPushButton("Start Camera", view_frame)
        self.start_camera_button.clicked.connect(self.start_camera_feed)
        controls_header_layout.addWidget(self.start_camera_button)

        self.stop_camera_button = QPushButton("Stop Camera", view_frame)
        self.stop_camera_button.clicked.connect(self.stop_camera_feed)
        self.stop_camera_button.setEnabled(False)
        controls_header_layout.addWidget(self.stop_camera_button)

        self.load_static_image_button = QPushButton("Load Static Image", view_frame)
        self.load_static_image_button.clicked.connect(self._show_load_static_image_dialog)
        controls_header_layout.addWidget(self.load_static_image_button)

        detection_label = QLabel("Layer:", view_frame) # Shorter label
        controls_header_layout.addWidget(detection_label)
        self.detection_layer_dropdown = QComboBox(view_frame)
        self.detection_layer_dropdown.addItems(["Detection", "Tracking", "Enemy"])
        self.detection_layer_dropdown.currentTextChanged.connect(self._on_detection_layer_change)
        controls_header_layout.addWidget(self.detection_layer_dropdown)
        frame_layout.addLayout(controls_header_layout)

        # --- Image Display Area ---
        self.image_display_label = QLabel(view_frame)
        self.image_display_label.setAlignment(Qt.AlignCenter)
        self.image_display_label.setMinimumSize(640, 480) # Default/minimum view size
        frame_layout.addWidget(self.image_display_label, 1) # Allow stretching

        main_layout.addWidget(view_frame)

        self._update_view_border_style() # Apply initial border
        self._display_default_content()  # Show placeholder or default image

    def _on_detection_layer_change(self, layer_name: str):
        """Handles detection layer selection change."""
        self.detection_layer_changed.emit(layer_name)
        self._update_view_border_style()

    def _get_border_color(self) -> str:
        """Determines border color based on current detection layer."""
        layer = self.detection_layer_dropdown.currentText()
        if layer == "Detection": return "#89b4fa" # Blue
        elif layer == "Tracking": return "#a6e3a1" # Green
        elif layer == "Enemy": return "#f38ba8"   # Red
        return "#cdd6f4" # Default

    def _update_view_border_style(self):
        """Applies border style to the image display label."""
        border_color = self._get_border_color()
        self.image_display_label.setStyleSheet(
            f"background-color: #1a1b26; border: 3px solid {border_color}; border-radius: 5px;"
        )

    def _display_default_content(self):
        """Displays default static image or a placeholder if camera isn't active."""
        # Determine project root based on this file's location (gui/components/image_view.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir)) # Up two levels
        default_static_image_path = os.path.join(project_root, "default_image.jpg")

        if os.path.exists(default_static_image_path):
            self.display_static_image(default_static_image_path)
        else:
            self.log_message_requested.emit(f"Default static image '{default_static_image_path}' not found.", True)
            self._set_placeholder_on_label("No Camera / Default Image Missing")

    def _set_placeholder_on_label(self, text: str):
        """Sets a placeholder pixmap with text on the display label."""
        # Use current label size for placeholder if available, else default
        width = self.image_display_label.width() if self.image_display_label.width() > 20 else 640
        height = self.image_display_label.height() if self.image_display_label.height() > 20 else 480
        
        placeholder = QPixmap(width, height)
        placeholder.fill(QColor("#1a1b26")) # Dark background for placeholder
        self.image_display_label.setPixmap(placeholder)
        self.image_display_label.setText(text)
        self.current_static_image_path = None # No static image is loaded

    def _show_load_static_image_dialog(self):
        """Opens dialog to load a static image. Stops camera if active."""
        self.stop_camera_feed() # Stop camera before loading static image
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Static Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.display_static_image(file_path)
            self.image_successfully_loaded.emit(file_path)

    def display_static_image(self, file_path: str):
        """Displays a static image from the given file path."""
        self.stop_camera_feed() # Ensure camera is off
        self.current_static_image_path = file_path

        if not os.path.exists(file_path):
            self.log_message_requested.emit(f"Static image not found: {file_path}", True)
            self._set_placeholder_on_label(f"Image Not Found: {os.path.basename(file_path)}")
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.log_message_requested.emit(f"Failed to load static image: {os.path.basename(file_path)}", True)
            self._set_placeholder_on_label(f"Load Failed: {os.path.basename(file_path)}")
            return

        self._apply_pixmap_to_label(pixmap)
        self.log_message_requested.emit(f"Displayed static image: {os.path.basename(file_path)}", False)
        self._update_view_border_style() # Ensure border is correct

    def _apply_pixmap_to_label(self, pixmap: QPixmap):
        """Scales and sets the provided QPixmap on the display label."""
        scaled_pixmap = pixmap.scaled(
            self.image_display_label.width(), self.image_display_label.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_display_label.setPixmap(scaled_pixmap)
        self.image_display_label.setText("") # Clear any placeholder text

    def _initialize_camera_capture(self) -> bool:
        """Initializes the cv2.VideoCapture object if not already done."""
        if self.camera_capture is None: # Only initialize if not already captured
            self.camera_capture = cv2.VideoCapture(self.camera_index)
            if not self.camera_capture.isOpened():
                self.log_message_requested.emit(f"Error: Could not open camera @ index {self.camera_index}.", True)
                self._set_placeholder_on_label(f"Camera {self.camera_index} Error/Unavailable")
                self.camera_capture = None # Reset to None if failed
                return False
            self.log_message_requested.emit(f"Camera {self.camera_index} opened.", False)
        return True

    def start_camera_feed(self):
        """Starts capturing and displaying frames from the camera."""
        if self.is_camera_feed_active: return

        if self._initialize_camera_capture():
            self.is_camera_feed_active = True
            self.camera_update_timer.start(self.CAMERA_UPDATE_INTERVAL_MS)
            self.start_camera_button.setEnabled(False)
            self.stop_camera_button.setEnabled(True)
            self.load_static_image_button.setEnabled(False) # Disable static load during live feed
            self.log_message_requested.emit("Camera feed started.", False)
            self.current_static_image_path = None # Live feed overrides static image path

    def stop_camera_feed(self):
        """Stops the camera feed and releases the camera resource."""
        # Consistent button state update, even if called redundantly
        self.start_camera_button.setEnabled(True)
        self.stop_camera_button.setEnabled(False)
        self.load_static_image_button.setEnabled(True)

        if not self.is_camera_feed_active and self.camera_capture is None:
            return # Nothing to stop

        self.is_camera_feed_active = False
        self.camera_update_timer.stop()
        if self.camera_capture is not None:
            self.camera_capture.release()
            self.camera_capture = None # Important to allow re-initialization
            self.log_message_requested.emit("Camera feed stopped and released.", False)

        # If no static image is set, show default content, otherwise static image remains.
        if not self.current_static_image_path:
            self._display_default_content()

    def _update_camera_frame_display(self):
        """Reads a frame, converts it to QPixmap, and displays it."""
        if not self.is_camera_feed_active or self.camera_capture is None:
            return

        read_success, frame_bgr = self.camera_capture.read()
        if read_success:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self._apply_pixmap_to_label(pixmap)
        else:
            self.log_message_requested.emit("Error reading frame from camera.", True)
            self.stop_camera_feed() # Stop feed if frames can't be read
            self._set_placeholder_on_label("Camera Frame Read Error")

    def resizeEvent(self, event):
        """Handles widget resize. Rescales displayed image/video frame."""
        super().resizeEvent(event)
        if self.is_camera_feed_active:
            # For live feed, the next frame update will scale correctly.
            # If an immediate rescale of the *current* frame is desired,
            # it would require caching the last QImage/QPixmap and re-applying,
            # but usually, letting the timer handle it is fine.
            pass
        elif self.current_static_image_path: # A static image is displayed
            # Re-apply the static image which will trigger rescaling
            self.display_static_image(self.current_static_image_path)
        else: # Placeholder is shown
            self._set_placeholder_on_label(self.image_display_label.text()) # Re-apply placeholder to resize it
            self._update_view_border_style() # Also ensure border is correct

    def cleanup_resources(self):
        """Releases camera resources. Call when parent is closing."""
        self.stop_camera_feed()