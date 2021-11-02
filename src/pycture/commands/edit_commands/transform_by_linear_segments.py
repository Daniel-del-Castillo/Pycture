from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow

from typing import List, Tuple
from matplotlib import pyplot as plt

from pycture.editor.image import Color
from pycture.dialogs import Notification, SegmentsInput
from ..command import Command


class TransformByLinearSegments(Command):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "By linear segments")

    def get_equation(self, segment: List[int]) -> Tuple:
        s = segment
        m = (s[1][1] - s[0][1]) / (s[1][0] - s[0][0])
        n = s[0][1] - m * s[0][0]
        return (lambda x: m * x + n)

    def get_LUT(self, segments: List):
        lut = list(range(256))
        num_of_segments = len(segments)
        equations = list(map(self.get_equation, segments))
        for i in range(256):
            j = 0
            s = segments[j]
            while (j < num_of_segments):
                s = segments[j]
                if (s[0][0] <= i <= s[1][0]):
                    break
                j += 1  # :(

            if (j < num_of_segments):
                equation = equations[j]
                lut[i] = round(equation(i))
        return lut

    def preview_transformation(self, points: List):
        x = []
        y = []
        for p in points:
            x.append(p[0])
            y.append(p[1])

        plt.style.use('dark_background')
        plt.clf()
        plt.plot(x, y)
        plt.xlabel("Vin")
        plt.ylabel("Vout")
        plt.title("Linear transformation")
        plt.show()

    def apply_transformation(
            self, main_window: QMainWindow, segments: List, opts: List[Color]):
        active_image = self.get_active_image(main_window)
        if active_image is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return
        if not active_image.load_finished:
            notification = Notification(main_window,
                                        "The image is still loading. Please wait a bit").exec()
            return

        lut = self.get_LUT(segments)
        title = self.get_active_title(main_window)

        transformed_img = active_image.apply_LUT(lut, opts)  # temp
        main_window.add_editor(QPixmap.fromImage(
            transformed_img), title + "-LT")

    def execute(self, main_window: QMainWindow):
        active_image = self.get_active_image(main_window)
        if active_image is None:
            notification = Notification(
                main_window, "There isn't an active editor!").exec()
            return
        if not active_image.load_finished:
            notification = Notification(main_window,
                                        "The image is still loading. Please wait a bit").exec()
            return

        dialog = SegmentsInput(main_window)
        dialog.previewed.connect(
            lambda s: self.preview_transformation(dialog.get_points()))
        dialog.applied.connect(
            lambda s: self.apply_transformation(
                main_window, s, dialog.get_color_opts()))