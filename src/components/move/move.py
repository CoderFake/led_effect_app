import flet as ft
from .move_action import MoveActionHandler


class MoveComponent(ft.Container):
    """Move configuration component for segments"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = MoveActionHandler(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build Move controls"""
        
        move_range_row = self._build_move_range_row()
        position_row = self._build_position_row()
        
        return ft.Column([
            ft.Text("Move", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Container(height=8),
            move_range_row,
            ft.Container(height=8),
            position_row
        ], spacing=0)
        
    def _build_move_range_row(self):
        """Build move range and speed controls"""
        
        self.move_start_field = ft.TextField(
            value="0",
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_range_change
        )
        
        self.move_end_field = ft.TextField(
            value="100",
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_range_change
        )
        
        self.move_speed_field = ft.TextField(
            value="1.0",
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_move_speed_change
        )
        
        self.move_speed_slider = ft.Slider(
            min=0,
            max=10,
            value=1.0,
            width=100,
            height=35,
            thumb_color=ft.Colors.BLUE,
            active_color=ft.Colors.BLUE_300,
            inactive_color=ft.Colors.GREY_300,
            on_change=self._on_speed_slider_change
        )
        
        return ft.Row([
            ft.Text("Move Range:", size=12, weight=ft.FontWeight.W_500, width=100),
            self.move_start_field,
            ft.Text("~", size=12, width=20, text_align=ft.TextAlign.CENTER),
            self.move_end_field,
            ft.Text("Move Speed:", size=12, weight=ft.FontWeight.W_500, width=80),
            self.move_speed_field,
            ft.Container(
                content=self.move_speed_slider,
                width=100
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.START)
        
    def _build_position_row(self):
        """Build initial position and edge reflect controls"""
        
        self.initial_position_field = ft.TextField(
            value="10",
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            on_change=self._on_initial_position_change
        )
        
        self.edge_reflect_dropdown = ft.Dropdown(
            value="bounce",
            options=[
                ft.dropdown.Option("bounce"),
                ft.dropdown.Option("wrap"),
                ft.dropdown.Option("stop")
            ],
            width=80,
            text_size=12,
            on_change=self._on_edge_reflect_change
        )
        
        return ft.Row([
            ft.Text("Initial Position:", size=12, weight=ft.FontWeight.W_500, width=100),
            self.initial_position_field,
            ft.Text("Edge Reflect:", size=12, weight=ft.FontWeight.W_500, width=100),
            self.edge_reflect_dropdown
        ], spacing=10, alignment=ft.MainAxisAlignment.START)
        
    def _on_move_range_change(self, e):
        """Handle move range change"""
        start = self.move_start_field.value
        end = self.move_end_field.value
        self.action_handler.update_move_range(start, end)
        
    def _on_move_speed_change(self, e):
        """Handle move speed field change"""
        try:
            speed = float(e.control.value)
            self.move_speed_slider.value = min(max(speed, 0), 10)
            self.action_handler.update_move_speed(speed)
            self.update()
        except ValueError:
            pass
            
    def _on_speed_slider_change(self, e):
        """Handle speed slider change"""
        speed = e.control.value
        self.move_speed_field.value = f"{speed:.1f}"
        self.action_handler.update_move_speed(speed)
        self.update()
        
    def _on_initial_position_change(self, e):
        """Handle initial position change"""
        position = e.control.value
        self.action_handler.update_initial_position(position)
        
    def _on_edge_reflect_change(self, e):
        """Handle edge reflect mode change"""
        mode = e.control.value
        self.action_handler.update_edge_reflect(mode)
        
    def get_move_parameters(self):
        """Get current move parameters"""
        return {
            'start': self.move_start_field.value,
            'end': self.move_end_field.value,
            'speed': self.move_speed_field.value,
            'initial_position': self.initial_position_field.value,
            'edge_reflect': self.edge_reflect_dropdown.value
        }
        
    def set_move_parameters(self, params):
        """Set move parameters programmatically"""
        if 'start' in params:
            self.move_start_field.value = str(params['start'])
        if 'end' in params:
            self.move_end_field.value = str(params['end'])
        if 'speed' in params:
            speed = float(params['speed'])
            self.move_speed_field.value = f"{speed:.1f}"
            self.move_speed_slider.value = speed
        if 'initial_position' in params:
            self.initial_position_field.value = str(params['initial_position'])
        if 'edge_reflect' in params:
            self.edge_reflect_dropdown.value = params['edge_reflect']
        self.update()