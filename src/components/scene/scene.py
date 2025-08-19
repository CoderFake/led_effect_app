import flet as ft
from .scene_action import SceneActionHandler


class SceneComponent(ft.Container):
    """Scene UI component with dropdown and control buttons"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = SceneActionHandler(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build Scene controls"""
        
        self.scene_dropdown = ft.Dropdown(
            label="Scene ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        scene_buttons = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ADD, 
                tooltip="Add Scene", 
                on_click=self.action_handler.add_scene
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE, 
                tooltip="Delete Scene", 
                on_click=self.action_handler.delete_scene
            ),
            ft.IconButton(
                icon=ft.Icons.COPY, 
                tooltip="Copy Scene", 
                on_click=self.action_handler.copy_scene
            )
        ], tight=True)
        
        return ft.Row([
            ft.Text("Scene ID:", size=12, weight=ft.FontWeight.W_500, width=80),
            self.scene_dropdown,
            scene_buttons
        ], spacing=5)
        
    def update_scenes(self, scenes_list):
        """Update scene dropdown options"""
        self.scene_dropdown.options = [
            ft.dropdown.Option(str(scene_id)) for scene_id in scenes_list
        ]
        self.update()
        
    def get_selected_scene(self):
        """Get currently selected scene ID"""
        return self.scene_dropdown.value