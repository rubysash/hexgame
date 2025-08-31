# HEX EXPLORATION GAME - PROJECT ARCHITECTURE
===============================================

This document outlines the complete architecture for the hex-based exploration game with procedural generation, settlement systems, and hex editing capabilities.

## Project Overview

The Hex Explorer is a pygame-based infinite world generator that creates realistic terrain and settlements using deterministic algorithms. Players can explore the world, edit hexes with custom content, and save/load world states. The system is designed for future integration with GURPS rules and AI-driven content generation.

## Current Implementation Status

### Fully Implemented
- Infinite procedural world generation with seed consistency
- Realistic terrain generation using neighbor-based logic
- Complete settlement system with 12 settlement types
- Interactive hex editing with persistent storage
- Memory-efficient viewport system
- Save/load functionality for world states
- Unicode symbol support for settlements
- Comprehensive UI with information panels

### Planned Features
- GURPS rule integration for movement and exploration
- AI-generated descriptions and narratives
- Encounter system with terrain-based tables
- NPC and creature lifecycle management
- Media support (images/audio) in hex editor
- Campaign timeline and world events

## Architecture Overview

```
/hex_explorer/
├── core/                   # Core game engine
│   ├── hex_grid.py        # Hexagonal coordinate mathematics
│   ├── world.py           # World state management and generation coordination
│   └── viewport.py        # Memory-efficient hex loading system
├── data/                   # Data models and persistence
│   ├── models.py          # Core data structures (Hex, TerrainType, SettlementType)
│   ├── hex_editor.py      # User edit data management and storage
│   └── persistence.py     # World save/load functionality
├── generation/             # Procedural generation systems
│   ├── config_data.py     # Settlement symbols, colors, and generation data
│   ├── terrain_generator.py # Terrain generation with geographic logic
│   └── settlement_generator.py # Settlement placement and naming
├── mechanics/              # Game mechanics (future expansion)
│   ├── exploration.py     # Discovery and visibility mechanics
│   └── movement.py        # Movement costs and pathfinding
├── ui/                     # User interface components
│   ├── game_window.py     # Main pygame window and game loop
│   ├── renderer.py        # Hex and settlement rendering
│   ├── panels.py          # UI information panels and displays
│   └── hex_editor_window.py # Tkinter hex editor popup
├── config.py              # Global configuration and seed management
└── main.py               # Application entry point
```

## Module Responsibilities

### Core Engine (`core/`)

**hex_grid.py**: Hexagonal Grid Mathematics
- `HexCoordinate`: Axial coordinate system with conversion methods
- Distance calculations, neighbor finding, pixel conversions
- Foundation for all hex-based operations

**world.py**: World Management
- `World`: Coordinates terrain generation, settlement generation, and edit data
- Manages hex storage and retrieval with lazy loading
- Tracks settlements by type and name for statistics
- Integrates edit data system for user customizations

**viewport.py**: Memory Management
- `Viewport`: Handles visible area calculation and hex loading/unloading
- Buffer system for smooth scrolling
- Memory optimization for infinite world exploration

### Data Layer (`data/`)

**models.py**: Core Data Structures
- `TerrainType`: Enum with display properties, movement costs, and generation weights
- `SettlementType`: Enum with population ranges, terrain preferences, and descriptions
- `Hex`: Complete hex data model with terrain, settlements, and discovery tracking
- `SettlementData`: Detailed settlement information with features and trade goods
- `DiscoveryData`: Exploration state tracking

**hex_editor.py**: Edit Data Management
- `HexEditData`: User customization data structure
- `HexEditorManager`: File-based storage for hex edits with caching
- Supports custom names, descriptions, notes, and exploration overrides

**persistence.py**: World Persistence
- `WorldPersistence`: Save/load complete world states to JSON
- Handles viewport position restoration
- Future: Campaign management with directory structures

### Generation Systems (`generation/`)

**terrain_generator.py**: Terrain Generation
- `TerrainGenerator`: Creates realistic terrain using neighbor influence weights
- Geographic logic prevents unrealistic combinations (desert next to water)
- Seed-based deterministic generation for consistency

**settlement_generator.py**: Settlement Generation
- `SettlementGenerator`: Places settlements based on terrain suitability
- Generates appropriate names using terrain-based prefix/suffix combinations
- Creates settlement details (population, prosperity, features, trade goods)

**config_data.py**: Generation Configuration
- Settlement symbols and colors for Unicode display
- Terrain-based settlement chances and type weights
- Extensive naming data with terrain-appropriate prefixes and suffixes

### User Interface (`ui/`)

**game_window.py**: Main Application
- `HexGridGame`: Main pygame window and game loop
- Event handling for movement, editing, and world interaction
- Integrates all UI components and manages game state

**renderer.py**: Visual Rendering
- `HexRenderer`: Draws hexes, terrain colors, and settlement symbols
- Unicode font support with fallback systems for cross-platform compatibility
- Configurable display options for settlements and coordinates

**panels.py**: Information Display
- `UIPanel`: Manages all UI information panels
- Settlement summary with largest settlements
- Terrain legend and world statistics
- Detailed tooltips with settlement and edit information

**hex_editor_window.py**: Hex Editing Interface
- `HexEditorWindow`: Tkinter-based popup editor for hex customization
- Fields for custom names, descriptions, notes, and exploration overrides
- Validation and change tracking with auto-save functionality

### Game Mechanics (`mechanics/`)

**exploration.py**: Discovery System
- `ExplorationManager`: Manages exploration levels and visibility
- Framework for future line-of-sight and discovery mechanics

**movement.py**: Movement System
- `MovementManager`: Calculates movement costs based on terrain
- A* pathfinding framework for future route planning

## Key Design Principles

### Terrain Generation Logic
The terrain generator uses weighted neighbor influences to create realistic geography:

```python
# Example: Forest terrain weights
NEIGHBOR_WEIGHTS = {
    TerrainType.FOREST: {
        TerrainType.FOREST: 2.0,    # Forests cluster strongly
        TerrainType.WATER: 1.5,     # Like water proximity
        TerrainType.DESERT: 0.1,    # Avoid desert adjacency
        # ... other relationships
    }
}
```

### Settlement Placement Rules
- **Density**: 1 village per 2-4 hexes in good terrain, cities rare (1 per 50-100 hexes)
- **Resource Access**: Water proximity increases settlement chances by 50%
- **Terrain Suitability**: Each settlement type has preferred terrain (logging camps need forests)
- **Realistic Populations**: Farmsteads (5-20) → Hamlets (20-100) → Villages (100-400) → Towns (400-2000) → Cities (2000-10000)

### Edit Data System
User customizations are stored separately from generated data:
- Edit files stored in `saves/edits/{world_seed}/` directory
- Individual JSON files per edited hex for efficient storage
- Edit data overlays on generated content without replacing it
- Supports custom names, descriptions, notes, and exploration state overrides

## Configuration and Seeding

### Seed Input Methods
1. **Command Line**: `python main.py --seed "MyWorld"`
2. **Environment Variable**: `HEX_WORLD_SEED=12345`
3. **String Hashing**: Non-numeric seeds are deterministically hashed
4. **Random Generation**: If no seed specified

### Display Configuration
```python
class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    HEX_SIZE = 35
    VIEWPORT_RADIUS = 15
    SHOW_SEED_IN_TITLE = True
    # ... other settings
```

## Game Controls

### Navigation
- **Arrow Keys**: Move camera around the world
- **Shift + Arrow**: Fast movement for quick exploration
- **Space**: Reset view to world origin (0,0)

### Interaction
- **Right-Click**: Open hex editor for hovered hex
- **E Key**: Alternative way to open hex editor
- **Left-Click**: Future media playback for hexes with audio/images

### Display Toggles
- **N**: Toggle settlement name display on/off
- **I**: Toggle settlement icon display on/off
- **L**: Toggle terrain type legend
- **P**: Toggle settlement summary panel
- **T**: Toggle world statistics panel

### World Management
- **Ctrl+S**: Save current world state to file
- **Ctrl+L**: Load world state from file
- **G**: Print detailed world statistics to console
- **ESC**: Exit application

## Data Structures

### Hex Data Model
Each hex contains:
- **Terrain Data**: Primary terrain type, elevation, special features
- **Settlement Data**: If present, complete settlement information
- **Discovery Data**: Exploration status and visibility
- **Edit Data**: User customizations (name, description, notes)

Full hex data see hex_sample.json for POSSIBILITIES

### Settlement Data
Settlements include:
- **Basic Info**: Type, name, population, prosperity level (1-5 stars)
- **Features**: Market squares, temples, blacksmiths, etc.
- **Trade Goods**: Terrain-appropriate products
- **Special Attributes**: Defenses, notable NPCs (future expansion)

### World Statistics
The system tracks comprehensive world statistics:
- Total hexes generated and settlement count
- Population distribution and largest settlements
- Terrain type distribution with percentages
- Settlement type breakdown
- Number of user-edited hexes

## File Storage

### World Save Format
Complete world states saved as JSON with:
- World seed and campaign information
- All generated hex data
- Current viewport position
- Global world state and timeline

### Edit Data Storage
User edits stored individually:
```
saves/edits/{world_seed}/
├── {world_seed}_+0000_+0000.json  # Edit for hex (0,0)
├── {world_seed}_+0015_-0007.json  # Edit for hex (15,-7)
└── ...
```

## Future Expansion Framework

The architecture supports planned features:

### AI Integration Points
- Hex description generation based on terrain and settlements
- NPC dialogue and personality generation
- Dynamic story events and consequences

### GURPS Rule Integration
- Movement point calculations based on terrain
- Skill checks for exploration actions
- Combat system integration
- Character progression tracking

### Media System
- Image galleries for hex locations
- Audio ambient tracks for terrain types
- Settlement music and sound effects
- Player-uploaded content support

### Advanced Game Features
- Encounter tables with terrain-specific creatures
- NPC lifecycle with organizational role replacement
- Trade route development between settlements
- Seasonal and weather effects
- Campaign timeline with world-changing events

## Performance Considerations

### Memory Management
- **Lazy Loading**: Hexes generated only when viewport approaches
- **Buffer System**: Maintains loaded hexes in rings around viewport
- **Efficient Storage**: Individual JSON files prevent loading entire world

### Scalability
- **Deterministic Generation**: Same coordinates always produce same content
- **Infinite Worlds**: No size limitations on world exploration
- **Modular Loading**: Only active viewport area kept in memory

## Development Guidelines

### Code Standards
- **PEP 8 Compliance**: All code follows Python style guidelines
- **DRY Principles**: Common functionality abstracted into reusable components
- **Type Hints**: Comprehensive type annotations for clarity
- **Documentation**: Detailed docstrings for all public methods

### Testing Strategy
- **Seed Consistency**: Verify same seeds produce identical worlds
- **UI Responsiveness**: Ensure smooth performance during world generation
- **Data Integrity**: Validate save/load functionality preserves all data
- **Cross-Platform**: Test Unicode symbol rendering across different systems

The current implementation provides a solid foundation for a sophisticated hex-based exploration game with room for extensive future expansion into AI-driven content and advanced game mechanics.