import flet as ft
import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from app.light_pattern_app import LightPatternApp
from utils.logger import AppLogger


def main(page: ft.Page):
    """Main function to initialize the Flet application"""
    
    page.title = "Light Pattern Designer"
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 1000
    page.window_min_height = 700
    page.padding = 0
    page.spacing = 0
    
    AppLogger.initialize(page)
    
    try:
        app = LightPatternApp(page)
        page.add(app)
        page.update()
        print("App added to page successfully")
    except Exception as e:
        print(f"Error creating app: {e}")
        error_text = ft.Text(f"App creation error: {e}", color=ft.Colors.RED, size=16)
        page.add(ft.Container(content=error_text, padding=20))
        page.update()
        return


if __name__ == "__main__":
    ft.app(target=main)