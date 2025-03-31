import pytest
from PySide6.QtWidgets import QApplication
from pytestqt.qt_compat import qt_api

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # We'll let the test framework clean up

@pytest.fixture
def qtbot(qapp, request):
    """Create a QtBot instance."""
    from pytestqt.qtbot import QtBot
    bot = QtBot(qapp)
    bot._request = request
    yield bot
    # Process events at the end of each test
    qapp.processEvents() 