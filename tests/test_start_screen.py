import pytest
from PySide6.QtCore import Qt
from ui.start_screen import StartScreen
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from ui.navigation import NavigationManager

@pytest.fixture
def nav_manager():
    """Create a navigation manager for testing."""
    return NavigationManager()

@pytest.fixture
def window(qapp, nav_manager):
    """Create a fresh window for each test."""
    # Register all screens
    nav_manager.register_screen("start", StartScreen)
    nav_manager.register_screen("civilisation_generation", CivilisationGenerationScreen)
    
    # Create and connect start screen
    window = StartScreen()
    window.navigate.connect(nav_manager.navigate_to)
    yield window
    window.close()

@pytest.mark.ui
def test_window_title(window):
    """Test that the window title is correct."""
    assert window.windowTitle() == "Text-Based Future"

@pytest.mark.ui
def test_button_text(window):
    """Test that the button texts are correct."""
    assert window.new_button.text() == "New Game"
    assert window.exit_button.text() == "Exit"

@pytest.mark.ui
@pytest.mark.interaction
def test_button_clicks(qtbot, window):
    """Test that buttons can be clicked."""
    # Track button clicks
    exit_clicked = False
    new_clicked = False
    
    def on_exit():
        nonlocal exit_clicked
        exit_clicked = True
    
    def on_new():
        nonlocal new_clicked
        new_clicked = True
    
    # Connect signals
    window.exit_button.clicked.connect(on_exit)
    window.new_button.clicked.connect(on_new)
    
    # Click buttons
    qtbot.mouseClick(window.exit_button, Qt.LeftButton)
    qtbot.mouseClick(window.new_button, Qt.LeftButton)
    
    # Verify clicks were registered
    assert exit_clicked, "Exit button click not registered"
    assert new_clicked, "New game button click not registered"

@pytest.mark.ui
@pytest.mark.interaction
def test_new_game_navigation(qtbot, window, nav_manager):
    """Test that clicking New Game shows the Civilisation Generation screen."""
    # Click the New Game button
    qtbot.mouseClick(window.new_button, Qt.LeftButton)
    
    # Verify the start screen is hidden
    assert not window.isVisible()
    
    # Verify the current screen is civilisation generation
    assert nav_manager.get_current_screen() == "civilisation_generation"