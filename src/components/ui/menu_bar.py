import flet as ft
from .toast import ToastManager


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
                expand=True,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Container(
                            content=ft.Text("File", size=14),
                            padding=ft.padding.symmetric(horizontal=20, vertical=8),
                            margin=ft.margin.all(0),
                            border=None
                        ),
                        leading=ft.Icon(ft.Icons.FOLDER, size=18),
                        style=ft.ButtonStyle(
                            elevation={
                                ft.ControlState.DEFAULT: 0,
                                ft.ControlState.HOVERED: 0,
                                ft.ControlState.FOCUSED: 0,
                                ft.ControlState.PRESSED: 0
                            },
                            shadow_color=ft.Colors.TRANSPARENT,
                            surface_tint_color=ft.Colors.TRANSPARENT,
                            bgcolor={
                                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                                ft.ControlState.HOVERED: ft.Colors.WHITE,
                                ft.ControlState.FOCUSED: ft.Colors.TRANSPARENT
                            },
                            color={
                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                ft.ControlState.HOVERED: ft.Colors.BLACK,
                                ft.ControlState.FOCUSED: ft.Colors.BLACK
                            },
                            side={
                                ft.ControlState.DEFAULT: ft.BorderSide(0, ft.Colors.TRANSPARENT),
                                ft.ControlState.HOVERED: ft.BorderSide(0, ft.Colors.TRANSPARENT),
                                ft.ControlState.FOCUSED: ft.BorderSide(0, ft.Colors.TRANSPARENT)
                            },
                            overlay_color=ft.Colors.TRANSPARENT,
                            shape=ft.RoundedRectangleBorder(radius=0),
                            padding=ft.padding.all(0)
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