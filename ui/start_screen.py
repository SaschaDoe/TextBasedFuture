from PySide6.QtWidgets import QPushButton
from ui.base_screen import BaseScreen
from ui.styles.button_styles import get_sci_fi_button_style

class StartScreen(BaseScreen):
    def __init__(self):
        super().__init__("Text-Based Future")
        
        # Create buttons
        self.new_button = QPushButton("New Game")
        self.exit_button = QPushButton("Exit")
        
        # Style buttons
        for button in [self.new_button, self.exit_button]:
            button.setMinimumSize(300, 60)
            button.setStyleSheet(get_sci_fi_button_style())
        
        # Add buttons to layout
        self.layout.addWidget(self.new_button)
        self.layout.addWidget(self.exit_button)
        
        # Connect signals
        self.new_button.clicked.connect(self._on_new_game)
        self.exit_button.clicked.connect(self.close)
    
    def _on_new_game(self):
        self.navigate_to("civilisation_generation") 