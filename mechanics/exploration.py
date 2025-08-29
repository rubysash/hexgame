
"""
mechanics/exploration.py - Exploration and discovery mechanics
"""

from typing import List, Set
from core.hex_grid import HexCoordinate
from core.world import World
from data.models import Hex

class ExplorationManager:
    """
    Manages exploration mechanics and discovery progression.
    Implements the discovery system from the design document.
    """
    
    def __init__(self, world: World):
        self.world = world
        self.visibility_range = 3  # Default visibility range
        
    def explore_hex(self, coord: HexCoordinate, exploration_level: int = 1):
        """
        Explore a hex to specified level:
        0 = Visible but unexplored
        1 = Surface exploration
        2 = Thorough exploration
        """
        hex_obj = self.world.get_hex(coord)
        
        # Update discovery data
        hex_obj.discovery_data.visible = True
        hex_obj.discovery_data.explored = True
        hex_obj.discovery_data.exploration_level = max(
            hex_obj.discovery_data.exploration_level,
            exploration_level
        )
        
        # Reveal content based on exploration level
        if exploration_level >= 1:
            # Surface exploration reveals basic features
            self._reveal_surface_features(hex_obj)
        
        if exploration_level >= 2:
            # Thorough exploration reveals hidden content
            self._reveal_hidden_features(hex_obj)
    
    def get_visible_hexes(self, from_coord: HexCoordinate) -> Set[HexCoordinate]:
        """Get all hexes visible from a position"""
        visible = set()
        
        for q in range(from_coord.q - self.visibility_range,
                      from_coord.q + self.visibility_range + 1):
            for r in range(from_coord.r - self.visibility_range,
                          from_coord.r + self.visibility_range + 1):
                coord = HexCoordinate(q, r)
                if coord.distance_to(from_coord) <= self.visibility_range:
                    if self._check_line_of_sight(from_coord, coord):
                        visible.add(coord)
        
        return visible
    
    def _check_line_of_sight(self, from_coord: HexCoordinate, 
                            to_coord: HexCoordinate) -> bool:
        """Check if there's line of sight between hexes"""
        # Future: Implement terrain-based LOS blocking
        # Mountains block sight, hills partially block, etc.
        return True
    
    def _reveal_surface_features(self, hex_obj: Hex):
        """Reveal surface-level features"""
        # Future: Generate and reveal surface features
        pass
    
    def _reveal_hidden_features(self, hex_obj: Hex):
        """Reveal hidden features requiring thorough exploration"""
        # Future: Generate and reveal hidden content
        pass

