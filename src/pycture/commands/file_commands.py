from os import path

from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap

from .command import Command
from ..dialogs import Notification


class OpenFile(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Open")

    def execute(self, main_window: QMainWindow):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Open an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        (_, filename) = path.split(file_path)
        main_window.add_editor(QPixmap(file_path), filename)


class SaveFile(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "Save")

    def execute(self, main_window: QMainWindow):
        image = self.get_active_image(main_window)
        if image is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save an image", "/home", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        _, extension = path.splitext(file_path)
        if not extension:
            extension = ".png"
        elif extension not in [".png", ".jpg", ".jpeg", ".bmp"]:
            notification = Notification(main_window,
                                        "Supported extensions are .png, .jpg, .jpeg and .bmp").exec()
            return
        image.pixmap().save(file_path, extension[1:])
