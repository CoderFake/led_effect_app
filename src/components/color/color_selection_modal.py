import flet as ft
from typing import Callable, Optional
from services.color_service import color_service


class ColorSelectionModal(ft.AlertDialog):
    """Modal to select color from current palette for segment edit"""

    def __init__(self, palette_id: int = 0, on_color_select: Optional[Callable] = None):
        super().__init__()
        self.palette_id = palette_id
        self.on_color_select = on_color_select
        self.selected_index: Optional[int] = None

        self.modal = True
        self.title = ft.Text(f"Select Color - Palette ID: {palette_id}")
        self.content = self._build_color_grid()
        self.actions = [ft.TextButton("Cancel", on_click=self._on_cancel)]
        self.actions_alignment = ft.MainAxisAlignment.END

        self.elevation = 24
        self.surface_tint_color = None
        self.width = 350
        self.height = 400

    def _build_color_grid(self) -> ft.Container:
        """Build grid of color boxes from current palette"""
        colors = color_service.get_palette_colors()
        color_names = ["Black", "Red", "Yellow", "Blue", "Green", "White"]

        rows = []
        for row in range(2):
            cols = []
            for col in range(3):
                index = row * 3 + col
                if index < len(colors):
                    cols.append(
                        self._create_color_box(
                            index=index,
                            color=colors[index],
                            name=color_names[index] if index < len(color_names) else f"Color {index}",
                        )
                    )
            if cols:
                rows.append(ft.Row(cols, alignment=ft.MainAxisAlignment.SPACE_EVENLY))

        return ft.Container(
            content=ft.Column(rows, spacing=10),
            width=300,
            height=200,
            padding=ft.padding.all(20),
        )

    def _create_color_box(self, index: int, color: str, name: str) -> ft.Container:
        """Create a clickable color box"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        width=60,
                        height=40,
                        bgcolor=color,
                        border_radius=4,
                        border=ft.border.all(2, ft.Colors.GREY_400),
                    ),
                    ft.Text(f"{index}", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(name, size=10, color=ft.Colors.GREY_600),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                tight=True,
            ),
            padding=ft.padding.all(8),
            border_radius=8,
            ink=True,
            on_click=lambda e, idx=index: self._on_color_click(idx),
            tooltip=f"Color Index {index}: {name}",
        )

    def _on_color_click(self, color_index: int):
        """Handle color box click"""
        self.selected_index = color_index

        if self.on_color_select:
            selected_color = color_service.get_palette_color(color_index)
            self.on_color_select(color_index, selected_color)

        self._close_modal()

    def _on_cancel(self, e):
        """Handle cancel button"""
        self._close_modal()

    def _close_modal(self):
        """Close modal using official Flet page.close() method"""
        try:
            if hasattr(self, "page") and self.page:
                self.page.close(self)
        except Exception as e:
            print(f"Error closing color modal: {e}")

    def get_selected_index(self) -> Optional[int]:
        """Get selected color index"""
        return self.selected_index


class ColorSelectionButton(ft.Container):
    """Button component for color selection in segment edit"""

    def __init__(
        self,
        slot_index: int,
        initial_color_index: int = 0,
        on_color_change: Optional[Callable] = None,
    ):
        super().__init__()
        self.slot_index = slot_index
        self.current_color_index = initial_color_index
        self.on_color_change = on_color_change

        self.width = 50
        self.height = 50
        self.border_radius = 8
        self.border = ft.border.all(2, ft.Colors.GREY_400)
        self.ink = True
        self.on_click = self._show_color_selection
        self.tooltip = f"Color Slot {slot_index + 1} - Click to change"

        self._update_appearance()

    def _update_appearance(self):
        """Update button appearance based on current color"""
        current_color = color_service.get_palette_color(self.current_color_index)

        self.bgcolor = current_color
        self.content = ft.Column(
            [
                ft.Text(
                    str(self.current_color_index),
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE if self._is_dark_color(current_color) else ft.Colors.BLACK,
                ),
                ft.Text(
                    f"Slot {self.slot_index + 1}",
                    size=8,
                    color=ft.Colors.WHITE70 if self._is_dark_color(current_color) else ft.Colors.BLACK54,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            main_alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            tight=True,
        )

    def _is_dark_color(self, hex_color: str) -> bool:
        """Check if color is dark (for text color contrast)"""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except Exception:
            return True

    def _show_color_selection(self, e):
        """Show color selection modal using official Flet page.open() method"""
        def on_select(color_index: int, color: str):
            self.set_color_index(color_index)
            if self.on_color_change:
                self.on_color_change(self.slot_index, color_index, color)

        modal = ColorSelectionModal(palette_id=0, on_color_select=on_select)
        self.page.open(modal)

    def set_color_index(self, color_index: int):
        """Set color index programmatically"""
        self.current_color_index = color_index
        self._update_appearance()
        self.update()

    def get_color_index(self) -> int:
        """Get current color index"""
        return self.current_color_index