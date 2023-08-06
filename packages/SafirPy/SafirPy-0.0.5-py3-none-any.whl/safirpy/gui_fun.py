# -*- coding: utf-8 -*-

import sys

from PySide2.QtWidgets import QApplication, QLabel
import PySide2.QtWidgets as QtWidgets

class EntryType1(QtWidgets.QDialog):

    def __init__(self):



class Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QtWidgets.QLineEdit("input file path")
        self.button = QtWidgets.QPushButton("select")

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.button.clicked.connect(self.get_file_path)

    # Greets the user
    def greetings(self):
        print("Hello %s" % self.edit.text())
        print(self.edit.isReadOnly())
        self.edit.setReadOnly(not self.edit.isReadOnly())

    def get_file_path(self):
        path_string = QtWidgets.QFileDialog().getOpenFileName()
        print(path_string)
        return path_string


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
