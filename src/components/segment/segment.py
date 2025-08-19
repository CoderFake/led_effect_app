import flet as ft
from .segment_action import SegmentActionHandler


class SegmentComponent(ft.Container):
    """Segment UI component with responsive buttons row"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = SegmentActionHandler(page)
        self.content = self.build_content()

    def _chip(self, ctrl: ft.Control, border_color=ft.Colors.GREY_500):
        return ft.Container(
            content=ctrl,
            width=40,
            height=40,
            alignment=ft.alignment.center,
            border=ft.border.all(1, border_color),
            border_radius=8,
            padding=0,
        )

    def build_content(self):
        self.segment_dropdown = ft.Dropdown(
            value="0",
            options=[ft.dropdown.Option("0")],
            hint_text="Segment ID",
            menu_width=150
        )

        buttons_row = ft.Row(
            controls=[
                self._chip(
                    ft.IconButton(
                        icon=ft.Icons.ADD, icon_size=18, icon_color=ft.Colors.BLACK,
                        tooltip="Add Segment", on_click=self.action_handler.add_segment
                    ),
                    ft.Colors.PRIMARY,
                ),
                self._chip(
                    ft.IconButton(
                        icon=ft.Icons.REMOVE, icon_size=18, icon_color=ft.Colors.BLACK,
                        tooltip="Delete Segment", on_click=self.action_handler.delete_segment
                    ),
                    ft.Colors.RED,
                ),
                self._chip(
                    ft.IconButton(
                        icon=ft.Icons.COPY, icon_size=18,
                        tooltip="Copy Segment", on_click=self.action_handler.copy_segment,
                        icon_color=ft.Colors.BLACK
                    ),
                    ft.Colors.GREEN,
                ),
                self._chip(
                    ft.TextButton(
                        text="S", tooltip="Solo",
                        on_click=self.action_handler.solo_segment
                    ),
                    ft.Colors.PRIMARY,
                ),
                self._chip(
                    ft.TextButton(
                        text="M", tooltip="Mute",
                        on_click=self.action_handler.mute_segment
                    ),
                    ft.Colors.RED,
                ),
                self._chip(
                    ft.IconButton(
                        icon=ft.Icons.SYNC_ALT, icon_size=18,
                        tooltip="Reorder", on_click=self.action_handler.reorder_segment
                    ),
                    ft.Colors.GREY_500,
                ),
            ],
            spacing=8,
            wrap=False,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        segment_responsive = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Text("Segment ID:", size=12, weight=ft.FontWeight.W_500, width=100),
                    col={"xs": 12, "md": 2},
                    alignment=ft.alignment.center_left,
                    padding=0
                ),
                ft.Container(
                    content=self.segment_dropdown,
                    col={"xs": 12, "md": 3},
                ),
                ft.Container(
                    content=buttons_row,
                    col={"xs": 12, "md": 7},
                    alignment=ft.alignment.center_left,
                ),
            ],
            columns=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.region_assign_dropdown = ft.Dropdown(
            value="0", options=[ft.dropdown.Option("0")],
            hint_text="Region Assign", expand=True,
            on_change=self._on_region_assign_change
        )

        region_row = ft.Row(
            [
                ft.Text("Region Assign:", size=12, weight=ft.FontWeight.W_500, width=100),
                self.region_assign_dropdown,
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Column([segment_responsive, region_row], spacing=10)

    def _on_region_assign_change(self, e):
        self.action_handler.assign_region_to_segment(
            self.segment_dropdown.value, e.control.value
        )

    def update_segments(self, segments_list):
        self.segment_dropdown.options = [ft.dropdown.Option(str(x)) for x in segments_list]
        if segments_list and (self.segment_dropdown.value not in [str(s) for s in segments_list]):
            self.segment_dropdown.value = str(segments_list[0])
        self.update()

    def update_regions(self, regions_list):
        self.region_assign_dropdown.options = [ft.dropdown.Option(str(x)) for x in regions_list]
        if regions_list and (self.region_assign_dropdown.value not in [str(r) for r in regions_list]):
            self.region_assign_dropdown.value = str(regions_list[0])
        self.update()

    def get_selected_segment(self):
        return self.segment_dropdown.value

    def get_assigned_region(self):
        return self.region_assign_dropdown.value
