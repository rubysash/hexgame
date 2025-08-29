"""
generation/terrain_generator.py - Terrain generation with logical rules
"""

import random
from typing import List, Dict
from core.hex_grid import HexCoordinate
from data.models import TerrainType

# Neighbor influence weights - what terrain likes to be next to what
NEIGHBOR_WEIGHTS = {
    TerrainType.PLAINS: {
        TerrainType.PLAINS: 1.5,
        TerrainType.FOREST: 1.2,
        TerrainType.HILLS: 1.0,
        TerrainType.MOUNTAINS: 0.3,
        TerrainType.WATER: 1.0,
        TerrainType.DESERT: 0.7
    },
    TerrainType.FOREST: {
        TerrainType.PLAINS: 1.0,
        TerrainType.FOREST: 2.0,
        TerrainType.HILLS: 1.3,
        TerrainType.MOUNTAINS: 0.5,
        TerrainType.WATER: 1.5,
        TerrainType.DESERT: 0.1
    },
    TerrainType.HILLS: {
        TerrainType.PLAINS: 0.8,
        TerrainType.FOREST: 1.0,
        TerrainType.HILLS: 1.5,
        TerrainType.MOUNTAINS: 2.0,
        TerrainType.WATER: 0.6,
        TerrainType.DESERT: 0.4
    },
    TerrainType.MOUNTAINS: {
        TerrainType.PLAINS: 0.2,
        TerrainType.FOREST: 0.5,
        TerrainType.HILLS: 2.0,
        TerrainType.MOUNTAINS: 2.5,
        TerrainType.WATER: 0.8,
        TerrainType.DESERT: 0.3
    },
    TerrainType.WATER: {
        TerrainType.PLAINS: 1.2,
        TerrainType.FOREST: 1.5,
        TerrainType.HILLS: 0.5,
        TerrainType.MOUNTAINS: 0.8,
        TerrainType.WATER: 2.0,
        TerrainType.DESERT: 0.1
    },
    TerrainType.DESERT: {
        TerrainType.PLAINS: 0.7,
        TerrainType.FOREST: 0.1,
        TerrainType.HILLS: 0.5,
        TerrainType.MOUNTAINS: 0.3,
        TerrainType.WATER: 0.1,
        TerrainType.DESERT: 2.5
    }
}

class TerrainGenerator:
    """
    Generates terrain following logical geographic rules.
    Implements the terrain generation rules from the design document.
    """
    
    def __init__(self, world_seed: int):
        self.world_seed = world_seed
        
    def generate_terrain(self, coord: HexCoordinate, 
                        neighbors: List[TerrainType]) -> TerrainType:
        """
        Generate terrain type based on neighboring hexes.
        Uses position-based seeding for consistent generation.
        """
        # Set seed based on position for consistent generation
        random.seed(self.world_seed + coord.q * 10000 + coord.r)
        
        # Calculate weighted probabilities
        weights: Dict[TerrainType, float] = {}
        for terrain_type in TerrainType:
            weights[terrain_type] = terrain_type.weight
            
        # Apply neighbor influences
        for neighbor_terrain in neighbors:
            for terrain_type in TerrainType:
                weights[terrain_type] *= NEIGHBOR_WEIGHTS[neighbor_terrain][terrain_type]
        
        # Select terrain type
        total_weight = sum(weights.values())
        rand_val = random.random() * total_weight
        
        current_weight = 0.0
        selected_terrain = TerrainType.PLAINS
        for terrain_type, weight in weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                selected_terrain = terrain_type
                break
        
        # Reset random seed
        random.seed()
        
        return selected_terrain
    
    def validate_terrain(self, terrain_type: TerrainType, 
                        neighbors: List[TerrainType]) -> bool:
        """Check if terrain type is valid given neighbors"""
        # Future: Implement hard constraints
        # e.g., no desert next to tundra
        return True
    
    def generate_special_features(self, terrain_type: TerrainType) -> List[str]:
        """Generate special features for the terrain"""
        # Future: Add ruins, springs, caves, etc.
        return []
