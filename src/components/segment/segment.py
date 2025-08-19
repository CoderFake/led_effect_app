"""
Segment UI component
Path: src/components/segment/segment.py
"""

import flet as ft
from .segment_action import SegmentActionHandler


class SegmentComponent(ft.Container):
    """Segment UI component with controls"""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.action_handler = SegmentActionHandler(page)
        self.content = self.build_content()
        
    def build_content(self):
        """Build Segment ID controls"""
        
        self.segment_dropdown = ft.Dropdown(
            label="Segment ID",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True
        )
        
        segment_buttons = ft.Row([
            ft.IconButton(
                icon=ft.Icons.ADD, 
                tooltip="Add Segment", 
                on_click=self.action_handler.add_segment
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE, 
                tooltip="Delete Segment", 
                on_click=self.action_handler.delete_segment
            ),
            ft.IconButton(
                icon=ft.Icons.COPY, 
                tooltip="Copy Segment", 
                on_click=self.action_handler.copy_segment
            ),
            ft.IconButton(
                icon=ft.Icons.VISIBILITY, 
                tooltip="Solo", 
                on_click=self.action_handler.solo_segment
            ),
            ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF, 
                tooltip="Mute", 
                on_click=self.action_handler.mute_segment
            )
        ], wrap=True, tight=True)
        
        self.region_assign_dropdown = ft.Dropdown(
            label="Region Assign",
            value="0",
            options=[ft.dropdown.Option("0")],
            expand=True,
            on_change=self._on_region_assign_change
        )
        
        return ft.Column([
            ft.Row([
                ft.Text("Segment ID:", size=12, weight=ft.FontWeight.W_500, width=80),
                self.segment_dropdown,
                segment_buttons
            ], spacing=5),
            ft.Row([
                ft.Text("Region Assign:", size=12, weight=ft.FontWeight.W_500, width=100),
                self.region_assign_dropdown
            ], spacing=5)
        ], spacing=8)
        
    def _on_region_assign_change(self, e):
        """Handle region assignment change"""
        self.action_handler.assign_region_to_segment(
            self.segment_dropdown.value,
            e.control.value
        )
        
    def update_segments(self, segments_list):
        """Update segment dropdown options"""
        self.segment_dropdown.options = [
            ft.dropdown.Option(str(segment_id)) for segment_id in segments_list
        ]
        self.update()
        
    def update_regions(self, regions_list):
        """Update region assignment dropdown"""
        self.region_assign_dropdown.options = [
            ft.dropdown.Option(str(region_id)) for region_id in regions_list
        ]
        self.update()
        
    def get_selected_segment(self):
        """Get currently selected segment ID"""
        return self.segment_dropdown.value
        
    def get_assigned_region(self):
        """Get currently assigned region ID"""
        return self.region_assign_dropdown.value