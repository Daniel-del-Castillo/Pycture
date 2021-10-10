from PyQt5.QtWidgets import QWidget, QMainWindow

from .command import Command

class EditBrightnessCommand(Command):
    def __init__(self, parent: QWidget):
        super().__init__("Brightness", parent)

    def execute(self, main_window: QMainWindow):
        print("Edits brightness")