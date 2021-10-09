from os import path

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent

from .menu_bar import MenuBar
from .editor import Editor
from .events import NewEditorEvent, DeleteEditorEvent, ChangeActiveEditorEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycture")
        self.setMenuBar(MenuBar(self))
        placeholder_widget = QWidget()
        placeholder_widget.setLayout(QGridLayout())
        self.setCentralWidget(placeholder_widget)
        self.editors = {}
        self.activeEditor = None
    
    def customEvent(self, event: QEvent):
        if type(event) == NewEditorEvent:
            event.command.execute(self)
        elif type(event) == DeleteEditorEvent:
            self.editors.pop(event.editor_name)
        elif type(event) == ChangeActiveEditorEvent:
            self.activeEditor = event.editor_name
        else:
            event.ignore()
            
    def addEditor(self, image: QPixmap, name: str):
        while self.editors.get(name):
            (name, extension) = path.splitext(name)
            name = name + "+" + extension
        self.editors[name] = Editor(self, image, name)