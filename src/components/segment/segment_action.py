import flet as ft
from ..ui.toast import ToastManager


class SegmentActionHandler:
    """Handle segment-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_segment(self, e):
        """Handle add segment action"""
        self.toast_manager.show_success_sync("Segment added successfully")
        
    def delete_segment(self, e):
        """Handle delete segment action"""
        self.toast_manager.show_warning_sync("Segment deleted")
        
    def copy_segment(self, e):
        """Handle copy segment action"""
        self.toast_manager.show_success_sync("Segment copied")
        
    def solo_segment(self, e):
        """Handle segment solo action"""
        self.toast_manager.show_info_sync("Segment solo mode activated")
        
    def mute_segment(self, e):
        """Handle segment mute action"""
        self.toast_manager.show_info_sync("Segment muted")
        
    def assign_region_to_segment(self, segment_id: str, region_id: str):
        """Handle region assignment to segment"""
        self.toast_manager.show_info_sync(f"Segment {segment_id} assigned to Region {region_id}")
        
    def create_segment_with_id(self, custom_id: int):
        """Create segment with custom ID"""
        self.toast_manager.show_success_sync(f"Segment {custom_id} created")
        
    def duplicate_segment(self, source_id: str):
        """Duplicate existing segment"""
        self.toast_manager.show_success_sync(f"Segment {source_id} duplicated")
        
    def reorder_segment(self, segment_id: str, new_position: int):
        """Reorder segment position"""
        self.toast_manager.show_info_sync(f"Segment {segment_id} moved to position {new_position}")
        
    def update_segment_parameter(self, segment_id: str, param: str, value):
        """Update segment parameter"""
        self.toast_manager.show_info_sync(f"Segment {segment_id} {param} updated to {value}")
        
    def toggle_solo_mode(self, segment_id: str, is_solo: bool):
        """Toggle segment solo mode"""
        status = "enabled" if is_solo else "disabled"
        self.toast_manager.show_info_sync(f"Segment {segment_id} solo {status}")
        
    def toggle_mute_mode(self, segment_id: str, is_muted: bool):
        """Toggle segment mute mode"""
        status = "enabled" if is_muted else "disabled"
        self.toast_manager.show_info_sync(f"Segment {segment_id} mute {status}")
        
    def validate_segment_parameters(self, move_range_start: int, move_range_end: int, initial_position: int):
        """Validate segment movement parameters"""
        if move_range_end < move_range_start:
            self.toast_manager.show_error_sync("Move range end must be >= start")
            return False
            
        if not (move_range_start <= initial_position <= move_range_end):
            self.toast_manager.show_warning_sync("Initial position should be within move range")
            
        return True