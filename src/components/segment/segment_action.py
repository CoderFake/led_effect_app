import flet as ft
from ..ui.toast import ToastManager
from services.data_cache import data_cache


class SegmentActionHandler:
    """Handle segment-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_segment(self, e):
        """Handle add segment action - show modal for custom ID input"""
        self._show_custom_id_dialog("Add Segment", self._create_segment_with_custom_id)
        
    def _show_custom_id_dialog(self, title: str, on_confirm_callback):
        """Show modal dialog for custom segment ID input"""
        def on_submit(e):
            try:
                custom_id = int(id_field.value)
                if on_confirm_callback(custom_id):
                    self.page.close(dialog)
            except ValueError:
                self.toast_manager.show_error_sync("Please enter a valid numeric ID")
                
        def on_cancel(e):
            self.page.close(dialog)
            
        id_field = ft.TextField(
            label="Segment ID",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
            autofocus=True
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Enter custom segment ID:"),
                    id_field
                ], spacing=10),
                width=250,
                height=100
            ),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.TextButton("OK", on_click=on_submit)
            ]
        )
        
        self.page.open(dialog)
        
    def _create_segment_with_custom_id(self, custom_id: int) -> bool:
        """Create segment with custom ID - add at end, set as current"""
        try:
            existing_ids = data_cache.get_segment_ids()
            if custom_id in existing_ids:
                self.toast_manager.show_error_sync(f"Segment ID {custom_id} already exists")
                return False
                
            success = data_cache.create_new_segment(custom_id)
            
            if success:
                self.toast_manager.show_success_sync(f"Segment {custom_id} created successfully")
                return True
            else:
                self.toast_manager.show_error_sync("Failed to create segment")
                return False
                
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to create segment: {str(ex)}")
            return False
        
    def delete_segment(self, e):
        """Handle delete segment action - remove current, move to lower ID"""
        current_segment_id = self._get_current_segment_id()
        if current_segment_id is None:
            self.toast_manager.show_warning_sync("No segment selected to delete")
            return
            
        all_segment_ids = data_cache.get_segment_ids()
        
        if len(all_segment_ids) <= 1:
            self.toast_manager.show_warning_sync("Cannot delete the last segment")
            return
            
        try:
            next_segment_id = None
            sorted_ids = sorted(all_segment_ids)
            current_index = sorted_ids.index(current_segment_id)
            
            if current_index > 0:
                next_segment_id = sorted_ids[current_index - 1]
            elif current_index + 1 < len(sorted_ids):
                next_segment_id = sorted_ids[current_index + 1]
                
            if next_segment_id is not None:
                success = data_cache.delete_segment(str(current_segment_id))
                if success:
                    self.toast_manager.show_warning_sync(f"Segment {current_segment_id} deleted, switched to Segment {next_segment_id}")
                else:
                    self.toast_manager.show_error_sync(f"Failed to delete segment {current_segment_id}")
            else:
                self.toast_manager.show_error_sync("Cannot determine next segment")
                
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to delete segment: {str(ex)}")
        
    def copy_segment(self, e):
        """Handle copy segment action - duplicate current segment at end, set as current"""
        current_segment_id = self._get_current_segment_id()
        if current_segment_id is None:
            self.toast_manager.show_warning_sync("No segment selected to duplicate")
            return
            
        try:
            new_segment_id = data_cache.duplicate_segment(str(current_segment_id))
            
            if new_segment_id is not None:
                self.toast_manager.show_success_sync(f"Segment {current_segment_id} duplicated as Segment {new_segment_id}")
            else:
                self.toast_manager.show_error_sync("Failed to duplicate segment")
                
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to duplicate segment: {str(ex)}")
        
    def solo_segment(self, e):
        """Handle segment solo action"""
        current_segment_id = self._get_current_segment_id()
        if current_segment_id is not None:
            segment = data_cache.get_segment(str(current_segment_id))
            if segment:
                current_solo = getattr(segment, 'is_solo', False)
                new_solo = not current_solo
                
                data_cache.update_segment_parameter(str(current_segment_id), "solo", new_solo)
                
                status = "enabled" if new_solo else "disabled"
                self.toast_manager.show_info_sync(f"Segment {current_segment_id} solo {status}")
        
    def mute_segment(self, e):
        """Handle segment mute action"""
        current_segment_id = self._get_current_segment_id()
        if current_segment_id is not None:
            segment = data_cache.get_segment(str(current_segment_id))
            if segment:
                current_mute = getattr(segment, 'is_mute', False)
                new_mute = not current_mute
            
                data_cache.update_segment_parameter(str(current_segment_id), "mute", new_mute)
                
                status = "enabled" if new_mute else "disabled"
                self.toast_manager.show_info_sync(f"Segment {current_segment_id} mute {status}")
        
    def reorder_segment(self, e):
        """Handle segment reorder action"""
        current_segment_id = self._get_current_segment_id()
        if current_segment_id is not None:
            self.toast_manager.show_info_sync(f"Segment {current_segment_id} reorder functionality - to be implemented")
        
    def assign_region_to_segment(self, segment_id: str, region_id: str):
        """Handle region assignment to segment"""
        self.toast_manager.show_info_sync(f"Segment {segment_id} assigned to Region {region_id}")
        
    def create_segment_with_id(self, custom_id: int):
        """Create segment with custom ID"""
        return self._create_segment_with_custom_id(custom_id)
        
    def duplicate_segment(self, source_id: str):
        """Duplicate existing segment"""
        try:
            new_segment_id = data_cache.duplicate_segment(source_id)
            
            if new_segment_id is not None:
                self.toast_manager.show_success_sync(f"Segment {source_id} duplicated as Segment {new_segment_id}")
                return new_segment_id
            else:
                self.toast_manager.show_error_sync(f"Failed to duplicate segment {source_id}")
                return None
                
        except Exception as ex:
            self.toast_manager.show_error_sync(f"Failed to duplicate segment: {str(ex)}")
            return None
        
    def update_segment_parameter(self, segment_id: str, param: str, value):
        """Update segment parameter with proper formatting"""
        try:
            success = data_cache.update_segment_parameter(segment_id, param, value)
            
            if success:
                if isinstance(value, (int, float)):
                    formatted_value = f"{float(value):.2f}"
                else:
                    formatted_value = str(value)
                
                self.toast_manager.show_info_sync(f"Segment {segment_id} {param} updated to {formatted_value}")
                return True
            else:
                self.toast_manager.show_error_sync(f"Failed to update segment {segment_id} {param}")
                return False
                
        except (ValueError, TypeError) as ex:
            self.toast_manager.show_error_sync(f"Invalid value for segment {param}")
            return False
        
    def toggle_solo_mode(self, segment_id: str, is_solo: bool):
        """Toggle segment solo mode"""
        success = data_cache.update_segment_parameter(segment_id, "solo", is_solo)
        if success:
            status = "enabled" if is_solo else "disabled"
            self.toast_manager.show_info_sync(f"Segment {segment_id} solo {status}")
        
    def toggle_mute_mode(self, segment_id: str, is_muted: bool):
        """Toggle segment mute mode"""
        success = data_cache.update_segment_parameter(segment_id, "mute", is_muted)
        if success:
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
        
    def _get_current_segment_id(self) -> int:
        """Get current segment ID from UI or cache"""
        try:
            segment_ids = data_cache.get_segment_ids()
            return segment_ids[0] if segment_ids else None
        except Exception:
            return None