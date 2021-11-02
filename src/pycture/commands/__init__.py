from .edit_commands import EditBrightness
from .file_commands import OpenFile, SaveFile
from .view_commands import (ViewRedHistogram, ViewGreenHistogram, ViewBlueHistogram,
                            ViewGrayScaleHistogram, ViewImageBrightness, ViewImageSize, ViewImageContrast,
                            ViewImageEntropy, ViewImageRanges)
from .help_commands import ShowHelp
from .command import Command


file_command_list = [OpenFile, SaveFile]
edit_command_list = [EditBrightness]
histogram_command_list = [
    ViewRedHistogram,
    ViewGreenHistogram,
    ViewBlueHistogram,
    ViewGrayScaleHistogram]
info_command_list = [
    ViewImageBrightness,
    ViewImageSize,
    ViewImageContrast,
    ViewImageEntropy,
    ViewImageRanges]
help_command_list = [ShowHelp]
