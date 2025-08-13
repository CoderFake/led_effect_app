
import flet as ft
from components.menu_bar import MenuBarComponent
from components.scene_effect_panel import SceneEffectPanel
from components.segment_edit import SegmentEditPanel


class LightPatternApp(ft.Container):
    """Main application container"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.content = self.build_content()
        
    def build_content(self):
        """Build the main application layout"""
        
        # Create main components
        self.menu_bar = MenuBarComponent(self.page)
        self.scene_effect_panel = SceneEffectPanel(self.page)
        self.segment_edit_panel = SegmentEditPanel(self.page)
        
        # Main layout: responsive row with two columns
        main_content = ft.ResponsiveRow([
            # Left column: Scene/Effect controls
            ft.Container(
                content=self.scene_effect_panel,
                col={"sm": 12, "md": 6, "lg": 5},
                padding=10
            ),
            # Right column: Segment Edit
            ft.Container(
                content=self.segment_edit_panel,
                col={"sm": 12, "md": 6, "lg": 7},
                padding=10
            )
        ])
        
        return ft.Column([
            # Menu bar at top
            self.menu_bar,
            # Divider
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            # Main content
            ft.Container(
                content=main_content,
                expand=True,
                padding=0
            )
        ],
        spacing=0,
        expand=True
        )