import flet as ft
from functools import partial
from components.toast import ToastManager
from components.tabbed_color_picker import TabbedColorPickerDialog
from services.color_service import color_service


class ColorPaletteComponent(ft.Container):
    """Color palette management component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        
        self.current_colors = color_service.get_palette_colors()
        
        color_service.add_color_change_listener(self._on_palette_change)
        
        self.content = self.build_content()
        
    def build_content(self):
        """Build color palette interface"""
        
        # Palette selector
        palette_dropdown = ft.Dropdown(
            label="Pallet ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150,
            expand=True
        )
        
        palette_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Palette", on_click=self._add_palette),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Palette", on_click=self._delete_palette),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Palette", on_click=self._copy_palette)
        ], tight=True)
        
        # Color boxes
        color_boxes = []
        for i, color in enumerate(self.current_colors):
            color_box = ft.Container(
                width=50,
                height=40,
                bgcolor=color,
                border=ft.border.all(2, ft.Colors.GREY_600),
                border_radius=4,
                on_click=partial(self._on_color_click_handler, i),
                tooltip=f"Color {i}"
            )
            color_boxes.append(color_box)
            
        color_row = ft.Row(
            controls=color_boxes,
            spacing=5,
            wrap=True
        )
        
        return ft.Column([
            ft.Text("Color Pallets", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text("Pallet ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                palette_dropdown,
                palette_buttons
            ], spacing=5),
            ft.Row([
                ft.Text("Color:", size=12, weight=ft.FontWeight.W_500, width=80),
                color_row
            ], spacing=5)
        ], spacing=8)
    
    def _on_color_click_handler(self, color_index, e):
        """Handle color box click event with proper self reference"""
        self._on_color_click(color_index)
        
    def _on_color_click(self, color_index):
        """Handle color box click - Show Color Picker"""
        current_color = self.current_colors[color_index]
        
        def on_color_confirm(selected_color: str):
            """Handle color picker confirmation"""
            self.current_colors[color_index] = selected_color
            self._update_color_boxes()
            color_service.update_palette_color(color_index, selected_color)
            self.toast_manager.show_success_sync(f"Color {color_index} updated to {selected_color}")
            
        try:
            color_dialog = TabbedColorPickerDialog(
                initial_color=current_color,
                on_confirm=on_color_confirm
            )
            
            color_dialog.page = self.page
            self.page.overlay.append(color_dialog)
            color_dialog.open = True
            self.page.update()
        except Exception as e:
            self.toast_manager.show_error_sync(f"Error: {str(e)}")
        
    def _update_color_boxes(self):
        """Update color boxes appearance after color change"""
        self.content = self.build_content()
        self.update()
        
    def _on_palette_change(self):
        """Handle palette changes from color service"""
        self.current_colors = color_service.get_palette_colors()
        self._update_color_boxes()
        
    def _add_palette(self, e):
        self.toast_manager.show_success_sync("Palette added successfully")
        
    def _delete_palette(self, e):
        self.toast_manager.show_warning_sync("Palette deleted")
        
    def _copy_palette(self, e):
        self.toast_manager.show_success_sync("Palette copied")