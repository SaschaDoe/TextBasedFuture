from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from typing import Optional, Callable

class BaseScreen(QMainWindow):
    # Signal emitted when navigation is requested
    navigate = Signal(str)  # Signal with screen name as parameter
    
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self._setup_window()
        
    def _setup_window(self):
        # Set window size to 70% of screen
        screen = self.screen().geometry()
        width = int(screen.width() * 0.7)
        height = int(screen.height() * 0.7)
        self.resize(width, height)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)
    
    def navigate_to(self, screen_name: str):
        """Request navigation to another screen"""
        self.navigate.emit(screen_name)
        self.hide()
    
    def show_screen(self):
        """Show this screen"""
        self.show() 