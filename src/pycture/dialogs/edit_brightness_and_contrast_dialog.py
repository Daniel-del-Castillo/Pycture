from typing import List

from PyQt5.QtWidgets import (
    QCheckBox, QDialog, QGridLayout, QVBoxLayout, QLabel, QMainWindow, QPushButton
)
from PyQt5.QtCore import Qt, Signal
from .widgets import RGBSliders, DropdownList

class EditBrightnessAndContrastDialog(QDialog):
    # The name of the editor and the values of the brightness and contrast
    applied = Signal(str, tuple, tuple)

    def __init__(self, parent: QMainWindow, editors: List[str]):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Edit brightness and contrast")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        

        self.layout.addWidget(QLabel(self, "Image:"))
        self.dropdown = DropdownList(self, editors)
        self.layout.addWidget(self.dropdown)
        self.dropdown.currentTextChanged.connect(self.update_selected_editor)
        self.current_brightness = [0] * 4
        self.current_contrast = [0] * 4
        
        gray_checkbox = QCheckBox("Gray scale")
        gray_checkbox.stateChanged.connect(self.toggle_gray)
        self.layout.addWidget(gray_checkbox)
        self.gray = False

        self.setup_sliders()
        apply_button = QPushButton("Apply", self)
        apply_button.pressed.connect(lambda:
            self.applied.emit(self.get_values())
        )
        self.layout.addWidget(apply_button)
        
        self.show()
        
    def setup_sliders(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Brightness", self), 0, 0)
        layout.addWidget(QLabel("Contrast", self), 0, 1)
        self.brightness_sliders = RGBSliders(self, 0, 255)
        self.brightness_sliders.set_values(self.current_brightness[:-1])
        layout.addWidget(self.brightness_sliders, 1, 0)
        self.contrast_sliders = RGBSliders(self, 0, 127)
        self.contrast_sliders.set_values(self.current_contrast[:-1])
        layout.addWidget(self.contrast_sliders, 1, 1)
        self.layout.addLayout(layout)

    def toggle_gray(self, gray: bool):
        self.gray = gray
        self.brightness_sliders.toggle_gray(gray)
        self.contrast_sliders.toggle_gray(gray)
        self.update_sliders()
        
    def update_sliders(self):
        if self.gray:
            brightness_values = [self.current_brightness[-1]] * 3
            contrast_values = [self.current_contrast[-1]] * 3
        else:
            brightness_values = self.current_brightness
            contrast_values = self.current_contrast
        self.brightness_sliders.set_values(brightness_values)
        self.contrast_sliders.set_values(contrast_values)
        
    def update_selected_editor(self, editor: str):
        image = self.parent().get_editor(editor).get_image()
        self.brightness_values = image.get_brightness()
        self.contrast_values = image.get_contrastbrightness()
        self.update_sliders()

    def get_values(self):
        brightness_values = self.brightness_sliders.get_values()
        contrast_values = self.contrast_sliders.get_values()
        return brightness_values, contrast_values
