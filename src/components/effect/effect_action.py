import flet as ft
from ..ui.toast import ToastManager


class EffectActionHandler:
    """Handle effect-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_effect(self, e):
        """Handle add effect action"""
        self.toast_manager.show_success_sync("Effect added successfully")
        
    def delete_effect(self, e):
        """Handle delete effect action"""
        self.toast_manager.show_warning_sync("Effect deleted")
        
    def copy_effect(self, e):
        """Handle copy effect action"""
        self.toast_manager.show_success_sync("Effect copied")
        
    def change_effect(self, effect_id: str):
        """Handle effect change"""
        self.toast_manager.show_info_sync(f"Changed to effect {effect_id}")
        
    def create_effect(self):
        """Create new effect"""
        self.toast_manager.show_success_sync("New effect created")
        
    def duplicate_effect(self, source_id: str):
        """Duplicate existing effect"""
        self.toast_manager.show_success_sync(f"Effect {source_id} duplicated")