from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QDateEdit, QPushButton, QFileDialog
)
from PySide6.QtGui import QFont, QPalette, QColor, QAction
from PySide6.QtCore import Qt, QDate
import sys

from PySide6.QtWidgets import QMessageBox

from updater import check_for_update, download_update, launch_update

from PySide6.QtCore import QTimer

import os

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        # title
        self.setWindowTitle("File Management")

        # window size
        self.setMinimumSize(500, 400)

        # Create light and dark palettes
        self.light_palette = self.create_light_palette()
        self.dark_palette = self.create_dark_palette()

        # Detect system theme at startup
        self.is_dark_mode = self.detect_system_dark_mode()
        self.apply_palette()

        # initialize ui
        self.init_ui()
        self.create_menu()

        # Run update check 1 second after window shows (to avoid startup lag)
        QTimer.singleShot(1000, self.check_for_updates_silent)

        # Check if the update was successful
        self.check_update_success_flag()

    def detect_system_dark_mode(self):
        """
        Detects if the system is in dark mode by checking the window color.
        """

        # Returns the systems color scheme
        palette = QApplication.palette()
        color = palette.color(QPalette.Window)
        # return True if the color is dark
        return color.value() < 128

    def create_light_palette(self):
        """
        Creates a light color palette for the application.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f9f9fb"))
        palette.setColor(QPalette.WindowText, QColor("#444444"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#e5e5e5"))
        palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ToolTipText, QColor("#000000"))
        palette.setColor(QPalette.Text, QColor("#222222"))
        palette.setColor(QPalette.Button, QColor("#5a9df9"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.BrightText, QColor("#ff0000"))
        palette.setColor(QPalette.Highlight, QColor("#3a7de0"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        return palette

    def create_dark_palette(self):
        """
        Creates a dark color palette for the application.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#e0e0e0"))
        palette.setColor(QPalette.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.AlternateBase, QColor("#2c2c2c"))
        palette.setColor(QPalette.ToolTipBase, QColor("#353535"))
        palette.setColor(QPalette.ToolTipText, QColor("#f0f0f0"))
        palette.setColor(QPalette.Text, QColor("#dddddd"))
        palette.setColor(QPalette.Button, QColor("#3a7de0"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.BrightText, QColor("#ff5555"))
        palette.setColor(QPalette.Highlight, QColor("#5a9df9"))
        palette.setColor(QPalette.HighlightedText, QColor("#000000"))
        return palette

    def apply_palette(self):
        """
        Applies the appropriate palette and stylesheet based on the current mode.
        """
        if self.is_dark_mode:
            QApplication.instance().setPalette(self.dark_palette)
            self.setStyleSheet(self.dark_stylesheet())
        else:
            QApplication.instance().setPalette(self.light_palette)
            self.setStyleSheet(self.light_stylesheet())

    def init_ui(self):
        """"
        Initializes the user interface of the application.
        """
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(30)
        central.setLayout(main_layout)

        # Title label
        title = QLabel("Choose a Date and Upload a File")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        main_layout.addWidget(title)

        # Date picker container
        date_label = QLabel("Select Date")
        date_label.setFont(QFont("Segoe UI", 10))
        date_label.setToolTip("Input a date stated on the invoice.")
        main_layout.addWidget(date_label)

        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setFont(QFont("Segoe UI", 11))
        main_layout.addWidget(self.date_picker)

        # File upload container
        file_label = QLabel("Upload File")
        file_label.setFont(QFont("Segoe UI", 10))
        file_label.setToolTip("Upload Invoice.")
        main_layout.addWidget(file_label)

        self.upload_btn = QPushButton("Select File")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setFont(QFont("Segoe UI", 11))
        self.upload_btn.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(self.upload_btn, alignment=Qt.AlignLeft)

        self.file_path_label = QLabel("No file selected.")
        self.file_path_label.setFont(QFont("Segoe UI", 9))
        main_layout.addWidget(self.file_path_label)

        # Confirm button
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.setCursor(Qt.PointingHandCursor)
        self.confirm_btn.setFont(QFont("Segoe UI", 11))
        self.confirm_btn.clicked.connect(self.confirm_file)
        main_layout.addWidget(self.confirm_btn, alignment=Qt.AlignCenter)

    def create_menu(self):
        # Create the menu bar
        menu_bar = self.menuBar()

        # Add View to Menu
        view_menu = menu_bar.addMenu("View")

        # Add Dark Mode Toggle Action
        self.dark_mode_action = QAction("Toggle Dark Mode", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(self.is_dark_mode)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)

        # Add Help Menu
        help_menu = menu_bar.addMenu("Help")

        # Add Check for Updates Action in the Help Menu
        self.update_action = QAction("Check for Updates", self)
        self.update_action.triggered.connect(self.check_for_updates_with_feedback)
        help_menu.addAction(self.update_action)

    def open_file_dialog(self):
        """
        Opens a file dialog to select a file and updates the label with the selected file path.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file")

        
        if file_path:
            # store file path for later use
            self.full_file_path = file_path
            # Shorten the file path for display if it's too long
            display_path = file_path if len(file_path) < 40 else "..." + file_path[-37:]
            self.file_path_label.setText(display_path)
        else:
            self.file_path_label.setText("No file selected.")

    def toggle_dark_mode(self):
        """
        Toggles between light and dark mode.
        """
        self.is_dark_mode = not self.is_dark_mode
        self.dark_mode_action.setChecked(self.is_dark_mode)
        self.apply_palette()

    def light_stylesheet(self):
        return """
        QWidget {
            background-color: #f9f9fb;
            color: #444444;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        QDateEdit {
            border: 1.8px solid #ccc;
            border-radius: 8px;
            padding: 8px 12px;
            background-color: #fff;
            color: #222;
            min-width: 160px;
        }
        QDateEdit:focus {
            border-color: #5a9df9;
            /* Qt stylesheets don't support box-shadow, so omitted */
        }
        QPushButton {
            background-color: #5a9df9;
            border-radius: 10px;
            color: white;
            padding: 10px 18px;
            min-width: 150px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #3a7de0;
        }
        QPushButton:pressed {
            background-color: #2f63b7;
        }
        QLabel {
            color: #222;
        }

        """

    def dark_stylesheet(self):
        return """
        QWidget {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        QDateEdit {
            border: 1.8px solid #444;
            border-radius: 8px;
            padding: 8px 12px;
            background-color: #1e1e1e;
            color: #ddd;
            min-width: 160px;
        }
        QDateEdit:focus {
            border-color: #5a9df9;
            /* box-shadow omitted */
        }
        QPushButton {
            background-color: #3a7de0;
            border-radius: 10px;
            color: white;
            padding: 10px 18px;
            min-width: 150px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #5a9df9;
        }
        QPushButton:pressed {
            background-color: #2f63b7;
        }
        QLabel {
            color: #ddd;
        }
        """
    
    def check_for_updates_with_feedback(self):
        """
        Checks for updates and gives user feedback if there is an update available.
        """

        has_update, new_version = check_for_update()
        if has_update:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version ({new_version}) is available.\nDo you want to download and install it?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                file_path = download_update()
                if file_path:
                    QMessageBox.information(self, "Download Complete", "The update will now install.")
                    launch_update(file_path)
                else:
                    QMessageBox.warning(self, "Download Failed", "Could not download the update.")
        else:
            QMessageBox.information(self, "Up to Date", "You are using the latest version.")
    
    def check_for_updates_silent(self):
        """
        Checks for update and only prompts the user if an update is available.
        """

        has_update, new_version = check_for_update()
        if has_update:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version ({new_version}) is available.\nDo you want to download and install it?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                file_path = download_update()
                if file_path:
                    QMessageBox.information(self, "Download Complete", "The update will now install.")
                    launch_update(file_path)
                else:
                    QMessageBox.warning(self, "Download Failed", "Could not download the update.")

    def confirm_file(self):
        """
        Validates the selected file and date, and simulates a submission.
        """
        file_path = self.file_path_label.text()
        date = self.date_picker.date().toString("yyyy-MM-dd")

        if file_path == "No file selected.":
            QMessageBox.warning(self, "Missing File", "Please select a file before submitting.")
            return

        # Simulate upload logic (replace with actual logic later)
        print(f"Submitting file: {self.full_file_path}")
        print(f"With date: {date}")
        
        # Show success message
        QMessageBox.information(self, "Submitted", f"File submitted for date: {date}")

    def check_update_success_flag(self):
        flag_path = os.path.join(os.path.dirname(sys.argv[0]), "update_success.flag")
        if os.path.exists(flag_path):
            QMessageBox.information(self, "Update Complete", "The application was successfully updated.")
            os.remove(flag_path)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Gui()
    window.show()
    sys.exit(app.exec())
