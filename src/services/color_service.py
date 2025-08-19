"""
Color Service - Handle color operations and palette management
Path: src/services/color_service.py
"""

import flet as ft
from typing import List, Optional, Callable
from models.color_palette import ColorPalette


class ColorService:
    """Service to handle color operations and palette management"""
    
    def __init__(self):
        self.current_palette: Optional[ColorPalette] = None
        self.color_change_callbacks: List[Callable] = []
        
    def set_current_palette(self, palette: ColorPalette):
        """Set the current active palette"""
        self.current_palette = palette
        self._notify_color_change()
        
    def update_palette_color(self, slot_index: int, color: str):
        """Update a specific color slot in the current palette"""
        if self.current_palette and 0 <= slot_index < len(self.current_palette.colors):
            self.current_palette.colors[slot_index] = color
            self._notify_color_change()
            
    def get_palette_colors(self) -> List[str]:
        """Get all colors from current palette"""
        if self.current_palette:
            return self.current_palette.colors.copy()
        return ["#000000"] * 6  # Default black colors
        
    def get_palette_color(self, slot_index: int) -> str:
        """Get specific color from palette by slot index"""
        if self.current_palette and 0 <= slot_index < len(self.current_palette.colors):
            return self.current_palette.colors[slot_index]
        return "#000000"  # Default black
        
    def add_color_change_listener(self, callback: Callable):
        """Add listener for color changes"""
        if callback not in self.color_change_callbacks:
            self.color_change_callbacks.append(callback)
            
    def remove_color_change_listener(self, callback: Callable):
        """Remove color change listener"""
        if callback in self.color_change_callbacks:
            self.color_change_callbacks.remove(callback)
            
    def _notify_color_change(self):
        """Notify all listeners about color changes"""
        for callback in self.color_change_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in color change callback: {e}")

color_service = ColorService()