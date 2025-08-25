import flet as ft
import flet_datatable2 as fdt
from .dimmer_action import DimmerActionHandler
from services.data_cache import data_cache


class DimmerComponent(ft.Container):
    """
    Dimmer sequence component
    """

    def __init__(self, page: ft.Page, button_variant: str = "text_icon"):
        super().__init__()
        self.page = page
        self.action_handler = DimmerActionHandler(page)
        self.button_variant = button_variant
        self.dimmer_data = []
        self.selected_row_index = None
        self.is_editing = False
        self.content = self.build_content()
        self.expand = True

    def build_content(self):
        # === TABLE ===========================================================
        self.data_table = fdt.DataTable2(
            columns=[
                fdt.DataColumn2(
                    label=ft.Container(
                        content=ft.Text("Index", size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                fdt.DataColumn2(
                    label=ft.Container(
                        content=ft.Text("Duration(ms)", size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                fdt.DataColumn2(
                    label=ft.Container(
                        content=ft.Text("Ini. Transparency", size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
                fdt.DataColumn2(
                    label=ft.Container(
                        content=ft.Text("Fin. Transparency", size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ),
            ],
            rows=[],
            heading_row_color=ft.Colors.GREY_100,
            column_spacing=10,
            horizontal_margin=5,
            show_bottom_border=False,
            data_text_style=ft.TextStyle(size=11, color=ft.Colors.BLACK),
            heading_text_style=ft.TextStyle(size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
            fixed_top_rows=1,
            divider_thickness=0.5,
            expand=False,
            show_checkbox_column=False,
        )

        self._load_initial_data()

        table_container = ft.Container(
            content=self.data_table,
            height=300,              
            padding=ft.padding.all(5),
            expand=True,              
        )

        right_controls = self._build_dimmer_controls()
        
        main_responsive = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=table_container,
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 8, "xl": 8},
                    expand=True,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    border_radius=ft.border_radius.all(8),
                ),
                ft.Container(
                    content=right_controls,
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 4, "xl": 4},
                    expand=False,
                ),
            ],
            spacing=10,
            run_spacing=10,
            expand=True,
        )

        return ft.Column(
            controls=[
                ft.Text("Dimmer Sequence", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Container(height=8),
                ft.Container(content=main_responsive, expand=True),
            ],
            spacing=0,
            expand=True,
        )

    # ----------------------------------------------------------------------

    def _load_initial_data(self):
        """Load initial dimmer data from cache or use default"""
        try:
            # Try to load data from cache first
            if data_cache.is_loaded and data_cache.current_scene_id is not None:
                scene = data_cache.get_scene(data_cache.current_scene_id)
                if scene and scene.effects and data_cache.current_effect_id is not None:
                    effect = scene.get_effect(data_cache.current_effect_id)
                    if effect and effect.segments:
                        # Get first segment's dimmer_time data
                        first_segment = next(iter(effect.segments.values()))
                        if hasattr(first_segment, 'dimmer_time') and first_segment.dimmer_time:
                            self.dimmer_data = []
                            for dimmer_entry in first_segment.dimmer_time:
                                if len(dimmer_entry) >= 3:
                                    self.dimmer_data.append({
                                        "duration": dimmer_entry[0],
                                        "initial": dimmer_entry[1], 
                                        "final": dimmer_entry[2]
                                    })
                            
                            if self.dimmer_data:
                                self._build_initial_table_rows()
                                return
            
            self._load_fallback_data()
            
        except Exception as e:
            print(f"Error loading initial data: {e}")
            self._load_fallback_data()
    
    def _load_fallback_data(self):
        """Load fallback default data if cache fails"""
        self.dimmer_data = [
            {"duration": 1000, "initial": 0, "final": 100},
            {"duration": 1000, "initial": 100, "final": 0},
        ]
        self._build_initial_table_rows()

    def _build_initial_table_rows(self):
        """Build initial table rows without calling update"""
        rows = []
        for i, item in enumerate(self.dimmer_data):
            def create_row_handler(index):
                return lambda e: self._on_row_click(index)
            
            row = fdt.DataRow2(
                cells=[
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(i), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(item["duration"]), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(item["initial"]), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(item["final"]), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                ],
                color=ft.Colors.BLUE_50 if self.selected_row_index == i else None,
            )
            rows.append(row)
        
        self.data_table.rows = rows

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
            on_blur=self._on_field_unfocus,
        )

        duration_section = ft.Row(
            [ft.Text("Duration:", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK), self.duration_field],
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
            on_blur=self._on_field_unfocus,
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
            on_blur=self._on_field_unfocus,
        )

        self.transparency_row = ft.ResponsiveRow(
            controls=[
                ft.Container(content=self.initial_transparency_field, col={"xs": 12, "sm": 12, "md": 12, "lg": 6}),
                ft.Container(content=self.final_transparency_field, col={"xs": 12, "sm": 12, "md": 12, "lg": 6}),
            ],
            spacing=10,
            run_spacing=5,
        )

        transparency_section = ft.Column(
            [ft.Text("Transparency", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLACK),
             ft.Container(height=5),
             self.transparency_row]
        )

        add_btn = self._make_button(
            label="Add", icon=ft.Icons.ADD, on_click=self._add_dimmer, color=ft.Colors.PRIMARY, outlined=True
        )
        del_btn = self._make_button(
            label="Delete", icon=ft.Icons.DELETE, on_click=self._delete_dimmer, color=ft.Colors.RED_500, outlined=True
        )

        button_column = ft.Column(
            controls=[add_btn, del_btn],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        return ft.Container(
            content=ft.Column(
                controls=[duration_section, ft.Container(height=10), transparency_section, ft.Container(height=10), button_column],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                tight=True,
            ),
            padding=ft.padding.all(15),
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=ft.border_radius.all(8),
            bgcolor=ft.Colors.GREY_50,
            width=280 if self.page.width and self.page.width >= 1024 else None,
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

    # ----------------------------------------------------------------------

    def _add_dimmer(self, e):
        duration = self.duration_field.value
        ini = self.initial_transparency_field.value
        fin = self.final_transparency_field.value
        
        print(f"Adding dimmer: duration={duration}, initial={ini}, final={fin}")
        print(f"Current dimmer_data type: {type(self.dimmer_data)}")
        print(f"Current dimmer_data: {self.dimmer_data}")
        
        if self.action_handler.add_dimmer_element(duration, ini, fin, self.dimmer_data):
            print(f"After add, dimmer_data: {self.dimmer_data}")
            self._refresh_table()
            self.clear_input_fields()

    def _delete_dimmer(self, e):
        if self.selected_row_index is not None:
            if self.action_handler.delete_dimmer_element(self.selected_row_index, self.dimmer_data):
                self._refresh_table()
                self.clear_input_fields()
                self.selected_row_index = None
        else:
            self.action_handler.toast_manager.show_warning_sync("Please select a row to delete")

    def _on_field_unfocus(self, e):
        """Handle auto-save when field loses focus"""
        if self.selected_row_index is not None and self.is_editing:
            duration = self.duration_field.value
            initial = self.initial_transparency_field.value
            final = self.final_transparency_field.value
            
            if self.action_handler.update_dimmer_element(
                self.selected_row_index, duration, initial, final, self.dimmer_data
            ):
                self._refresh_table()
                self.is_editing = False

    def _refresh_table(self):
        """Refresh the data table with current dimmer data"""
        rows = []
        for i, item in enumerate(self.dimmer_data):
            def create_row_handler(index):
                return lambda e: self._on_row_click(index)
            
            if isinstance(item, dict):
                duration = item.get("duration", 0)
                initial = item.get("initial", 0)
                final = item.get("final", 0)
            elif isinstance(item, (list, tuple)) and len(item) >= 3:
                duration, initial, final = item[0], item[1], item[2]
            
            row = fdt.DataRow2(
                cells=[
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(i), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(duration), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(initial), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(final), size=11, color=ft.Colors.BLACK, no_wrap=False),
                            alignment=ft.alignment.center,
                            padding=ft.padding.all(5),
                        ),
                        on_tap=create_row_handler(i),
                    ),
                ],
                color=ft.Colors.BLUE_50 if self.selected_row_index == i else None,
            )
            rows.append(row)
        
        self.data_table.rows = rows
        try:
            if hasattr(self.data_table, 'page') and self.data_table.page is not None:
                self.data_table.update()
        except Exception as e:
            pass
        
        self._sync_to_cache()

    def _sync_to_cache(self):
        """Sync current dimmer data back to cache"""
        try:
            if data_cache.is_loaded and data_cache.current_scene_id is not None:
                scene = data_cache.get_scene(data_cache.current_scene_id)
                if scene and scene.effects and data_cache.current_effect_id is not None:
                    effect = scene.get_effect(data_cache.current_effect_id)
                    if effect and effect.segments:
                        first_segment = next(iter(effect.segments.values()))
                        if hasattr(first_segment, 'dimmer_time'):
                            dimmer_time_data = []
                            for item in self.dimmer_data:
                                if isinstance(item, dict):
                                    duration = item.get("duration", 0)
                                    initial = item.get("initial", 0)
                                    final = item.get("final", 0)
                                elif isinstance(item, (list, tuple)) and len(item) >= 3:
                                    duration, initial, final = item[0], item[1], item[2]
                            
                                dimmer_time_data.append([duration, initial, final])
                            first_segment.dimmer_time = dimmer_time_data
        except Exception as e:
            print(f"Error syncing to cache: {e}")

    def update_dimmer_table(self, dimmer_data):
        """Update table with external dimmer data"""
        self.dimmer_data = dimmer_data
        self._refresh_table()

    def _on_row_click(self, row_index):
        """Handle row click and populate right controls"""
        
        if self.selected_row_index == row_index:
            self.selected_row_index = None
            self.is_editing = False
        else:
            self.selected_row_index = row_index
            self.is_editing = True
            
            if 0 <= row_index < len(self.dimmer_data):
                item = self.dimmer_data[row_index]
                if isinstance(item, dict):
                    self.duration_field.value = str(item.get("duration", ""))
                    self.initial_transparency_field.value = str(item.get("initial", ""))
                    self.final_transparency_field.value = str(item.get("final", ""))
                elif isinstance(item, (list, tuple)) and len(item) >= 3:
                    self.duration_field.value = str(item[0])
                    self.initial_transparency_field.value = str(item[1])
                    self.final_transparency_field.value = str(item[2])
                else:
                    self.duration_field.value = ""
                    self.initial_transparency_field.value = ""
                    self.final_transparency_field.value = ""
                
                try:
                    if hasattr(self.duration_field, 'page') and self.duration_field.page is not None:
                        self.duration_field.update()
                        self.initial_transparency_field.update()
                        self.final_transparency_field.update()
                except Exception as ex:
                    print(f"Error updating fields: {ex}")
                
        self._refresh_table()

    def _on_row_select(self, e, row_index):
        """Handle row selection and populate right controls - DEPRECATED, use _on_row_click"""
        
        if getattr(e.control, "selected", False):
            self.selected_row_index = row_index
            self.is_editing = True
            
            if 0 <= row_index < len(self.dimmer_data):
                item = self.dimmer_data[row_index]
                
                self.duration_field.value = str(item["duration"])
                self.initial_transparency_field.value = str(item["initial"])
                self.final_transparency_field.value = str(item["final"])
                
                try:
                    if hasattr(self.duration_field, 'page') and self.duration_field.page is not None:
                        self.duration_field.update()
                        self.initial_transparency_field.update()
                        self.final_transparency_field.update()
                except Exception as ex:
                    print(f"Error updating fields: {ex}")
                
                self._refresh_table()
        else:
            if self.selected_row_index == row_index:
                self.selected_row_index = None
                self.is_editing = False
                self._refresh_table()

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
        try:
            if hasattr(self.duration_field, 'page') and self.duration_field.page is not None:
                self.duration_field.update()
                self.initial_transparency_field.update()
                self.final_transparency_field.update()
        except:
            pass
