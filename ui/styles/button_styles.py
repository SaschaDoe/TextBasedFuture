from PySide6.QtCore import Qt

def get_sci_fi_button_style() -> str:
    return """
        QPushButton {
            background-color: #1a1a2e;
            color: #00ff9d;
            border: 2px solid #00ff9d;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        QPushButton:hover {
            background-color: #16213e;
            border-color: #00ffcc;
            box-shadow: 0 0 15px #00ff9d;
        }
        QPushButton:pressed {
            background-color: #0f172a;
            border-color: #00ffb3;
        }
    """ 