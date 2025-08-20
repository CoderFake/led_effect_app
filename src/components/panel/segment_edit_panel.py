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

        self.palette_colors = list(color_service.get_palette_colors())

        color_select_row = self._build_color_select_row(self.palette_colors)    
        transparency_row = self._build_transparency_row(self.palette_colors)    
        length_row = self._build_length_row(self.palette_colors)              

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

    # -------------------------------
    # Row 1: Color Select
    # -------------------------------
    def _build_color_select_row(self, colors):
        """Row contain color boxes for selection"""
        self.color_boxes = []

        for index, color in enumerate(colors[:5]):
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

    # -------------------------------
    # Row 2: Transparency
    # -------------------------------
    def _build_transparency_row(self, colors):
        """Row contain TextField + Slider for each color slot"""
        self.transparency_fields = []
        self.transparency_sliders = []
        containers = []

        for index, _ in enumerate(colors[:5]):
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

    # -------------------------------
    # Row 3: Length
    # -------------------------------
    def _build_length_row(self, colors):
        """Row contain TextField length for each color slot"""
        self.length_fields = []
        items = []

        for index, _ in enumerate(colors[:5]):
            field = ft.TextField(
                value="10",
                height=30,
                text_size=11,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border=ft.Colors.GREY_400,
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

    # ===============================
    # Actions
    # ===============================
    def _select_color(self, color_index: int):
        """Show Color Selection Modal and update segment param"""
        def on_color_change(slot_index: int, selected_color_index: int, color: str):
            self.segment_component.action_handler.update_segment_parameter(
                self.segment_component.get_selected_segment(),
                f"color_slot_{slot_index}",
                f"palette_color_{selected_color_index}",
            )

            # Update UI
            self.color_boxes[slot_index].content.controls[1].bgcolor = color
            self.color_boxes[slot_index].update()

        try:
            modal = ColorSelectionModal(
                palette_id=0,
                on_color_select=lambda idx, color: on_color_change(color_index, idx, color),
            )
            modal.page = self.page
            self.page.dialog = modal
            modal.open = True
            self.page.update()
        except Exception as e:
            print(f"Error opening color modal: {e}")

    def _on_transparency_field_change(self, index: int, value: str):
        """Field → Slider"""
        try:
            transparency = float(value)
            if 0 <= transparency <= 1:
                self.transparency_sliders[index].value = transparency
                self.transparency_sliders[index].update()
                self.segment_component.action_handler.update_segment_parameter(
                    self.segment_component.get_selected_segment(),
                    f"transparency_{index}",
                    transparency,
                )
        except ValueError:
            pass

    def _on_transparency_slider_change(self, index: int, value: float):
        """Slider → Field"""
        try:
            v = float(value)
            self.transparency_fields[index].value = f"{v:.2f}"
            self.transparency_fields[index].update()
            self.segment_component.action_handler.update_segment_parameter(
                self.segment_component.get_selected_segment(),
                f"transparency_{index}",
                v,
            )
        except ValueError:
            pass

    def _on_length_change(self, index: int, value: str):
        """Update length"""
        try:
            length = int(value)
            if length > 0:
                self.segment_component.action_handler.update_segment_parameter(
                    self.segment_component.get_selected_segment(),
                    f"length_{index}",
                    length,
                )
        except ValueError:
            pass

    # ===============================
    # External updates
    # ===============================
    def update_segments_list(self, segments_list):
        self.segment_component.update_segments(segments_list)

    def update_regions_list(self, regions_list):
        self.segment_component.update_regions(regions_list)

    def get_current_segment_data(self):
        """Get current segment configuration"""
        return {
            "segment_id": self.segment_component.get_selected_segment(),
            "assigned_region": self.segment_component.get_assigned_region(),
            "move_params": self.move_component.get_move_parameters(),
            "dimmer_data": self.dimmer_component.get_dimmer_input_values(),
        }