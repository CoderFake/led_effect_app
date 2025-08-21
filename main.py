import flet as ft
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app.light_pattern_app import LightPatternApp
from src.utils.logger import AppLogger
from src.components.ui.introduction_screen import IntroductionManager


def main(page: ft.Page):
    page.title = "Light Pattern Designer"
    page.window.maximized = True
    page.window.resizable = True
    
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    AppLogger.initialize()
    
    intro_manager = IntroductionManager(page)
    
    def create_main_app():
        app = LightPatternApp(page, use_menu_bar=True)
        return app
    
    page.run_task(intro_manager.show_introduction, create_main_app)


if __name__ == "__main__":
    ft.app(target=main)