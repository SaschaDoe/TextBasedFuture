import sys
from PySide6.QtWidgets import QApplication
from ui.start_screen import StartScreen
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from ui.navigation import NavigationManager
from config.container import Container

def main():
    # Create dependency injection container
    container = Container()
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create navigation manager
    nav_manager = NavigationManager()
    
    # Register screens with dependencies
    nav_manager.register_screen("start", StartScreen)
    nav_manager.register_screen("civilisation_generation", 
                              lambda: CivilisationGenerationScreen(container.table_loader()))
    
    # Start with the start screen
    nav_manager.navigate_to("start")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 