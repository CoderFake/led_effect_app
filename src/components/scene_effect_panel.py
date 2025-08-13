"""
Scene and Effect control panel
Path: src/components/scene_effect_panel.py
"""

import flet as ft
from components.color_palette import ColorPaletteComponent
from components.region_settings import RegionSettingsComponent


class SceneEffectPanel(ft.Container):
    """Left panel containing Scene/Effect controls"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build the scene/effect panel"""
        
        # Scene/Effect section
        scene_effect_section = self._build_scene_effect_section()
        
        # Scene Settings section
        scene_settings_section = self._build_scene_settings_section()
        
        # Color Palette component
        self.color_palette = ColorPaletteComponent(self.page)
        
        # Region Settings component
        self.region_settings = RegionSettingsComponent(self.page)
        
        return ft.Column([
            scene_effect_section,
            ft.Divider(),
            scene_settings_section,
            ft.Divider(),
            self.color_palette,
            ft.Divider(),
            self.region_settings
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
        )
        
    def _build_scene_effect_section(self):
        """Build Scene and Effect controls"""
        
        # Scene controls
        scene_dropdown = ft.Dropdown(
            label="Scene ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        scene_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Scene", on_click=self._add_scene),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Scene", on_click=self._delete_scene),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Scene", on_click=self._copy_scene)
        ])
        
        # Effect controls
        effect_dropdown = ft.Dropdown(
            label="Effect ID",
            value="0", 
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        effect_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Effect", on_click=self._add_effect),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Effect", on_click=self._delete_effect),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Effect", on_click=self._copy_effect)
        ])
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Scene / Effect", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Row([scene_dropdown, scene_buttons], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                ft.Row([effect_dropdown, effect_buttons], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
        
    def _build_scene_settings_section(self):
        """Build Scene Settings controls"""
        
        led_count_field = ft.TextField(
            label="LED Count",
            value="255",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        fps_dropdown = ft.Dropdown(
            label="FPS",
            value="60",
            options=[
                ft.dropdown.Option("30"),
                ft.dropdown.Option("60")
            ],
            width=100
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Scene Settings", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Row([led_count_field, fps_dropdown], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
    
    def _add_scene(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Scene added successfully"))
        )
        
    def _delete_scene(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Scene deleted"))
        )
        
    def _copy_scene(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Scene copied"))
        )
        
    def _add_effect(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Effect added successfully"))
        )
        
    def _delete_effect(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Effect deleted"))
        )
        
    def _copy_effect(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Effect copied"))
        )