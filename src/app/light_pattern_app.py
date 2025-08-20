import flet as ft
from typing import Optional
from components.panel import SceneEffectPanel, SegmentEditPanel
from services.color_service import color_service
from models.color_palette import ColorPalette


class LightPatternApp(ft.Container):
    """Main application container"""
    
    def __init__(self, page: ft.Page, use_menu_bar: bool = True, file_service=None):
        super().__init__()
        self.page = page
        self.use_menu_bar = use_menu_bar
        self.file_service = file_service
        self.expand = True
        
        self.opacity = 1.0
        self.animate_opacity = ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        
        default_palette = ColorPalette.create_default(0)
        color_service.set_current_palette(default_palette)
        
        self.content = self.build_content()
        
    def build_content(self):
        """Build the main application layout"""
        
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
        
        if self.use_menu_bar:
            from components.ui import MenuBarComponent
            menu_bar = MenuBarComponent(self.page, self.file_service)
            
            return ft.Column([
                ft.Container(
                    content=menu_bar,
                    height=50,
                    bgcolor=ft.Colors.GREY_50
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_400),
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
        else:
            return ft.Container(
                content=main_content,
                expand=True,
                padding=10,
                bgcolor=ft.Colors.WHITE
            )