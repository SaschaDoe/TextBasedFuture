import sys
from PySide6.QtWidgets import QApplication
from ui.start_screen import StartScreen
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from ui.navigation import NavigationManager

def main():
    app = QApplication(sys.argv)
    
    # Create navigation manager
    nav_manager = NavigationManager()
    
    # Register screens
    nav_manager.register_screen("start", StartScreen)
    nav_manager.register_screen("civilisation_generation", CivilisationGenerationScreen)
    
    # Connect navigation signals
    for screen in [StartScreen, CivilisationGenerationScreen]:
        screen.navigate.connect(nav_manager.navigate_to)
    
    # Start with the start screen
    nav_manager.navigate_to("start")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 