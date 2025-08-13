"""
Toast-based logging system for Light Pattern Designer
Path: src/utils/logger.py
"""

import flet as ft
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
        """Internal method to show toast with appropriate styling"""
        
        # Color mapping for different log levels
        color_map = {
            LogLevel.INFO: ft.colors.BLUE,
            LogLevel.SUCCESS: ft.colors.GREEN,
            LogLevel.WARNING: ft.colors.ORANGE,
            LogLevel.ERROR: ft.colors.RED
        }
        
        # Create action button if provided
        action = None
        if action_label and action_callback:
            action = ft.TextButton(
                text=action_label,
                on_click=action_callback
            )
        
        snack_bar = ft.SnackBar(
            content=ft.Text(
                message,
                color=ft.colors.WHITE
            ),
            bgcolor=color_map.get(level, ft.colors.BLUE),
            action=action,
            action_color=ft.colors.WHITE
        )
        
        self.page.show_snack_bar(snack_bar)


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