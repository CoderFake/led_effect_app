"""
Color components package - Updated with ColorPaletteComponent
Path: src/components/color/__init__.py
"""

from .color_wheel import ColorWheel
from .color_picker import ColorPicker
from .tabbed_color_picker import TabbedColorPickerDialog
from .color_selection_modal import ColorSelectionModal, ColorSelectionButton
from .color_palette import ColorPaletteComponent

__all__ = [
    'ColorWheel',
    'ColorPicker', 
    'TabbedColorPickerDialog',
    'ColorSelectionModal',
    'ColorSelectionButton',
    'ColorPaletteComponent'
]