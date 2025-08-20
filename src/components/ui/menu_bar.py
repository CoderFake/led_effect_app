import flet as ft
from .menu_bar_action import MenuBarActionHandler


class MenuBarComponent(ft.Container):
    """Cross-platform file menu bar component"""
    
    def __init__(self, page: ft.Page, file_service=None):
        super().__init__()
        self.page = page
        self.action_handler = MenuBarActionHandler(page, file_service)
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
                        items=self._build_popup_menu_items(),
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
                        f"{self.action_handler.get_platform_info()}",
                        size=12,
                        color=ft.Colors.GREY_600
                    ),
                    padding=ft.padding.only(right=20)
                )
            ], spacing=0),
            height=35,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_400))
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
                            controls=self._build_file_menu_items()
                        )
                    ]
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(
                        f"{self.action_handler.get_platform_info()}",
                        size=12,
                        color=ft.Colors.GREY_600
                    ),
                    padding=ft.padding.only(right=20)
                )
            ], spacing=0),
            height=40,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_400))
        )
        
    def _build_file_menu_items(self):
        """Build file menu items with actions"""
        return [
            ft.MenuItemButton(
                content=ft.Text("Open...", size=14),
                leading=ft.Icon(ft.Icons.FOLDER_OPEN, size=18),
                on_click=self.action_handler.handle_open_file
            ),
            ft.MenuItemButton(
                content=ft.Text("Save", size=14),
                leading=ft.Icon(ft.Icons.SAVE, size=18),
                on_click=self.action_handler.handle_save_file
            ),
            ft.MenuItemButton(
                content=ft.Text("Save as...", size=14),
                leading=ft.Icon(ft.Icons.SAVE_AS, size=18),
                on_click=self.action_handler.handle_save_as_file
            ),
        ]
        
    def _build_popup_menu_items(self):
        """Build popup menu items for Windows-style menu"""
        return [
            ft.PopupMenuItem(
                text="Open...",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=self.action_handler.handle_open_file
            ),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(
                text="Save",
                icon=ft.Icons.SAVE,
                on_click=self.action_handler.handle_save_file
            ),
            ft.PopupMenuItem(
                text="Save As...",
                icon=ft.Icons.SAVE_AS,
                on_click=self.action_handler.handle_save_as_file
            ),
        ]
        
    def get_file_status(self) -> str:
        """Get current file status for display - delegate to action handler"""
        status_data = self.action_handler.get_file_status_data()
        return status_data['display_name']