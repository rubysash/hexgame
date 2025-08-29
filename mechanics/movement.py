"""
mechanics/movement.py - Movement rules and pathfinding
"""

from typing import List, Optional, Set
from core.hex_grid import HexCoordinate
from core.world import World
from data.models import TerrainType

class MovementManager:
    """
    Handles movement rules, costs, and pathfinding.
    Implements movement system from the design document.
    """
    
    def __init__(self, world: World):
        self.world = world
        self.base_movement_points = 8  # Per day
        
    def calculate_movement_cost(self, from_coord: HexCoordinate,
                               to_coord: HexCoordinate) -> Optional[float]:
        """Calculate movement cost between adjacent hexes"""
        # Check if hexes are adjacent
        if from_coord.distance_to(to_coord) != 1:
            return None
        
        to_hex = self.world.get_hex(to_coord)
        
        # Check if terrain is passable
        if to_hex.terrain.movement_cost is None:
            return None  # Impassable (e.g., water without boat)
        
        return to_hex.terrain.movement_cost
    
    def get_reachable_hexes(self, start: HexCoordinate, 
                           movement_points: float) -> Set[HexCoordinate]:
        """Get all hexes reachable with given movement points"""
        reachable = set()
        visited = {start: 0}  # coord -> cost to reach
        frontier = [(start, 0)]  # (coord, cost)
        
        while frontier:
            current, current_cost = frontier.pop(0)
            
            for neighbor in current.get_neighbors():
                move_cost = self.calculate_movement_cost(current, neighbor)
                
                if move_cost is None:
                    continue  # Impassable
                
                new_cost = current_cost + move_cost
                
                if new_cost <= movement_points:
                    if neighbor not in visited or new_cost < visited[neighbor]:
                        visited[neighbor] = new_cost
                        frontier.append((neighbor, new_cost))
                        reachable.add(neighbor)
        
        return reachable
    
    def find_path(self, start: HexCoordinate, 
                  goal: HexCoordinate) -> Optional[List[HexCoordinate]]:
        """A* pathfinding between hexes"""
        # Future: Implement A* pathfinding
        return None