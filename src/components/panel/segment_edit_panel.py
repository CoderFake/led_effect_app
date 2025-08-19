import flet as ft
from ..segment import SegmentComponent
from ..move import MoveComponent
from ..dimmer import DimmerComponent
from ..color import ColorSelectionModal
from services.color_service import color_service


class SegmentEditPanel(ft.Container):
    """Right panel for segment editing"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build segment edit panel"""
        
        self.segment_component = SegmentComponent(self.page)
        color_composition_section = self._build_color_composition_section()
        self.move_component = MoveComponent(self.page)
        self.dimmer_component = DimmerComponent(self.page)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Segment Edit", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Container(height=15),
                
                ft.Container(
                    content=self.segment_component,
                    padding=ft.padding.all(15),
                    margin=ft.margin.all(5),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                ),
                
                ft.Container(height=15),
                color_composition_section,
                
                ft.Container(height=15), 
                ft.Container(
                    content=self.move_component,
                    padding=ft.padding.all(15),
                    margin=ft.margin.all(5),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                ),
                
                ft.Container(height=15),
                ft.Container(
                    content=self.dimmer_component,
                    padding=ft.padding.all(15),
                    margin=ft.margin.all(5),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.all(1, ft.Colors.GREY_300),
            expand=True
        )
        
    def _build_color_composition_section(self):
        """Build Color Composition controls with column layout"""
        columns = []
        
        label_column = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("Color Slot:", size=12, weight=ft.FontWeight.W_500),
                    height=30
                ),
                ft.Container(
                    content=ft.Text("Color Select:", size=12, weight=ft.FontWeight.W_500),
                    height=35
                ),
                ft.Container(
                    content=ft.Text("Transparency:", size=12, weight=ft.FontWeight.W_500),
                    height=130  
                ),
                ft.Container(
                    content=ft.Text("Length:", size=12, weight=ft.FontWeight.W_500),
                    height=35
                )
            ], spacing=2),
            width=100
        )
        columns.append(label_column)
        
        try:
            colors = color_service.get_palette_colors()
        except Exception:
            colors = [ft.Colors.BLACK, ft.Colors.RED, ft.Colors.YELLOW, ft.Colors.BLUE, ft.Colors.GREEN]

        for i in range(len(colors)):
            slot_column = self._create_color_slot_column(i, colors[i])
            columns.append(slot_column)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Color Composition", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ft.Container(
                    content=ft.Row(columns, spacing=5, scroll=ft.ScrollMode.AUTO),
                    height=240
                )
            ], spacing=0),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
    def _create_color_slot_column(self, index: int, color: str):
        """Create a single color slot column"""
        
        transparency_field = ft.TextField(
            value="1.0",
            width=80,
            height=25,
            text_size=11,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            content_padding=ft.padding.all(1),
            on_change=lambda e, idx=index: self._on_transparency_field_change(idx, e.control.value)
        )
        
        transparency_slider = ft.Slider(
            min=0,
            max=1,
            value=1.0,
            width=80,
            height=120,
            thumb_color=ft.Colors.BLUE,
            active_color=ft.Colors.BLUE_300,
            inactive_color=ft.Colors.GREY_300,
            on_change=lambda e, idx=index, field=transparency_field: self._on_transparency_slider_change(idx, e.control.value, field)
        )
        
        length_field = ft.TextField(
            value="10",
            width=80,
            height=35,
            text_size=11,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            content_padding=ft.padding.all(3),
            on_change=lambda e, idx=index: self._on_length_change(idx, e.control.value)
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(str(index), size=12, text_align=ft.TextAlign.CENTER),
                    height=30
                ),
                ft.Container(
                    width=80,
                    height=35,
                    bgcolor=color,
                    border=ft.border.all(1, ft.Colors.GREY_600),
                    border_radius=4,
                    on_click=lambda e, idx=index: self._select_color(idx),
                    tooltip=f"Color {index} - Click to change"
                ),
                ft.Container(
                    content=ft.Stack([
                        ft.Container(
                            content=transparency_field,
                            top=0,
                            left=0
                        ),
                        ft.Container(
                            content=ft.Container(
                                content=transparency_slider,
                                margin=ft.margin.only(bottom=-15),
                                padding=ft.padding.all(0)
                            ),
                            top=5, 
                            left=0
                        )
                    ]),
                    width=80,
                    height=130  
                ),
                length_field
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=80
        )
        
    def _select_color(self, color_index):
        """Handle color selection for segment - Show Color Selection Modal"""
        def on_color_change(slot_index: int, selected_color_index: int, color: str):
            """Handle color change from modal"""
            self.segment_component.action_handler.update_segment_parameter(
                self.segment_component.get_selected_segment(),
                f"color_slot_{slot_index}",
                f"palette_color_{selected_color_index}"
            )
            
        try:
            modal = ColorSelectionModal(
                palette_id=0,
                on_color_select=lambda idx, color: on_color_change(color_index, idx, color)
            )
            modal.page = self.page
            self.page.dialog = modal
            modal.open = True
            self.page.update()
        except Exception as e:
            print(f"Error opening color modal: {e}")
            
    def _on_transparency_field_change(self, index: int, value: str):
        """Handle transparency field change"""
        try:
            transparency = float(value)
            if 0 <= transparency <= 1:
                self.segment_component.action_handler.update_segment_parameter(
                    self.segment_component.get_selected_segment(),
                    f"transparency_{index}",
                    transparency
                )
        except ValueError:
            pass
            
    def _on_transparency_slider_change(self, index: int, value: float, field: ft.TextField):
        """Handle transparency slider change"""
        field.value = f"{value:.2f}"
        field.update()
        self.segment_component.action_handler.update_segment_parameter(
            self.segment_component.get_selected_segment(),
            f"transparency_{index}",
            value
        )
        
    def _on_length_change(self, index: int, value: str):
        """Handle length field change"""
        try:
            length = int(value)
            if length > 0:
                self.segment_component.action_handler.update_segment_parameter(
                    self.segment_component.get_selected_segment(),
                    f"length_{index}",
                    length
                )
        except ValueError:
            pass
            
    def update_segments_list(self, segments_list):
        """Update segments dropdown"""
        self.segment_component.update_segments(segments_list)
        
    def update_regions_list(self, regions_list):
        """Update region assignment dropdown"""
        self.segment_component.update_regions(regions_list)
        
    def get_current_segment_data(self):
        """Get current segment configuration"""
        return {
            'segment_id': self.segment_component.get_selected_segment(),
            'assigned_region': self.segment_component.get_assigned_region(),
            'move_params': self.move_component.get_move_parameters(),
            'dimmer_data': self.dimmer_component.get_dimmer_input_values()
        }