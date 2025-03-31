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
    nav_manager.register_screen("start", lambda: StartScreen())
    nav_manager.register_screen("civilisation_generation", 
                              lambda: CivilisationGenerationScreen(container.table_loader()))
    
    # Start with the start screen
    nav_manager.navigate_to("start")
    
    # Connect navigation signals from screens to navigation manager
    for screen_name, screen in nav_manager._screens.items():
        screen.navigate.connect(lambda target_screen: nav_manager.navigate_to(target_screen))
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 