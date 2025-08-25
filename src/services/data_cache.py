from typing import Dict, List, Optional, Any, Callable
import json
import copy
import inspect
from src.models.scene import Scene
from src.models.effect import Effect
from src.models.segment import Segment
from src.models.region import Region
from utils.logger import AppLogger


class DataCacheService:
    """In-memory database cache service with full CRUD operations"""
    
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
        """Initialize cache with default data structure"""
        try:
            initial_segment = {
                "segment_id": 0,
                "color": [0, 1, 2, 3, 4, 5],
                "transparency": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                "length": [10, 10, 10, 10, 10],
                "move_speed": 100.0,
                "move_range": [0, 250],
                "initial_position": 0,
                "current_position": 0.0,
                "is_edge_reflect": True,
                "dimmer_time": [
                    [1000, 0, 100],
                    [1000, 100, 0]
                ]
            }
            
            initial_effect = {
                "effect_id": 0,
                "segments": {
                    "0": initial_segment
                }
            }
            
            initial_palette = [
                [0, 0, 0],       # Black
                [255, 0, 0],     # Red  
                [255, 255, 0],   # Yellow
                [0, 0, 255],     # Blue
                [0, 255, 0],     # Green
                [255, 255, 255]  # White
            ]
            
            initial_scene_data = {
                "scene_id": 0,
                "led_count": 250,
                "fps": 60,
                "current_effect_id": 0,
                "current_palette_id": 0,
                "palettes": [initial_palette],
                "effects": [initial_effect]
            }
            
            scene = Scene.from_dict(initial_scene_data)
            self.scenes[0] = scene
            
            self._create_initial_regions()
            
            self.current_scene_id = 0
            self.current_effect_id = 0
            self.current_palette_id = 0
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
            
            # Auto-fix JSON data before loading
            fixed_json_data = self._auto_fix_json_data(json_data)
            
            for scene_data in fixed_json_data.get('scenes', []):
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
            
    def _auto_fix_json_data(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-fix JSON data to ensure proper array sizes"""
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
        """Fix arrays in segment data to ensure proper sizes"""
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
                
            expected_length_count = max(0, color_count - 1)
            if len(length) != expected_length_count:
                if len(length) < expected_length_count:
                    length.extend([0] * (expected_length_count - len(length)))
                else:
                    length = length[:expected_length_count]
                segment_data['length'] = length
                
            AppLogger.info(f"Fixed segment {segment_data.get('segment_id')}: colors={color_count}, transparency={len(transparency)}, length={len(length)}")
            
        except Exception as e:
            AppLogger.error(f"Error fixing segment arrays: {e}")
            
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
            
    # ===== Getters =====
    
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
        
    # ===== Setters =====
        
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
        
    # ===== Scene CRUD =====
        
    def create_new_scene(self, led_count: int, fps: int) -> int:
        """Create new scene in cache and return new scene ID"""
        new_id = max(self.scenes.keys()) + 1 if self.scenes else 0
        
        default_palette = [
            [255, 0, 0], [0, 255, 0], [0, 0, 255],
            [255, 255, 0], [255, 0, 255], [0, 255, 255]
        ]
        
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
        
    # ===== Effect CRUD =====
        
    def create_new_effect(self, scene_id: Optional[int] = None) -> Optional[int]:
        """Create new effect in scene and return new effect ID"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        
        if scene:
            existing_ids = scene.get_effect_ids()
            new_id = max(existing_ids) + 1 if existing_ids else 0
            
            new_effect = Effect(effect_id=new_id)
            scene.add_effect(new_effect)
            
            self._notify_change()
            return new_id
        return None
        
    def delete_effect(self, effect_id: int, scene_id: Optional[int] = None) -> bool:
        """Delete effect from scene"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        
        if scene and effect_id != self.current_effect_id:
            success = scene.remove_effect(effect_id)
            if success:
                self._notify_change()
            return success
        return False
        
    def duplicate_effect(self, source_effect_id: int, scene_id: Optional[int] = None) -> Optional[int]:
        """Duplicate effect in scene and return new effect ID"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        source_effect = self.get_effect(scene_id, source_effect_id)
        
        if scene and source_effect:
            existing_ids = scene.get_effect_ids()
            new_id = max(existing_ids) + 1 if existing_ids else 0
            
            effect_data = source_effect.to_dict()
            effect_data['effect_id'] = new_id
            
            new_effect = Effect.from_dict(effect_data)
            scene.add_effect(new_effect)
            
            self._notify_change()
            return new_id
        return None
        
    # ===== Segment CRUD =====
        
    def create_new_segment(self, custom_id: int, scene_id: Optional[int] = None, effect_id: Optional[int] = None) -> bool:
        """Create new segment with custom ID"""
        effect = self.get_effect(scene_id, effect_id)
        
        if effect:
            if str(custom_id) in effect.segments:
                return False
                
            new_segment = Segment(
                segment_id=custom_id,
                color=[0],  
                transparency=[1.0], 
                length=[], 
                move_speed=100.0,
                move_range=[0, 100],
                initial_position=0,
                current_position=0.0,
                is_edge_reflect=True,
                dimmer_time=[[1000, 100, 100]]
            )
            
            effect.add_segment(new_segment)
            self._notify_change()
            return True
        return False
        
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
        
    # ===== Palette CRUD =====
        
    def create_new_palette(self, scene_id: Optional[int] = None) -> Optional[int]:
        """Create new palette in scene and return new palette ID"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        
        if scene:
            new_id = len(scene.palettes)
            
            default_palette = [
                [0, 0, 0], [255, 0, 0], [255, 255, 0],
                [0, 0, 255], [0, 255, 0], [255, 255, 255]
            ]
            
            scene.palettes.append(default_palette)
            self._notify_change()
            return new_id
        return None
        
    def delete_palette(self, palette_id: int, scene_id: Optional[int] = None) -> bool:
        """Delete palette from scene"""
        scene_id = scene_id or self.current_scene_id
        scene = self.get_scene(scene_id)
        
        if scene and palette_id != self.current_palette_id and 0 <= palette_id < len(scene.palettes):
            del scene.palettes[palette_id]
            
            if self.current_palette_id > palette_id:
                self.