import flet as ft
import platform
from .toast import ToastManager


class MenuBarActionHandler:
    """Handle menu bar-related actions and business logic"""
    
    def __init__(self, page: ft.Page, file_service=None):
        self.page = page
        self.file_service = file_service
        self.toast_manager = ToastManager(page)
        self.current_platform = platform.system()
        
    def handle_open_file(self, e):
        """Handle open file action"""
        if self.check_unsaved_changes_before_open():
            if self.file_service:
                self.file_service.open_file()
                self.toast_manager.show_info_sync("Opening file...")
            else:
                self.toast_manager.show_info_sync("Open file dialog will be implemented")
        
    def handle_save_file(self, e):
        """Handle save file action"""
        if self.validate_file_operation("save"):
            if self.file_service:
                self.file_service.save_file()
                self.toast_manager.show_success_sync("File saved")
            else:
                self.toast_manager.show_success_sync("File saved successfully")
        
    def handle_save_as_file(self, e):
        """Handle save as file action"""
        if self.file_service:
            self.file_service.save_as_file()
            self.toast_manager.show_info_sync("Save as dialog opened")
        else:
            self.toast_manager.show_info_sync("Save as dialog will be implemented")
            
    def get_file_status_data(self):
        """Get current file status data"""
        if self.file_service:
            file_name = self.file_service.get_current_file_name()
            has_changes = self.file_service.has_unsaved_changes()
            return {
                'file_name': file_name,
                'has_unsaved_changes': has_changes,
                'display_name': f"{file_name}*" if has_changes else file_name
            }
        return {
            'file_name': "No file loaded",
            'has_unsaved_changes': False,
            'display_name': "No file loaded"
        }
        
    def get_platform_info(self) -> str:
        """Get current platform information"""
        return self.current_platform
        
    def validate_file_operation(self, operation_type: str) -> bool:
        """Validate file operation before execution"""
        if operation_type == "save" and self.file_service:
            if not self.file_service.has_unsaved_changes():
                self.toast_manager.show_info_sync("No changes to save")
                return False
                
        return True
        
    def check_unsaved_changes_before_open(self) -> bool:
        """Check for unsaved changes before opening new file"""
        if self.file_service and self.file_service.has_unsaved_changes():
            self.toast_manager.show_warning_sync("You have unsaved changes")
            return True
        return True
        
    def process_file_operation_result(self, operation: str, success: bool, error_message: str = None):
        """Process file operation result"""
        if success:
            if operation == "open":
                self.toast_manager.show_success_sync("File opened successfully")
            elif operation == "save":
                self.toast_manager.show_success_sync("File saved successfully")
            elif operation == "save_as":
                self.toast_manager.show_success_sync("File saved as new file")
        else:
            error_msg = error_message or f"Failed to {operation} file"
            self.toast_manager.show_error_sync(error_msg)
            
    def get_recent_files_list(self):
        """Get recent files list for menu"""
        if self.file_service and hasattr(self.file_service, 'get_recent_files'):
            return self.file_service.get_recent_files()
        return []
        
    def handle_recent_file_selection(self, file_path: str):
        """Handle recent file selection"""
        if self.check_unsaved_changes_before_open():
            if self.file_service and hasattr(self.file_service, 'open_file_by_path'):
                self.file_service.open_file_by_path(file_path)
                self.toast_manager.show_info_sync(f"Opening recent file: {file_path}")
            else:
                self.toast_manager.show_info_sync(f"Would open recent file: {file_path}")
                
    def validate_file_path(self, file_path: str) -> bool:
        """Validate file path"""
        if not file_path:
            self.toast_manager.show_error_sync("Invalid file path")
            return False
        if not file_path.endswith('.json'):
            self.toast_manager.show_warning_sync("File should be JSON format")
        return True