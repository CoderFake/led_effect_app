import flet as ft
from ..ui.toast import ToastManager


class DimmerActionHandler:
    """Handle dimmer-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_dimmer_element(self, duration: str, initial_brightness: str, final_brightness: str):
        """Handle add dimmer element action"""
        if self._validate_dimmer_inputs(duration, initial_brightness, final_brightness):
            self.toast_manager.show_success_sync("Dimmer sequence added")
            return True
        return False
        
    def delete_dimmer_element(self):
        """Handle delete dimmer element action"""
        self.toast_manager.show_warning_sync("Dimmer sequence deleted")
        
    def update_dimmer_element(self, index: int, duration: str, initial: str, final: str):
        """Handle update dimmer element"""
        if self._validate_dimmer_inputs(duration, initial, final):
            self.toast_manager.show_info_sync(f"Dimmer element {index} updated")
            return True
        return False
        
    def create_dimmer_sequence(self, segment_id: str, duration_ms: int, initial_brightness: int, final_brightness: int):
        """Create dimmer sequence for segment"""
        if self._validate_brightness_values(initial_brightness, final_brightness):
            self.toast_manager.show_success_sync(f"Dimmer created for segment {segment_id}")
            return True
        return False
        
    def delete_dimmer_by_index(self, segment_id: str, index: int):
        """Delete dimmer element by index"""
        self.toast_manager.show_warning_sync(f"Dimmer element {index} deleted from segment {segment_id}")
        
    def reorder_dimmer_elements(self, segment_id: str, old_index: int, new_index: int):
        """Reorder dimmer elements"""
        self.toast_manager.show_info_sync(f"Dimmer element moved from {old_index} to {new_index}")
        
    def _validate_dimmer_inputs(self, duration: str, initial: str, final: str):
        """Validate dimmer input values"""
        try:
            duration_val = int(duration)
            initial_val = int(initial)
            final_val = int(final)
            
            if duration_val <= 0:
                self.toast_manager.show_error_sync("Duration must be positive (milliseconds)")
                return False
                
            if not self._validate_brightness_values(initial_val, final_val):
                return False
                
            return True
            
        except ValueError:
            self.toast_manager.show_error_sync("Please enter valid numeric values")
            return False
            
    def _validate_brightness_values(self, initial: int, final: int):
        """Validate brightness values (0-100 scale)"""
        if not (0 <= initial <= 100):
            self.toast_manager.show_error_sync("Initial brightness must be 0-100")
            return False
            
        if not (0 <= final <= 100):
            self.toast_manager.show_error_sync("Final brightness must be 0-100")
            return False
            
        return True
        
    def calculate_dimmer_total_duration(self, dimmer_elements):
        """Calculate total duration of dimmer sequence"""
        total = sum(element['duration'] for element in dimmer_elements)
        self.toast_manager.show_info_sync(f"Total sequence duration: {total}ms ({total/1000:.1f}s)")
        return total
        
    def validate_dimmer_sequence(self, dimmer_elements):
        """Validate entire dimmer sequence"""
        if not dimmer_elements:
            self.toast_manager.show_warning_sync("No dimmer elements defined")
            return False
            
        for i, element in enumerate(dimmer_elements):
            if element['duration'] <= 0:
                self.toast_manager.show_error_sync(f"Element {i}: Invalid duration")
                return False
                
        return True