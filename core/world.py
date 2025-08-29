"""
core/world.py - World management and global state (Updated with Settlements)
"""

import random
from typing import Dict, Tuple, Optional, List
from core.hex_grid import HexCoordinate
from data.models import Hex, TerrainType
from generation.terrain_generator import TerrainGenerator
from generation.settlement_generator import SettlementGenerator

class World:
    """
    Manages the entire game world state.
    Coordinates between terrain generation, settlement generation, hex storage, and game systems.
    """
    
    def __init__(self, world_seed: Optional[int] = None):
        self.world_seed = world_seed or random.randint(0, 1000000)
        self.hexes: Dict[Tuple[int, int], Hex] = {}
        self.terrain_generator = TerrainGenerator(self.world_seed)
        self.settlement_generator = SettlementGenerator(self.world_seed)
        
        # Settlement tracking
        self.settlements_by_type: Dict[str, List[Hex]] = {}
        self.named_settlements: Dict[str, Hex] = {}
        
        # Future: Campaign state
        self.campaign_name = "default"
        self.world_timeline = []
        self.global_state = {}
        
    def get_hex(self, coord: HexCoordinate) -> Hex:
        """Get or generate a hex at the given coordinates"""
        key = coord.to_tuple()
        if key not in self.hexes:
            self.generate_hex(coord)
        return self.hexes[key]
    
    def generate_hex(self, coord: HexCoordinate):
        """Generate a new hex using terrain generation rules"""
        # Get neighboring terrain for context
        neighbor_terrains = []
        for neighbor_coord in coord.get_neighbors():
            key = neighbor_coord.to_tuple()
            if key in self.hexes:
                neighbor_terrains.append(self.hexes[key].terrain)
        
        # Generate terrain
        terrain = self.terrain_generator.generate_terrain(coord, neighbor_terrains)
        
        # Create hex
        new_hex = Hex(coord.q, coord.r, terrain)
        self.hexes[coord.to_tuple()] = new_hex
        
        # Generate settlement if appropriate
        settlement = self.settlement_generator.generate_settlement(
            coord, terrain, neighbor_terrains
        )
        
        if settlement:
            new_hex.settlement_data = settlement
            self._track_settlement(new_hex)
        
        # Future: Generate additional content layers
        # self.generate_inhabitants(new_hex)
        # self.generate_resources(new_hex)
        # self.generate_encounters(new_hex)
        
    def _track_settlement(self, hex_obj: Hex):
        """Track settlement for easy lookup"""
        if not hex_obj.settlement_data:
            return
            
        settlement = hex_obj.settlement_data
        settlement_type = settlement.settlement_type.name
        
        # Track by type
        if settlement_type not in self.settlements_by_type:
            self.settlements_by_type[settlement_type] = []
        self.settlements_by_type[settlement_type].append(hex_obj)
        
        # Track by name (ensure unique names)
        base_name = settlement.name
        name = base_name
        counter = 1
        while name in self.named_settlements:
            counter += 1
            name = f"{base_name} {counter}"
        
        settlement.name = name
        self.named_settlements[name] = hex_obj
    
    def get_hexes_in_range(self, center: HexCoordinate, radius: int) -> List[Hex]:
        """Get all hexes within radius of center"""
        hexes = []
        for q in range(center.q - radius, center.q + radius + 1):
            for r in range(center.r - radius, center.r + radius + 1):
                coord = HexCoordinate(q, r)
                if coord.distance_to(center) <= radius:
                    hexes.append(self.get_hex(coord))
        return hexes
    
    def get_settlements_in_range(self, center: HexCoordinate, radius: int) -> List[Hex]:
        """Get all settlements within radius of center"""
        hexes = self.get_hexes_in_range(center, radius)
        return [hex_obj for hex_obj in hexes if hex_obj.has_settlement]
    
    def find_nearest_settlement(self, coord: HexCoordinate, max_radius: int = 20) -> Optional[Hex]:
        """Find the nearest settlement to a coordinate"""
        for radius in range(1, max_radius + 1):
            settlements = self.get_settlements_in_range(coord, radius)
            if settlements:
                # Return the closest one
                return min(settlements, 
                          key=lambda h: HexCoordinate(h.q, h.r).distance_to(coord))
        return None
    
    def get_settlement_by_name(self, name: str) -> Optional[Hex]:
        """Get settlement hex by name"""
        return self.named_settlements.get(name)
    
    def get_settlements_by_type(self, settlement_type: str) -> List[Hex]:
        """Get all settlements of a specific type"""
        return self.settlements_by_type.get(settlement_type, [])
    
    def get_world_statistics(self) -> Dict:
        """Get statistics about the generated world"""
        stats = {
            'total_hexes': len(self.hexes),
            'total_settlements': len(self.named_settlements),
            'settlements_by_type': {k: len(v) for k, v in self.settlements_by_type.items()},
            'terrain_distribution': {},
            'largest_city': None,
            'total_population': 0
        }
        
        # Calculate terrain distribution
        terrain_counts = {}
        largest_population = 0
        largest_city = None
        total_pop = 0
        
        for hex_obj in self.hexes.values():
            terrain_name = hex_obj.terrain.name
            terrain_counts[terrain_name] = terrain_counts.get(terrain_name, 0) + 1
            
            if hex_obj.has_settlement:
                pop = hex_obj.settlement_data.population
                total_pop += pop
                if pop > largest_population:
                    largest_population = pop
                    largest_city = hex_obj.settlement_data.name
        
        stats['terrain_distribution'] = terrain_counts
        stats['largest_city'] = largest_city
        stats['total_population'] = total_pop
        
        return stats
    
    def update_timeline(self, current_date):
        """Process world timeline events (respawns, migrations, etc.)"""
        # Future: Process timeline events
        # - Settlement growth/decline
        # - Trade route development
        # - Seasonal changes
        # - Political changes
        pass