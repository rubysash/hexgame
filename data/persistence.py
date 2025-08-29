"""
data/persistence.py - World persistence and save/load functionality
"""

import json
import os
from typing import Dict, Any, Tuple, TYPE_CHECKING
from core.hex_grid import HexCoordinate
from data.models import Hex

# Use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from core.world import World
    from core.viewport import Viewport

class WorldPersistence:
    """Handles saving and loading world data"""
    
    def save_world(self, world: 'World', viewport: 'Viewport', filename: str):
        """Save world to JSON file"""
        data = {
            'version': '1.0',
            'seed': world.world_seed,
            'viewport_center': {
                'q': viewport.center.q,
                'r': viewport.center.r
            },
            'campaign_name': world.campaign_name,
            'hexes': [hex_obj.to_dict() for hex_obj in world.hexes.values()],
            'world_timeline': world.world_timeline,
            'global_state': world.global_state
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_world(self, filename: str) -> Tuple['World', HexCoordinate]:
        """Load world from JSON file"""
        # Import here to avoid circular import
        from core.world import World
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create world with saved seed
        world = World(data['seed'])
        world.campaign_name = data.get('campaign_name', 'default')
        world.world_timeline = data.get('world_timeline', [])
        world.global_state = data.get('global_state', {})
        
        # Load hexes
        world.hexes = {}
        for hex_data in data['hexes']:
            hex_obj = Hex.from_dict(hex_data)
            world.hexes[(hex_obj.q, hex_obj.r)] = hex_obj
        
        # Get viewport center
        vc = data['viewport_center']
        viewport_center = HexCoordinate(vc['q'], vc['r'])
        
        return world, viewport_center
    
    def save_campaign(self, world: 'World', campaign_dir: str):
        """Save complete campaign with all files"""
        # Future: Save campaign with proper directory structure
        # /campaign_name/
        #   world_config.json
        #   hexes/
        #   templates/
        #   campaign_state.json
        pass
    
    def load_campaign(self, campaign_dir: str) -> 'World':
        """Load complete campaign"""
        # Future: Load campaign from directory structure
        pass