import pytest
from PySide6.QtCore import Qt
from ui.navigation import NavigationManager
from ui.start_screen import StartScreen
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from unittest.mock import Mock

def test_navigation_with_dependencies(qtbot):
    nav_manager = NavigationManager()
    mock_table_loader = Mock()
    
    nav_manager.register_screen("start", StartScreen)
    nav_manager.register_screen(
        "civilisation_generation", 
        lambda: CivilisationGenerationScreen(mock_table_loader)
    )
    
    nav_manager.navigate_to("start")
    nav_manager.navigate_to("civilisation_generation") 

@pytest.mark.ui
def test_navigate_from_start_to_generation_screen(qtbot):
    # Create navigation manager
    nav_manager = NavigationManager()
    mock_table_loader = Mock()
    
    # Register screens
    nav_manager.register_screen("start", lambda: StartScreen())
    nav_manager.register_screen(
        "civilisation_generation", 
        lambda: CivilisationGenerationScreen(mock_table_loader)
    )
    
    # Navigate to start screen
    nav_manager.navigate_to("start")
    start_screen = nav_manager._screens["start"]
    qtbot.addWidget(start_screen)
    
    # Connect navigation signal
    start_screen.navigate.connect(lambda screen_name: nav_manager.navigate_to(screen_name))
    
    # Click the New Game button to navigate to generation screen
    qtbot.mouseClick(start_screen.new_button, Qt.LeftButton)
    
    # Process events
    qtbot.wait(100)
    
    # Verify we've navigated to the generation screen
    assert nav_manager.get_current_screen() == "civilisation_generation"
    
    # Get the generation screen and verify the generate button exists
    generation_screen = nav_manager._screens["civilisation_generation"]
    assert hasattr(generation_screen, "generate_button")
    assert generation_screen.generate_button.button.isVisible() 