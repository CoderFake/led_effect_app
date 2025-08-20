import flet as ft
from ..segment import SegmentComponent
from ..move import MoveComponent
from ..dimmer import DimmerComponent
from ..color.color_selection_modal import ColorSelectionModal
from .segment_edit_action import SegmentEditActionHandler
from services.color_service import color_service


class SegmentEditPanel(ft.Container):
    """Right panel for segment editing"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = SegmentEditActionHandler(page)
        self.expand = True
        self.content = self.build_content()

    def build_content(self):
        """Build segment edit panel"""

        self.segment_component = SegmentComponent(self.page)

        color_section = self._build_color_composition_section()

        self.move_component = MoveComponent(self.page)
        self.dimmer_component = DimmerComponent(self.page)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Segment Edit", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                    ft.Container(height=15),

                    # Segment
                    ft.Container(
                        content=self.segment_component,
                        padding=ft.padding.all(15),
                        margin=ft.margin.all(5),
                        border_radius=10,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                    ),

                    ft.Container(height=15),

                    color_section,

                    ft.Container(height=15),

                    ft.Container(
                        content=self.move_component,
                        padding=ft.padding.all(15),
                        margin=ft.margin.all(5),
                        border_radius=10,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                    ),

                    ft.Container(height=15),

                    ft.Container(
                        content=self.dimmer_component,
                        padding=ft.padding.all(15),
                        margin=ft.margin.all(5),
                        border_radius=10,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.all(1, ft.Colors.GREY_400),
            expand=True,
        )

    def _build_color_composition_section(self):
        """Build Color Composition controls"""

        color_select_row = self._build_color_select_row()    
        transparency_row = self._build_transparency_row()    
        length_row = self._build_length_row()              

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Color Composition", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Container(height=8),

                    ft.Row(
                        [
                            ft.Text("Color Select:", size=12, weight=ft.FontWeight.W_500, width=100),
                            color_select_row,
                        ],
                        spacing=5,
                        expand=True,
                    ),
                    ft.Container(height=8),

                    ft.Row(
                        [
                            ft.Text("Transparency:", size=12, weight=ft.FontWeight.W_500, width=100),
                            transparency_row,
                        ],
                        spacing=5,
                        expand=True,
                    ),
                    ft.Container(height=8),

                    ft.Row(
                        [
                            ft.Text("Length:", size=12, weight=ft.FontWeight.W_500, width=100),
                            length_row,
                        ],
                        spacing=5,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_400),
            expand=True,
        )

    def _build_color_select_row(self):
        """Row contain color boxes for selection"""
        self.color_boxes = []
        colors = self.action_handler.get_palette_colors_for_display()

        for index, color in enumerate(colors[:6]):
            box = ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                str(index),
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            height=20,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            bgcolor=color,
                            height=30,
                            border_radius=4,
                            border=ft.border.all(1, ft.Colors.GREY_400),
                            ink=True,
                            on_click=lambda e, idx=index: self._select_color(idx),
                            tooltip=f"Color slot {index} - Click to change",
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                expand=True,
            )
            self.color_boxes.append(box)

        return ft.Container(
            content=ft.Row(
                self.color_boxes,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=5,
                expand=True,
            ),
            expand=True,
        )

    def _select_color(self, color_index: int):
        """Handle color selection - delegate to action handler"""
        self.action_handler.handle_color_slot_selection(color_index, self.segment_component)
        
        def on_color_change(selected_color_index: int, selected_color: str):
            segment_id = self.segment_component.get_selected_segment()
            
            if self.action_handler.update_segment_color_slot(segment_id, color_index, selected_color_index):
                self.color_boxes[color_index].content.controls[1].bgcolor = selected_color
                self.color_boxes[color_index].update()

        try:
            modal = ColorSelectionModal(
                palette_id=0,
                on_color_select=on_color_change
            )
            self.page.open(modal)
        except Exception as e:
            print(f"Error opening color modal: {e}")

    def _build_transparency_row(self):
        """Row contain TextField + Slider for each color slot"""
        self.transparency_fields = []
        self.transparency_sliders = []
        containers = []

        for index in range(6):
            field = ft.TextField(
                value="1.0",
                height=30,
                text_size=11,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400,
                content_padding=ft.padding.all(3),
                on_change=lambda e, idx=index: self._on_transparency_field_change(idx, e.control.value),
                expand=True,
            )
            slider = ft.Slider(
                min=0,
                max=1,
                value=1.0,
                height=60,
                thumb_color=ft.Colors.BLUE,
                active_color=ft.Colors.BLUE_300,
                inactive_color=ft.Colors.GREY_400,
                on_change=lambda e, idx=index: self._on_transparency_slider_change(idx, e.control.value),
                expand=True,
            )

            self.transparency_fields.append(field)
            self.transparency_sliders.append(slider)

            containers.append(
                ft.Container(
                    content=ft.Column([field, slider], spacing=2, expand=True),
                    expand=True,
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=15),
                    ft.Row(containers, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                spacing=5,
                expand=True,
            ),
            expand=True,
        )

    def _build_length_row(self):
        """Row contain TextField length for each color slot"""
        self.length_fields = []
        items = []

        for index in range(6):
            field = ft.TextField(
                value="10",
                height=30,
                text_size=11,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400,
                content_padding=ft.padding.all(3),
                on_change=lambda e, idx=index: self._on_length_change(idx, e.control.value),
                expand=True,
            )
            self.length_fields.append(field)
            items.append(field)

        return ft.Container(
            content=ft.Row(
                items,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=7,
                expand=True,
            ),
            expand=True,
        )

    def _on_transparency_field_change(self, index: int, value: str):
        """Field → Slider - delegate to action handler"""
        result = self.action_handler.update_transparency_from_field(index, value, self.segment_component)
        if result is not None:
            self.transparency_sliders[index].value = result
            self.transparency_sliders[index].update()

    def _on_transparency_slider_change(self, index: int, value: float):
        """Slider → Field - delegate to action handler"""
        result = self.action_handler.update_transparency_from_slider(index, value, self.segment_component)
        if result is not None:
            self.transparency_fields[index].value = self.action_handler.format_transparency_value(result)
            self.transparency_fields[index].update()

    def _on_length_change(self, index: int, value: str):
        """Update length - delegate to action handler"""
        self.action_handler.update_length_parameter(index, value, self.segment_component)

    def update_segments_list(self, segments_list):
        """Update segments list - delegate to action handler"""
        processed_list = self.action_handler.process_segments_list_update(segments_list)
        if processed_list:
            self.segment_component.update_segments(processed_list)

    def update_regions_list(self, regions_list):
        """Update regions list - delegate to action handler"""
        processed_list = self.action_handler.process_regions_list_update(regions_list)
        if processed_list:
            self.segment_component.update_regions(processed_list)

    def get_current_segment_data(self):
        """Get current segment configuration - delegate to action handler"""
        return self.action_handler.get_current_segment_data(
            self.segment_component, 
            self.move_component, 
            self.dimmer_component
        )