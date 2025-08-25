import flet as ft
from typing import Dict, Any, Optional
from services.data_cache import data_cache
from services.color_service import color_service
from models.color_palette import ColorPalette
from components.ui.toast import ToastManager
from utils.helpers import safe_component_update
from utils.logger import AppLogger


class DataActionHandler:
    """Action handler to work with data cache and update UI"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.toast_manager = ToastManager(page)
        self.scene_effect_panel = None
        self.segment_edit_panel = None
        data_cache.add_change_listener(self._on_cache_changed)
        self._initialize_ui_with_cache_data()
        
    def _initialize_ui_with_cache_data(self):
        """Initialize UI components with initial cache data"""
        try:
            if data_cache.is_loaded:
                self._update_color_service()
        except Exception as e:
            self.toast_manager.show_error_sync(f"Error initializing UI with cache data: {str(e)}")
        
    def register_panels(self, scene_effect_panel, segment_edit_panel):
        """Register UI panels for updates"""
        self.scene_effect_panel = scene_effect_panel
        self.segment_edit_panel = segment_edit_panel
        self.page.run_task(self._delayed_update_task)
        
    async def _delayed_update_task(self):
        """Delayed update task to ensure components are ready"""
        import asyncio
        await asyncio.sleep(0.2)
        
        try:
            self.update_all_ui_from_cache()
        except Exception as e:
            AppLogger.error(f"Error in UI update: {e}")
        
    def load_json_data(self, json_data: Dict[str, Any]) -> bool:
        """Load JSON data and update UI"""
        try:
            self._set_loading_state(True)
            success = data_cache.load_from_json_data(json_data)
            if success:
                self.update_all_ui_from_cache()
                self.toast_manager.show_success_sync("Loaded JSON data successfully")
            else:
                self.toast_manager.show_error_sync("Failed to load JSON data")
            return success
        except Exception as e:
            self.toast_manager.show_error_sync(f"Error loading JSON data: {str(e)}")
            return False
        finally:
            self._set_loading_state(False)
            
    def load_json_file(self, file_path: str) -> bool:
        """Load JSON file and update UI"""
        try:
            self._set_loading_state(True)
            success = data_cache.load_from_file(file_path)
            if success:
                self.update_all_ui_from_cache()
                self.toast_manager.show_success_sync(f"Loaded file {file_path} successfully")
            else:
                self.toast_manager.show_error_sync(f"Failed to load file {file_path}")
            return success
        except Exception as e:
            self.toast_manager.show_error_sync(f"Error loading file {file_path}: {str(e)}")
            return False
        finally:
            self._set_loading_state(False)
            
    def _set_loading_state(self, is_loading: bool):
        """Set loading state on all action handlers and services"""
        try:
            color_service.set_loading_state(is_loading)
            if self.segment_edit_panel and hasattr(self.segment_edit_panel, 'action_handler'):
                self.segment_edit_panel.action_handler.set_loading_state(is_loading)
        except Exception as e:
            AppLogger.error(f"Error setting loading state: {e}")
            
    def update_all_ui_from_cache(self):
        """Update all UI components from cache data"""
        try:
            if not data_cache.is_loaded:
                self.toast_manager.show_warning_sync("No data loaded in cache")
                return
                
            self._update_scene_effect_panel()
            self._update_segment_edit_panel()
            self._update_color_service()
            
        except Exception as e:
            self.toast_manager.show_error_sync(f"Failed to update UI from cache")
            AppLogger.error(f"Failed to update UI from cache: {str(e)}")
            
    def _update_scene_effect_panel(self):
        """Update Scene/Effect panel with cache data"""
        if not self.scene_effect_panel:
            return
            
        try:
            scene_ids = data_cache.get_scene_ids()
            effect_ids = data_cache.get_effect_ids()
            palette_ids = data_cache.get_palette_ids()
            region_ids = data_cache.get_region_ids()
            
            if hasattr(self.scene_effect_panel, 'update_scenes_list'):
                self.scene_effect_panel.update_scenes_list(scene_ids)
                
            if hasattr(self.scene_effect_panel, 'update_effects_list'):
                self.scene_effect_panel.update_effects_list(effect_ids)

            if hasattr(self.scene_effect_panel, 'update_regions_list'):
                self.scene_effect_panel.update_regions_list(region_ids)

            if hasattr(self.scene_effect_panel, 'color_palette'):
                cp = self.scene_effect_panel.color_palette
                if hasattr(cp, 'update_palette_list'):
                    cp.update_palette_list(palette_ids)

            self._update_scene_settings()
            self._update_scene_selection()
            safe_component_update(self.scene_effect_panel, "scene_effect_panel_update")
                
        except Exception as e:
            self.toast_manager.show_error_sync(f"Failed to update scene/effect panel: {str(e)}")
            AppLogger.error(f"Error updating scene/effect panel: {e}")
            
    def _update_scene_settings(self):
        """Update scene settings (LED count, FPS)"""
        if not self.scene_effect_panel:
            return
            
        try:
            current_scene = data_cache.get_current_scene()
            if current_scene and hasattr(self.scene_effect_panel, 'scene_settings'):
                settings = self.scene_effect_panel.scene_settings
                if hasattr(settings, 'set_scene_data'):
                    settings.set_scene_data({
                        'led_count': current_scene.led_count,
                        'fps': current_scene.fps
                    })
        except Exception as e:
            AppLogger.error(f"Error updating scene settings: {e}")
            
    def _update_scene_selection(self):
        """Update scene/effect selection dropdowns"""
        if not self.scene_effect_panel:
            return
            
        try:
            if hasattr(self.scene_effect_panel, 'scene_effect_selector'):
                selector = self.scene_effect_panel.scene_effect_selector
                
                if hasattr(selector, 'scene_dropdown') and data_cache.current_scene_id:
                    selector.scene_dropdown.value = str(data_cache.current_scene_id)
                    selector.scene_dropdown.update()
                    
                if hasattr(selector, 'effect_dropdown') and data_cache.current_effect_id:
                    selector.effect_dropdown.value = str(data_cache.current_effect_id)
                    selector.effect_dropdown.update()
                    
        except Exception as e:
            AppLogger.error(f"Error updating scene selection: {e}")
                
    def _update_segment_edit_panel(self):
        """Update Segment Edit panel with cache data"""
        if not self.segment_edit_panel:
            return
            
        try:
            segment_ids = data_cache.get_segment_ids()
            region_ids = data_cache.get_region_ids()
            
            if hasattr(self.segment_edit_panel, 'update_segments_list'):
                self.segment_edit_panel.update_segments_list(segment_ids)
                
            if hasattr(self.segment_edit_panel, 'update_regions_list'):
                self.segment_edit_panel.update_regions_list(region_ids)
                
            self._update_segment_data()
            safe_component_update(self.segment_edit_panel, "segment_edit_panel_update")
                
        except Exception as e:
            self.toast_manager.show_error_sync(f"Failed to update segment edit panel: {str(e)}")
            AppLogger.error(f"Error updating segment edit panel: {e}")
            
    def _update_segment_data(self):
        """Update segment data if segment is selected"""
        if not self.segment_edit_panel:
            return
            
        try:
            segment_ids = data_cache.get_segment_ids()
            if segment_ids:
                current_id = color_service.current_segment_id
                selected_id = (
                    current_id
                    if current_id is not None and int(current_id) in segment_ids
                    else str(segment_ids[0])
                )
                segment = data_cache.get_segment(selected_id)

                if segment and hasattr(self.segment_edit_panel, 'segment_component'):
                    self._set_loading_state(True)
                    
                    sc = self.segment_edit_panel.segment_component
                    if hasattr(sc, 'segment_dropdown'):
                        sc.segment_dropdown.value = selected_id
                        sc.segment_dropdown.update()
                    if hasattr(sc, 'region_assign_dropdown'):
                        sc.region_assign_dropdown.value = str(getattr(segment, 'region_id', 0))
                        sc.region_assign_dropdown.update()

                    self._set_loading_state(False)

                color_service.set_current_segment_id(selected_id)
                self._update_move_component(segment)
                self._update_dimmer_component(segment)

                if hasattr(self.segment_edit_panel, 'update_color_composition'):
                    self.segment_edit_panel.update_color_composition()
            else:
                color_service.set_current_segment_id(None)

                if hasattr(self.segment_edit_panel, 'segment_component'):
                    sc = self.segment_edit_panel.segment_component
                    if hasattr(sc, 'segment_dropdown'):
                        sc.segment_dropdown.value = None
                        sc.segment_dropdown.update()
                    if hasattr(sc, 'region_assign_dropdown'):
                        sc.region_assign_dropdown.value = None
                        sc.region_assign_dropdown.update()

                self._update_move_component(None)
                self._update_dimmer_component(None)

                if hasattr(self.segment_edit_panel, 'update_color_composition'):
                    self.segment_edit_panel.update_color_composition()
                    
        except Exception as e:
            AppLogger.error(f"Error updating segment data: {e}")
                
    def _update_move_component(self, segment):
        """Update move component with segment data"""
        if not segment or not hasattr(self.segment_edit_panel, 'move_component'):
            return
            
        try:
            move_component = self.segment_edit_panel.move_component
            
            if hasattr(move_component, 'set_move_parameters'):
                move_params = {
                    'start': segment.move_range[0],
                    'end': segment.move_range[1],
                    'speed': segment.move_speed,
                    'initial_position': segment.initial_position,
                    'edge_reflect': segment.is_edge_reflect
                }
                AppLogger.info(f"Setting move parameters: {move_params}")
                move_component.set_move_parameters(move_params)
                
        except Exception as e:
            AppLogger.error(f"Error updating move component: {e}")
            
    def _update_dimmer_component(self, segment):
        """Update dimmer component with segment data"""
        if not segment or not hasattr(self.segment_edit_panel, 'dimmer_component'):
            return
            
        try:
            dimmer_component = self.segment_edit_panel.dimmer_component

            if hasattr(dimmer_component, 'set_current_segment'):
                dimmer_component.set_current_segment(str(segment.segment_id))
                
        except Exception as e:
            AppLogger.error(f"Error updating dimmer component: {e}")
            
    def _update_color_service(self):
        """Update color service with current cache data"""
        try:
            current_scene = data_cache.get_current_scene()
            if current_scene:
                color_service.set_current_scene_id(current_scene.scene_id)
                
                current_effect = data_cache.get_current_effect()
                if current_effect:
                    color_service.set_current_effect_id(current_effect.effect_id)
                    
                    current_palette = data_cache.get_current_palette()
                    if current_palette:
                        color_service.set_current_palette_id(current_palette.palette_id)
                        color_service.update_palette_cache(current_palette)
                        
        except Exception as e:
            AppLogger.error(f"Error updating color service: {e}")
            
    def _on_cache_changed(self):
        """Handle cache changes"""
        try:
            self.update_all_ui_from_cache()
        except Exception as e:
            AppLogger.error(f"Error handling cache change: {e}")
            
    def export_current_data(self) -> Dict[str, Any]:
        """Export current cache data"""
        try:
            return data_cache.export_to_dict()
        except Exception as e:
            self.toast_manager.show_error_sync(f"Failed to export data: {str(e)}")
            return {}
            
    def _update_color_service(self):
        """Update color service with current cache data"""
        try:
            current_scene = data_cache.get_current_scene()
            if current_scene:
                color_service.set_current_scene_id(current_scene.scene_id)
                
                current_effect = data_cache.get_current_effect()
                if current_effect:
                    color_service.set_current_effect_id(current_effect.effect_id)
                    
                    # Get current palette as RGB array
                    current_palette = data_cache.get_current_palette()
                    if current_palette:
                        color_service.set_current_palette_id(data_cache.current_palette_id)
                        color_service.update_palette_cache(current_palette)
                        
        except Exception as e:
            AppLogger.error(f"Error updating color service: {e}")
            
    def get_cache_status(self) -> Dict[str, Any]:
        """Get current cache status for integrity check"""
        try:
            return {
                'is_loaded': data_cache.is_loaded,
                'scene_count': len(data_cache.scenes),
                'current_scene_id': data_cache.current_scene_id,
                'current_effect_id': data_cache.current_effect_id,
                'current_palette_id': data_cache.current_palette_id
            }
        except Exception as e:
            AppLogger.error(f"Error getting cache status: {e}")
    def get_cache_status(self) -> Dict[str, Any]:
        """Get current cache status for integrity check"""
        try:
            return {
                'is_loaded': data_cache.is_loaded,
                'scene_count': len(data_cache.scenes),
                'current_scene_id': data_cache.current_scene_id,
                'current_effect_id': data_cache.current_effect_id,
                'current_palette_id': data_cache.current_palette_id
            }
        except Exception as e:
            AppLogger.error(f"Error getting cache status: {e}")
            return {'is_loaded': False}