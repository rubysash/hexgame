# Hex Explorer - Infinite World with Settlements

A hex-based exploration and role-playing game featuring procedural world generation, settlement systems, and interactive hex editing. The world generates infinite terrain and settlements following realistic geographic rules, with a built-in editor for customization.

Designed to assist with gameplay for various RPG games, especially written for solo GURPS play/storywriting.

![Hex Explorer Demo](https://github.com/rubysash/hexgame/blob/main/demo/demo.v01.gif?raw=true)

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

### Game Controls

Planned and working controls

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


## Current Status

The game currently implements:
- ✅ Infinite procedural world generation
- ✅ Realistic terrain clustering and transitions
- ✅ Complete settlement system with 12 settlement types
- ✅ Interactive hex editing with persistent storage
- ✅ Memory-efficient viewport system
- ✅ Comprehensive UI with multiple information panels
- ✅ Unicode symbol support for settlement display

## Getting Started

1. **Install Dependencies**: 
```
git clone git@github.com:rubysash/hexgame.git
python -m venv hexgame
cd hexgame
scripts\activate
python -m pip install pip --upgrade pip
python -m pip install -r requirements.txt
```
2. **Run the Game**: `start.bat or python main.py`
3. **Optional Seed**: `python main.py --seed "YourWorldName"`
4. **Explore**: Use arrow keys to navigate, right-click hexes to edit
5. **Edit**: Right click a hex to edit that hex.   Use same seed to see edits.

## Development

The codebase follows PEP 8 standards and DRY principles with:

- **Modular Architecture**: Clear separation of concerns across modules
- **Type Hints**: Comprehensive type annotations for better code clarity
- **Configurable Settings**: All game parameters centralized in `config.py`
- **Extensible Design**: Easy to add new terrain types, settlement types, or mechanics

Each hex is designed to be 1 mile approximately.    It is labeled as it's dominant biome feature.    Mountains can still have streams and forests for example, but it's a mountain.

## Future Planned Notes

### Next Update Focus

Encounter tables such as boars in a forest, caves in a mountain, cougar in mountains, etc

### World Story Arcs

These are planned data points that will influence and interact with world creation.

- Hierarchical relationships (parent organizations, sub-factions)
- Influence zones (which hexes/settlements are controlled/influenced)
- Relationship matrices (ally/enemy/neutral between factions)
- Timeline events (how these organizations change over time)
- Settlement affiliations (which settlements belong to which factions)

### GM Controls

A client-server architecture where the GM runs the authoritative world instance and clients receive viewport updates where the GM pushes camera positions to force client views.  The idea being that a remote GM could explain things to a party, and bring up a battle map when required.

### Needs attention

- Save/load functionality for world states (needs attention)

### Random Thoughts

Things I want to accomplish in the code, but haven't gotten to yet.  Don't want to forget the ideas.

- print viewable section as html+javascript interaction for player references/demo
- GURPS rule integration for various aspects
- AI-generated descriptions and narratives
- Encounter system with terrain-based tables
- NPC and creature lifecycle management
- Media support (images and audio) in hex editor
- Campaign timeline and world events
- Search field for keywords, populations, trades, npcs, etc
- clickable search results zoom to
- clickable "top 3" zoom to
- mousewheel zoom in/out keybind
- audio/image ambience defaults + special edits
- images  vs just background color on hexes
- Change outline color or image if explored, exploration tracker
- random encounters listed with gurps stats
- gurps combat, with easy to use selectors
- edit hex can place "specials"
- verify ruins, watchtowers, etc in pool
- verify all keybinds work, rethink useful keybinds.
- sliders on population density and thinking through how it affects seed (will need seed + settings to recreate)
- click hex, new map appears as expanded detail (cities, dungeons etc can be generated/static)
- create/use character based on GURPS
