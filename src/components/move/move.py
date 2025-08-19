import flet as ft
from .move_action import MoveActionHandler


class MoveComponent(ft.Container):
    """Move configuration component layout"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = MoveActionHandler(page)
        self.expand = True
        self.content = self.build_content()

    def build_content(self):
        range_row = self._build_move_range_row()
        speed_row = self._build_speed_row()
        position_row = self._build_position_row()

        return ft.Column(
            [
                ft.Text("Move", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                range_row,
                ft.Container(height=8),
                speed_row,
                ft.Container(height=8),
                position_row,
            ],
            spacing=12,
            expand=True,
        )

    def _build_move_range_row(self):
        """Build move range controls"""

        self.move_start_input = ft.TextField(
            label="Start",
            value="0",
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_range_change,
            expand=True,
        )

        self.move_end_input = ft.TextField(
            label="End",
            value="100",
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_range_change,
            expand=True,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("Move Range:", size=12, weight=ft.FontWeight.W_500, width=100),
                    ft.Row(
                        [
                            ft.Container(content=self.move_start_input, expand=True, margin=ft.margin.only(right=20)),
                            ft.Container(content=ft.Text("~", size=12, text_align=ft.TextAlign.CENTER), width=20),
                            ft.Container(content=self.move_end_input, expand=True, margin=ft.margin.only(left=20)),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
        )

    def _build_speed_row(self):
        """Build speed controls (field + slider)"""

        self.SPEED_MIN = 0
        self.SPEED_MAX = 1023

        self.move_speed_input = ft.TextField(
            value="1.0",
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_speed_change,
            expand=True,
        )

        self.move_speed_slider = ft.Slider(
            min=self.SPEED_MIN,
            max=self.SPEED_MAX,
            value=1.0,
            height=35,
            thumb_color=ft.Colors.BLUE,
            active_color=ft.Colors.BLUE_300,
            inactive_color=ft.Colors.GREY_300,
            on_change=self._on_speed_slider_change,
            expand=True,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("Move Speed:", size=12, weight=ft.FontWeight.W_500, width=100),
                    ft.Row(
                        [
                            ft.Container(content=self.move_speed_input, expand=True, margin=ft.margin.only(right=20)),
                            ft.Container(content=ft.Text(" ", size=12), width=20),
                            ft.Container(content=self.move_speed_slider, expand=True),
                        ],
                        spacing=5,
                        expand=True,
                    ),
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
        )
    
    def _build_position_row(self):
        """Build initial position and edge reflect controls"""

        self.initial_position_input = ft.TextField(
            value="10",
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_initial_position_change,
            expand=True,
        )

        self.edge_reflect_checkbox = ft.Checkbox(
            label="Enable",
            value=True,
            on_change=self._on_edge_reflect_change,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("Initial Position:", size=12, weight=ft.FontWeight.W_500, width=100),
                    ft.Row(
                        [
                            ft.Container(content=self.initial_position_input, expand=True, margin=ft.margin.only(right=20)),
                            ft.Text("Edge Reflect:", size=12, weight=ft.FontWeight.W_500, width=100),
                            ft.Container(content=self.edge_reflect_checkbox, expand=True),
                        ],
                        spacing=10,
                        expand=True,
                    ),
                ],
                spacing=10,
                expand=True,
            ),
            expand=True,
        )

    def _on_move_range_change(self, e):
        """Handle move range change"""
        start = self.move_start_input.value
        end = self.move_end_input.value
        self.action_handler.update_move_range(start, end)

    def _on_move_speed_change(self, e):
        """Handle move speed field change (sync slider)"""
        try:
            speed = float(e.control.value)
            speed_clamped = max(self.SPEED_MIN, min(self.SPEED_MAX, speed))
            self.move_speed_slider.value = speed_clamped
            self.action_handler.update_move_speed(speed_clamped)
            self.move_speed_slider.update()
        except ValueError:
            pass

    def _on_speed_slider_change(self, e):
        """Handle speed slider change (sync field)"""
        try:
            speed = float(e.control.value)
            self.move_speed_input.value = f"{speed:.1f}"
            self.action_handler.update_move_speed(speed)
            self.move_speed_input.update()
        except ValueError:
            pass

    def _on_initial_position_change(self, e):
        """Handle initial position change"""
        position = e.control.value
        self.action_handler.update_initial_position(position)

    def _on_edge_reflect_change(self, e):
        """Handle edge reflect toggle change (checkbox)"""
        enabled = bool(e.control.value)
        self.action_handler.update_edge_reflect(enabled)

    def get_move_parameters(self):
        """Get current move parameters"""
        return {
            "start": self.move_start_input.value,
            "end": self.move_end_input.value,
            "speed": self.move_speed_input.value,
            "initial_position": self.initial_position_input.value,
            "edge_reflect": self.edge_reflect_checkbox.value,
        }

    def set_move_parameters(self, params):
        """Set move parameters programmatically"""
        if "start" in params:
            self.move_start_input.value = str(params["start"])
        if "end" in params:
            self.move_end_input.value = str(params["end"])
        if "speed" in params:
            try:
                speed = float(params["speed"])
                speed_clamped = max(self.SPEED_MIN, min(self.SPEED_MAX, speed))
                self.move_speed_input.value = f"{speed_clamped:.1f}"
                self.move_speed_slider.value = speed_clamped
            except (TypeError, ValueError):
                pass
        if "initial_position" in params:
            self.initial_position_input.value = str(params["initial_position"])
        if "edge_reflect" in params:
            self.edge_reflect_checkbox.value = bool(params["edge_reflect"])

        self.update()
