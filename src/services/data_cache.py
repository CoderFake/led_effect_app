import json
import copy
from typing import Dict, Any, List, Optional, Callable
from models.scene import Scene
from models.effect import Effect
from models.segment import Segment
from models.region import Region
from utils.logger import AppLogger


class DataCacheService:
    """Centralized data cache service for managing application state"""
    
    def __init__(self):
        self.scenes: Dict[int, Scene] = {}
        self.regions: Dict[int, Region] = {}
        self.current_scene_id: Optional[int] = None
        self.current_effect_id: Optional[int] = None
        self.current_palette_id: Optional[int] = None
        self.is_loaded: bool = False
        self._change_listeners: List[Callable] = []
        self._initialize_default_data()
        
    def _initialize_default_data(self):
        """Initialize with default data structure"""
        try:
            initial_segment = Segment(
                segment_id=0,
                color=[0, 1, 2, 3, 4, 5],
                transparency=[1.0, 0.8, 0.6, 0.4, 0.2, 0.0],
                length=[50, 50, 50, 50, 50],
                move_speed=100.0,
                move_range=[0, 249],
                initial_position=0,
                current_position=0.0,
                is_edge_reflect=True,
                region_id=0,
                dimmer_time=[[1000, 0, 100], [1000, 100, 0]]
            )
            
            default_effect = Effect(effect_id=0)
            default_effect.add_segment(initial_segment)
            
            default_palette = [
                [0, 0, 0],       # Black
                [255, 0, 0],     # Red
                [255, 255, 0],   # Yellow
                [0, 0, 255],     # Blue
                [0, 255, 0],     # Green
                [255, 255, 255]  # White
            ]
            
            default_scene = Scene(
                scene_id=0,
                led_count=250,
                fps=30,
                current_effect_id=0,
                current_palette_id=0,
                palettes=[default_palette],
                effects=[default_effect]
            )
            
            self.scenes[0] = default_scene
            self.current_scene_id = 0
            self.current_effect_id = 0
            self.current_palette_id = 0
            
            self._create_initial_regions()
            self.is_loaded = True
            self._notify_change()
            
        except Exception as e:
            AppLogger.error(f"Error initializing default data: {e}")
            self.is_loaded = False
            
    def _create_initial_regions(self):
        """Create initial regions for LED management"""
        self.regions[0] = Region(
            region_id=0,
            name="Main Region",
            start=0,
            end=249 
        )
        
        self.regions[1] = Region(
            region_id=1,
            name="Front Section",
            start=0,
            end=83
        )
        
        self.regions[2] = Region(
            region_id=2,
            name="Middle Section", 
            start=84,
            end=166 
        )
        
        self.regions[3] = Region(
            region_id=3,
            name="Rear Section",
            start=167,
            end=249
        )
        
    def load_from_json_data(self, json_data: Dict[str, Any]) -> bool:
        """Load data from JSON structure into cache with auto-fix"""
        try:
            self.scenes.clear()
            self.regions.clear()
            
            fixed_json_data = self._auto_fix_json_data(json_data)
            
            for scene_data in fixed_json_data.get('scenes', []):
                scene = Scene.from_dict(scene_data)
                self.scenes[scene.scene_id] = scene
                
            self._create_initial_regions()
            
            if self.scenes:
                first_scene = next(iter(self.scenes.values()))
                self.current_scene_id = first_scene.scene_id
                self.current_effect_id = first_scene.current_effect_id
                self.current_palette_id = first_scene.current_palette_id
                
            self.is_loaded = True
            self._notify_change()
            return True
            
        except Exception as e:
            raise Exception(f"Failed to load JSON data: {str(e)}")
            
    def _auto_fix_json_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-fix JSON data to ensure proper array sizes and valid values"""
        try:
            fixed_data = copy.deepcopy(json_data)
            
            for scene_data in fixed_data.get('scenes', []):
                for effect_data in scene_data.get('effects', []):
                    for segment_id, segment_data in effect_data.get('segments', {}).items():
                        self._fix_segment_arrays(segment_data)
                        
            return fixed_data
            
        except Exception as e:
            AppLogger.warning(f"Could not auto-fix JSON data: {e}")
            return json_data
    
    def _fix_segment_arrays(self, segment_data: Dict[str, Any]):
        """Fix arrays in segment data to ensure proper sizes and valid values"""
        try:
            color_count = len(segment_data.get('color', []))
            transparency = segment_data.get('transparency', [])
            length = segment_data.get('length', [])
            
            if len(transparency) != color_count:
                if len(transparency) < color_count:
                    transparency.extend([1.0] * (color_count - len(transparency)))
                else:
                    transparency = transparency[:color_count]
                segment_data['transparency'] = transparency
                
            expected_length_count = max(0, max(color_count, len(transparency)) - 1)
            if len(length) != expected_length_count:
                if len(length) < expected_length_count:
                    length.extend([10] * (expected_length_count - len(length)))
                else:
                    length = length[:expected_length_count]
                segment_data['length'] = length

            segment_data['length'] = [max(1, val) for val in segment_data['length']]

            if 'region_id' not in segment_data:
                segment_data['region_id'] = 0
                
            AppLogger.info(f"Fixed segment {segment_data.get('segment_id')}: colors={color_count}, transparency={len(transparency)}, length={len(length)}")
            
        except Exception as e:
            AppLogger.error(f"Error fixing segment arrays: {e}")
            
    def load_from_file(self, file_path: str) -> bool:
        """Load data from JSON file into cache"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            return self.load_from_json_data(json_data)
        except Exception as e:
            raise Exception(f"Failed to load file {file_path}: {str(e)}")

    def add_change_listener(self, callback: Callable):
        """Add listener for cache changes"""
        if callback not in self._change_listeners:
            self._change_listeners.append(callback)
            
    def remove_change_listener(self, callback: Callable):
        """Remove change listener"""
        if callback in self._change_listeners:
            self._change_listeners.remove(callback)
            
    def _notify_change(self):
        """Notify all listeners about cache changes"""
        for callback in self._change_listeners[:]:
            try:
                if callable(callback):
                    callback()
                else:
                    self._change_listeners.remove(callback)
            except Exception as e:
                AppLogger.error(f"Error in change callback: {e}")
                if callback in self._change_listeners:
                    self._change_listeners.remove(callback)
                    
    def get_scene_ids(self) -> List[int]:
        """Get all available scene IDs"""
        return sorted(self.scenes.keys())
        
    def get_scene(self, scene_id: int) -> Optional[Scene]:
        """Get scene by ID from cache"""
        return self.scenes.get(scene_id)
        
    def get_current_scene(self) -> Optional[Scene]:
        """Get current active scene from cache"""
        if self.current_scene_id is not None:
            return self.scenes.get(self.current_scene_id)
        return None
        
    def get_effect_ids(self, scene_id: Optional[int] = None) -> List[int]:
        """Get effect IDs for scene"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene:
            return scene.get_effect_ids()
        return []
        
    def get_effect(self, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> Optional[Effect]:
        """Get effect from scene"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene:
            return scene.get_effect(effect_id or self.current_effect_id)
        return None
        
    def get_current_effect(self) -> Optional[Effect]:
        """Get current active effect"""
        return self.get_effect()
        
    def get_palette_ids(self, scene_id: Optional[int] = None) -> List[int]:
        """Get palette IDs for scene"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene:
            return list(range(len(scene.palettes)))
        return []
        
    def get_palette_colors(self, palette_id: Optional[int] = None, scene_id: Optional[int] = None) -> List[str]:
        """Get palette colors as hex strings"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene and 0 <= (palette_id or self.current_palette_id) < len(scene.palettes):
            rgb_colors = scene.palettes[palette_id or self.current_palette_id]
            return [f"#{r:02X}{g:02X}{b:02X}" for r, g, b in rgb_colors]
        return ["#000000", "#FF0000", "#FFFF00", "#0000FF", "#00FF00", "#FFFFFF"]
        
    def get_current_palette(self) -> List[str]:
        """Get current active palette as hex strings"""
        return self.get_palette_colors()
        
    def get_current_palette_colors(self) -> List[str]:
        """Get current palette colors as hex strings"""
        return self.get_palette_colors()
        
    def get_segment_ids(self, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> List[int]:
        """Get segment IDs for effect"""
        effect = self.get_effect(scene_id, effect_id)
        if effect:
            return effect.get_segment_ids()
        return []
        
    def get_segment(self, segment_id: str, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> Optional[Segment]:
        """Get segment from effect"""
        effect = self.get_effect(scene_id, effect_id)
        if effect:
            return effect.get_segment(segment_id)
        return None
        
    def get_region_ids(self) -> List[int]:
        """Get all region IDs"""
        return sorted(self.regions.keys())
        
    def get_region(self, region_id: int) -> Optional[Region]:
        """Get region by ID"""
        return self.regions.get(region_id)

    def create_scene(self, scene_data: Dict[str, Any]) -> Optional[int]:
        """Create new scene"""
        try:
            existing_ids = list(self.scenes.keys())
            new_id = max(existing_ids) + 1 if existing_ids else 0
            
            scene_data['scene_id'] = new_id
            new_scene = Scene.from_dict(scene_data)
            self.scenes[new_id] = new_scene
            
            self._notify_change()
            return new_id
        except Exception as e:
            AppLogger.error(f"Error creating scene: {e}")
            return None
            
    def delete_scene(self, scene_id: int) -> bool:
        """Delete scene"""
        try:
            if scene_id in self.scenes:
                del self.scenes[scene_id]
                if self.current_scene_id == scene_id:
                    remaining_ids = list(self.scenes.keys())
                    self.current_scene_id = remaining_ids[0] if remaining_ids else None
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error deleting scene: {e}")
        return False
        
    def duplicate_scene(self, source_scene_id: int) -> Optional[int]:
        """Duplicate scene"""
        try:
            source_scene = self.get_scene(source_scene_id)
            if source_scene:
                scene_data = source_scene.to_dict()
                return self.create_scene(scene_data)
        except Exception as e:
            AppLogger.error(f"Error duplicating scene: {e}")
        return None
        
    def update_scene(self, scene_id: int, updates: Dict[str, Any]) -> bool:
        """Update scene properties"""
        try:
            scene = self.get_scene(scene_id)
            if scene:
                for key, value in updates.items():
                    if hasattr(scene, key):
                        setattr(scene, key, value)
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error updating scene: {e}")
        return False
        
    def create_effect(self, scene_id: Optional[int] = None) -> Optional[int]:
        """Create new effect in scene"""
        try:
            scene = self.get_scene(scene_id or self.current_scene_id)
            if scene:
                existing_ids = scene.get_effect_ids()
                new_id = max(existing_ids) + 1 if existing_ids else 0
                
                new_effect = Effect(effect_id=new_id)
                scene.effects.append(new_effect)
                
                self._notify_change()
                return new_id
        except Exception as e:
            AppLogger.error(f"Error creating effect: {e}")
        return None
        
    def delete_effect(self, effect_id: int, scene_id: Optional[int] = None) -> bool:
        """Delete effect from scene"""
        try:
            scene = self.get_scene(scene_id or self.current_scene_id)
            if scene:
                success = scene.remove_effect(effect_id)
                if success:
                    if self.current_effect_id == effect_id:
                        remaining_ids = scene.get_effect_ids()
                        self.current_effect_id = remaining_ids[0] if remaining_ids else None
                    self._notify_change()
                return success
        except Exception as e:
            AppLogger.error(f"Error deleting effect: {e}")
        return False
        
    def duplicate_effect(self, source_effect_id: int, scene_id: Optional[int] = None) -> Optional[int]:
        """Duplicate effect in scene"""
        try:
            source_effect = self.get_effect(scene_id, source_effect_id)
            if source_effect:
                scene = self.get_scene(scene_id or self.current_scene_id)
                if scene:
                    existing_ids = scene.get_effect_ids()
                    new_id = max(existing_ids) + 1 if existing_ids else 0
                    
                    effect_data = source_effect.to_dict()
                    effect_data['effect_id'] = new_id
                    
                    new_effect = Effect.from_dict(effect_data)
                    scene.effects.append(new_effect)
                    
                    self._notify_change()
                    return new_id
        except Exception as e:
            AppLogger.error(f"Error duplicating effect: {e}")
        return None
        
    def create_palette(self, palette_data: List[List[int]], scene_id: Optional[int] = None) -> Optional[int]:
        """Create new palette in scene"""
        try:
            scene = self.get_scene(scene_id or self.current_scene_id)
            if scene:
                scene.palettes.append(palette_data)
                new_id = len(scene.palettes) - 1
                self._notify_change()
                return new_id
        except Exception as e:
            AppLogger.error(f"Error creating palette: {e}")
        return None
        
    def delete_palette(self, palette_id: int, scene_id: Optional[int] = None) -> bool:
        """Delete palette from scene"""
        try:
            scene = self.get_scene(scene_id or self.current_scene_id)
            if scene and 0 <= palette_id < len(scene.palettes):
                del scene.palettes[palette_id]
                if self.current_palette_id == palette_id:
                    self.current_palette_id = 0 if scene.palettes else None
                elif self.current_palette_id > palette_id:
                    self.current_palette_id -= 1
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error deleting palette: {e}")
        return False
        
    def duplicate_palette(self, source_palette_id: int, scene_id: Optional[int] = None) -> Optional[int]:
        """Duplicate palette in scene"""
        try:
            source_palette = self.get_palette_colors(source_palette_id, scene_id)
            if source_palette:
                palette_copy = copy.deepcopy(source_palette)
                return self.create_palette(palette_copy, scene_id)
        except Exception as e:
            AppLogger.error(f"Error duplicating palette: {e}")
        return None
        
    def update_palette_color(self, palette_id: int, color_index: int, color: List[int], scene_id: Optional[int] = None) -> bool:
        """Update palette color"""
        try:
            scene = self.get_scene(scene_id or self.current_scene_id)
            if scene and 0 <= palette_id < len(scene.palettes) and 0 <= color_index < len(scene.palettes[palette_id]):
                scene.palettes[palette_id][color_index] = color
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error updating palette color: {e}")
        return False
        
    def create_region(self, region_data: Dict[str, Any]) -> Optional[int]:
        """Create new region"""
        try:
            existing_ids = list(self.regions.keys())
            new_id = max(existing_ids) + 1 if existing_ids else 0
            
            region_data['region_id'] = new_id
            new_region = Region.from_dict(region_data)
            self.regions[new_id] = new_region
            
            self._notify_change()
            return new_id
        except Exception as e:
            AppLogger.error(f"Error creating region: {e}")
        return None
        
    def delete_region(self, region_id: int) -> bool:
        """Delete region"""
        try:
            if region_id in self.regions and region_id != 0:
                del self.regions[region_id]
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error deleting region: {e}")
        return False
        
    def update_region(self, region_id: int, updates: Dict[str, Any]) -> bool:
        """Update region properties"""
        try:
            region = self.get_region(region_id)
            if region:
                for key, value in updates.items():
                    if hasattr(region, key):
                        setattr(region, key, value)
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error updating region: {e}")
        return False
        
    def create_segment(self, scene_id: Optional[int] = None, effect_id: Optional[int] = None, custom_id: Optional[int] = None) -> Optional[int]:
        """Create new segment in effect"""
        effect = self.get_effect(scene_id, effect_id)
        
        if effect:
            existing_ids = effect.get_segment_ids()
            new_id = custom_id if custom_id is not None else (max(existing_ids) + 1 if existing_ids else 0)
            
            if str(new_id) in effect.segments:
                return None
                
            new_segment = Segment(
                segment_id=new_id,
                color=[0, 1, 2],
                transparency=[1.0, 0.8, 0.6],
                length=[10, 15],
                move_speed=100.0,
                move_range=[0, 249],
                initial_position=0,
                current_position=0.0,
                is_edge_reflect=True,
                region_id=0,
                dimmer_time=[[1000, 0, 100], [1000, 100, 0]]
            )

            effect.add_segment(new_segment)
            self._notify_change()
            return new_id

        return None
        
    def delete_segment(self, segment_id: str, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Delete segment from effect"""
        effect = self.get_effect(scene_id, effect_id)
        
        if effect:
            success = effect.remove_segment(segment_id)
            if success:
                self._notify_change()
            return success
        return False
        
    def duplicate_segment(self, source_segment_id: str, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> Optional[int]:
        """Duplicate segment and return new segment ID"""
        effect = self.get_effect(scene_id, effect_id)
        source_segment = self.get_segment(source_segment_id, scene_id, effect_id)
        
        if effect and source_segment:
            existing_ids = effect.get_segment_ids()
            new_id = max(existing_ids) + 1 if existing_ids else 0
            
            segment_data = source_segment.to_dict()
            segment_data['segment_id'] = new_id
            
            new_segment = Segment.from_dict(segment_data)
            effect.add_segment(new_segment)
            
            self._notify_change()
            return new_id
        return None
        
    def reorder_segments(self, segment_order: List[str], scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Reorder segments in effect"""
        try:
            effect = self.get_effect(scene_id, effect_id)
            if effect:
                success = effect.reorder_segments(segment_order)
                if success:
                    self._notify_change()
                return success
        except Exception as e:
            AppLogger.error(f"Error reordering segments: {e}")
        return False
        
    def add_dimmer_element(self, segment_id: str, dimmer_element: List[int], scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Add dimmer element to segment"""
        try:
            segment = self.get_segment(segment_id, scene_id, effect_id)
            if segment:
                segment.dimmer_time.append(dimmer_element)
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error adding dimmer element: {e}")
        return False
        
    def delete_dimmer_element(self, segment_id: str, element_index: int, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Delete dimmer element from segment"""
        try:
            segment = self.get_segment(segment_id, scene_id, effect_id)
            if segment and 0 <= element_index < len(segment.dimmer_time):
                del segment.dimmer_time[element_index]
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error deleting dimmer element: {e}")
        return False
        
    def update_dimmer_element(self, segment_id: str, element_index: int, dimmer_element: List[int], scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Update dimmer element in segment"""
        try:
            segment = self.get_segment(segment_id, scene_id, effect_id)
            if segment and 0 <= element_index < len(segment.dimmer_time):
                segment.dimmer_time[element_index] = dimmer_element
                self._notify_change()
                return True
        except Exception as e:
            AppLogger.error(f"Error updating dimmer element: {e}")
        return False
        
    def set_current_scene(self, scene_id: int) -> bool:
        """Set current active scene"""
        if scene_id in self.scenes:
            self.current_scene_id = scene_id
            scene = self.scenes[scene_id]
            self.current_effect_id = scene.current_effect_id
            self.current_palette_id = scene.current_palette_id
            self._notify_change()
            return True
        return False
        
    def set_current_effect(self, effect_id: int, scene_id: Optional[int] = None) -> bool:
        """Set current active effect"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene and effect_id in [e.effect_id for e in scene.effects]:
            self.current_effect_id = effect_id
            scene.current_effect_id = effect_id
            self._notify_change()
            return True
        return False
        
    def set_current_palette(self, palette_id: int, scene_id: Optional[int] = None) -> bool:
        """Set current active palette"""
        scene = self.get_scene(scene_id or self.current_scene_id)
        if scene and 0 <= palette_id < len(scene.palettes):
            self.current_palette_id = palette_id
            scene.current_palette_id = palette_id
            self._notify_change()
            return True
        return False
        
    def update_segment_parameter(self, segment_id: str, param: str, value: Any, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Update segment parameter in cache"""
        segment = self.get_segment(segment_id, scene_id, effect_id)
        
        if segment:
            try:
                if param == "segment_id":
                    new_id = int(value)
                    effect = self.get_effect(scene_id, effect_id)
                    if effect and str(new_id) not in effect.segments:
                        effect.segments[str(new_id)] = effect.segments.pop(segment_id)
                        segment.segment_id = new_id
                        self._notify_change()
                        return True
                    return False

                if param == "color":
                    if isinstance(value, dict) and "index" in value and "color_index" in value:
                        index = value["index"]
                        color_index = value["color_index"]
                        if index >= 0:
                            if index >= len(segment.color):
                                segment.color.extend([0] * (index + 1 - len(segment.color)))
                            if index >= len(segment.transparency):
                                segment.transparency.extend([1.0] * (index + 1 - len(segment.transparency)))
                            expected_len = len(segment.color) - 1
                            if len(segment.length) < expected_len:
                                segment.length.extend([10] * (expected_len - len(segment.length)))
                            segment.color[index] = color_index
                    elif isinstance(value, list):
                        segment.color = value

                elif param == "transparency":
                    if isinstance(value, dict) and "index" in value and "transparency" in value:
                        index = value["index"]
                        transparency = value["transparency"]
                        if index >= 0:
                            if index >= len(segment.transparency):
                                segment.transparency.extend([1.0] * (index + 1 - len(segment.transparency)))
                            if index >= len(segment.color):
                                segment.color.extend([0] * (index + 1 - len(segment.color)))
                            expected_len = len(segment.color) - 1
                            if len(segment.length) < expected_len:
                                segment.length.extend([10] * (expected_len - len(segment.length)))
                            segment.transparency[index] = transparency
                    elif isinstance(value, list):
                        segment.transparency = value

                elif param == "length":
                    if isinstance(value, dict) and "index" in value and "length" in value:
                        index = value["index"]
                        length = value["length"]
                        if index >= 0:
                            if index >= len(segment.length):
                                segment.length.extend([10] * (index + 1 - len(segment.length)))
                            required_colors = index + 2
                            if len(segment.color) < required_colors:
                                add = required_colors - len(segment.color)
                                segment.color.extend([0] * add)
                                segment.transparency.extend([1.0] * add)
                            segment.length[index] = length
                    elif isinstance(value, list):
                        segment.length = value
                        
                elif param == "move_speed":
                    segment.move_speed = float(value)
                elif param == "move_range":
                    if isinstance(value, list) and len(value) == 2:
                        segment.move_range = value
                elif param == "initial_position":
                    segment.initial_position = int(value)
                elif param == "current_position":
                    segment.current_position = float(value)
                elif param == "is_edge_reflect":
                    segment.is_edge_reflect = bool(value)
                elif param == "region_id":
                    segment.region_id = int(value)
                elif param == "dimmer_time":
                    segment.dimmer_time = value
                else:
                    return False
                    
                self._notify_change()
                return True
                
            except Exception as e:
                AppLogger.error(f"Error updating segment parameter {param}: {e}")
                return False
        return False
        
    def export_to_dict(self) -> Dict[str, Any]:
        """Export cache data to dictionary structure"""
        try:
            scenes_data = []
            for scene in self.scenes.values():
                scenes_data.append(scene.to_dict())
                
            return {
                'scenes': scenes_data,
                'current_scene_id': self.current_scene_id,
                'current_effect_id': self.current_effect_id,
                'current_palette_id': self.current_palette_id
            }
        except Exception as e:
            raise Exception(f"Failed to export data: {str(e)}")
            
    def clear(self):
        """Clear all cached data and reinitialize"""
        self.scenes.clear()
        self.regions.clear()
        self.current_scene_id = None
        self.current_effect_id = None
        self.current_palette_id = None
        self.is_loaded = False
        
        self._initialize_default_data()
        
    def clear_cache(self):
        """Public method to clear cache"""
        self.clear()


data_cache = DataCacheService()