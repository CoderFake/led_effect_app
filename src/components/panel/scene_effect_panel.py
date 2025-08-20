import flet as ft
from ..scene import SceneComponent
from ..effect import EffectComponent
from ..color import ColorPaletteComponent
from ..region import RegionComponent


class SceneEffectPanel(ft.Container):
    """Left panel containing Scene/Effect controls"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build the scene/effect panel"""
        
        scene_effect_section = self._build_scene_effect_section()
        scene_settings_section = self._build_scene_settings_section()

        self.color_palette = ColorPaletteComponent(self.page)
        self.region_settings = RegionComponent(self.page)
        
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
                padding=ft.padding.all(20),
                margin=ft.margin.all(5),
                border_radius=10,
                bgcolor=ft.Colors.GREY_50,
                border=ft.border.all(1, ft.Colors.GREY_400)
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True
        )
        
    def _build_scene_effect_section(self):
        """Build Scene and Effect controls using refactored components"""
        
        self.scene_component = SceneComponent(self.page)
        self.effect_component = EffectComponent(self.page)
        
        return ft.Container(
            ft.Column([
                ft.Text("Scene / Effect", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                self.scene_component,
                self.effect_component
            ], spacing=8),
            margin=ft.margin.only(left=10, right=5)
        )

    def _build_scene_settings_section(self):
        """Build Scene Settings controls"""
        
        self.led_count_field = ft.TextField(
            hint_text="LED Count",
            value="255",
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_led_count_change
        )
        
        self.fps_dropdown = ft.Dropdown(
            hint_text="FPS",
            value="60",
            options=[
                ft.dropdown.Option("20"),
                ft.dropdown.Option("40"),
                ft.dropdown.Option("60"),
                ft.dropdown.Option("80"),
                ft.dropdown.Option("100"),
                ft.dropdown.Option("120")
            ],
            expand=True,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_fps_change
        )
        
        return ft.Column([
            ft.Text("Scene Settings", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
            ft.Container(height=25),
            ft.Row([
                ft.Text("LED Count:", size=12, weight=ft.FontWeight.W_500, width=80),
                self.led_count_field,
                ft.Text("FPS:", size=12, weight=ft.FontWeight.W_500, width=50),
                self.fps_dropdown
            ], spacing=10)
        ], spacing=0)
        
    def _on_led_count_change(self, e):
        """Handle LED count change"""
        try:
            led_count = int(e.control.value)
            if led_count > 0:
                current_scene = self.scene_component.get_selected_scene()
                self.scene_component.action_handler.create_scene_with_params(led_count, int(self.fps_dropdown.value))
        except ValueError:
            pass
            
    def _on_fps_change(self, e):
        """Handle FPS change"""
        fps = int(e.control.value)
        current_scene = self.scene_component.get_selected_scene()
        led_count = int(self.led_count_field.value) if self.led_count_field.value else 255
        self.scene_component.action_handler.create_scene_with_params(led_count, fps)
        
    def update_scenes_list(self, scenes_list):
        """Update scenes dropdown"""
        self.scene_component.update_scenes(scenes_list)
        
    def update_effects_list(self, effects_list):
        """Update effects dropdown"""
        self.effect_component.update_effects(effects_list)
        
    def update_regions_list(self, regions_list):
        """Update regions dropdown"""
        self.region_settings.update_regions(regions_list)
        
    def get_current_selection(self):
        """Get current scene/effect selection"""
        return {
            'scene_id': self.scene_component.get_selected_scene(),
            'effect_id': self.effect_component.get_selected_effect(),
            'region_id': self.region_settings.get_selected_region(),
            'palette_id': self.color_palette.get_selected_palette(),
            'led_count': self.led_count_field.value,
            'fps': self.fps_dropdown.value
        }