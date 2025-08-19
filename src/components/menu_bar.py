import flet as ft
from components.toast import ToastManager


class MenuBarComponent(ft.Container):
    """File menu bar component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build menu bar"""
        
        return ft.Container(
            content=ft.MenuBar(
                controls=[
                    ft.SubmenuButton(
                        content=ft.Container(
                            content=ft.Text("File", size=14),
                            padding=ft.padding.symmetric(horizontal=12, vertical=8)
                        ),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Open...", size=14),
                                leading=ft.Icon(ft.Icons.FOLDER_OPEN, size=18),
                                on_click=self._open_file
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Save", size=14),
                                leading=ft.Icon(ft.Icons.SAVE, size=18),
                                on_click=self._save_file
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Save as...", size=14),
                                leading=ft.Icon(ft.Icons.SAVE_AS, size=18),
                                on_click=self._save_as_file
                            ),
                        ]
                    )
                ]
            ),
            height=40
        )
        
    def _open_file(self, e):
        """Handle open file action"""
        self.toast_manager.show_info_sync("Open file dialog will be implemented")
        
    def _save_file(self, e):
        """Handle save file action"""
        self.toast_manager.show_success_sync("File saved successfully")
        
    def _save_as_file(self, e):
        """Handle save as file action"""
        self.toast_manager.show_info_sync("Save as dialog will be implemented")