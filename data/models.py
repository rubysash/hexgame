
"""
data/models.py - Core data models for hexes, terrain, and game state
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

class TerrainType(Enum):
    """Terrain types with display properties and generation weights"""
    # (display_name, color_rgb, description, base_weight, movement_cost)
    PLAINS = ("Plains", (144, 238, 144), "Flat grasslands suitable for travel", 30, 1.0)
    FOREST = ("Forest", (34, 139, 34), "Dense woodland with abundant resources", 25, 1.5)
    HILLS = ("Hills", (205, 133, 63), "Rolling hills with moderate elevation", 20, 2.0)
    MOUNTAINS = ("Mountains", (139, 115, 85), "Towering peaks difficult to traverse", 10, 3.0)
    WATER = ("Water", (70, 130, 180), "Lakes and rivers providing fresh water", 10, None)
    DESERT = ("Desert", (244, 164, 96), "Arid wasteland with scarce resources", 5, 1.5)
    
    def __init__(self, display_name, color, description, weight, movement_cost):
        self.display_name = display_name
        self.color = color
        self.description = description
        self.weight = weight
        self.movement_cost = movement_cost

@dataclass
class TerrainData:
    """Detailed terrain information for a hex"""
    primary: TerrainType
    secondary: Optional[TerrainType] = None
    elevation: int = 0  # Future: for river flow
    special_features: List[str] = field(default_factory=list)

@dataclass
class DiscoveryData:
    """Tracks exploration and discovery state"""
    visible: bool = False
    explored: bool = False
    exploration_level: int = 0  # 0=unexplored, 1=surface, 2=thorough
    last_visited: Optional[datetime] = None
    discovery_notes: List[str] = field(default_factory=list)

@dataclass
class InhabitantData:
    """Tracks NPCs and creatures in a hex"""
    permanent: List[Dict] = field(default_factory=list)
    temporary: List[Dict] = field(default_factory=list)
    respawn_queue: List[Dict] = field(default_factory=list)

@dataclass
class ResourceData:
    """Tracks resources and treasures in a hex"""
    harvestable: List[str] = field(default_factory=list)
    treasure: List[Dict] = field(default_factory=list)
    consumed: List[str] = field(default_factory=list)

@dataclass
class EncounterData:
    """Manages encounters for a hex"""
    recent: List[Dict] = field(default_factory=list)
    scripted: List[Dict] = field(default_factory=list)
    tables: List[str] = field(default_factory=list)

class Hex:
    """Complete hex data model aligned with design document"""
    
    def __init__(self, q: int, r: int, terrain: TerrainType):
        # Core coordinates
        self.q = q
        self.r = r
        self.s = -q - r
        
        # Layer system from design doc
        self.terrain_data = TerrainData(primary=terrain)
        self.discovery_data = DiscoveryData()
        self.inhabitant_data = InhabitantData()
        self.resource_data = ResourceData()
        self.encounter_data = EncounterData()
        
        # Modifications tracking
        self.player_changes: List[Dict] = []
        self.environmental_changes: List[Dict] = []
        self.history: List[Dict] = []
        
    @property
    def terrain(self) -> TerrainType:
        """Quick access to primary terrain"""
        return self.terrain_data.primary
    
    @property
    def id(self) -> str:
        """Unique identifier for the hex"""
        return f"{self.q},{self.r}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize hex to dictionary for saving"""
        return {
            'q': self.q,
            'r': self.r,
            'terrain': self.terrain.name,
            'terrain_data': {
                'primary': self.terrain_data.primary.name,
                'secondary': self.terrain_data.secondary.name if self.terrain_data.secondary else None,
                'elevation': self.terrain_data.elevation,
                'special_features': self.terrain_data.special_features
            },
            'discovery': {
                'visible': self.discovery_data.visible,
                'explored': self.discovery_data.explored,
                'exploration_level': self.discovery_data.exploration_level,
                'last_visited': self.discovery_data.last_visited.isoformat() if self.discovery_data.last_visited else None,
                'discovery_notes': self.discovery_data.discovery_notes
            }
            # Add more layers as implemented
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hex':
        """Create hex from dictionary"""
        hex_obj = cls(data['q'], data['r'], TerrainType[data['terrain']])
        
        # Load additional data if present
        if 'discovery' in data:
            disc = data['discovery']
            hex_obj.discovery_data.visible = disc.get('visible', False)
            hex_obj.discovery_data.explored = disc.get('explored', False)
            hex_obj.discovery_data.exploration_level = disc.get('exploration_level', 0)
            
        return hex_obj
