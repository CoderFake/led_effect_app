import flet as ft
from components.color_palette import ColorPaletteComponent
from components.region_settings import RegionSettingsComponent
from components.toast import ToastManager


class SceneEffectPanel(ft.Container):
    """Left panel containing Scene/Effect controls"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build the scene/effect panel"""
        
        scene_effect_section = self._build_scene_effect_section()
        scene_settings_section = self._build_scene_settings_section()

        self.color_palette = ColorPaletteComponent(self.page)
        self.region_settings = RegionSettingsComponent(self.page)
        
        return ft.Column([
            scene_effect_section,
            ft.Container(height=5),  
            ft.Container(
                content=ft.Column([
                    scene_settings_section,
                    ft.Container(height=15),
                    self.color_palette,
                    ft.Container(height=15),
                    self.region_settings
                ], spacing=0),
                padding=ft.padding.all(15),
                margin=ft.margin.all(5),
                border_radius=10,
                bgcolor=ft.Colors.GREY_50,
                border=ft.border.all(1, ft.Colors.GREY_300)
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True
        )
        
    def _build_scene_effect_section(self):
        """Build Scene and Effect controls"""
    
        scene_dropdown = ft.Dropdown(
            label="Scene ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        scene_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Scene", on_click=self._add_scene),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Scene", on_click=self._delete_scene),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Scene", on_click=self._copy_scene)
        ], tight=True)
        
        effect_dropdown = ft.Dropdown(
            label="Effect ID",
            value="0", 
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        effect_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Effect", on_click=self._add_effect),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Effect", on_click=self._delete_effect),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Effect", on_click=self._copy_effect)
        ], tight=True)
        
        return ft.Column([
            ft.Text("Scene / Effect", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Text("Scene ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                scene_dropdown,
                scene_buttons
            ], spacing=5),
            ft.Row([
                ft.Text("Effect ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                effect_dropdown,
                effect_buttons
            ], spacing=5)
        ], spacing=8)
        
    def _build_scene_settings_section(self):
        """Build Scene Settings controls"""
        
        led_count_field = ft.TextField(
            label="LED Count",
            value="255",
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        fps_dropdown = ft.Dropdown(
            label="FPS",
            value="60",
            options=[
                ft.dropdown.Option("30"),
                ft.dropdown.Option("60")
            ],
            expand=True
        )
        
        return ft.Column([
            ft.Text("Scene Settings", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
            ft.Container(height=8),
            ft.Row([
                ft.Text("LED Count:", size=12, weight=ft.FontWeight.W_500, width=80),
                led_count_field,
                ft.Text("FPS:", size=12, weight=ft.FontWeight.W_500, width=50),
                fps_dropdown
            ], spacing=10)
        ], spacing=0)
    
    def _add_scene(self, e):
        self.toast_manager.show_success_sync("Scene added successfully")
        
    def _delete_scene(self, e):
        self.toast_manager.show_warning_sync("Scene deleted")
        
    def _copy_scene(self, e):
        self.toast_manager.show_success_sync("Scene copied")
        
    def _add_effect(self, e):
        self.toast_manager.show_success_sync("Effect added successfully")
        
    def _delete_effect(self, e):
        self.toast_manager.show_warning_sync("Effect deleted")
        
    def _copy_effect(self, e):
        self.toast_manager.show_success_sync("Effect copied")