import flet as ft
from components.ui import MenuBarComponent
from components.panel import SceneEffectPanel, SegmentEditPanel
from services.color_service import color_service
from models.color_palette import ColorPalette


class LightPatternApp(ft.Container):
    """Main application container"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        default_palette = ColorPalette.create_default(0)
        color_service.set_current_palette(default_palette)
        
        self.content = self.build_content()
        
    def build_content(self):
        """Build the main application layout"""
        
        self.menu_bar = MenuBarComponent(self.page)
        self.scene_effect_panel = SceneEffectPanel(self.page)
        self.segment_edit_panel = SegmentEditPanel(self.page)
        
        main_content = ft.Row([
            ft.Container(
                content=self.scene_effect_panel,
                width=None,
                expand=True,
                padding=ft.padding.all(5)
            ),
            ft.Container(
                content=self.segment_edit_panel,
                width=None,
                expand=True,
                padding=ft.padding.all(5)
            )
        ],
        expand=True,
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.START)
        
        return ft.Column([
            ft.Container(
                content=self.menu_bar,
                height=50,
                bgcolor=ft.Colors.GREY_50
            ),

            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Container(
                content=main_content,
                expand=True,
                padding=0,
                bgcolor=ft.Colors.WHITE
            )
        ],
        spacing=0,
        expand=True
        )