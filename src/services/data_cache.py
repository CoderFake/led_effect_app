from typing import Dict, List, Optional, Any, Callable
import json
from src.models.scene import Scene
from src.models.effect import Effect
from src.models.segment import Segment
from src.models.region import Region


class DataCacheService:
    """In-memory database cache service"""
    
    def __init__(self):
        self.scenes: Dict[int, Scene] = {}
        self.regions: Dict[int, Region] = {}
        self.current_scene_id: Optional[int] = None
        self.current_effect_id: Optional[int] = None
        self.current_palette_id: Optional[int] = None
        self.is_loaded: bool = False
        self._change_listeners: List[Callable] = []
        
    def load_from_json_data(self, json_data: Dict[str, Any]) -> bool:
        """Load data from JSON structure into cache"""
        try:
            self.scenes.clear()
            self.regions.clear()
            
            for scene_data in json_data.get('scenes', []):
                scene = Scene.from_dict(scene_data)
                self.scenes[scene.scene_id] = scene
                
            self._create_default_regions()
            
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
        """Clear all cached data"""
        self.scenes.clear()
        self.regions.clear()
        self.current_scene_id = None
        self.current_effect_id = None
        self.current_palette_id = None
        self.is_loaded = False
        self._notify_change()
            
    def load_from_file(self, file_path: str) -> bool:
        """Load data from JSON file into cache"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            return self.load_from_json_data(json_data)
        except Exception as e:
            raise Exception(f"Failed to load file {file_path}: {str(e)}")
            
    def _create_default_regions(self):
        """Create default regions based on loaded scenes"""
        if self.scenes:
            first_scene = next(iter(self.scenes.values()))
            led_count = first_scene.led_count
            
            self.regions[0] = Region.create_default(0, led_count)
            
            quarter = led_count // 4
            self.regions[1] = Region(1, "Front Strip", 0, quarter - 1)
            self.regions[2] = Region(2, "Side Strip", quarter, quarter * 3 - 1)
            self.regions[3] = Region(3, "Rear Strip", quarter * 3, led_count - 1)
            
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
        
    def to_json_data(self) -> Dict[str, Any]:
        """Export cache data to JSON structure"""
        return {
            'scenes': [scene.to_dict() for scene in self.scenes.values()]
        }
        
    def get_effect_ids(self, scene_id: Optional[int] = None) -> List[int]:
        """Get effect IDs for scene"""
        scene_id = scene_id or self.current_scene_id
        if scene_id is not None:
            scene = self.get_scene(scene_id)
            if scene:
                return scene.get_effect_ids()
        return []
        
    def get_effect(self, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> Optional[Effect]:
        """Get effect from cache"""
        scene_id = scene_id or self.current_scene_id
        effect_id = effect_id or self.current_effect_id
        
        if scene_id is not None and effect_id is not None:
            scene = self.get_scene(scene_id)
            if scene:
                return scene.get_effect(effect_id)
        return None
        
    def get_segment_ids(self, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> List[int]:
        """Get segment IDs for effect"""
        effect = self.get_effect(scene_id, effect_id)
        if effect:
            return effect.get_segment_ids()
        return []
        
    def get_segment(self, segment_id: str, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> Optional[Segment]:
        """Get segment from cache"""
        effect = self.get_effect(scene_id, effect_id)
        if effect:
            return effect.get_segment(segment_id)
        return None
        
    def get_palette_ids(self, scene_id: Optional[int] = None) -> List[int]:
        """Get palette IDs for scene"""
        scene_id = scene_id or self.current_scene_id
        if scene_id is not None:
            scene = self.get_scene(scene_id)
            if scene:
                return list(range(scene.get_palette_count()))
        return []
        
    def get_palette_colors(self, palette_id: Optional[int] = None, scene_id: Optional[int] = None) -> List[str]:
        """Get palette colors as hex strings"""
        scene_id = scene_id or self.current_scene_id
        palette_id = palette_id or self.current_palette_id
        
        if scene_id is not None and palette_id is not None:
            scene = self.get_scene(scene_id)
            if scene:
                return scene.get_palette_colors(palette_id)
        return ["#000000"] * 6
        
    def get_current_palette_colors(self) -> List[str]:
        """Get current palette colors"""
        return self.get_palette_colors()
        
    def get_region_ids(self) -> List[int]:
        """Get all region IDs"""
        return sorted(self.regions.keys())
        
    def get_region(self, region_id: int) -> Optional[Region]:
        """Get region by ID"""
        return self.regions.get(region_id)
        
    def get_regions(self) -> List[Region]:
        """Get all regions"""
        return list(self.regions.values())
        
    def set_current_scene(self, scene_id: int) -> bool:
        """Set current active scene"""
        if scene_id in self.scenes:
            scene = self.scenes[scene_id]
            self.current_scene_id = scene_id
            self.current_effect_id = scene.current_effect_id
            self.current_palette_id = scene.current_palette_id
            self._notify_change()
            return True
        return False
            
    def set_current_effect(self, effect_id: int) -> bool:
        """Set current active effect"""
        if self.current_scene_id is not None:
            scene = self.get_current_scene()
            if scene and effect_id in scene.get_effect_ids():
                self.current_effect_id = effect_id
                scene.current_effect_id = effect_id
                self._notify_change()
                return True
        return False
                
    def set_current_palette(self, palette_id: int) -> bool:
        """Set current active palette"""
        if self.current_scene_id is not None:
            scene = self.get_current_scene()
            if scene and 0 <= palette_id < scene.get_palette_count():
                self.current_palette_id = palette_id
                scene.current_palette_id = palette_id
                self._notify_change()
                return True
        return False
                
    def get_scene_settings(self, scene_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get scene settings (LED count, FPS)"""
        scene_id = scene_id or self.current_scene_id
        if scene_id is not None:
            scene = self.get_scene(scene_id)
            if scene:
                return {
                    'led_count': scene.led_count,
                    'fps': scene.fps,
                    'scene_id': scene.scene_id
                }
        return None
        
    def get_current_selection(self) -> Dict[str, Any]:
        """Get current selection state"""
        return {
            'scene_id': self.current_scene_id,
            'effect_id': self.current_effect_id,
            'palette_id': self.current_palette_id,
            'is_loaded': self.is_loaded
        }
        
    def add_change_listener(self, callback: Callable):
        """Add listener for data changes"""
        if callback not in self._change_listeners:
            self._change_listeners.append(callback)
            
    def remove_change_listener(self, callback: Callable):
        """Remove change listener"""
        if callback in self._change_listeners:
            self._change_listeners.remove(callback)
            
    def _notify_change(self):
        """Notify all listeners about data changes"""
        for callback in self._change_listeners:
            try:
                callback()
            except Exception:
                pass
                
    def clear_cache(self):
        """Clear all cached data"""
        self.scenes.clear()
        self.regions.clear()
        self.current_scene_id = None
        self.current_effect_id = None
        self.current_palette_id = None
        self.is_loaded = False
        self._notify_change()
        
    def update_scene_settings(self, scene_id: int, led_count: Optional[int] = None, fps: Optional[int] = None) -> bool:
        """Update scene settings in cache"""
        scene = self.get_scene(scene_id)
        if scene:
            if led_count is not None:
                scene.led_count = led_count
            if fps is not None:
                scene.fps = fps
            self._notify_change()
            return True
        return False
        
    def update_segment_parameter(self, segment_id: str, param: str, value: Any, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Update segment parameter in cache"""
        segment = self.get_segment(segment_id, scene_id, effect_id)
        if segment:
            if param == "move_speed":
                segment.move_speed = float(value)
            elif param == "move_range":
                segment.move_range = list(value)
            elif param == "initial_position":
                segment.initial_position = int(value)
            elif param == "is_edge_reflect":
                segment.is_edge_reflect = bool(value)
            elif param == "transparency":
                if isinstance(value, dict) and "index" in value and "transparency" in value:
                    idx = value["index"]
                    if 0 <= idx < len(segment.transparency):
                        segment.transparency[idx] = float(value["transparency"])
            elif param == "length":
                if isinstance(value, dict) and "index" in value and "length" in value:
                    idx = value["index"]
                    if 0 <= idx < len(segment.length):
                        segment.length[idx] = int(value["length"])
            elif param == "color":
                if isinstance(value, dict) and "index" in value and "color_index" in value:
                    idx = value["index"]
                    if 0 <= idx < len(segment.color):
                        segment.color[idx] = int(value["color_index"])
            
            self._notify_change()
            return True
        return False
        
    def update_palette_color(self, palette_id: int, color_index: int, color: str, scene_id: Optional[int] = None) -> bool:
        """Update palette color in cache"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        if scene and 0 <= palette_id < len(scene.palettes) and 0 <= color_index < 6:
            hex_color = color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            scene.palettes[palette_id][color_index] = [r, g, b]
            self._notify_change()
            return True
        return False
        
    def add_dimmer_element(self, segment_id: str, duration: int, initial_brightness: int, final_brightness: int, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Add dimmer element to segment in cache"""
        segment = self.get_segment(segment_id, scene_id, effect_id)
        if segment:
            segment.add_dimmer_element(duration, initial_brightness, final_brightness)
            self._notify_change()
            return True
        return False
        
    def remove_dimmer_element(self, segment_id: str, index: int, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Remove dimmer element from segment in cache"""
        segment = self.get_segment(segment_id, scene_id, effect_id)
        if segment:
            success = segment.remove_dimmer_element(index)
            if success:
                self._notify_change()
            return success
        return False
        
    def update_dimmer_element(self, segment_id: str, index: int, duration: int, initial_brightness: int, final_brightness: int, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Update dimmer element in segment in cache"""
        segment = self.get_segment(segment_id, scene_id, effect_id)
        if segment:
            success = segment.update_dimmer_element(index, duration, initial_brightness, final_brightness)
            if success:
                self._notify_change()
            return success
        return False
        
    def create_new_scene(self, led_count: int, fps: int) -> int:
        """Create new scene in cache and return new scene ID"""
        new_id = max(self.scenes.keys()) + 1 if self.scenes else 0
        
        default_palette = [
            [255, 0, 0], [0, 255, 0], [0, 0, 255],
            [255, 255, 0], [255, 0, 255], [0, 255, 255]
        ]
        
        from models.effect import Effect
        default_effect = Effect(effect_id=0)
        
        scene = Scene(
            scene_id=new_id,
            led_count=led_count,
            fps=fps,
            current_effect_id=0,
            current_palette_id=0,
            palettes=[default_palette],
            effects=[default_effect]
        )
        
        self.scenes[new_id] = scene
        self._notify_change()
        return new_id
        
    def delete_scene(self, scene_id: int) -> bool:
        """Delete scene from cache"""
        if scene_id in self.scenes and scene_id != self.current_scene_id:
            del self.scenes[scene_id]
            self._notify_change()
            return True
        return False
        
    def duplicate_scene(self, source_scene_id: int) -> Optional[int]:
        """Duplicate scene in cache and return new scene ID"""
        source_scene = self.get_scene(source_scene_id)
        if source_scene:
            new_id = max(self.scenes.keys()) + 1 if self.scenes else 0
            scene_data = source_scene.to_dict()
            scene_data['scene_id'] = new_id
            
            new_scene = Scene.from_dict(scene_data)
            self.scenes[new_id] = new_scene
            self._notify_change()
            return new_id
        return None


data_cache = DataCacheService()