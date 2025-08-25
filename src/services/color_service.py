import flet as ft
from typing import List, Optional, Callable
from models.color_palette import ColorPalette
from services.data_cache import data_cache


class ColorService:
    """Service to handle color operations and palette management"""
    
    def __init__(self):
        self.current_palette: Optional[ColorPalette] = None
        self.color_change_callbacks: List[Callable] = []
        self.current_segment_id: Optional[str] = None
        
    def set_current_segment_id(self, segment_id: str):
        """Set the current segment ID for color operations"""
        self.current_segment_id = segment_id
        self._notify_color_change()
        
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
        """Get all colors from current palette (6 colors)"""
        if self.current_palette:
            return self.current_palette.colors.copy()
        return ["#000000"] * 6
        
    def get_segment_composition_colors(self) -> List[str]:
        """Get color composition from current segment"""
        result_colors = ["#000000"] * 6
    
        if self.current_segment_id is not None:
            segment = data_cache.get_segment(self.current_segment_id)
            if segment and segment.color:
                palette_colors = data_cache.get_current_palette_colors()
                if palette_colors:
                    for i, color_index in enumerate(segment.color):
                        if i < 6 and 0 <= color_index < len(palette_colors):
                            result_colors[i] = palette_colors[color_index]
  
        return result_colors  
        
    def get_palette_color(self, slot_index: int) -> str:
        """Get specific color from palette by slot index"""
        if self.current_palette and 0 <= slot_index < len(self.current_palette.colors):
            return self.current_palette.colors[slot_index]
        return "#000000"
        
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
        for callback in self.color_change_callbacks[:]:
            try:
                if callable(callback):
                    callback()
                else:
                    self.color_change_callbacks.remove(callback)
            except Exception:
                if callback in self.color_change_callbacks:
                    self.color_change_callbacks.remove(callback)

color_service = ColorService()