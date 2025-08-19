import flet as ft
import math
from typing import Callable, Optional


class ColorWheel(ft.Container):
    """Simplified color wheel picker component using Container with gradient"""
    
    def __init__(self, initial_color: str = "#FF0000", on_color_change: Optional[Callable[[str], None]] = None):
        super().__init__()
        self.initial_color = initial_color
        self.on_color_change = on_color_change
        self.current_color = initial_color
        
        self.bgcolor = ft.Colors.TRANSPARENT
        self.border = None
        
        self.hue = 0  # 0-360
        self.saturation = 1.0  # 0-1
        self.value = 1.0  # 0-1
        
        self._parse_hex_color(initial_color)
        
        self.width = 300
        self.height = 350
        
        self.content = self._build_content()
        
    def _parse_hex_color(self, hex_color: str):
        """Parse hex color to HSV values"""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        # Convert RGB to HSV
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Value
        self.value = max_val
        
        # Saturation
        if max_val == 0:
            self.saturation = 0
        else:
            self.saturation = diff / max_val
            
        # Hue
        if diff == 0:
            self.hue = 0
        elif max_val == r:
            self.hue = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            self.hue = (60 * ((b - r) / diff) + 120) % 360
        else:
            self.hue = (60 * ((r - g) / diff) + 240) % 360
    
    def _hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Convert HSV to hex color"""
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
        
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def _build_content(self) -> ft.Column:
        """Build color wheel UI"""
        
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
            width=60,
            height=60,
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
                    ft.Text(f"HSV({int(self.hue)}°, {int(self.saturation * 100)}%, {int(self.value * 100)}%)", 
                            size=10, color=ft.Colors.GREY_600)
                ], spacing=2)
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
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
        
    def _update_color(self):
        """Update color based on HSV values"""
        self.current_color = self._hsv_to_hex(self.hue, self.saturation, self.value)
        
        if hasattr(self, 'color_preview'):
            self.color_preview.bgcolor = self.current_color
        if hasattr(self, 'color_display'):
            self.color_display.value = self.current_color.upper()
        if hasattr(self, 'value_slider'):
            self.value_slider.label = f"Brightness: {int(self.value * 100)}%"
        
        self.update()
        
        if self.on_color_change:
            self.on_color_change(self.current_color)
    
    def get_color(self) -> str:
        """Get current selected color"""
        return self.current_color
    
    def set_color(self, hex_color: str, notify=False):
        """Set color programmatically"""
        self.current_color = hex_color
        self._parse_hex_color(hex_color)
        
        if hasattr(self, 'color_preview'):
            self.color_preview.bgcolor = self.current_color
        
        if hasattr(self, 'value_slider'):
            self.value_slider.value = self.value
            self.value_slider.label = f"Brightness: {int(self.value * 100)}%"
            
        if hasattr(self, 'color_display'):
            self.color_display.value = self.current_color.upper()
            
        self.update()
        
        if notify and self.on_color_change:
            self.on_color_change(self.current_color)
