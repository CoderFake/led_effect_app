import flet as ft
from .dimmer_action import DimmerActionHandler


class DimmerComponent(ft.Container):
    """
    Responsive dimmer sequence component using Flet DataTable
    Supports icon-only or icon+text buttons and full-width controls
    """

    def __init__(self, page: ft.Page, button_variant: str = "text_icon"):
        super().__init__()
        self.page = page
        self.action_handler = DimmerActionHandler(page)
        self.button_variant = button_variant
        self.content = self.build_content()
        self.expand = True

    def build_content(self):
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text("Index", size=11, weight=ft.FontWeight.W_600),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text("Duration(ms)", size=11, weight=ft.FontWeight.W_600),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text("Ini. Transparency", size=11, weight=ft.FontWeight.W_600),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text("Fin. Transparency", size=11, weight=ft.FontWeight.W_600),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
            ],
            rows=[],
            expand=True,
            heading_row_color=ft.Colors.GREY_100,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            data_row_max_height=float("inf"),
            data_row_min_height=35,
            column_spacing=20,
            horizontal_margin=10,
            show_bottom_border=True,
            data_text_style=ft.TextStyle(size=11),
            heading_text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_600),
        )

        self._load_initial_data()

        table_container = ft.Container(
            content=ft.Column(
                controls=[self.data_table],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=ft.padding.all(5),
        )

        right_controls = self._build_dimmer_controls()

        main_responsive = ft.ResponsiveRow(
            controls=[
                ft.Container(content=table_container, col={"xs": 12, "sm": 12, "md": 8, "lg": 8}),
                ft.Container(content=right_controls, col={"xs": 12, "sm": 12, "md": 4, "lg": 4}),
            ],
            spacing=10,
            run_spacing=10,
        )

        return ft.Column(
            controls=[
                ft.Text("Dimmer Sequence", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                main_responsive,
            ],
            spacing=0,
            expand=True,
        )

    def _load_initial_data(self):
        initial_data = [
            (0, 1000, 0, 100),
            (1, 1000, 100, 0),
        ]
        self.data_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(content=ft.Text(str(idx), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(duration), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(ini), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(fin), size=11), alignment=ft.alignment.center)),
                ]
            )
            for idx, duration, ini, fin in initial_data
        ]

    def _build_dimmer_controls(self):
        self.duration_field = ft.TextField(
            label="ms",
            value="0",
            height=50,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            expand=True,
        )

        duration_section = ft.Row(
            [ft.Text("Duration:", size=12, weight=ft.FontWeight.W_500), self.duration_field],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.initial_transparency_field = ft.TextField(
            label="Initial",
            value="0",
            height=50,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            expand=True,
        )

        self.final_transparency_field = ft.TextField(
            label="Final",
            value="0",
            height=50,
            text_size=12,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.GREY_400,
            expand=True,
        )

        self.transparency_row = ft.ResponsiveRow(
            controls=[
                ft.Container(content=self.initial_transparency_field, col={"xs": 12, "sm": 6}),
                ft.Container(content=self.final_transparency_field, col={"xs": 12, "sm": 6}),
            ],
            spacing=10,
        )

        transparency_section = ft.Column(
            [ft.Text("Transparency", size=12, weight=ft.FontWeight.W_500), ft.Container(height=5), self.transparency_row]
        )

        add_btn = self._make_button(
            label="Add",
            icon=ft.Icons.ADD,
            on_click=self._add_dimmer,
            color=ft.Colors.PRIMARY,
            outlined=True,
        )
        del_btn = self._make_button(
            label="Delete",
            icon=ft.Icons.DELETE,
            on_click=self._delete_dimmer,
            color=ft.Colors.RED_500,
            outlined=True,
        )

        button_column = ft.Column(
            controls=[add_btn, del_btn],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    duration_section,
                    ft.Container(height=10),
                    transparency_section,
                    ft.Container(height=10),
                    button_column,
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                tight=True,
            ),
            padding=ft.padding.all(15),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=ft.border_radius.all(8),
            bgcolor=ft.Colors.GREY_50,
        )

    def _make_button(self, label: str, icon, on_click, color, outlined: bool = True):
        if self.button_variant == "icon_only":
            return ft.OutlinedButton(
                icon=icon,
                text="",
                on_click=on_click,
                height=44,
                expand=True,
                style=ft.ButtonStyle(
                    color=color,
                    bgcolor=None,
                    side=ft.BorderSide(1, color),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    alignment=ft.alignment.center,
                ),
            )
        if outlined:
            return ft.OutlinedButton(
                text=label,
                icon=icon,
                on_click=on_click,
                height=44,
                expand=True,
                style=ft.ButtonStyle(
                    color=color,           
                    bgcolor=None,          
                    side=ft.BorderSide(1, color),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    alignment=ft.alignment.center,
                ),
            )
        return ft.TextButton(
            text=label,
            icon=icon,
            on_click=on_click,
            height=44,
            expand=True,
            style=ft.ButtonStyle(
                color=ft.Colors.BLACK,
                bgcolor=None,
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                alignment=ft.alignment.center,
            ),
        )

    def _add_dimmer(self, e):
        duration = self.duration_field.value
        ini = self.initial_transparency_field.value
        fin = self.final_transparency_field.value
        self.action_handler.add_dimmer_element(duration, ini, fin)

    def _delete_dimmer(self, e):
        self.action_handler.delete_dimmer_element()

    def update_dimmer_table(self, dimmer_data):
        self.data_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(content=ft.Text(str(i), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(duration), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(initial), size=11), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=ft.Text(str(final), size=11), alignment=ft.alignment.center)),
                ],
                on_select_changed=lambda e, idx=i: self._on_row_select(e, idx),
            )
            for i, (duration, initial, final) in enumerate(dimmer_data)
        ]
        self.data_table.update()

    def _on_row_select(self, e, row_index):
        if e.control.selected:
            print(f"Selected row {row_index}")

    def get_dimmer_input_values(self):
        return {
            "duration": self.duration_field.value,
            "initial_transparency": self.initial_transparency_field.value,
            "final_transparency": self.final_transparency_field.value,
        }

    def clear_input_fields(self):
        self.duration_field.value = "0"
        self.initial_transparency_field.value = "0"
        self.final_transparency_field.value = "0"
        self.update()
