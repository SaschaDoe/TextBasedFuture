import pytest
from PySide6.QtCore import Qt
from unittest.mock import Mock
from ui.start_screen import StartScreen
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from ui.navigation import NavigationManager

@pytest.fixture
def mock_table_loader():
    return Mock()

@pytest.fixture
def nav_manager():
    nav_manager = NavigationManager()
    mock_table_loader = Mock()
    
    # Register screens with factories
    nav_manager.register_screen("start", lambda: StartScreen())
    nav_manager.register_screen(
        "civilisation_generation", 
        lambda: CivilisationGenerationScreen(mock_table_loader)
    )
    return nav_manager

@pytest.fixture
def window(qtbot, nav_manager):
    window = StartScreen()
    # Connect navigation signals to navigation manager
    window.navigate.connect(lambda screen_name: nav_manager.navigate_to(screen_name))
    qtbot.addWidget(window)
    window.show()
    return window

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
def test_button_clicks(qtbot, window, nav_manager):
    """Test that clicking buttons triggers navigation."""
    # Track button clicks with flags
    exit_clicked = False
    new_clicked = False

    def on_exit():
        nonlocal exit_clicked
        exit_clicked = True

    def on_new():
        nonlocal new_clicked
        new_clicked = True

    # Connect our test handlers to the buttons
    window.exit_button.clicked.connect(on_exit)
    window.new_button.clicked.connect(on_new)

    # Click the buttons
    qtbot.mouseClick(window.exit_button, Qt.LeftButton)
    qtbot.mouseClick(window.new_button, Qt.LeftButton)

    # Verify the clicks were registered
    assert exit_clicked, "Exit button click not registered"
    assert new_clicked, "New button click not registered"

@pytest.mark.ui
@pytest.mark.interaction
def test_new_game_navigation(qtbot, window, nav_manager):
    """Test that clicking New Game shows the Civilisation Generation screen."""
    # Click the New Game button
    qtbot.mouseClick(window.new_button, Qt.LeftButton)
    
    # Process events to allow signal propagation
    qtbot.wait(100)
    
    # Verify the start screen is hidden
    assert not window.isVisible()
    
    # Verify the current screen is civilisation generation
    assert nav_manager.get_current_screen() == "civilisation_generation"