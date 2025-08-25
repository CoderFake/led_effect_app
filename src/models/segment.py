from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Segment:
    """Segment model containing color, movement and dimmer configuration"""
    
    segment_id: int
    color: List[int]
    transparency: List[float]
    length: List[int]
    move_speed: float
    move_range: List[int]
    initial_position: int
    current_position: float
    is_edge_reflect: bool
    region_id: int
    dimmer_time: List[List[int]]
    
    def __post_init__(self):
        """Validate and auto-fix segment data after initialization"""
        if self.segment_id < 0:
            raise ValueError("Segment ID must be non-negative")
        if len(self.move_range) != 2:
            raise ValueError("Move range must contain exactly 2 values")
        if self.move_range[1] < self.move_range[0]:
            raise ValueError("Move range end must be >= start")
        if self.region_id < 0:
            raise ValueError("Region ID must be non-negative")
        
        if len(self.color) != len(self.transparency):
            target_size = len(self.color)
            if len(self.transparency) < target_size:
                self.transparency.extend([1.0] * (target_size - len(self.transparency)))
            elif len(self.transparency) > target_size:
                self.transparency = self.transparency[:target_size]
        
        expected_length_size = max(0, max(len(self.color), len(self.transparency)) - 1)
        if len(self.length) != expected_length_size:
            if len(self.length) < expected_length_size:
                self.length.extend([10] * (expected_length_size - len(self.length)))
            elif len(self.length) > expected_length_size:
                self.length = self.length[:expected_length_size]

        self.length = [max(1, value) for value in self.length]
            
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Segment':
        """Create Segment from dictionary"""
        return cls(
            segment_id=data['segment_id'],
            color=data['color'],
            transparency=data['transparency'],
            length=data['length'],
            move_speed=data['move_speed'],
            move_range=data['move_range'],
            initial_position=data['initial_position'],
            current_position=data['current_position'],
            is_edge_reflect=data['is_edge_reflect'],
            region_id=data.get('region_id', 0),
            dimmer_time=data['dimmer_time']
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert Segment to dictionary"""
        return {
            'segment_id': self.segment_id,
            'color': self.color,
            'transparency': self.transparency,
            'length': self.length,
            'move_speed': self.move_speed,
            'move_range': self.move_range,
            'initial_position': self.initial_position,
            'current_position': self.current_position,
            'is_edge_reflect': self.is_edge_reflect,
            'region_id': self.region_id,
            'dimmer_time': self.dimmer_time
        }