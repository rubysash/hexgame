HEX EXPLORATION GAME - PROJECT SKELETON
========================================
This file outlines the complete architecture for a hex-based exploration game
with AI-driven content generation and GURPS rule integration.

Key Design Decisions in the Skeleton:

Modular Architecture: Separated into logical modules (core, data, generation, mechanics, AI, UI) for clean code organization
Memory Management: The Viewport class handles loading/unloading hexes based on proximity to keep memory usage low
Terrain Generation Logic: The TerrainGenerator uses neighbor-based weights and validation rules to ensure realistic geography (rivers flow downhill, mountains cluster, etc.)
Flexible Data Model: HexData class can serialize/deserialize to JSON for easy file storage and debugging
NPC Lifecycle: The skeleton includes respawn logic for organizational roles vs. unique NPCs

Minimum Viable Product Path:
Start with these core components:

HexCoordinate and HexGrid for basic grid math
TerrainGenerator with simple neighbor-based rules
HexData with JSON persistence
Basic console UI to test mechanics
Simple Viewport for displaying a 21x21 hex area

The terrain generation rules in the MVP will use probability weights based on neighbors:

If neighbor is Mountain → 30% Mountain, 50% Hills, 20% other
If neighbor is Water → 40% Plains, 25% Forest, 20% Water
Rivers originate in mountains and flow toward lower elevations


PROJECT STRUCTURE:
==================
/hex_explorer/
    /core/              # Core game engine
        __init__.py
        hex_grid.py     # Hex grid mathematics and coordinate system
        world.py        # World management and state
        viewport.py     # Viewport and rendering management
        
    /data/              # Data models and persistence
        __init__.py
        hex_model.py    # Hex data structures
        world_model.py  # World configuration and state
        persistence.py  # Save/load functionality
        
    /generation/        # Content generation systems
        __init__.py
        terrain_gen.py  # Terrain generation with logical rules
        encounter_gen.py # Encounter and NPC generation
        settlement_gen.py # Settlement and civilization generation
        
    /mechanics/         # Game mechanics
        __init__.py
        exploration.py  # Exploration and discovery mechanics
        movement.py     # Movement rules and pathfinding
        encounter.py    # Encounter resolution
        combat.py       # Combat system (GURPS integration)
        
    /ai/                # AI integration
        __init__.py
        story_engine.py # AI narrative generation
        npc_dialogue.py # NPC conversation system
        
    /ui/                # User interface
        __init__.py
        main_window.py  # Main application window
        hex_viewport.py # Hex map display
        control_panel.py # Character info and controls
        combat_view.py  # Combat interface
        
    /resources/         # Static resources
        /templates/     # JSON templates for content
        /images/        # Graphics and icons
        /data/          # Static game data
        
    main.py             # Application entry point
    config.py           # Configuration settings
"""

# ============================================================================
# CORE/HEX_GRID.PY - Hexagonal grid mathematics and coordinate system
# ============================================================================

class HexCoordinate:
    """
    Represents a hexagonal coordinate using axial coordinates (x, y).
    Handles conversion between different hex coordinate systems.
    """
    def __init__(self, x: int, y: int):
        # Store axial coordinates
        pass
    
    def get_neighbors(self):
        """Return list of 6 adjacent hex coordinates"""
        pass
    
    def distance_to(self, other):
        """Calculate hex distance to another coordinate"""
        pass
    
    def to_pixel(self, hex_size: float):
        """Convert hex coordinate to pixel position for rendering"""
        pass
    
    def to_filename(self):
        """Generate filename for this hex (e.g., '0015_0007.json')"""
        pass


class HexGrid:
    """
    Manages the hexagonal grid structure and operations.
    """
    def __init__(self, origin=(0, 0)):
        # Initialize grid with origin point
        pass
    
    def get_hexes_in_range(self, center: HexCoordinate, range: int):
        """Get all hexes within range of center"""
        pass
    
    def get_line(self, start: HexCoordinate, end: HexCoordinate):
        """Get hexes along a line for line-of-sight calculations"""
        pass
    
    def get_ring(self, center: HexCoordinate, radius: int):
        """Get hexes forming a ring at specific radius"""
        pass


# ============================================================================
# CORE/WORLD.PY - World management and global state
# ============================================================================

class World:
    """
    Manages the entire game world state and coordinates subsystems.
    """
    def __init__(self, campaign_name: str):
        # self.campaign_name = campaign_name
        # self.loaded_hexes = {}  # Cache of loaded hex data
        # self.viewport = None
        # self.party_state = None
        # self.world_timeline = None
        pass
    
    def load_hex(self, coord: HexCoordinate):
        """Load hex data from file or generate if new"""
        pass
    
    def save_hex(self, coord: HexCoordinate):
        """Save hex data to file"""
        pass
    
    def generate_new_hex(self, coord: HexCoordinate):
        """Generate new hex using terrain generation rules"""
        pass
    
    def update_timeline(self, date):
        """Process world timeline events (respawns, migrations, etc.)"""
        pass


# ============================================================================
# CORE/VIEWPORT.PY - Viewport and memory management
# ============================================================================

class Viewport:
    """
    Manages the visible area of the world and memory optimization.
    """
    def __init__(self, center: HexCoordinate, radius: int = 10):
        # self.center = center
        # self.radius = radius  # Viewport radius in hexes
        # self.buffer_radius = radius + 2  # Buffer zone for smooth scrolling
        # self.loaded_hexes = set()
        pass
    
    def move_to(self, new_center: HexCoordinate):
        """Move viewport to new center, load/unload hexes as needed"""
        pass
    
    def get_visible_hexes(self):
        """Return list of hexes currently visible in viewport"""
        pass
    
    def should_load(self, coord: HexCoordinate):
        """Check if hex should be loaded based on distance from viewport"""
        pass
    
    def should_unload(self, coord: HexCoordinate):
        """Check if hex should be unloaded to save memory"""
        pass


# ============================================================================
# DATA/HEX_MODEL.PY - Hex data structures
# ============================================================================

class TerrainType:
    """
    Defines a terrain type with its properties and rules.
    """
    def __init__(self, name: str):
        # self.name = name  # plains, forest, hills, mountains, water, desert
        # self.movement_cost = 1.0
        # self.visibility_modifier = 0
        # self.encounter_tables = []
        # self.compatible_neighbors = []  # Terrain types that can be adjacent
        pass


class HexData:
    """
    Complete data structure for a single hex.
    """
    def __init__(self, coordinate: HexCoordinate):
        # self.coordinate = coordinate
        # self.terrain = TerrainData()
        # self.discovery = DiscoveryData()
        # self.inhabitants = InhabitantData()
        # self.resources = ResourceData()
        # self.encounters = EncounterData()
        # self.modifications = ModificationData()
        pass
    
    def to_json(self):
        """Serialize hex data to JSON format"""
        pass
    
    def from_json(self, json_data):
        """Deserialize hex data from JSON"""
        pass
    
    def is_explorable_from(self, other_hex):
        """Check if this hex can be explored from another hex"""
        pass


class DiscoveryData:
    """
    Tracks exploration and discovery state of a hex.
    """
    def __init__(self):
        # self.visible = False
        # self.explored = False
        # self.exploration_level = 0  # 0=unexplored, 1=surface, 2=thorough
        # self.last_visited = None
        # self.discovery_notes = []
        pass


# ============================================================================
# GENERATION/TERRAIN_GEN.PY - Terrain generation with logical rules
# ============================================================================

class TerrainGenerator:
    """
    Generates terrain following logical geographic rules.
    """
    def __init__(self, seed=None):
        # self.seed = seed
        # self.terrain_weights = {}  # Probability weights for terrain types
        # self.transition_rules = {}  # Rules for terrain transitions
        pass
    
    def generate_terrain(self, coord: HexCoordinate, neighbors: list):
        """
        Generate terrain type based on neighboring hexes.
        Follows rules like:
        - Mountains cluster together
        - Rivers flow from mountains to lakes
        - Deserts avoid water
        - Gradual transitions between climate zones
        """
        pass
    
    def validate_terrain(self, terrain_type: str, neighbors: list):
        """Check if terrain type is valid given neighbors"""
        pass
    
    def generate_features(self, terrain_type: str):
        """Generate special features for the terrain"""
        pass


class RiverGenerator:
    """
    Specialized generator for river systems.
    """
    def generate_river_path(self, start: HexCoordinate, end: HexCoordinate):
        """Generate realistic river path from mountains to lakes/ocean"""
        pass


# ============================================================================
# GENERATION/ENCOUNTER_GEN.PY - Encounter and NPC generation
# ============================================================================

class EncounterGenerator:
    """
    Generates encounters appropriate to terrain and world state.
    """
    def __init__(self):
        # self.encounter_tables = {}  # Loaded from templates
        # self.creature_database = {}
        pass
    
    def generate_encounter(self, hex_data: HexData, party_level: int):
        """Generate encounter appropriate to hex and party"""
        pass
    
    def roll_on_table(self, table_name: str):
        """Roll on specific encounter table"""
        pass


class NPCGenerator:
    """
    Generates NPCs with personalities and motivations.
    """
    def generate_npc(self, role: str, location: HexCoordinate):
        """Generate NPC appropriate to role and location"""
        pass
    
    def generate_replacement(self, original_npc):
        """Generate replacement for dead organizational role"""
        pass


# ============================================================================
# MECHANICS/EXPLORATION.PY - Exploration and discovery mechanics
# ============================================================================

class ExplorationManager:
    """
    Manages exploration mechanics and discovery progression.
    """
    def __init__(self, world: World):
        # self.world = world
        # self.visibility_rules = {}
        pass
    
    def explore_hex(self, coord: HexCoordinate, exploration_level: int):
        """
        Explore a hex to specified level:
        0 = Visible but unexplored
        1 = Surface exploration
        2 = Thorough exploration
        """
        pass
    
    def update_visibility(self, party_position: HexCoordinate):
        """Update which hexes are visible from party position"""
        pass
    
    def calculate_line_of_sight(self, from_hex: HexCoordinate, to_hex: HexCoordinate):
        """Calculate if there's line of sight between hexes"""
        pass


# ============================================================================
# MECHANICS/MOVEMENT.PY - Movement rules and pathfinding
# ============================================================================

class MovementManager:
    """
    Handles movement rules, costs, and pathfinding.
    """
    def __init__(self):
        # self.base_movement_rate = 1
        # self.terrain_costs = {}  # Movement costs by terrain
        pass
    
    def calculate_movement_cost(self, from_hex: HexData, to_hex: HexData):
        """Calculate movement cost between adjacent hexes"""
        pass
    
    def find_path(self, start: HexCoordinate, end: HexCoordinate):
        """A* pathfinding between hexes"""
        pass
    
    def get_reachable_hexes(self, start: HexCoordinate, movement_points: int):
        """Get all hexes reachable with given movement points"""
        pass


# ============================================================================
# AI/STORY_ENGINE.PY - AI narrative generation
# ============================================================================

class StoryEngine:
    """
    Integrates with AI API for narrative generation.
    """
    def __init__(self, api_key: str):
        # self.api_key = api_key
        # self.world_bible = {}  # Core lore and consistency rules
        # self.context_window = []  # Recent events for context
        pass
    
    def generate_hex_description(self, hex_data: HexData, discovery_level: int):
        """Generate description based on exploration level"""
        pass
    
    def generate_encounter_narrative(self, encounter_data, hex_data: HexData):
        """Generate narrative for an encounter"""
        pass
    
    def maintain_consistency(self, generated_content):
        """Check generated content against world bible for consistency"""
        pass


# ============================================================================
# UI/MAIN_WINDOW.PY - Main application window
# ============================================================================

class MainWindow:
    """
    Main application window using tkinter/pygame/etc.
    """
    def __init__(self):
        # self.hex_viewport = HexViewport()
        # self.control_panel = ControlPanel()
        # self.current_view = "exploration"  # or "combat"
        pass
    
    def switch_to_combat_view(self):
        """Switch from hex view to combat view"""
        pass
    
    def update_display(self):
        """Refresh all UI components"""
        pass


class HexViewport:
    """
    Displays the hex map with zoom and pan controls.
    """
    def __init__(self, viewport: Viewport):
        # self.viewport = viewport
        # self.hex_size = 32  # Pixels
        # self.zoom_level = 1.0
        pass
    
    def render_hex(self, hex_data: HexData, position):
        """Render a single hex at screen position"""
        pass
    
    def handle_click(self, screen_position):
        """Convert screen click to hex coordinate"""
        pass


class ControlPanel:
    """
    Right-side panel showing party info, current hex details, etc.
    """
    def __init__(self):
        # self.party_display = PartyDisplay()
        # self.hex_info_display = HexInfoDisplay()
        # self.encounter_display = EncounterDisplay()
        pass


# ============================================================================
# MAIN.PY - Application entry point
# ============================================================================

class HexExplorerGame:
    """
    Main game application coordinating all systems.
    """
    def __init__(self):
        # self.world = None
        # self.ui = None
        # self.story_engine = None
        # self.exploration_manager = None
        # self.movement_manager = None
        pass
    
    def new_campaign(self, campaign_name: str):
        """Start a new campaign"""
        pass
    
    def load_campaign(self, campaign_name: str):
        """Load existing campaign"""
        pass
    
    def run(self):
        """Main game loop"""
        pass


# ============================================================================
# CONFIG.PY - Configuration settings
# ============================================================================

class Config:
    """
    Global configuration settings.
    """
    # File paths
    CAMPAIGNS_DIR = "campaigns/"
    TEMPLATES_DIR = "resources/templates/"
    
    # Viewport settings
    DEFAULT_VIEWPORT_RADIUS = 10
    BUFFER_ZONE_SIZE = 2
    
    # Generation settings
    WORLD_SEED = None  # Random if None
    
    # AI settings
    AI_API_KEY = ""
    AI_MODEL = "gpt-4"
    
    # Game rules
    MOVEMENT_POINTS_PER_DAY = 8
    BASE_VISIBILITY_RANGE = 3

