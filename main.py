from PySide6.QtWidgets import QApplication
import sys
from gui import Gui

def main():
    # Initalize the application
    app = QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()