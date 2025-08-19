
import flet as ft
from components.toast import ToastManager


class RegionSettingsComponent(ft.Container):
    """Region settings management component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build region settings interface"""
        
        # Region selector
        region_dropdown = ft.Dropdown(
            label="Region ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150,
            expand=True
        )
        
        region_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Region", on_click=self._add_region),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Region", on_click=self._delete_region)
        ], tight=True)
        
        # LED ID settings
        start_field = ft.TextField(
            label="Start",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True
        )
        
        end_field = ft.TextField(
            label="End",
            value="0", 
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True
        )
        
        return ft.Column([
            ft.Text("Region Settings", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text("Region ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                region_dropdown,
                region_buttons
            ], spacing=5),
            ft.Row([
                ft.Text("LED ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                ft.Text("Start:", size=11, width=40),
                start_field,
                ft.Text("End:", size=11, width=30),
                end_field
            ], spacing=5)
        ], spacing=8)
    
    def _add_region(self, e):
        self.toast_manager.show_success_sync("Region added successfully")
        
    def _delete_region(self, e):
        self.toast_manager.show_warning_sync("Region deleted")