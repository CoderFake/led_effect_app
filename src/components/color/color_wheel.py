import flet as ft
import math
from typing import Callable, Optional


class ColorWheel(ft.Container):
    """Color wheel picker component with RGB display"""
    
    def __init__(self, initial_color: str = "#FF0000", on_color_change: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.initial_color = initial_color
        self.on_color_change = on_color_change
        self.current_color = initial_color
        
        self.bgcolor = ft.Colors.TRANSPARENT
        self.border = None
        
        self.hue = 0  
        self.saturation = 1.0
        self.value = 1.0
        
        self.r = 255
        self.g = 0
        self.b = 0
        
        self._parse_hex_color(initial_color)
        
        self.width = 400
        self.height = 480
        
        self.content = self._build_content()
        
    def _parse_hex_color(self, hex_color: str):
        """Parse hex color to HSV and RGB values"""
        hex_color = hex_color.lstrip('#')
        
        self.r = int(hex_color[0:2], 16)
        self.g = int(hex_color[2:4], 16)
        self.b = int(hex_color[4:6], 16)
        
        r_norm = self.r / 255.0
        g_norm = self.g / 255.0
        b_norm = self.b / 255.0
        
        max_val = max(r_norm, g_norm, b_norm)
        min_val = min(r_norm, g_norm, b_norm)
        diff = max_val - min_val
        
        self.value = max_val
        
        if max_val == 0:
            self.saturation = 0
        else:
            self.saturation = diff / max_val
            
        if diff == 0:
            self.hue = 0
        elif max_val == r_norm:
            self.hue = (60 * ((g_norm - b_norm) / diff) + 360) % 360
        elif max_val == g_norm:
            self.hue = (60 * ((b_norm - r_norm) / diff) + 120) % 360
        else:
            self.hue = (60 * ((r_norm - g_norm) / diff) + 240) % 360
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> tuple:
        """Convert HSV to RGB values"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
            
        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)
        
        return r, g, b
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex color"""
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def _build_content(self) -> ft.Column:
        """Build color wheel UI with RGB display"""
        
        self.color_wheel_container = ft.Container(
            width=200,
            height=200,
            border_radius=100,
            gradient=ft.SweepGradient(
                center=ft.alignment.center,
                colors=[
                    "#FF0000",  # 0° - Red
                    "#FF4000",  # 15°
                    "#FF8000",  # 30° - Red-Orange
                    "#FFBF00",  # 45°
                    "#FFFF00",  # 60° - Yellow
                    "#BFFF00",  # 75°
                    "#80FF00",  # 90° - Yellow-Green
                    "#40FF00",  # 105°
                    "#00FF00",  # 120° - Green
                    "#00FF40",  # 135°
                    "#00FF80",  # 150° - Green-Cyan
                    "#00FFBF",  # 165°
                    "#00FFFF",  # 180° - Cyan
                    "#00BFFF",  # 195°
                    "#0080FF",  # 210° - Cyan-Blue
                    "#0040FF",  # 225°
                    "#0000FF",  # 240° - Blue
                    "#4000FF",  # 255°
                    "#8000FF",  # 270° - Blue-Magenta
                    "#BF00FF",  # 285°
                    "#FF00FF",  # 300° - Magenta
                    "#FF00BF",  # 315°
                    "#FF0080",  # 330° - Magenta-Red
                    "#FF0040",  # 345°
                    "#FF0000"   # 360° - Back to Red
                ],
                stops=[0.0, 0.042, 0.083, 0.125, 0.167, 0.208, 0.25, 0.292, 0.333, 0.375, 0.417, 0.458, 0.5, 0.542, 0.583, 0.625, 0.667, 0.708, 0.75, 0.792, 0.833, 0.875, 0.917, 0.958, 1.0]
            ),
            content=ft.GestureDetector(
                on_pan_update=self._on_container_pan,
                on_tap_down=self._on_container_tap,
                drag_interval=10
            )
        )
        
        self.color_preview = ft.Container(
            width=85,
            height=85,
            bgcolor=self.current_color,
            border_radius=8,
            border=ft.border.all(2, ft.Colors.GREY_400),
        )
        
        self.value_slider = ft.Slider(
            min=0,
            max=1,
            value=self.value,
            divisions=100,
            label=f"Brightness: {int(self.value * 100)}%",
            on_change=self._on_value_change,
            width=250
        )
        
        self.color_display = ft.Text(
            value=self.current_color.upper(),
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.red_field = ft.TextField(
            value=str(self.r),
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.RED_400,
            on_change=self._on_rgb_field_change,
            on_submit=self._on_rgb_field_change
        )
        
        self.green_field = ft.TextField(
            value=str(self.g),
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREEN_400,
            on_change=self._on_rgb_field_change,
            on_submit=self._on_rgb_field_change
        )
        
        self.blue_field = ft.TextField(
            value=str(self.b),
            width=60,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.BLUE_400,
            on_change=self._on_rgb_field_change,
            on_submit=self._on_rgb_field_change
        )
        
        return ft.Column([
            ft.Container(
                content=self.color_wheel_container,
                alignment=ft.alignment.center,
                padding=10
            ),
            ft.Row([
                self.color_preview,
                ft.Column([
                    self.color_display,
                    ft.Row([
                        ft.Column([
                            ft.Text("R", size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                            self.red_field
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Text("G", size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                            self.green_field
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Text("B", size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                            self.blue_field
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Brightness", size=12, weight=ft.FontWeight.W_500),
            self.value_slider,
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _on_container_tap(self, e):
        """Handle container tap"""
        self._handle_container_interaction(e.local_x, e.local_y)
        
    def _on_container_pan(self, e):
        """Handle container pan/drag"""
        self._handle_container_interaction(e.local_x, e.local_y)
        
    def _handle_container_interaction(self, x: float, y: float):
        """Handle container interaction (tap or drag)"""
        center_x = 100 
        center_y = 100
        radius = 100
        
        dx = x - center_x
        dy = y - center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance <= radius:
            angle = math.degrees(math.atan2(dy, dx)) + 90
            if angle < 0:
                angle += 360
            
            saturation = min(distance / radius, 1.0)
            
            self.hue = angle % 360
            self.saturation = saturation
            
            self._update_color()
    
    def _on_value_change(self, e):
        """Handle brightness slider change"""
        self.value = e.control.value
        self._update_color()
        
    def _on_rgb_field_change(self, e):
        """Handle RGB field changes"""
        try:
            r = max(0, min(255, int(self.red_field.value or 0)))
            g = max(0, min(255, int(self.green_field.value or 0)))
            b = max(0, min(255, int(self.blue_field.value or 0)))
            
            self.r = r
            self.g = g
            self.b = b
            
            self.current_color = self._rgb_to_hex(r, g, b)
            
            self._parse_hex_color(self.current_color)
            self._update_ui_elements()
            
            if self.on_color_change:
                self.on_color_change(self.current_color)
                
        except ValueError:
            pass
        
    def _update_color(self):
        """Update color based on HSV values"""
        self.r, self.g, self.b = self._hsv_to_rgb(self.hue, self.saturation, self.value)
        self.current_color = self._rgb_to_hex(self.r, self.g, self.b)
        
        self._update_ui_elements()
        
        if self.on_color_change:
            self.on_color_change(self.current_color)
    
    def _update_ui_elements(self):
        """Update UI elements with current color values"""
        if hasattr(self, 'color_preview'):
            self.color_preview.bgcolor = self.current_color
            
        if hasattr(self, 'color_display'):
            self.color_display.value = self.current_color.upper()
            
        if hasattr(self, 'value_slider'):
            self.value_slider.value = self.value
            self.value_slider.label = f"Brightness: {int(self.value * 100)}%"
            
        # Update RGB fields without triggering events
        if hasattr(self, 'red_field'):
            self.red_field.value = str(self.r)
        if hasattr(self, 'green_field'):
            self.green_field.value = str(self.g)
        if hasattr(self, 'blue_field'):
            self.blue_field.value = str(self.b)
        
        self.update()
    
    def get_color(self) -> str:
        """Get current selected color"""
        return self.current_color
    
    def get_rgb(self) -> tuple:
        """Get current RGB values"""
        return (self.r, self.g, self.b)
    
    def set_color(self, hex_color: str, notify=True):
        """Set color programmatically"""
        self.current_color = hex_color
        self._parse_hex_color(hex_color)
        
        self._update_ui_elements()
        
        if notify and self.on_color_change:
            self.on_color_change(self.current_color)
            
    def set_rgb(self, r: int, g: int, b: int, notify=True):
        """Set color using RGB values"""
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        
        self.current_color = self._rgb_to_hex(self.r, self.g, self.b)
        self._parse_hex_color(self.current_color)
        
        self._update_ui_elements()
        
        if notify and self.on_color_change:
            self.on_color_change(self.current_color)