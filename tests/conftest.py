import pytest
from pytestqt.qt_compat import qt_api
from pytestqt.qtbot import QtBot

@pytest.fixture
def qapp():
    """Create a QApplication instance."""
    app = qt_api.QtWidgets.QApplication.instance()
    if app is None:
        app = qt_api.QtWidgets.QApplication([])
    yield app
    app.quit()

@pytest.fixture
def qtbot(qapp):
    """Fixture for Qt GUI testing."""
    return QtBot(qapp) 