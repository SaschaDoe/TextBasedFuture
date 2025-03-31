import pytest
from unittest.mock import Mock, MagicMock, patch
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtWidgets import QProgressBar, QApplication
from ui.civilisation_generation_screen import CivilisationGenerationScreen
from data.table_loader import TableLoader

@pytest.fixture
def mock_table_loader():
    loader = Mock(spec=TableLoader)
    # Add the dice_factory attribute needed by the TableLoadingThread
    loader.dice_factory = Mock()
    return loader

@pytest.fixture
def window(qtbot, mock_table_loader, monkeypatch):
    # Patch the TableLoadingThread to prevent it from starting automatically
    # This prevents the real thread from running and setting the button to enabled
    original_start = CivilisationGenerationScreen.start_data_loading
    
    def mock_start_data_loading(self):
        self.generate_button.setEnabled(False)
        # Do not start the actual thread
    
    monkeypatch.setattr(CivilisationGenerationScreen, "start_data_loading", mock_start_data_loading)
    
    window = CivilisationGenerationScreen(mock_table_loader)
    qtbot.addWidget(window)
    window.show()
    
    # Restore original method after initialization
    monkeypatch.setattr(CivilisationGenerationScreen, "start_data_loading", original_start)
    
    return window

@pytest.mark.ui
def test_generate_button_initial_state(window):
    """Test that the Generate button is disabled initially."""
    assert not window.generate_button.is_enabled()

@pytest.mark.ui
@pytest.mark.interaction
def test_generate_button_progress(qtbot, window, monkeypatch):
    """Test that the Generate button shows progress and becomes enabled when complete."""
    # Verify initial state
    assert not window.generate_button.is_enabled()
    
    # Create a mock thread with proper signals
    class MockThread(QObject):
        progress = Signal(int)
        finished = Signal(dict)
        
        def __init__(self, *args, **kwargs):
            super().__init__()
            
        def start(self):
            # Immediately emit progress completion and finished signal
            QTimer.singleShot(100, lambda: self.progress.emit(100))
            QTimer.singleShot(200, lambda: self.finished.emit({"test": MagicMock()}))
    
    # Create our mock thread instance
    mock_thread = MockThread()
    
    # Patch the thread constructor
    def mock_thread_constructor(*args, **kwargs):
        return mock_thread
    
    # Apply the patch
    monkeypatch.setattr("ui.civilisation_generation_screen.TableLoadingThread", mock_thread_constructor)
    
    # Wait for the state_changed signal to be emitted when button is enabled
    with qtbot.waitSignal(window.generate_button.state_changed, timeout=1000) as blocker:
        # Start loading data (this will use our mock)
        window.start_data_loading()
    
    # Verify the signal was emitted with the correct value
    assert blocker.args == [True]
    
    # Verify the button is now enabled
    assert window.generate_button.is_enabled()
    assert window.generate_button.button.isEnabled()

def test_generate_button_initially_disabled(window):
    assert not window.generate_button.is_enabled()

# Create a helper for mocking Table class and instances
class MockTable:
    def __init__(self):
        self.roll_result = MagicMock()
        self.roll_result.value = "Test Value"
        self.roll_result.text = "Test Description"
    
    def roll(self):
        return self.roll_result

# Now using signals for proper testing - no need to skip
def test_generate_button_enabled_after_loading(qtbot, window):
    """Test that the button can be properly enabled after loading."""
    # Verify initially disabled
    assert not window.generate_button.is_enabled()
    
    # Create a mock table with the minimum required interface
    mock_table = MockTable()
    
    # Wait for the signal when calling _on_tables_loaded
    window._on_tables_loaded({"test_table": mock_table})
    qtbot.waitUntil(lambda: window.generate_button.is_enabled(), timeout=1000)
    
    # Verify the button is now enabled - using both methods to ensure consistency
    assert window.generate_button.is_enabled()
    assert window.generate_button.button.isEnabled()
    
    # Additional verification that states are consistent
    assert window.generate_button.is_enabled() == window.generate_button.button.isEnabled()

# Add other tests as needed 