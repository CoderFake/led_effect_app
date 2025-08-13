"""
Toast-based logging system for Light Pattern Designer
Path: src/utils/logger.py
"""

import flet as ft
import asyncio
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """Log levels for different types of messages"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ToastLogger:
    """Toast-based logger for user notifications"""
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def info(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show info message"""
        self._show_toast(message, LogLevel.INFO, action_label, action_callback)
    
    def success(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show success message"""
        self._show_toast(message, LogLevel.SUCCESS, action_label, action_callback)
    
    def warning(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show warning message"""
        self._show_toast(message, LogLevel.WARNING, action_label, action_callback)
    
    def error(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show error message"""
        self._show_toast(message, LogLevel.ERROR, action_label, action_callback)
    
    def _show_toast(self, message: str, level: LogLevel, action_label: Optional[str] = None, action_callback=None):
        """Show a bottom-right toast with fade in/out, similar to web bootstrap."""

        color_map = {
            LogLevel.INFO: ft.Colors.BLUE,
            LogLevel.SUCCESS: ft.Colors.GREEN,
            LogLevel.WARNING: ft.Colors.ORANGE,
            LogLevel.ERROR: ft.Colors.RED,
        }

        action_ctrl = None
        if action_label and action_callback:
            action_ctrl = ft.TextButton(text=action_label, on_click=action_callback)

        toast = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(message, color=ft.Colors.WHITE, size=13),
                    action_ctrl if action_ctrl else ft.Container(width=0, height=0),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=color_map.get(level, ft.Colors.BLUE),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.Colors.with_opacity(ft.Colors.BLACK, 0.2)),
            opacity=0,
            animate_opacity=300,
            right=16,
            bottom=16,
        )

        self.page.overlay.append(toast)
        self.page.update()

        # Fade in
        toast.opacity = 1
        self.page.update()

        async def auto_dismiss():
            await asyncio.sleep(2.5)
            toast.opacity = 0
            self.page.update()
            await asyncio.sleep(0.3)
            if toast in self.page.overlay:
                self.page.overlay.remove(toast)
                self.page.update()

        if hasattr(self.page, "run_task"):
            self.page.run_task(auto_dismiss)
        else:
            asyncio.get_event_loop().create_task(auto_dismiss())


class AppLogger:
    """Global logger instance"""
    _instance = None
    _logger = None
    
    @classmethod
    def initialize(cls, page: ft.Page):
        """Initialize the global logger"""
        cls._logger = ToastLogger(page)
    
    @classmethod
    def get_logger(cls) -> ToastLogger:
        """Get the global logger instance"""
        if cls._logger is None:
            raise RuntimeError("Logger not initialized. Call AppLogger.initialize() first.")
        return cls._logger
    
    @classmethod
    def info(cls, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show info message using global logger"""
        cls.get_logger().info(message, action_label, action_callback)
    
    @classmethod
    def success(cls, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show success message using global logger"""
        cls.get_logger().success(message, action_label, action_callback)
    
    @classmethod
    def warning(cls, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show warning message using global logger"""
        cls.get_logger().warning(message, action_label, action_callback)
    
    @classmethod
    def error(cls, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show error message using global logger"""
        cls.get_logger().error(message, action_label, action_callback)