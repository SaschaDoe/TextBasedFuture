import pytest
from PySide6.QtWidgets import QApplication
from config.container import Container
from ui.navigation import NavigationManager
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from ui.start_screen import StartScreen

@pytest.fixture
def app(qtbot):
    container = Container()
    # You can configure the container for testing if needed
    # container.config.from_dict({"test_config": "value"})
    
    app = QApplication([])
    nav_manager = NavigationManager()
    
    nav_manager.register_screen("start", StartScreen)
    nav_manager.register_screen(
        "civilisation_generation", 
        lambda: CivilisationGenerationScreen(container.table_loader())
    )
    
    return app, nav_manager 