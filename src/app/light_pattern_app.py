"""src/app/light_pattern_app.py"""

import flet as ft
import os
from typing import Optional
from components.panel import SceneEffectPanel, SegmentEditPanel
from components.data import DataActionHandler
from components.ui.menu_bar import MenuBarComponent
from services.color_service import color_service
from services.file_service import FileService
from services.data_cache import data_cache
from models.color_palette import ColorPalette


class LightPatternApp(ft.Container):
    """Main application container with data action handler integration"""
    
    def __init__(self, page: ft.Page, use_menu_bar: bool = True):
        super().__init__()
        self.page = page
        self.use_menu_bar = use_menu_bar
        
        self.data_action_handler = DataActionHandler(page)
        self.file_service = FileService(data_cache)
        
        self._setup_file_service_callbacks()
        
        self.expand = True
        
        self.opacity = 1.0
        self.animate_opacity = ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
        
        default_palette = ColorPalette.create_default(0)
        color_service.set_current_palette(default_palette)
        
        self.content = self.build_content()
        
        self._register_ui_panels()
        
    def _setup_file_service_callbacks(self):
        """Setup callbacks between file service and data action handler"""
        def on_file_loaded(file_path: str, success: bool, error_message: str = None):
            if success:
                self.data_action_handler.update_all_ui_from_cache()
                self.data_action_handler.toast_manager.show_success_sync(f"File loaded successfully: {os.path.basename(file_path)}")
            else:
                self.data_action_handler.toast_manager.show_error_sync(error_message or "Failed to load file")
        
        def on_file_saved(file_path: str, success: bool, error_message: str = None):
            if success:
                self.data_action_handler.toast_manager.show_success_sync(f"File saved successfully: {os.path.basename(file_path)}")
            else:
                self.data_action_handler.toast_manager.show_error_sync(error_message or "Failed to save file")
        
        def on_error(error_message: str):
            self.data_action_handler.toast_manager.show_error_sync(error_message)
        
        self.file_service.on_file_loaded = on_file_loaded
        self.file_service.on_file_saved = on_file_saved
        self.file_service.on_error = on_error
        
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
            menu_bar = MenuBarComponent(self.page, self.file_service, self.data_action_handler)
            
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
            
    def _register_ui_panels(self):
        """Register UI panels with data action handler"""
        self.data_action_handler.register_panels(
            self.scene_effect_panel,
            self.segment_edit_panel
        )
        
    def get_cache_status(self) -> dict:
        """Get current cache status"""
        return self.data_action_handler.get_cache_status()
        
    def refresh_ui(self):
        """Force refresh all UI components"""
        self.data_action_handler.refresh_ui()
        
    def clear_data(self):
        """Clear all loaded data via action handler"""
        self.data_action_handler.clear_data()
        self.file_service.clear_current_file()