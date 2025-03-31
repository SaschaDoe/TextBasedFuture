from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt
from ui.styles.button_styles import get_sci_fi_button_style

class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text-Based Future")
        
        # Get screen size and set window size to 70% of screen
        screen = self.screen().geometry()
        width = int(screen.width() * 0.7)
        height = int(screen.height() * 0.7)
        self.resize(width, height)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Create buttons
        self.new_button = QPushButton("New Game")
        self.exit_button = QPushButton("Exit")
        
        # Style buttons
        for button in [self.new_button, self.exit_button]:
            button.setMinimumSize(300, 60)
            button.setStyleSheet(get_sci_fi_button_style())
        
        # Add buttons to layout
        layout.addWidget(self.new_button)
        layout.addWidget(self.exit_button)
        
        # Connect signals
        self.new_button.clicked.connect(self._on_new_game)
        self.exit_button.clicked.connect(self.close)
    
    def _on_new_game(self):
        # Placeholder for navigation logic
        print("New Game clicked") 