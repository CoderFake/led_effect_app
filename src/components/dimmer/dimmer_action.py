import flet as ft
from ..ui.toast import ToastManager
from services.data_service import DataService


class DimmerActionHandler:
    """Handle dimmer-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        self.data_service = DataService()
        
    def add_dimmer_element(self, duration: str, initial_brightness: str, final_brightness: str, dimmer_data: list):
        """Handle add dimmer element action"""
        if self._validate_dimmer_inputs(duration, initial_brightness, final_brightness):
            try:
                new_element = {
                    "duration": int(duration),
                    "initial": int(initial_brightness), 
                    "final": int(final_brightness)
                }
                
                response = self.data_service.add_dimmer_element(new_element)
                if response.get("success", False):
                    dimmer_data.append(new_element)
                    self.toast_manager.show_success_sync("Dimmer sequence added")
                    return True
                else:
                    self.toast_manager.show_error_sync(response.get("message", "Failed to add dimmer element"))
                    return False
                    
            except Exception as e:
                self.toast_manager.show_error_sync(f"Error adding dimmer element: {str(e)}")
                return False
        return False
        
    def delete_dimmer_element(self, index: int, dimmer_data: list):
        """Handle delete dimmer element action"""
        if 0 <= index < len(dimmer_data):
            try:
                # Call service to delete element
                response = self.data_service.delete_dimmer_element(index)
                if response.get("success", False):
                    deleted_element = dimmer_data.pop(index)
                    self.toast_manager.show_warning_sync(f"Dimmer element {index} deleted")
                    return True
                else:
                    self.toast_manager.show_error_sync(response.get("message", "Failed to delete dimmer element"))
                    return False
                    
            except Exception as e:
                self.toast_manager.show_error_sync(f"Error deleting dimmer element: {str(e)}")
                return False
        else:
            self.toast_manager.show_error_sync("Invalid row index for deletion")
            return False
        
    def update_dimmer_element(self, index: int, duration: str, initial: str, final: str, dimmer_data: list):
        """Handle update dimmer element on unfocus"""
        if not (0 <= index < len(dimmer_data)):
            self.toast_manager.show_error_sync("Invalid row index for update")
            return False
            
        if self._validate_dimmer_inputs(duration, initial, final):
            try:
                updated_element = {
                    "duration": int(duration),
                    "initial": int(initial),
                    "final": int(final)
                }
                
                # Call service to update element
                response = self.data_service.update_dimmer_element(index, updated_element)
                if response.get("success", False):
                    dimmer_data[index] = updated_element
                    self.toast_manager.show_info_sync(f"Dimmer element {index} updated")
                    return True
                else:
                    self.toast_manager.show_error_sync(response.get("message", "Failed to update dimmer element"))
                    return False
                    
            except Exception as e:
                self.toast_manager.show_error_sync(f"Error updating dimmer element: {str(e)}")
                return False
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