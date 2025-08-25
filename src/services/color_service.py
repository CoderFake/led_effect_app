from typing import List, Optional, Callable
from models.color_palette import ColorPalette
from services.data_cache import data_cache
from utils.logger import AppLogger


class ColorService:
    """Service to handle color operations and palette management with cache integration"""
    
    def __init__(self):
        self.current_palette: Optional[ColorPalette] = None
        self.color_change_callbacks: List[Callable] = []
        self.current_segment_id: Optional[str] = None
        self.current_scene_id: Optional[int] = None
        self.current_effect_id: Optional[int] = None
        self.current_palette_id: Optional[int] = None
        self.is_loading_data = False
        
        self._initialize_default_palette()
        
    def _initialize_default_palette(self):
        """Initialize with default color palette"""
        try:
            default_colors = [
                "#000000",  # Black
                "#FF0000",  # Red  
                "#FFFF00",  # Yellow
                "#0000FF",  # Blue
                "#00FF00",  # Green
                "#FFFFFF"   # White
            ]
            
            self.current_palette = ColorPalette(
                id=0,
                name="Default Palette",
                colors=default_colors
            )
            
        except Exception as e:
            AppLogger.error(f"Error initializing color service: {e}")
        
    def set_loading_state(self, is_loading: bool):
        """Set loading state to suppress validation and notifications during data load"""
        self.is_loading_data = is_loading
        
    def set_current_segment_id(self, segment_id: Optional[str]):
        """Set the current segment ID for color operations"""
        self.current_segment_id = segment_id
        if not self.is_loading_data:
            AppLogger.info(f"Current segment set to: {segment_id}" if segment_id is not None else "No segment selected")
        self._notify_color_change()
        
    def set_current_scene_id(self, scene_id: Optional[int]):
        """Set current scene ID"""
        self.current_scene_id = scene_id
        
    def set_current_effect_id(self, effect_id: Optional[int]):
        """Set current effect ID"""
        self.current_effect_id = effect_id
        
    def set_current_palette_id(self, palette_id: Optional[int]):
        """Set current palette ID"""
        self.current_palette_id = palette_id
        
    def set_current_palette(self, palette: ColorPalette):
        """Set the current active palette"""
        self.current_palette = palette
        self._notify_color_change()
        
    def update_palette_color(self, slot_index: int, color: str):
        """Update a specific color slot in the current palette"""
        if self.current_palette and 0 <= slot_index < len(self.current_palette.colors):
            old_color = self.current_palette.colors[slot_index]
            self.current_palette.colors[slot_index] = color
            AppLogger.info(f"Color slot {slot_index} updated: {old_color} -> {color}")
            self._notify_color_change()
            
    def get_palette_colors(self) -> List[str]:
        """Get all colors from current palette (6 colors)"""
        if self.current_palette:
            return self.current_palette.colors.copy()
        
        try:
            cache_colors = data_cache.get_current_palette_colors()
            if cache_colors and len(cache_colors) >= 6:
                return cache_colors[:6]
        except Exception:
            pass
        
        return ["#000000", "#FF0000", "#FFFF00", "#0000FF", "#00FF00", "#FFFFFF"]
        
    def get_segment_colors(self) -> List[int]:
        """Get current segment colors - always return 6 values"""
        result_colors = [0] * 6
        
        try:
            if self.current_segment_id is not None:
                segment = data_cache.get_segment(self.current_segment_id)
                if segment and segment.color:
                    for i, color_index in enumerate(segment.color):
                        if i < 6:
                            result_colors[i] = color_index
                    
                    AppLogger.info(f"Segment {self.current_segment_id} colors: {result_colors}")
                    return result_colors
        except Exception as e:
            AppLogger.error(f"Error getting segment colors: {e}")
            
        return result_colors
        
    def get_segment_transparency(self) -> List[float]:
        """Get current segment transparency - always return 6 values"""
        result_transparency = [1.0] * 6
        
        try:
            if self.current_segment_id is not None:
                segment = data_cache.get_segment(self.current_segment_id)
                if segment and segment.transparency:
                    for i, transparency in enumerate(segment.transparency):
                        if i < 6:
                            result_transparency[i] = transparency
                    
                    AppLogger.info(f"Segment {self.current_segment_id} transparency: {result_transparency}")
                    return result_transparency
        except Exception as e:
            AppLogger.error(f"Error getting segment transparency: {e}")
            
        return result_transparency
        
    def get_segment_length(self) -> List[int]:
        """Get current segment length - always return 5 values (n-1)"""
        result_length = [0] * 5
        
        try:
            if self.current_segment_id is not None:
                segment = data_cache.get_segment(self.current_segment_id)
                if segment and segment.length:
                    for i, length in enumerate(segment.length):
                        if i < 5:
                            result_length[i] = length
                    
                    AppLogger.info(f"Segment {self.current_segment_id} length: {result_length}")
                    return result_length
        except Exception as e:
            AppLogger.error(f"Error getting segment length: {e}")
            
        return result_length
        
    def get_segment_transparency_values(self) -> List[float]:
        """Get transparency values from current segment - always return 6 values"""
        return self.get_segment_transparency()
        
    def get_segment_length_values(self) -> List[int]:
        """Get length values from current segment - always return 5 values (n-1)"""
        return self.get_segment_length()
        
    def get_segment_composition_colors(self) -> List[str]:
        """Get color composition from current segment with cache integration - always return 6 colors"""
        result_colors = ["#000000"] * 6
    
        try:
            if self.current_segment_id is not None:
                segment = data_cache.get_segment(self.current_segment_id)
                if segment and segment.color:
                    palette_colors = data_cache.get_current_palette_colors()
                    if palette_colors:
                        for i, color_index in enumerate(segment.color):
                            if i < 6 and 0 <= color_index < len(palette_colors):
                                result_colors[i] = palette_colors[color_index]
                        
                        return result_colors
        except Exception as e:
            AppLogger.error(f"Error getting segment composition colors: {e}")
  
        palette_colors = self.get_palette_colors()
        for i in range(min(6, len(palette_colors))):  
            if i < len(result_colors):
                result_colors[i] = palette_colors[i]
                
        return result_colors  
        
    def get_palette_color(self, slot_index: int) -> str:
        """Get specific color from palette by slot index"""
        palette_colors = self.get_palette_colors()
        if 0 <= slot_index < len(palette_colors):
            return palette_colors[slot_index]
        return "#000000"
        
    def update_segment_color_slot(self, segment_id: str, slot_index: int, color_index: int) -> bool:
        """Update segment color slot in cache"""
        try:
            success = data_cache.update_segment_parameter(
                segment_id, 
                "color", 
                {"index": slot_index, "color_index": color_index}
            )
            
            if success:
                AppLogger.info(f"Segment {segment_id} color slot {slot_index} updated to color index {color_index}")
                self._notify_color_change()
                return True
                
        except Exception as e:
            AppLogger.error(f"Error updating segment color slot: {e}")
            
        return False
        
    def update_segment_transparency(self, segment_id: str, slot_index: int, transparency: float) -> bool:
        """Update segment transparency in cache"""
        try:
            success = data_cache.update_segment_parameter(
                segment_id,
                "transparency", 
                {"index": slot_index, "transparency": transparency}
            )
            
            if success:
                AppLogger.info(f"Segment {segment_id} transparency slot {slot_index} updated to {transparency}")
                self._notify_color_change()
                return True
                
        except Exception as e:
            AppLogger.error(f"Error updating segment transparency: {e}")
            
        return False
        
    def update_segment_length(self, segment_id: str, slot_index: int, length: int) -> bool:
        """Update segment length in cache"""
        try:
            if not self.is_loading_data and length <= 0:
                return False
                
            success = data_cache.update_segment_parameter(
                segment_id,
                "length",
                {"index": slot_index, "length": length}
            )
            
            if success:
                AppLogger.info(f"Segment {segment_id} length slot {slot_index} updated to {length}")
                self._notify_color_change()
                return True
                
        except Exception as e:
            if not self.is_loading_data:
                AppLogger.error(f"Error updating segment length: {e}")
            
        return False
        
    def sync_with_cache_palette(self):
        """Sync current palette with cache data"""
        try:
            colors = data_cache.get_current_palette_colors()
            palette_id = data_cache.current_palette_id or 0
            
            if colors:
                self.current_palette = ColorPalette(
                    id=palette_id,
                    name=f"Palette {palette_id}",
                    colors=colors
                )
                AppLogger.info(f"Color service synced with cache palette {palette_id}")
                self._notify_color_change()
                
        except Exception as e:
            AppLogger.error(f"Error syncing with cache palette: {e}")
        
    def add_color_change_listener(self, callback: Callable):
        """Add listener for color changes"""
        if callback not in self.color_change_callbacks:
            self.color_change_callbacks.append(callback)
            
    def remove_color_change_listener(self, callback: Callable):
        """Remove color change listener"""
        if callback in self.color_change_callbacks:
            self.color_change_callbacks.remove(callback)
            AppLogger.info(f"Color change listener removed (total: {len(self.color_change_callbacks)})")
            
    def _notify_color_change(self):
        """Notify all listeners about color changes"""
        if self.is_loading_data:
            return
            
        for callback in self.color_change_callbacks[:]:
            try:
                if callable(callback):
                    callback()
                else:
                    self.color_change_callbacks.remove(callback)
            except Exception as e:
                AppLogger.error(f"Error in color change callback: {e}")
                if callback in self.color_change_callbacks:
                    self.color_change_callbacks.remove(callback)


color_service = ColorService()