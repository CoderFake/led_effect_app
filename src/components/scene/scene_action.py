import flet as ft
from ..ui.toast import ToastManager


class SceneActionHandler:
    """Handle scene-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_scene(self, e):
        """Handle add scene action"""
        self.toast_manager.show_success_sync("Scene added successfully")
        
    def delete_scene(self, e):
        """Handle delete scene action"""
        self.toast_manager.show_warning_sync("Scene deleted")
        
    def copy_scene(self, e):
        """Handle copy scene action"""
        self.toast_manager.show_success_sync("Scene copied")
        
    def change_scene(self, scene_id: str):
        """Handle scene change"""
        self.toast_manager.show_info_sync(f"Changed to scene {scene_id}")
        
    def create_scene_with_params(self, led_count: int, fps: int):
        """Create scene with specific parameters"""
        self.toast_manager.show_success_sync(f"Scene created with {led_count} LEDs at {fps} FPS")