import flet as ft


class SegmentEditPanel(ft.Container):
    """Right panel for segment editing"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build segment edit panel"""

        segment_id_section = self._build_segment_id_section()
        color_composition_section = self._build_color_composition_section()
        move_section = self._build_move_section()
        dimmer_sequence_section = self._build_dimmer_sequence_section()
        
        return ft.Column([
            segment_id_section,
            ft.Divider(),
            color_composition_section,
            ft.Divider(), 
            move_section,
            ft.Divider(),
            dimmer_sequence_section
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
        )
        
    def _build_segment_id_section(self):
        """Build Segment ID controls"""
        
        segment_dropdown = ft.Dropdown(
            label="Segment ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        segment_buttons = ft.Row([
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add Segment", on_click=self._add_segment),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete Segment", on_click=self._delete_segment),
            ft.IconButton(icon=ft.Icons.COPY, tooltip="Copy Segment", on_click=self._copy_segment),
            ft.IconButton(icon=ft.Icons.VISIBILITY, tooltip="Solo", on_click=self._solo_segment),
            ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, tooltip="Mute", on_click=self._mute_segment)
        ])
        
        region_assign_dropdown = ft.Dropdown(
            label="Region Assign",
            value="0",
            options=[ft.dropdown.Option("0")],
            width=150
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Segment Edit", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Row([segment_dropdown, segment_buttons], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
                region_assign_dropdown
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
        
    def _build_color_composition_section(self):
        """Build Color Composition controls"""
        
        # Color slots with transparency and length controls
        color_slots = []
        for i in range(5):
            slot_container = ft.Container(
                content=ft.Column([
                    ft.Text(f"{i}", text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        width=40,
                        height=30,
                        bgcolor=ft.Colors.BLACK if i == 0 else ft.Colors.RED if i == 1 else ft.Colors.YELLOW if i == 2 else ft.Colors.BLUE if i == 3 else ft.Colors.GREEN,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                        border_radius=4,
                        on_click=lambda e, idx=i: self._select_color(idx)
                    ),
                    ft.TextField(
                        value="1.0",
                        width=60,
                        text_size=13,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        label="Trans"
                    ),
                    ft.TextField(
                        value="10", 
                        width=60,
                        text_size=13,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        label="Len"
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5)
            )
            color_slots.append(slot_container)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Color Composition", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Text("Color Select:"),
                ft.Row(color_slots, spacing=10, wrap=True),
                ft.Row([
                    ft.Text("Transparency:"),
                    ft.Text("Length:")
                ])
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
        
    def _build_move_section(self):
        """Build Move controls"""
        
        move_range_start = ft.TextField(
            label="Move Range Start",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        move_range_end = ft.TextField(
            label="End",
            value="100",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        move_speed = ft.TextField(
            label="Move Speed",
            value="1.0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        initial_position = ft.TextField(
            label="Initial Position", 
            value="10",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        edge_reflect = ft.Dropdown(
            label="Edge Reflect",
            value="v",
            options=[ft.dropdown.Option("v")],
            width=100
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Move", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Row([move_range_start, move_range_end]),
                ft.Row([move_speed, initial_position, edge_reflect])
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
        
    def _build_dimmer_sequence_section(self):
        """Build Dimmer Sequence controls"""
        
        # Dimmer list table
        dimmer_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Idx")),
                ft.DataColumn(ft.Text("Duration")),
                ft.DataColumn(ft.Text("Init")),
                ft.DataColumn(ft.Text("Final"))
            ],
            column_spacing=18,
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("0")),
                    ft.DataCell(ft.Text("1000")),
                    ft.DataCell(ft.Text("0")),
                    ft.DataCell(ft.Text("100"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("1")),
                    ft.DataCell(ft.Text("1000")),
                    ft.DataCell(ft.Text("100")),
                    ft.DataCell(ft.Text("0"))
                ])
            ]
        )
        
        # Control fields
        duration_field = ft.TextField(
            label="Duration",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        initial_trans = ft.TextField(
            label="Initial",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        final_trans = ft.TextField(
            label="Final", 
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        add_button = ft.ElevatedButton("Add", on_click=self._add_dimmer)
        delete_button = ft.ElevatedButton("Delete", on_click=self._delete_dimmer)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Dimmer Sequence", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=dimmer_table,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    padding=5
                ),
                ft.Row([duration_field, initial_trans, final_trans]),
                ft.Row([add_button, delete_button])
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8
        )
    
    def _add_segment(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Segment added successfully"))
        )
        
    def _delete_segment(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Segment deleted"))
        )
        
    def _copy_segment(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Segment copied"))
        )
        
    def _solo_segment(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Segment solo mode activated"))
        )
        
    def _mute_segment(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Segment muted"))
        )
        
    def _select_color(self, color_index):
        self.page.open(
            ft.SnackBar(content=ft.Text(f"Color selector for slot {color_index} will be implemented"))
        )
        
    def _add_dimmer(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Dimmer sequence added"))
        )
        
    def _delete_dimmer(self, e):
        self.page.open(
            ft.SnackBar(content=ft.Text("Dimmer sequence deleted"))
        )