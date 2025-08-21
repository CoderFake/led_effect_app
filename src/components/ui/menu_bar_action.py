import flet as ft
import platform
from .toast import ToastManager


class MenuBarActionHandler:
    """Handle menu bar-related actions and business logic"""
    
    def __init__(self, page: ft.Page, file_service=None, data_action_handler=None):
        self.page = page
        self.file_service = file_service
        self.data_action_handler = data_action_handler
        self.toast_manager = ToastManager(page)
        self.current_platform = platform.system()
        
        # Set up file service callbacks if provided
        if self.file_service:
            self.file_service.on_file_open_requested = self._handle_file_open_request
            self.file_service.on_file_save_as_requested = self._handle_file_save_as_request
            self.file_service.on_file_loaded = self._handle_file_loaded_result
            self.file_service.on_file_saved = self._handle_file_saved_result
            self.file_service.on_error = self._handle_file_error
            
        # Initialize file picker dialogs but don't add to overlay yet
        self.file_picker = None
        self.save_file_picker = None
        
    def handle_open_file(self, e):
        """Handle open file action"""
        print("DEBUG: handle_open_file called")  # Debug log
        if self.check_unsaved_changes_before_open():
            if self.file_service:
                print("DEBUG: Calling file_service.request_file_open()")  # Debug log
                self.file_service.request_file_open()
            else:
                self.toast_manager.show_info_sync("File service not available")
                
    def _handle_file_open_request(self):
        """Handle file open request from service"""
        print("DEBUG: _handle_file_open_request called")
        
        # Create new file picker each time
        if self.file_picker:
            # Remove old picker
            try:
                self.page.overlay.remove(self.file_picker)
            except:
                pass
        
        self.file_picker = ft.FilePicker(
            on_result=self._on_file_picker_result
        )
        
        # Add to overlay and update
        self.page.overlay.append(self.file_picker)
        self.page.update()
        
        print("DEBUG: About to call file_picker.pick_files()")
        
        # Call pick_files
        self.file_picker.pick_files(
            dialog_title="Open JSON File",
            allowed_extensions=["json"],
            allow_multiple=False
        )
        
    def _on_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle file picker result"""
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            if self.file_service:
                self.file_service.load_file_from_path(file_path)
        else:
            self.toast_manager.show_warning_sync("No file selected")
            
    def _handle_file_loaded_result(self, file_path: str, success: bool, error_message: str = None):
        """Handle file loaded result from service"""
        if success:
            self.toast_manager.show_success_sync(f"File loaded successfully: {file_path}")
        else:
            error_msg = error_message or "Failed to load file"
            self.toast_manager.show_error_sync(error_msg)
        
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
            self.file_service.request_save_as()
        else:
            self.toast_manager.show_info_sync("File service not available")
            
    def _handle_file_save_as_request(self):
        """Handle file save as request from service"""
        print("DEBUG: _handle_file_save_as_request called")
        
        # Create new save file picker each time
        if self.save_file_picker:
            # Remove old picker
            try:
                self.page.overlay.remove(self.save_file_picker)
            except:
                pass
        
        self.save_file_picker = ft.FilePicker(
            on_result=self._on_save_file_picker_result
        )
        
        # Add to overlay and update
        self.page.overlay.append(self.save_file_picker)
        self.page.update()
        
        print("DEBUG: About to call save_file_picker.save_file()")
        
        # Call save_file
        self.save_file_picker.save_file(
            dialog_title="Save JSON File",
            file_name="data.json",
            allowed_extensions=["json"]
        )
        
    def _on_save_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle save file picker result"""
        if e.path:
            if self.file_service:
                self.file_service.save_to_path(e.path)
        else:
            self.toast_manager.show_warning_sync("No file path selected")
            
    def _handle_file_saved_result(self, file_path: str, success: bool, error_message: str = None):
        """Handle file saved result from service"""
        if success:
            self.toast_manager.show_success_sync(f"File saved successfully: {file_path}")
        else:
            error_msg = error_message or "Failed to save file"
            self.toast_manager.show_error_sync(error_msg)
            
    def _handle_file_error(self, error_message: str):
        """Handle file service errors"""
        self.toast_manager.show_error_sync(error_message)
            
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
            if self.file_service and hasattr(self.file_service, 'load_file_from_path'):
                self.file_service.load_file_from_path(file_path)
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