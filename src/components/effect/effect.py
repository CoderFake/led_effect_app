import flet as ft
from .effect_action import EffectActionHandler
from ..ui import CommonBtn


class EffectComponent(ft.Container):
    """Effect UI component with dropdown and control buttons"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = EffectActionHandler(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build Effect controls"""
        
        self.effect_dropdown = ft.Dropdown(
            hint_text="Effect ID",
            value="0", 
            border_color=ft.Colors.GREY_400,
            options=[ft.dropdown.Option("0")],
            expand=True
        )

        effect_buttons = CommonBtn().get_buttons(
            ("Add Effect", self.action_handler.add_effect),
            ("Delete Effect", self.action_handler.delete_effect),
            ("Copy Effect", self.action_handler.copy_effect)
        )

        return ft.Row([
            ft.Text("Effect ID:", size=12, weight=ft.FontWeight.W_500, width=80),
            self.effect_dropdown,
            effect_buttons
        ], spacing=5)
        
    def update_effects(self, effects_list):
        """Update effect dropdown options"""
        self.effect_dropdown.options = [
            ft.dropdown.Option(str(effect_id)) for effect_id in effects_list
        ]
        
    def get_selected_effect(self):
        """Get currently selected effect ID"""
        return self.effect_dropdown.value