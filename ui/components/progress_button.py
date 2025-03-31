from PySide6.QtWidgets import QPushButton, QProgressBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from ui.styles.button_styles import get_sci_fi_button_style

class ProgressButton(QWidget):
    """A button component that includes a progress bar.
    
    This component combines a button and progress bar, where the button is disabled
    while the progress bar is active. The progress bar appears inside the button
    at the bottom and animates from 0 to 100%.
    
    Note: This component uses is_enabled() and set_enabled() methods instead of Qt's
    built-in isEnabled() and setEnabled() to provide consistent behavior with the
    progress bar state.
    """
    
    # Signals
    progress_complete = Signal()
    clicked = Signal()
    state_changed = Signal(bool)  # Signal emitted when enabled state changes
    
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._enabled = False  # Track enabled state internally
        self._setup_ui(text)
        
    def _setup_ui(self, text: str):
        # Set the size for the whole widget
        self.setMinimumSize(300, 60)
        self.setMaximumWidth(300)
        
        # Create button (will be our container)
        self.button = QPushButton(text, self)
        self.button.setMinimumSize(300, 60)
        self.button.setMaximumWidth(300)
        self.button.setStyleSheet(get_sci_fi_button_style())
        self.button.setEnabled(False)  # Start disabled
        self.button.clicked.connect(self.clicked.emit)
        self.button.setGeometry(0, 0, 300, 60)  # Position at 0,0 with full size
        
        # Create progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # Hide the text label
        
        # Position the progress bar at the bottom of the button
        progress_height = 4
        self.progress_bar.setGeometry(QRect(0, 60 - progress_height, 300, progress_height))
        
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: transparent;
                height: 4px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
                border-radius: 2px;
            }
        """)
        
        # Create timer for progress animation
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_progress)
        self._progress = 0
        self._is_progressing = False
    
    def start_progress(self):
        """Start the progress animation"""
        self._progress = 0
        self._is_progressing = True
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.set_enabled(False)  # Use wrapper method
        self._timer.start(50)  # Update every 50ms
    
    def set_progress(self, value: int):
        """Set the progress value directly"""
        self._progress = value
        self.progress_bar.setValue(value)
        if value >= 100:
            self._timer.stop()
            self._is_progressing = False
            # Keep progress bar visible but at 100%
            self.progress_bar.setValue(100)
            self.set_enabled(True)  # Use wrapper method
            self.progress_complete.emit()
    
    def _update_progress(self):
        """Update the progress bar value"""
        if not self._is_progressing:
            return
        
        self._progress += 1
        self.progress_bar.setValue(self._progress)
        
        if self._progress >= 100:
            self._timer.stop()
            self._is_progressing = False
            # Keep progress bar visible but at 100%
            self.progress_bar.setValue(100)
            self.set_enabled(True)  # Use wrapper method
            self.progress_complete.emit()
    
    def is_enabled(self) -> bool:
        """Check if the button is enabled"""
        return self._enabled  # Use internal state instead of querying widget
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the button"""
        if self._enabled != enabled:  # Only change if different
            self._enabled = enabled
            self.button.setEnabled(enabled)
            self.state_changed.emit(enabled)
    
    # Override Qt's native methods to redirect to our custom methods
    def isEnabled(self) -> bool:
        """Override Qt's isEnabled to use our wrapper method"""
        return self.is_enabled()
        
    def setEnabled(self, enabled: bool):
        """Override Qt's setEnabled to use our wrapper method"""
        self.set_enabled(enabled)
    
    def setText(self, text: str):
        """Update the button text"""
        self.button.setText(text)
        print(f"ProgressButton.setText called with: {text}")
        print(f"Button text is now: {self.button.text()}")
        
    def resizeEvent(self, event):
        """Handle resize events to reposition the progress bar"""
        super().resizeEvent(event)
        width = event.size().width()
        height = event.size().height()
        
        # Update button size
        self.button.setGeometry(0, 0, width, height)
        
        # Update progress bar position
        progress_height = 4
        self.progress_bar.setGeometry(QRect(0, height - progress_height, width, progress_height)) 