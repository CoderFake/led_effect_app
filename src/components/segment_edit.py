import flet as ft
from components.toast import ToastManager
from services.color_service import color_service
from components.color.color_selection_modal import ColorSelectionModal


class SegmentEditPanel(ft.Container):
    """Right panel for segment editing"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.toast_manager = ToastManager(page)
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build segment edit panel"""
        
        segment_id_section = self._build_segment_id_section()
        color_composition_section = self._build_color_composition_section()
        move_section = self._build_move_section()
        dimmer_sequence_section = self._build_dimmer_sequence_section()
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Segment Edit", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Container(height=15),
                segment_id_section,
                ft.Container(height=15),
                color_composition_section,
                ft.Container(height=15), 
                move_section,
                ft.Container(height=15),
                dimmer_sequence_section
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
        
    def _build_segment_id_section(self):
        """Build Segment ID controls"""
        
        segment_dropdown = ft.Dropdown(
            label="Segment ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        segment_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Segment", on_click=self._add_segment),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Segment", on_click=self._delete_segment),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Segment", on_click=self._copy_segment),
            ft.IconButton(icon=ft.Icons.VISIBILITY, tooltip="Solo", on_click=self._solo_segment),
            ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, tooltip="Mute", on_click=self._mute_segment)
        ], wrap=True, tight=True)
        
        region_assign_dropdown = ft.Dropdown(
            label="Region Assign",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Segment ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                    segment_dropdown,
                    segment_buttons
                ], spacing=5),
                ft.Row([
                    ft.Text("Region Assign:", size=12, weight=ft.FontWeight.W_500, width=100),
                    region_assign_dropdown
                ], spacing=5)
            ], spacing=8),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300)
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
            slot_column = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(str(i), size=12, text_align=ft.TextAlign.CENTER),
                        height=30
                    ),
                    ft.Container(
                        width=80,
                        height=35,
                        bgcolor=colors[i],
                        border=ft.border.all(1, ft.Colors.GREY_600),
                        border_radius=4,
                        on_click=lambda e, idx=i: self._select_color(idx),
                        tooltip=f"Color {i}"
                    ),
                    ft.Container(
                        content=ft.Stack([
                            ft.Container(
                                content=ft.TextField(
                                    value="1.0",
                                    width=80,
                                    height=25,
                                    text_size=11,
                                    text_align=ft.TextAlign.CENTER,
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    border_color=ft.Colors.GREY_400,
                                    content_padding=ft.padding.all(1)
                                ),
                                top=0,
                                left=0
                            ),
                            ft.Container(
                                content=ft.Container(
                                    content=ft.Slider(
                                        min=0,
                                        max=1,
                                        value=1.0,
                                        width=80,
                                        height=120,
                                        thumb_color=ft.Colors.BLUE,
                                        active_color=ft.Colors.BLUE_300,
                                        inactive_color=ft.Colors.GREY_300,
                                        on_change=lambda e, idx=i: self._on_transparency_change(idx, e.control.value)
                                    ),
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
                    ft.TextField(
                        value="10",
                        width=80,
                        height=35,
                        text_size=11,
                        text_align=ft.TextAlign.CENTER,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        border_color=ft.Colors.GREY_400,
                        content_padding=ft.padding.all(3)
                    )
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=80
            )
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
        
    def _build_move_section(self):
        """Build Move controls"""
        
        move_range_row = ft.Row([
            ft.Text("Move Range:", size=12, weight=ft.FontWeight.W_500, width=100),
            ft.TextField(
                value="0",
                width=60,
                height=35,
                text_size=12,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400
            ),
            ft.Text("~", size=12, width=20, text_align=ft.TextAlign.CENTER),
            ft.TextField(
                value="100",
                width=60,
                height=35,
                text_size=12,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400
            ),
            ft.Text("Move Speed:", size=12, weight=ft.FontWeight.W_500, width=80),
            ft.TextField(
                value="1.0",
                width=60,
                height=35,
                text_size=12,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400
            ),
            ft.Container(
                content=ft.Slider(
                    min=0,
                    max=10,
                    value=1.0,
                    width=100,
                    height=35,
                    thumb_color=ft.Colors.BLUE,
                    active_color=ft.Colors.BLUE_300,
                    inactive_color=ft.Colors.GREY_300
                ),
                width=100
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.START)
        
        position_row = ft.Row([
            ft.Text("Initial Position:", size=12, weight=ft.FontWeight.W_500, width=100),
            ft.TextField(
                value="10",
                width=60,
                height=35,
                text_size=12,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400
            ),
            ft.Text("Edge Reflect:", size=12, weight=ft.FontWeight.W_500, width=100),
            ft.Dropdown(
                value="v",
                options=[
                    ft.dropdown.Option("v"),
                    ft.dropdown.Option("bounce"),
                    ft.dropdown.Option("wrap")
                ],
                width=80,
                text_size=12
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.START)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Move", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                move_range_row,
                ft.Container(height=8),
                position_row
            ], spacing=0),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
    def _build_dimmer_sequence_section(self):
        """Build Dimmer Sequence controls"""
        
        dimmer_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Index", size=11)),
                ft.DataColumn(ft.Text("Duration(ms)", size=11)),
                ft.DataColumn(ft.Text("Ini. Transparency", size=11)),
                ft.DataColumn(ft.Text("Fin. Transparency", size=11))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("0", size=11)),
                    ft.DataCell(ft.Text("1000", size=11)),
                    ft.DataCell(ft.Text("0", size=11)),
                    ft.DataCell(ft.Text("100", size=11))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("1", size=11)),
                    ft.DataCell(ft.Text("1000", size=11)),
                    ft.DataCell(ft.Text("100", size=11)),
                    ft.DataCell(ft.Text("0", size=11))
                ])
            ],
            column_spacing=15,
            data_row_max_height=35
        )
        
        right_controls = ft.Column([
            ft.Text("Duration", size=12, weight=ft.FontWeight.W_500),
            ft.TextField(
                value="0",
                width=80,
                height=35,
                text_size=12,
                text_align=ft.TextAlign.CENTER,
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.GREY_400
            ),
            ft.Text("Transparency", size=12, weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Column([
                    ft.Text("Initial:", size=10),
                    ft.TextField(
                        value="0",
                        width=60,
                        height=30,
                        text_size=11,
                        text_align=ft.TextAlign.CENTER,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        border_color=ft.Colors.GREY_400
                    )
                ], spacing=2),
                ft.Column([
                    ft.Text("Final:", size=10),
                    ft.TextField(
                        value="0",
                        width=60,
                        height=30,
                        text_size=11,
                        text_align=ft.TextAlign.CENTER,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        border_color=ft.Colors.GREY_400
                    )
                ], spacing=2)
            ], spacing=5),
            ft.ElevatedButton(
                "Add", 
                width=80,
                height=30,
                on_click=self._add_dimmer
            ),
            ft.ElevatedButton(
                "Delete", 
                width=80,
                height=30,
                on_click=self._delete_dimmer
            )
        ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        main_row = ft.Row([
            ft.Container(
                content=dimmer_table,
                border=ft.border.all(1, ft.Colors.GREY_400),
                padding=8,
                expand=True
            ),
            ft.Container(
                content=right_controls,
                width=150,
                padding=10
            )
        ], spacing=10)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Dimmer Sequence", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                main_row
            ], spacing=0),
            padding=ft.padding.all(15),
            margin=ft.margin.all(5),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
    
    def _add_segment(self, e):
        self.toast_manager.show_success_sync("Segment added successfully")
        
    def _delete_segment(self, e):
        self.toast_manager.show_warning_sync("Segment deleted")
        
    def _copy_segment(self, e):
        self.toast_manager.show_success_sync("Segment copied")
        
    def _solo_segment(self, e):
        self.toast_manager.show_info_sync("Segment solo mode activated")
        
    def _mute_segment(self, e):
        self.toast_manager.show_info_sync("Segment muted")
        
    def _select_color(self, color_index):
        """Handle color selection for segment - Show Color Selection Modal"""
        def on_color_change(slot_index: int, selected_color_index: int, color: str):
            """Handle color change from modal"""
            self.toast_manager.show_success_sync(
                f"Color Slot {slot_index + 1} set to Color Index {selected_color_index}"
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
            self.toast_manager.show_error_sync(f"Error: {str(e)}")
        
    def _on_transparency_change(self, index, value):
        """Handle transparency slider change"""
        pass
        
    def _add_dimmer(self, e):
        self.toast_manager.show_success_sync("Dimmer sequence added")
        
    def _delete_dimmer(self, e):
        self.toast_manager.show_warning_sync("Dimmer sequence deleted")