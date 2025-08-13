"""
Color palette management component
Path: src/components/color_palette.py
"""

import flet as ft


class ColorPaletteComponent(ft.Container):
    """Color palette management component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.current_colors = [
            ft.Colors.BLACK,
            ft.Colors.RED, 
            ft.Colors.YELLOW,
            ft.Colors.BLUE,
            ft.Colors.GREEN,
            ft.Colors.WHITE
        ]
        self.content = self.build_content()
        
    def build_content(self):
        """Build color palette interface"""
        
        # Palette selector
        palette_dropdown = ft.Dropdown(
            label="Pallet ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        palette_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Palette", on_click=self._add_palette),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Palette", on_click=self._delete_palette),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Palette", on_click=self._copy_palette)
        ])
        
        # Color boxes
        color_boxes = []
        for i, color in enumerate(self.current_colors):
            color_box = ft.Container(
                width=50,
                height=40,
                bgcolor=color,
                border=ft.border.all(2, ft.Colors.GREY_600),
                border_radius=4,
                on_click=lambda e, idx=i: self._on_color_click(idx),
                tooltip=f"Color {i}"
            )
            color_boxes.append(color_box)
            
        color_row = ft.Row(controls=color_boxes, spacing=6, wrap=True)
        
    def build_content(self):
        """Build color palette interface"""
        
        # Palette selector
        palette_dropdown = ft.Dropdown(
            label="Pallet ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        palette_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Palette", on_click=self._add_palette),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Palette", on_click=self._delete_palette),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Palette", on_click=self._copy_palette)
        ])
        
        # Color boxes
        color_boxes = []
        for i, color in enumerate(self.current_colors):
            color_box = ft.Container(
                width=50,
                height=40,
                bgcolor=color,
                border=ft.border.all(2, ft.Colors.GREY_600),
                border_radius=4,
                on_click=lambda e, idx=i: self._on_color_click(idx),
                tooltip=f"Color {i}"
            )
            color_boxes.append(color_box)
            
        color_row = ft.Row(controls=color_boxes, spacing=6, wrap=True)
        
        return ft.Column([
            ft.Text("Color Pallets", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Row([palette_dropdown, palette_buttons]),
            ft.Text("Color:"),
            color_row
        ])
    
    def _on_color_click(self, color_index):
        """Handle color box click to open color picker"""
        self.page.open(
            ft.SnackBar(content=ft.Text(f"Color picker for Color {color_index} will be implemented"))
        )
        
    def _add_palette(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Palette added successfully"))
        )
        
    def _delete_palette(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Palette deleted"))
        )
        
    def _copy_palette(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Palette copied"))
        )