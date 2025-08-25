import flet as ft
from services.color_service import color_service
from .tabbed_color_picker import TabbedColorPickerDialog
from ..ui.toast import ToastManager


class ColorPaletteActionHandler:
    """Handle color palette-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_palette(self, e):
        """Handle add palette action"""
        self.toast_manager.show_success_sync("Palette added successfully")
        
    def delete_palette(self, e):
        """Handle delete palette action"""
        self.toast_manager.show_warning_sync("Palette deleted")
        
    def copy_palette(self, e):
        """Handle copy palette action"""
        self.toast_manager.show_success_sync("Palette copied")
        
    def edit_color(self, color_index: int, on_update_callback=None):
        """Handle color editing action"""
        current_color = color_service.get_palette_color(color_index)
        
        def on_color_confirm(selected_color: str):
            try:
                color_service.update_palette_color(color_index, selected_color)
                self.toast_manager.show_success_sync(f"Color {color_index + 1} updated")
                if on_update_callback:
                    on_update_callback()
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                self.toast_manager.show_error_sync(f"Error in color change callback: {str(e)}\n{tb}")
            
        color_picker = TabbedColorPickerDialog(
            initial_color=current_color,
            on_confirm=on_color_confirm
        )
        self.page.open(color_picker)
        
    def update_palette_dropdown_data(self, palette_ids):
        """Process palette IDs for dropdown update"""
        return [str(palette_id) for palette_id in palette_ids]
        
    def get_selected_palette_data(self, current_value):
        """Get currently selected palette data"""
        return current_value
        
    def set_palette_selection(self, new_palette_id: str):
        """Process palette selection change"""
        self.toast_manager.show_info_sync(f"Switched to palette {new_palette_id}")
        return new_palette_id
        
    def handle_palette_changed(self, color_boxes=None, color_container=None):
        """Handle palette change from color service"""
        try:
            colors = color_service.get_palette_colors()
            return colors
        except Exception as e:
            self.toast_manager.show_error_sync(f"Error updating palette: {e}")
            return None
            
    def validate_color_index(self, color_index: int) -> bool:
        """Validate color index for editing"""
        if not (0 <= color_index <= 5):
            self.toast_manager.show_error_sync("Invalid color index")
            return False
        return True
        
    def get_palette_colors(self):
        """Get current palette colors"""
        return color_service.get_palette_colors()
        
    def validate_palette_operation(self, operation: str, palette_id: str = None) -> bool:
        """Validate palette operations"""
        if operation == "delete" and palette_id == "0":
            self.toast_manager.show_warning_sync("Cannot delete default palette")
            return False
        return True