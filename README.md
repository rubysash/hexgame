# Hex Explorer - Infinite World with Settlements

A hex-based exploration and role-playing game featuring procedural world generation, settlement systems, and interactive hex editing. The world generates infinite terrain and settlements following realistic geographic rules, with a built-in editor for customization.

![Hex Explorer Demo](https://github.com/rubysash/hexgame/blob/main/mvp-demo.png?raw=true)

## Core Features

###  Infinite World Generation
- **Procedural Terrain**: Six terrain types (Plains, Forest, Hills, Mountains, Water, Desert) generated using neighbor-based logic
- **Realistic Geography**: Mountains cluster together, rivers flow logically, deserts avoid water
- **Settlement System**: 12 settlement types from farmsteads to cities, with ruins and specialty camps
- **Seed-Based Consistency**: Same seed always generates the same world

###  Dynamic Settlement System
- **Population Simulation**: Each settlement has realistic population ranges and prosperity levels
- **Terrain-Appropriate Placement**: Logging camps in forests, mining camps in mountains, ports near water
- **Special Features**: Markets, temples, blacksmiths, and other features based on settlement size
- **Trade Goods**: Settlements produce appropriate goods (timber from logging camps, ore from mines)
- **Naming System**: Procedural names using terrain-appropriate prefixes and suffixes

###  Interactive Hex Editor
- **Custom Names**: Override procedural names with custom titles
- **Rich Descriptions**: Add detailed descriptions and notes to any hex
- **Exploration Tracking**: Mark hexes as explored with different exploration levels
- **Media Support**: Framework for adding images and audio (future expansion)
- **Persistent Storage**: All edits saved as individual JSON files

### 🎮 Game Controls
- **Arrow Keys**: Navigate the world
- **Shift + Arrow**: Fast movement
- **Right-Click/E**: Open hex editor for the hovered hex
- **Space**: Reset to world origin (0,0)
- **N**: Toggle settlement name display
- **I**: Toggle settlement icon display
- **L**: Toggle terrain legend
- **P**: Toggle settlement summary panel
- **T**: Toggle world statistics panel
- **G**: Print detailed world statistics to console
- **Ctrl+S**: Save world state
- **Ctrl+L**: Load world state

## Technical Architecture

### Core Systems
- **World Management** (`core/world.py`): Manages global world state and coordinates all generation systems
- **Hex Grid Mathematics** (`core/hex_grid.py`): Handles hexagonal coordinate system and conversions
- **Viewport System** (`core/viewport.py`): Manages memory-efficient loading of visible hexes
- **Terrain Generation** (`generation/terrain_generator.py`): Creates realistic terrain using weighted neighbor influences
- **Settlement Generation** (`generation/settlement_generator.py`): Places and configures settlements based on terrain

### Data Layer
- **Hex Data Model** (`data/models.py`): Complete hex data structure with terrain, settlements, and discovery tracking
- **Edit Data System** (`data/hex_editor.py`): Manages user customizations and overrides
- **World Persistence** (`data/persistence.py`): Save/load functionality for complete world states

### User Interface
- **Main Game Window** (`ui/game_window.py`): PyGame-based main interface with viewport and controls
- **Hex Renderer** (`ui/renderer.py`): Handles visual rendering of hexes, settlements, and Unicode symbols
- **UI Panels** (`ui/panels.py`): Information displays, legends, and settlement summaries
- **Hex Editor** (`ui/hex_editor_window.py`): Tkinter-based popup editor for hex customization

### Game Mechanics
- **Exploration System** (`mechanics/exploration.py`): Discovery mechanics and visibility rules
- **Movement System** (`mechanics/movement.py`): Movement costs and pathfinding framework

## World Generation Rules

### Terrain Logic
Each terrain type has specific generation weights and neighbor preferences:

- **Plains**: Clusters moderately, likes forest neighbors, avoids mountains
- **Forest**: Strong clustering, enhanced by water proximity, incompatible with desert
- **Hills**: Transition zones, enhanced by mountain neighbors
- **Mountains**: Strong clustering, creates natural barriers
- **Water**: Lakes and rivers following elevation rules
- **Desert**: Clusters strongly, avoids water and forest

### Settlement Placement
Settlement generation follows realistic density and placement rules:

- **Density**: Rural areas have 1 village per 2-4 hexes, cities are rare (1 per 50-100 hexes)
- **Resource Access**: Settlements prefer water access, logging camps need forests
- **Terrain Suitability**: Each settlement type has preferred terrain types
- **Population Ranges**: From farmsteads (5-20) to cities (2000-10000)

## Configuration and Seeding

### Seed System
World generation supports multiple seed input methods:
1. Command line: `python main.py --seed "MyWorld"`
2. Environment variable: `HEX_WORLD_SEED=12345`
3. String seeds are deterministically hashed for consistency
4. Random generation if no seed specified

### File Structure
```
hex_explorer/
├── saves/                  # World save files
│   └── edits/             # Individual hex edit files
├── core/                  # Core game engine
├── data/                  # Data models and persistence
├── generation/            # Procedural generation systems
├── mechanics/             # Game mechanics (exploration, movement)
├── ui/                    # User interface components
├── config.py              # Global configuration
└── main.py               # Application entry point
```

## Current Status

The game currently implements:
- ✅ Infinite procedural world generation
- ✅ Realistic terrain clustering and transitions
- ✅ Complete settlement system with 12 settlement types
- ✅ Interactive hex editing with persistent storage
- ✅ Memory-efficient viewport system
- ✅ Save/load functionality for world states
- ✅ Comprehensive UI with multiple information panels
- ✅ Unicode symbol support for settlement display

### Planned Features
- 🔄 GURPS rule integration for movement and exploration
- 🔄 AI-generated descriptions and narratives
- 🔄 Encounter system with terrain-based tables
- 🔄 NPC and creature lifecycle management
- 🔄 Media support (images and audio) in hex editor
- 🔄 Campaign timeline and world events

## Getting Started

1. **Install Dependencies**: Ensure pygame and tkinter are installed
2. **Run the Game**: `python main.py`
3. **Optional Seed**: `python main.py --seed "YourWorldName"`
4. **Explore**: Use arrow keys to navigate, right-click hexes to edit
5. **Save/Load**: Use Ctrl+S/Ctrl+L to save and load world states

## Development

The codebase follows PEP 8 standards and DRY principles with:
- **Modular Architecture**: Clear separation of concerns across modules
- **Type Hints**: Comprehensive type annotations for better code clarity
- **Configurable Settings**: All game parameters centralized in `config.py`
- **Extensible Design**: Easy to add new terrain types, settlement types, or mechanics

Each hex is approximately 6 miles across, creating a realistic scale for medieval fantasy exploration and settlement density.