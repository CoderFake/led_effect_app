import flet as ft
import platform
from .toast import ToastManager


class MenuBarComponent(ft.Container):
    """Cross-platform file menu bar component"""
    
    def __init__(self, page: ft.Page, file_service=None):
        super().__init__()
        self.page = page
        self.file_service = file_service
        self.toast_manager = ToastManager(page)
        self.current_platform = platform.system()
        self.content = self.build_content()
        
    def build_content(self):
        return self._build_default_menu()
            
    def _build_windows_style_menu(self):
        """Build Windows-style menu bar"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.PopupMenuButton(
                        content=ft.Container(
                            content=ft.Text("File", size=14, weight=ft.FontWeight.W_500),
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        ),
                        items=[
                            ft.PopupMenuItem(
                                text="Open...",
                                icon=ft.Icons.FOLDER_OPEN,
                                on_click=self._open_file
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                text="Save",
                                icon=ft.Icons.SAVE,
                                on_click=self._save_file
                            ),
                            ft.PopupMenuItem(
                                text="Save As...",
                                icon=ft.Icons.SAVE_AS,
                                on_click=self._save_as_file
                            ),
                        ],
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                                ft.ControlState.HOVERED: ft.Colors.GREY_200,
                            },
                            overlay_color=ft.Colors.TRANSPARENT,
                            elevation=0,
                            shape=ft.RoundedRectangleBorder(radius=0),
                        )
                    ),
                    border_radius=0
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(
                        f"{self.current_platform}",
                        size=12,
                        color=ft.Colors.GREY_600
                    ),
                    padding=ft.padding.only(right=20)
                )
            ], spacing=0),
            height=35,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
        
    def _build_default_menu(self):
        """Build default menu bar for all platforms"""
        return ft.Container(
            content=ft.Row([
                ft.MenuBar(
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
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(
                        f"{self.current_platform}",
                        size=12,
                        color=ft.Colors.GREY_600
                    ),
                    padding=ft.padding.only(right=20)
                )
            ], spacing=0),
            height=40,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
        
    def _open_file(self, e):
        """Handle open file action"""
        if self.file_service:
            self.file_service.open_file()
        else:
            self.toast_manager.show_info_sync("Open file dialog will be implemented")
        
    def _save_file(self, e):
        """Handle save file action"""
        if self.file_service:
            self.file_service.save_file()
        else:
            self.toast_manager.show_success_sync("File saved successfully")
        
    def _save_as_file(self, e):
        """Handle save as file action"""
        if self.file_service:
            self.file_service.save_as_file()
        else:
            self.toast_manager.show_info_sync("Save as dialog will be implemented")
            
    def _get_file_status(self) -> str:
        """Get current file status for display"""
        if self.file_service:
            file_name = self.file_service.get_current_file_name()
            if self.file_service.has_unsaved_changes():
                return f"{file_name}*"
            return file_name
        return "No file loaded"