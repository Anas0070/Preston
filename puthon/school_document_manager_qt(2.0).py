import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

DOC_TYPES = ["Admission Form", "Fee Receipt", "Exam Result"]

class DocumentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Preston Higher Secondary School - Document Manager")
        self.setFixedSize(600, 400)
        self.center()

        # Stylesheet
        self.setStyleSheet("""
            QWidget { background: #f4f4f4; }
            QLabel { font-size: 16px; color: #333; }
            QLineEdit, QComboBox {
                background: #fff; padding: 6px;
                border-radius: 6px; border: 1px solid #ccc;
                font-size: 15px;
            }
            QPushButton {
                background: #007bff; color: #fff;
                border-radius: 8px; font-size: 16px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: #0056b3;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(40, 40, 40, 40)

        # Browse
        self.browse_btn = QPushButton("Browse Document")
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn)

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        # Name
        layout.addWidget(QLabel("Document Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Type
        layout.addWidget(QLabel("Document Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(DOC_TYPES)
        layout.addWidget(self.type_combo)

        # Save
        self.save_btn = QPushButton("Save Document")
        self.save_btn.clicked.connect(self.save_document)
        layout.addWidget(self.save_btn)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        screen = QApplication.primaryScreen()
        if screen is not None:
            cp = screen.availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Document", "",
            "All Supported Files (*.pdf *.jpg *.png);;PDF Files (*.pdf);;JPEG Files (*.jpg);;PNG Files (*.png)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
        else:
            self.selected_file = None
            self.file_label.setText("No file selected")

    def save_document(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a document file.")
            return

        doc_name = self.name_input.text().strip()
        if not doc_name:
            QMessageBox.warning(self, "Error", "Please enter a document name.")
            return

        doc_type = self.type_combo.currentText()
        dest_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not dest_folder:
            return

        _, ext = os.path.splitext(self.selected_file)
        new_filename = f"{doc_name}_{doc_type.replace(' ', '_')}{ext}"
        dest_path = os.path.join(dest_folder, new_filename)

        try:
            shutil.copy2(self.selected_file, dest_path)
            self.status_label.setText(f"Document saved as {new_filename}")
            QMessageBox.information(self, "Success", f"Document saved successfully:\n{new_filename}")
        except Exception as e:
            self.status_label.setText("Failed to save document.")
            QMessageBox.critical(self, "Error", f"Failed to save document:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocumentManager()
    window.show()
    sys.exit(app.exec_())