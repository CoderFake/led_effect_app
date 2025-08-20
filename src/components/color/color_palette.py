import flet as ft
from services.color_service import color_service
from .tabbed_color_picker import TabbedColorPickerDialog
from ..ui import ToastManager, CommonBtn


class ColorPaletteComponent(ft.Container):
    """Color palette component that auto-fills container width"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        self.current_editing_slot = None
        
        self.content = self.build_content()
        color_service.add_color_change_listener(self._on_palette_changed)
        
        self.page.on_resize = self._on_page_resize
        
    def build_content(self):
        """Build color palette interface with auto-fill layout"""
        
        self.palette_dropdown = ft.Dropdown(
            hint_text="Palette ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=120,
            expand=True
        )
        
        palette_buttons = CommonBtn().get_buttons(
            ("Add Palette", self._add_palette),
            ("Delete Palette", self._delete_palette),
            ("Copy Palette", self._copy_palette)
        )
        
        self.color_container = ft.Container(
            content=self._build_auto_fill_color_row(),
            expand=True,
            padding=ft.padding.symmetric(vertical=5)
        )
        
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Color Palettes", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Text("Palette ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                        self.palette_dropdown,
                        palette_buttons
                    ], spacing=5),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text("Color:", size=12, weight=ft.FontWeight.W_500, width=80),
                        self.color_container
                    ], spacing=5)
                ], spacing=0
            ),
            expand=True,
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.all(15),
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10
        )

    def _build_auto_fill_color_row(self):
        """Build color row that fills available width"""
        colors = color_service.get_palette_colors()
        color_names = ["Black", "Red", "Yellow", "Blue", "Green", "White"]

        self.color_boxes = []
        for index in range(len(colors)):
            color_box = self._create_auto_fill_color_box(
                index=index,
                color=colors[index],
                name=color_names[index] if index < len(color_names) else f"Color {index}",
            )
            self.color_boxes.append(color_box)
        
        return ft.Row(
            self.color_boxes,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=5,
            expand=True
        )
        
    def _create_auto_fill_color_box(self, index: int, color: str, name: str):
        """Create color box that expands to fill available space"""
        return ft.Container(
            bgcolor=color,
            height=30,
            border_radius=4,
            border=ft.border.all(1, ft.Colors.GREY_400),
            ink=True,
            on_click=lambda e, idx=index: self._edit_color(idx),
            tooltip=f"Click to edit color {index + 1}",
            expand=True, 
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
        
    def _on_page_resize(self, e):
        """Handle page resize to maintain fill behavior"""
        try:
            if hasattr(self, 'color_container'):
                self.color_container.update()
        except Exception as e:
            print(f"Error handling page resize: {e}")
            
    def _edit_color(self, color_index: int):
        """Open color picker for editing using official Flet page.open() method"""
        self.current_editing_slot = color_index
        current_color = color_service.get_palette_color(color_index)
        
        def on_color_confirm(selected_color: str):
            color_service.update_palette_color(color_index, selected_color)
            self.toast_manager.show_success_sync(f"Color {color_index + 1} updated")
            
        color_picker = TabbedColorPickerDialog(
            initial_color=current_color,
            on_confirm=on_color_confirm
        )
        self.page.open(color_picker)
        
    def _add_palette(self, e):
        """Handle add palette action"""
        self.toast_manager.show_success_sync("Palette added successfully")
        
    def _delete_palette(self, e):
        """Handle delete palette action"""
        self.toast_manager.show_warning_sync("Palette deleted")
        
    def _copy_palette(self, e):
        """Handle copy palette action"""
        self.toast_manager.show_success_sync("Palette copied")
        
    def _on_palette_changed(self):
        """Handle palette change from color service"""
        try:
            colors = color_service.get_palette_colors()
            
            if hasattr(self, 'color_boxes') and len(self.color_boxes) == len(colors):
                for color_box, color in zip(self.color_boxes, colors):
                    color_box.bgcolor = color
                self.update()
            else:
                self.color_container.content = self._build_auto_fill_color_row()
                self.update()
                
        except Exception as e:
            print(f"Error updating palette display: {e}")
            
    def update_palette_list(self, palette_ids):
        """Update palette dropdown options"""
        self.palette_dropdown.options = [
            ft.dropdown.Option(str(palette_id)) for palette_id in palette_ids
        ]
        self.update()
        
    def get_selected_palette(self):
        """Get currently selected palette ID"""
        return self.palette_dropdown.value
        
    def set_selected_palette(self, palette_id: str):
        """Set selected palette programmatically"""
        self.palette_dropdown.value = palette_id
        self.update()
        
    def set_color_box_height(self, height: int):
        """Set custom height for color boxes"""
        if hasattr(self, 'color_boxes'):
            for color_box in self.color_boxes:
                color_box.height = height
            self.update()