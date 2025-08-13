"""
Menu bar component for file operations
Path: src/components/menu_bar.py
"""

import flet as ft
from flet import icons


class MenuBarComponent(ft.Container):
    """File menu bar component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build_content()
        
    def build_content(self):
        """Build menu bar"""
        
    def build_content(self):
        """Build menu bar"""
        
        return ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("File"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("Open..."),
                            leading=ft.Icon(icons.FOLDER_OPEN),
                            on_click=self._open_file
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Save"),
                            leading=ft.Icon(icons.SAVE),
                            on_click=self._save_file
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Save as..."),
                            leading=ft.Icon(icons.SAVE_AS),
                            on_click=self._save_as_file
                        ),
                    ]
                )
            ]
        )
        
    def _open_file(self, e):
        """Handle open file action"""
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Open file dialog will be implemented"))
        )
        
    def _save_file(self, e):
        """Handle save file action"""
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("File saved successfully"))
        )
        
    def _save_as_file(self, e):
        """Handle save as file action"""
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Save as dialog will be implemented"))
        )