import flet as ft
from ..ui.toast import ToastManager


class RegionActionHandler:
    """Handle region-related actions and business logic"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        
    def add_region(self, e):
        """Handle add region action"""
        self.toast_manager.show_success_sync("Region added successfully")
        
    def delete_region(self, e):
        """Handle delete region action"""
        self.toast_manager.show_warning_sync("Region deleted")
        
    def update_region_range(self, region_id: str, start: str, end: str):
        """Handle region range update"""
        try:
            start_val = int(start) if start else 0
            end_val = int(end) if end else 0
            
            if end_val < start_val:
                self.toast_manager.show_warning_sync("End LED must be >= Start LED")
                return False
                
            self.toast_manager.show_info_sync(f"Region {region_id} range updated: {start_val}-{end_val}")
            return True
            
        except ValueError:
            self.toast_manager.show_error_sync("Please enter valid LED numbers")
            return False
            
    def validate_region_overlap(self, regions_data):
        """Validate if regions overlap and warn user"""
        overlaps = []
        for i, region1 in enumerate(regions_data):
            for j, region2 in enumerate(regions_data[i+1:], i+1):
                if self._regions_overlap(region1, region2):
                    overlaps.append((region1['id'], region2['id']))
                    
        if overlaps:
            overlap_text = ", ".join([f"Region {r1} & {r2}" for r1, r2 in overlaps])
            self.toast_manager.show_warning_sync(f"Overlapping regions detected: {overlap_text}")
            
    def _regions_overlap(self, region1, region2):
        """Check if two regions overlap"""
        return not (region1['end'] < region2['start'] or region2['end'] < region1['start'])
        
    def create_region_with_range(self, start: int, end: int):
        """Create new region with specific range"""
        if end < start:
            self.toast_manager.show_error_sync("Invalid range: End must be >= Start")
            return False
            
        self.toast_manager.show_success_sync(f"Region created with range {start}-{end}")
        return True