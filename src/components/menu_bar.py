"""
Menu bar component for file operations
Path: src/components/menu_bar.py
"""

import flet as ft


class MenuBarComponent(ft.Container):
    """File menu bar component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build_content()
        
    def build_content(self):
        """Build menu bar"""
        
        return ft.MenuBar(
            style=ft.MenuStyle(bgcolor=ft.Colors.TRANSPARENT),
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("File"),
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        bgcolor={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.4, ft.Colors.GREY_200)},
                    ),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("Open..."),
                            leading=ft.Icon(ft.Icons.FOLDER_OPEN),
                            on_click=self._open_file
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Save"),
                            leading=ft.Icon(ft.Icons.SAVE),
                            on_click=self._save_file
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Save as..."),
                            leading=ft.Icon(ft.Icons.SAVE_AS),
                            on_click=self._save_as_file
                        ),
                    ]
                )
            ]
        )
        
    def _open_file(self, e):
        """Handle open file action"""
        self.page.open(
            ft.SnackBar(content=ft.Text("Open file dialog will be implemented"))
        )
        
    def _save_file(self, e):
        """Handle save file action"""
        self.page.open(
            ft.SnackBar(content=ft.Text("File saved successfully"))
        )
        
    def _save_as_file(self, e):
        """Handle save as file action"""
        self.page.open(
            ft.SnackBar(content=ft.Text("Save as dialog will be implemented"))
        )