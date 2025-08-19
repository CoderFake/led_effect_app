import flet as ft
from enum import Enum
from typing import Optional
from src.components.ui.toast import ToastManager


class LogLevel(Enum):
    """Log levels for different types of messages"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class ToastLogger:
    """Toast-based logger using custom ToastManager"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
    
    def info(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show info message"""
        self.toast_manager.show_info_sync(message)
    
    def success(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show success message"""
        self.toast_manager.show_success_sync(message)
    
    def warning(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show warning message"""
        self.toast_manager.show_warning_sync(message)
    
    def error(self, message: str, action_label: Optional[str] = None, action_callback=None):
        """Show error message"""
        self.toast_manager.show_error_sync(message)


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