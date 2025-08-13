"""
Entry point for Light Pattern Designer application
Path: src/main.py
"""

import flet as ft
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from app.light_pattern_app import LightPatternApp
from utils.logger import AppLogger


def main(page: ft.Page):
    """Main function to initialize the Flet application"""
    
    # Configure page properties
    page.title = "Light Pattern Designer"
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 1000
    page.window_min_height = 700
    page.padding = 0
    page.spacing = 0
    
    # Initialize global logger
    AppLogger.initialize(page)
    
    # Create and add the main application
    app = LightPatternApp(page)
    page.add(app)
    
    # Update page to show the application
    page.update()
    
    # Show welcome message
    AppLogger.info("Light Pattern Designer started successfully")


if __name__ == "__main__":
    ft.app(target=main)