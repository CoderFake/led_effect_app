import flet as ft
from .dimmer_action import DimmerActionHandler


class DimmerComponent(ft.Container):
    """Dimmer sequence management component"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = DimmerActionHandler(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build Dimmer Sequence controls"""
        
        self.dimmer_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Index", size=11)),
                ft.DataColumn(ft.Text("Duration(ms)", size=11)),
                ft.DataColumn(ft.Text("Ini. Brightness", size=11)),
                ft.DataColumn(ft.Text("Fin. Brightness", size=11))
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
        
        right_controls = self._build_dimmer_controls()
        
        main_row = ft.Row([
            ft.Container(
                content=self.dimmer_table,
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
        
        return ft.Column([
            ft.Text("Dimmer Sequence", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Container(height=8),
            main_row
        ], spacing=0)
        
    def _build_dimmer_controls(self):
        """Build dimmer control inputs"""
        
        self.duration_field = ft.TextField(
            value="0",
            width=80,
            height=35,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400
        )
        
        self.initial_brightness_field = ft.TextField(
            value="0",
            width=60,
            height=30,
            text_size=11,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400
        )
        
        self.final_brightness_field = ft.TextField(
            value="0",
            width=60,
            height=30,
            text_size=11,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400
        )
        
        return ft.Column([
            ft.Text("Duration", size=12, weight=ft.FontWeight.W_500),
            self.duration_field,
            ft.Text("Brightness", size=12, weight=ft.FontWeight.W_500),
            ft.Row([
                ft.Column([
                    ft.Text("Initial:", size=10),
                    self.initial_brightness_field
                ], spacing=2),
                ft.Column([
                    ft.Text("Final:", size=10),
                    self.final_brightness_field
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
        
    def _add_dimmer(self, e):
        """Handle add dimmer button click"""
        duration = self.duration_field.value
        initial = self.initial_brightness_field.value
        final = self.final_brightness_field.value
        
        self.action_handler.add_dimmer_element(duration, initial, final)
        
    def _delete_dimmer(self, e):
        """Handle delete dimmer button click"""
        self.action_handler.delete_dimmer_element()
        
    def update_dimmer_table(self, dimmer_data):
        """Update dimmer table with new data"""
        rows = []
        for i, (duration, initial, final) in enumerate(dimmer_data):
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(i), size=11)),
                ft.DataCell(ft.Text(str(duration), size=11)),
                ft.DataCell(ft.Text(str(initial), size=11)),
                ft.DataCell(ft.Text(str(final), size=11))
            ]))
        
        self.dimmer_table.rows = rows
        self.update()
        
    def get_dimmer_input_values(self):
        """Get current input field values"""
        return {
            'duration': self.duration_field.value,
            'initial_brightness': self.initial_brightness_field.value,
            'final_brightness': self.final_brightness_field.value
        }
        
    def clear_input_fields(self):
        """Clear input fields after adding dimmer"""
        self.duration_field.value = "0"
        self.initial_brightness_field.value = "0"
        self.final_brightness_field.value = "0"
        self.update()