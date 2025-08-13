"""
Region settings component
Path: src/components/region_settings.py
"""

import flet as ft


class RegionSettingsComponent(ft.Container):
    """Region settings management component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build_content()
        
    def build_content(self):
        """Build region settings interface"""
        
        # Region selector
        region_dropdown = ft.Dropdown(
            label="Region ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        region_buttons = ft.Row([
            ft.IconButton(ft.icons.ADD, tooltip="Add Region", on_click=self._add_region),
            ft.IconButton(ft.icons.DELETE, tooltip="Delete Region", on_click=self._delete_region)
        ])
        
        # LED ID settings
        start_field = ft.TextField(
            label="Start",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        end_field = ft.TextField(
            label="End",
            value="0", 
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
    def build_content(self):
        """Build region settings interface"""
        
        # Region selector
        region_dropdown = ft.Dropdown(
            label="Region ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        region_buttons = ft.Row([
            ft.IconButton(ft.icons.ADD, tooltip="Add Region", on_click=self._add_region),
            ft.IconButton(ft.icons.DELETE, tooltip="Delete Region", on_click=self._delete_region)
        ])
        
        # LED ID settings
        start_field = ft.TextField(
            label="Start",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        end_field = ft.TextField(
            label="End",
            value="0", 
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        return ft.Column([
            ft.Text("Region Settings", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Row([region_dropdown, region_buttons]),
            ft.Text("LED ID:"),
            ft.Row([start_field, end_field])
        ])
    
    def _add_region(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Region added successfully"))
        )
        
    def _delete_region(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Region deleted"))
        )