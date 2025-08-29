"""
data/models.py - Core data models for hexes, terrain, and game state (Updated with Settlements)
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
    DESERT = ("Desert", (255, 255, 244), "Arid wasteland with scarce resources", 5, 1.5)
    
    def __init__(self, display_name, color, description, weight, movement_cost):
        self.display_name = display_name
        self.color = color
        self.description = description
        self.weight = weight
        self.movement_cost = movement_cost

class SettlementType(Enum):
    """Settlement types with population and requirements"""
    # (name, min_pop, max_pop, description, terrain_preferences, map_symbol)
    FARMSTEAD = ("Farmstead", 5, 20, "Single family farm with outbuildings", 
                 ["PLAINS", "FOREST"], "⌂")
    
    HAMLET = ("Hamlet", 20, 100, "Small cluster of farms around a common", 
              ["PLAINS"], "⌂⌂")
    
    VILLAGE = ("Village", 100, 400, "Rural community with basic services", 
               ["PLAINS", "HILLS"], "🏘️")
    
    TOWN = ("Town", 400, 2000, "Market town with specialized crafts", 
            ["PLAINS", "HILLS"], "🏙️")
    
    CITY = ("City", 2000, 10000, "Major population center with walls", 
            ["PLAINS"], "🏛️")
    
    # Specialty settlements
    LOGGING_CAMP = ("Logging Camp", 15, 60, "Temporary lumber operation", 
                    ["FOREST"], "🪵")
    
    MINING_CAMP = ("Mining Camp", 30, 150, "Resource extraction settlement", 
                   ["HILLS", "MOUNTAINS"], "⛏️")
    
    MONASTERY = ("Monastery", 10, 50, "Religious retreat and learning center", 
                 ["HILLS", "FOREST"], "⛪")
    
    WATCHTOWER = ("Watchtower", 3, 12, "Military outpost with small garrison", 
                  ["HILLS"], "🗼")
    
    # Ruins and abandoned places
    RUINS_VILLAGE = ("Ruined Village", 0, 0, "Abandoned settlement, partially intact", 
                     ["PLAINS", "FOREST"], "🏚️")
    
    RUINS_KEEP = ("Ruined Keep", 0, 0, "Abandoned fortification", 
                  ["HILLS"], "🏰")
    
    ANCIENT_RUINS = ("Ancient Ruins", 0, 0, "Mysterious pre-human structures", 
                     ["MOUNTAINS", "FOREST"], "🗿")

    def __init__(self, display_name, min_pop, max_pop, description, terrain_prefs, symbol):
        self.display_name = display_name
        self.min_population = min_pop
        self.max_population = max_pop
        self.description = description
        self.terrain_preferences = terrain_prefs
        self.map_symbol = symbol
        self.is_ruins = min_pop == 0

@dataclass
class TerrainData:
    """Detailed terrain information for a hex"""
    primary: TerrainType
    secondary: Optional[TerrainType] = None
    elevation: int = 0  # Future: for river flow
    special_features: List[str] = field(default_factory=list)

@dataclass
class SettlementData:
    """Data for a settlement within a hex"""
    settlement_type: SettlementType
    name: str
    population: int
    prosperity_level: int = 1  # 1-5 scale
    special_features: List[str] = field(default_factory=list)
    notable_npcs: List[Dict] = field(default_factory=list)
    trade_goods: List[str] = field(default_factory=list)
    defenses: List[str] = field(default_factory=list)
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get formatted display information"""
        return {
            'name': self.name,
            'type': self.settlement_type.display_name,
            'population': self.population,
            'prosperity': '★' * self.prosperity_level,
            'symbol': self.settlement_type.map_symbol,
            'description': self.settlement_type.description
        }

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
        
        # NEW: Settlement data
        self.settlement_data: Optional[SettlementData] = None
        
        # Modifications tracking
        self.player_changes: List[Dict] = []
        self.environmental_changes: List[Dict] = []
        self.history: List[Dict] = []
        
    @property
    def terrain(self) -> TerrainType:
        """Quick access to primary terrain"""
        return self.terrain_data.primary
    
    @property
    def has_settlement(self) -> bool:
        """Check if hex has a settlement"""
        return self.settlement_data is not None
    
    @property
    def settlement_name(self) -> Optional[str]:
        """Get settlement name if present"""
        return self.settlement_data.name if self.settlement_data else None
    
    @property
    def id(self) -> str:
        """Unique identifier for the hex"""
        return f"{self.q},{self.r}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize hex to dictionary for saving"""
        data = {
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
        }
        
        # Add settlement data if present
        if self.settlement_data:
            data['settlement'] = {
                'type': self.settlement_data.settlement_type.name,
                'name': self.settlement_data.name,
                'population': self.settlement_data.population,
                'prosperity_level': self.settlement_data.prosperity_level,
                'special_features': self.settlement_data.special_features,
                'notable_npcs': self.settlement_data.notable_npcs,
                'trade_goods': self.settlement_data.trade_goods,
                'defenses': self.settlement_data.defenses
            }
        
        return data
    
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
        
        # Load settlement data if present
        if 'settlement' in data:
            settlement = data['settlement']
            hex_obj.settlement_data = SettlementData(
                settlement_type=SettlementType[settlement['type']],
                name=settlement['name'],
                population=settlement['population'],
                prosperity_level=settlement.get('prosperity_level', 1),
                special_features=settlement.get('special_features', []),
                notable_npcs=settlement.get('notable_npcs', []),
                trade_goods=settlement.get('trade_goods', []),
                defenses=settlement.get('defenses', [])
            )
            
        return hex_obj