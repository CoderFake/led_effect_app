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
    dimmer_time: List[List[int]]
    
    def __post_init__(self):
        """Validate segment data after initialization"""
        if self.segment_id < 0:
            raise ValueError("Segment ID must be non-negative")
        if len(self.move_range) != 2:
            raise ValueError("Move range must contain exactly 2 values")
        if self.move_range[1] < self.move_range[0]:
            raise ValueError("Move range end must be >= start")
        if len(self.color) != len(self.transparency) or len(self.color) != len(self.length):
            raise ValueError("Color, transparency and length arrays must have same size")
            
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
            'dimmer_time': self.dimmer_time
        }
        
    def get_color_count(self) -> int:
        """Get number of colors in this segment"""
        return len(self.color)
        
    def get_dimmer_count(self) -> int:
        """Get number of dimmer elements"""
        return len(self.dimmer_time)
        
    def get_total_length(self) -> int:
        """Get total LED length of this segment"""
        return sum(self.length)
        
    def is_position_in_range(self, position: int) -> bool:
        """Check if position is within move range"""
        return self.move_range[0] <= position <= self.move_range[1]
        
    def get_move_distance(self) -> int:
        """Get total move distance"""
        return abs(self.move_range[1] - self.move_range[0])
        
    def add_dimmer_element(self, duration: int, initial_brightness: int, final_brightness: int):
        """Add dimmer element"""
        self.dimmer_time.append([duration, initial_brightness, final_brightness])
        
    def remove_dimmer_element(self, index: int) -> bool:
        """Remove dimmer element by index"""
        if 0 <= index < len(self.dimmer_time):
            del self.dimmer_time[index]
            return True
        return False
        
    def update_dimmer_element(self, index: int, duration: int, initial_brightness: int, final_brightness: int) -> bool:
        """Update dimmer element by index"""
        if 0 <= index < len(self.dimmer_time):
            self.dimmer_time[index] = [duration, initial_brightness, final_brightness]
            return True
        return False