import sys
from PySide6.QtWidgets import QApplication
from ui.start_screen import StartScreen

def main():
    app = QApplication(sys.argv)
    window = StartScreen()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 