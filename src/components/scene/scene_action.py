import flet as ft
from components.ui.toast import ToastManager
from services.data_cache import data_cache


class SceneActionHandler:
    """Handle scene-related actions and update cache database"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_scene(self, e):
        """Handle add scene action - create in cache database"""
        try:
            new_scene_id = data_cache.create_new_scene(led_count=255, fps=60)
            self.toast_manager.show_success_sync(f"Scene {new_scene_id} added successfully")
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to add scene: {str(ex)}")
        
    def delete_scene(self, e):
        """Handle delete scene action - remove from cache database"""
        current_scene = data_cache.get_current_scene()
        if current_scene:
            try:
                success = data_cache.delete_scene(current_scene.scene_id)
                if success:
                    self.toast_manager.show_warning_sync("Scene deleted")
                else:
                    self.toast_manager.show_error_sync("Cannot delete current scene")
            except Exception as ex:
                self.toast_manager.show_error_sync(f"Failed to delete scene: {str(ex)}")
        
    def copy_scene(self, e):
        """Handle copy scene action - duplicate in cache database"""
        current_scene = data_cache.get_current_scene()
        if current_scene:
            try:
                new_scene_id = data_cache.duplicate_scene(current_scene.scene_id)
                if new_scene_id:
                    self.toast_manager.show_success_sync(f"Scene copied as {new_scene_id}")
                else:
                    self.toast_manager.show_error_sync("Failed to copy scene")
            except Exception as ex:
                self.toast_manager.show_error_sync(f"Failed to copy scene: {str(ex)}")
        
    def change_scene(self, scene_id: str):
        """Handle scene change - update cache database"""
        try:
            scene_id_int = int(scene_id)
            success = data_cache.set_current_scene(scene_id_int)
            if success:
                self.toast_manager.show_info_sync(f"Changed to scene {scene_id}")
            else:
                self.toast_manager.show_error_sync(f"Failed to change to scene {scene_id}")
        except ValueError:
            self.toast_manager.show_error_sync(f"Invalid scene ID: {scene_id}")
        
    def create_scene_with_params(self, led_count: int, fps: int):
        """Create scene with specific parameters - add to cache database"""
        try:
            new_scene_id = data_cache.create_new_scene(led_count, fps)
            self.toast_manager.show_success_sync(f"Scene {new_scene_id} created with {led_count} LEDs at {fps} FPS")
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to create scene: {str(ex)}")
        
    def update_scene_settings(self, led_count: str, fps: str):
        """Update scene settings - modify cache database"""
        try:
            if data_cache.current_scene_id is not None:
                success = data_cache.update_scene_settings(
                    data_cache.current_scene_id,
                    int(led_count) if led_count else None,
                    int(fps) if fps else None
                )
                if success:
                    self.toast_manager.show_info_sync(f"Scene settings updated: {led_count} LEDs, {fps} FPS")
                else:
                    self.toast_manager.show_error_sync("Failed to update scene settings")
        except ValueError:
            self.toast_manager.show_error_sync("Invalid scene settings values")
        
    def get_available_scenes(self):
        """Get available scenes from cache database"""
        return data_cache.get_scene_ids()
        
    def get_current_scene_data(self):
        """Get current scene data from cache database"""
        return data_cache.get_current_scene()