import flet as ft
import json
import os
from typing import Optional, Dict, Any
from ..utils.logger import AppLogger


class FileActionService:
    """Service to handle file operations like open, save, save as"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_file_path: Optional[str] = None
        self.current_data: Dict[str, Any] = {}
        self.is_modified: bool = False
        
    def open_file(self):
        """Open file dialog and load JSON data"""
        def on_file_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    self.current_file_path = file_path
                    self.current_data = data
                    self.is_modified = False
                    
                    AppLogger.success(f"File opened: {os.path.basename(file_path)}")
                    self._notify_data_loaded(data)
                    
                except json.JSONDecodeError as e:
                    AppLogger.error(f"Invalid JSON file: {str(e)}")
                except Exception as e:
                    AppLogger.error(f"Failed to open file: {str(e)}")
        
        file_picker = ft.FilePicker(on_result=on_file_result)
        file_picker.pick_files(
            dialog_title="Open Light Pattern File",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["json"]
        )
        
        self.page.overlay.append(file_picker)
        self.page.update()
        
    def save_file(self):
        """Save current data to existing file or show save as dialog"""
        if self.current_file_path:
            try:
                self._save_to_path(self.current_file_path)
                AppLogger.success(f"File saved: {os.path.basename(self.current_file_path)}")
            except Exception as e:
                AppLogger.error(f"Failed to save file: {str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        """Show save as dialog and save to new file"""
        def on_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                file_path = e.path
                if not file_path.endswith('.json'):
                    file_path += '.json'
                    
                try:
                    self._save_to_path(file_path)
                    self.current_file_path = file_path
                    AppLogger.success(f"File saved as: {os.path.basename(file_path)}")
                except Exception as e:
                    AppLogger.error(f"Failed to save file: {str(e)}")
        
        file_picker = ft.FilePicker(on_result=on_file_result)
        file_picker.save_file(
            dialog_title="Save Light Pattern File",
            file_name="light_pattern.json",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["json"]
        )
        
        self.page.overlay.append(file_picker)
        self.page.update()
        
    def _save_to_path(self, file_path: str):
        """Save current data to specified path"""
        current_state = self._get_current_application_state()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(current_state, f, indent=2, ensure_ascii=False)
            
        self.current_data = current_state
        self.is_modified = False
        
    def _get_current_application_state(self) -> Dict[str, Any]:
        """Get current application state for saving"""
        # TODO: Implement getting state from all components
        return {
            "version": "1.0",
            "scenes": [],
            "effects": [],
            "palettes": [],
            "segments": [],
            "regions": [],
            "settings": {
                "led_count": 255,
                "fps": 60
            },
            "metadata": {
                "created_with": "Light Pattern Designer",
                "file_format_version": "1.0"
            }
        }
        
    def _notify_data_loaded(self, data: Dict[str, Any]):
        """Notify application components that new data has been loaded"""
        # TODO: Implement notifying all components about loaded data
        AppLogger.info("Data loaded successfully")
        
    def update_current_data(self, data: Dict[str, Any]):
        """Update current data and mark as modified"""
        self.current_data = data
        self.is_modified = True
        
    def get_current_file_name(self) -> str:
        """Get current file name for display"""
        if self.current_file_path:
            return os.path.basename(self.current_file_path)
        return "Untitled"
        
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes"""
        return self.is_modified
        
    def _get_default_data(self) -> Dict[str, Any]:
        """Get default data for new file"""
        return {
            "version": "1.0",
            "scenes": [
                {
                    "id": 0,
                    "name": "Scene 1",
                    "led_count": 255,
                    "fps": 60
                }
            ],
            "effects": [
                {
                    "id": 0,
                    "name": "Effect 1",
                    "scene_id": 0
                }
            ],
            "palettes": [
                {
                    "id": 0,
                    "name": "Default Palette",
                    "colors": ["#000000", "#FF0000", "#FFFF00", "#0000FF", "#00FF00"]
                }
            ],
            "segments": [],
            "regions": [
                {
                    "id": 0,
                    "name": "All LEDs",
                    "start": 0,
                    "end": 254
                }
            ],
            "settings": {
                "led_count": 255,
                "fps": 60
            }
        }