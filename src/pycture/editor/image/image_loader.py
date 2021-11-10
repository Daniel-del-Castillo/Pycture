from PyQt5.QtCore import QObject, Signal
from PyQt5.QtGui import QImage
from .color import Color, RGBColor, GrayScaleLUT
from .pixel import Pixel
from ctypes import string_at


class ImageLoader(QObject):
    finished = Signal()

    def __init__(self, image):
        super().__init__()
        self.image = image

    def run(self):

        image: QImage = self.image
        image.histograms = [[0] * 256, [0] * 256, [0] * 256, [0] * 256]
        image.ranges = [[255, 0], [255, 0], [255, 0], [255, 0]]
     
        size = image.width() * image.height()

        pixels = image.constBits().asstring(size * 4)
        for i in range(size):
            i_ = i * 4
            bgr_bytes = pixels[i_:i_+3]
            b, g, r = [int.from_bytes(bgr_bytes[j:j+1], 'big') for j in range(3)]
 
            gray_value = 0
            rgb_values = [r, g, b]
            for i, value in enumerate(rgb_values):
                
                image.histograms[i][value] += 1

                gray_value += GrayScaleLUT[i][value]
            gray_value = round(gray_value)
            image.histograms[Color.Gray.value][gray_value] += 1
    
        
        image.histograms = list(map(lambda histogram:
                                    list(
                                        map(lambda x: x / size, histogram)),
                                    image.histograms
                                    ))
        self.load_means()
        image.load_finished = True
        
        self.finished.emit()

    def load_means(self):
        image = self.image
        image.means = [self.calculate_mean(hist) for hist in image.histograms]


    def calculate_mean(self, normalized_histogram):
        mean = sum([normalized_histogram[i] * i for i in range(len(normalized_histogram))])
        return mean
