"""
generation/settlement_generator.py - Settlement generation system
"""

import random
from typing import List, Dict, Optional
from core.hex_grid import HexCoordinate
from data.models import TerrainType, SettlementType, SettlementData

class SettlementGenerator:
    """Generates settlements based on terrain and regional factors"""
    
    # Settlement density by terrain (chance per hex)
    SETTLEMENT_CHANCES = {
        TerrainType.PLAINS: 0.15,     # 15% chance in plains hexes
        TerrainType.FOREST: 0.08,     # 8% chance in forest hexes
        TerrainType.HILLS: 0.12,      # 12% chance in hills hexes
        TerrainType.MOUNTAINS: 0.05,  # 5% chance in mountain hexes
        TerrainType.WATER: 0.18,      # 18% chance near water
        TerrainType.DESERT: 0.02,     # 2% chance in desert
    }
    
    # Settlement type weights by terrain
    TYPE_WEIGHTS = {
        TerrainType.PLAINS: {
            SettlementType.FARMSTEAD: 35,
            SettlementType.HAMLET: 25,
            SettlementType.VILLAGE: 20,
            SettlementType.TOWN: 8,
            SettlementType.CITY: 2,
            SettlementType.RUINS_VILLAGE: 10,
        },
        TerrainType.FOREST: {
            SettlementType.FARMSTEAD: 15,
            SettlementType.LOGGING_CAMP: 25,
            SettlementType.HAMLET: 15,
            SettlementType.VILLAGE: 10,
            SettlementType.MONASTERY: 8,
            SettlementType.RUINS_VILLAGE: 15,
            SettlementType.ANCIENT_RUINS: 12,
        },
        TerrainType.HILLS: {
            SettlementType.FARMSTEAD: 12,
            SettlementType.HAMLET: 18,
            SettlementType.VILLAGE: 20,
            SettlementType.TOWN: 12,
            SettlementType.WATCHTOWER: 15,
            SettlementType.MINING_CAMP: 15,
            SettlementType.RUINS_KEEP: 8,
        },
        TerrainType.MOUNTAINS: {
            SettlementType.MINING_CAMP: 35,
            SettlementType.MONASTERY: 15,
            SettlementType.WATCHTOWER: 15,
            SettlementType.HAMLET: 10,
            SettlementType.RUINS_KEEP: 15,
            SettlementType.ANCIENT_RUINS: 10,
        },
        TerrainType.WATER: {
            SettlementType.HAMLET: 25,      # Fishing villages
            SettlementType.VILLAGE: 25,
            SettlementType.TOWN: 25,        # Port towns
            SettlementType.CITY: 15,        # Major ports
            SettlementType.WATCHTOWER: 10,
        },
        TerrainType.DESERT: {
            SettlementType.HAMLET: 40,      # Oasis settlements
            SettlementType.MONASTERY: 20,   # Desert monasteries
            SettlementType.RUINS_VILLAGE: 20,
            SettlementType.ANCIENT_RUINS: 20,
        }
    }
    
    # Name components for procedural generation
    TERRAIN_PREFIXES = {
        TerrainType.PLAINS: ["Green", "Golden", "Fair", "Broad", "Rich", "New", "Old"],
        TerrainType.FOREST: ["Deep", "Dark", "Green", "Wild", "Hidden", "Lost", "Ancient"],
        TerrainType.HILLS: ["High", "Stone", "Wind", "Rolling", "Bright", "Crown", "Eagle"],
        TerrainType.MOUNTAINS: ["Iron", "Stone", "Peak", "Ridge", "Snow", "Storm", "Dragon"],
        TerrainType.WATER: ["River", "Lake", "Ford", "Bridge", "Harbor", "Bay", "Shore"],
        TerrainType.DESERT: ["Sand", "Sun", "Dry", "Lost", "Mirage", "Bone", "Dune"],
    }
    
    TERRAIN_SUFFIXES = {
        TerrainType.PLAINS: ["field", "meadow", "haven", "vale", "stead", "moor", "lea"],
        TerrainType.FOREST: ["wood", "grove", "glade", "hollow", "thicket", "brake", "shaw"],
        TerrainType.HILLS: ["hill", "ridge", "crest", "tor", "mount", "down", "fell"],
        TerrainType.MOUNTAINS: ["peak", "fell", "crag", "stone", "hold", "gate", "pass"],
        TerrainType.WATER: ["ford", "bridge", "port", "bay", "crossing", "mouth", "dock"],
        TerrainType.DESERT: ["well", "springs", "rest", "sanctuary", "refuge", "shade", "rock"],
    }
    
    SETTLEMENT_SUFFIXES = {
        SettlementType.FARMSTEAD: ["Farm", "Stead", "Homestead", "Ranch"],
        SettlementType.HAMLET: ["Hamlet", "Grove", "Glen", "Corner"],
        SettlementType.VILLAGE: ["Village", "Borough", "Green", "Commons"],
        SettlementType.TOWN: ["Town", "Market", "Cross", "Mills"],
        SettlementType.CITY: ["City", "Keep", "Hold", "Fortress"],
        SettlementType.LOGGING_CAMP: ["Camp", "Lodge", "Mill", "Clearing"],
        SettlementType.MINING_CAMP: ["Mine", "Quarry", "Delve", "Shaft"],
        SettlementType.MONASTERY: ["Abbey", "Monastery", "Priory", "Sanctuary"],
        SettlementType.WATCHTOWER: ["Watch", "Tower", "Guard", "Beacon"],
    }
    
    def __init__(self, world_seed: int):
        self.world_seed = world_seed
    
    def should_generate_settlement(self, coord: HexCoordinate, terrain: TerrainType, 
                                 neighbors: List[TerrainType]) -> bool:
        """Determine if this hex should have a settlement"""
        # Set seed based on position for consistent generation
        random.seed(self.world_seed + coord.q * 7919 + coord.r * 7907)
        
        base_chance = self.SETTLEMENT_CHANCES.get(terrain, 0.05)
        
        # Modify chance based on neighbors
        water_nearby = TerrainType.WATER in neighbors
        if water_nearby:
            base_chance *= 1.5
        
        # Reduce chance if it's isolated in hostile terrain
        if terrain == TerrainType.MOUNTAINS:
            plains_nearby = TerrainType.PLAINS in neighbors
            if not plains_nearby:
                base_chance *= 0.5
        
        # Desert settlements need water access
        if terrain == TerrainType.DESERT and not water_nearby:
            base_chance *= 0.3
        
        result = random.random() < base_chance
        random.seed()  # Reset seed
        return result
    
    def generate_settlement_type(self, coord: HexCoordinate, 
                               terrain: TerrainType) -> SettlementType:
        """Generate appropriate settlement type for terrain"""
        random.seed(self.world_seed + coord.q * 7919 + coord.r * 7907)
        
        weights = self.TYPE_WEIGHTS.get(terrain, {SettlementType.HAMLET: 100})
        
        total_weight = sum(weights.values())
        rand_val = random.random() * total_weight
        
        current_weight = 0
        selected_type = SettlementType.HAMLET
        for settlement_type, weight in weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                selected_type = settlement_type
                break
        
        random.seed()  # Reset seed
        return selected_type
    
    def generate_settlement_name(self, coord: HexCoordinate, settlement_type: SettlementType, 
                               terrain: TerrainType) -> str:
        """Generate appropriate name for settlement"""
        random.seed(self.world_seed + coord.q * 7919 + coord.r * 7907 + 123)
        
        prefixes = self.TERRAIN_PREFIXES.get(terrain, ["New", "Old", "Little"])
        terrain_suffixes = self.TERRAIN_SUFFIXES.get(terrain, ["place", "burg", "ton"])
        
        # Sometimes use settlement type suffix instead
        if random.random() < 0.4 and settlement_type in self.SETTLEMENT_SUFFIXES:
            suffixes = self.SETTLEMENT_SUFFIXES[settlement_type]
        else:
            suffixes = terrain_suffixes
        
        name = f"{random.choice(prefixes)}{random.choice(suffixes)}"
        
        random.seed()  # Reset seed
        return name
    
    def generate_settlement_details(self, coord: HexCoordinate, 
                                  settlement_type: SettlementType) -> SettlementData:
        """Generate complete settlement with all details"""
        random.seed(self.world_seed + coord.q * 7919 + coord.r * 7907 + 456)
        
        # Generate population within type range
        if settlement_type.max_population > 0:
            population = random.randint(settlement_type.min_population, 
                                      settlement_type.max_population)
        else:
            population = 0  # Ruins
        
        # Generate prosperity (1-5 scale, weighted toward middle)
        prosperity_roll = random.choices([1, 2, 3, 4, 5], weights=[10, 20, 40, 20, 10])[0]
        
        # Generate special features based on settlement type
        special_features = []
        if settlement_type == SettlementType.TOWN or settlement_type == SettlementType.CITY:
            features = ["market_square", "inn", "blacksmith", "temple"]
            special_features = random.sample(features, random.randint(2, len(features)))
        elif settlement_type == SettlementType.VILLAGE:
            features = ["inn", "blacksmith", "temple", "mill"]
            special_features = random.sample(features, random.randint(1, 2))
        elif settlement_type == SettlementType.MONASTERY:
            special_features = ["library", "herb_garden", "scriptorium"]
        elif settlement_type.name.startswith("RUINS"):
            features = ["collapsed_buildings", "overgrown_roads", "hidden_cellars", "ancient_well"]
            special_features = random.sample(features, random.randint(1, 3))
        
        # Generate basic trade goods
        trade_goods = []
        if settlement_type == SettlementType.LOGGING_CAMP:
            trade_goods = ["timber", "furs"]
        elif settlement_type == SettlementType.MINING_CAMP:
            goods = ["iron_ore", "coal", "stone", "gems"]
            trade_goods = [random.choice(goods)]
        elif settlement_type in [SettlementType.VILLAGE, SettlementType.TOWN, SettlementType.CITY]:
            goods = ["grain", "livestock", "pottery", "cloth", "tools"]
            trade_goods = random.sample(goods, random.randint(1, 3))
        
        settlement = SettlementData(
            settlement_type=settlement_type,
            name="",  # Will be set by caller
            population=population,
            prosperity_level=prosperity_roll,
            special_features=special_features,
            trade_goods=trade_goods
        )
        
        random.seed()  # Reset seed
        return settlement
    
    def generate_settlement(self, coord: HexCoordinate, terrain: TerrainType, 
                          neighbors: List[TerrainType]) -> Optional[SettlementData]:
        """Main method to generate a complete settlement if appropriate"""
        if not self.should_generate_settlement(coord, terrain, neighbors):
            return None
        
        settlement_type = self.generate_settlement_type(coord, terrain)
        settlement = self.generate_settlement_details(coord, settlement_type)
        
        # Generate the name
        settlement.name = self.generate_settlement_name(coord, settlement_type, terrain)
        
        return settlement