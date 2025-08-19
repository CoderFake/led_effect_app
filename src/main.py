import flet as ft
import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from app.light_pattern_app import LightPatternApp
from utils.logger import AppLogger


def main(page: ft.Page):
    page.title = "Light Pattern Designer"
    page.window.full_screen = True
    
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_50 
    
    AppLogger.initialize(page)

    app = LightPatternApp(page)
    page.add(app)
    page.update()
    
    AppLogger.info("Light Pattern Designer started successfully")


if __name__ == "__main__":
    ft.app(target=main)