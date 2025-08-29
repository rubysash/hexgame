# Core Architecture Components

## 1. Data Layer Architecture
Hex Data Structure

Static World Data: Immutable terrain, biomes, major landmarks, climate zones
Dynamic State Data: Current conditions, temporary effects, seasonal changes
Discovery State: What's been revealed through exploration vs. what remains hidden
Interaction History: Previous encounters, changes made by player actions

### Data Persistence Strategy

World Definition Files: JSON files defining the base world (terrain, major features)
Discovery Database: SQLite or JSON files tracking exploration progress
Session State: Current game state, player position, active effects
Backup/Versioning: Save states for different campaign moments

## 2. Content Generation Framework

### Layered Content System

Base Layer: Geographic features (mountains, rivers, forests)
Biome Layer: Ecosystem types that influence encounters
Civilization Layer: Settlements, roads, territories, political boundaries
Dynamic Layer: Weather, seasonal effects, temporary events
Mystery Layer: Hidden secrets, dungeons, special locations

### Content Categories to Design

Terrain Types: Each with movement costs, visibility ranges, encounter tables
Settlement Types: Villages, cities, ruins - each with different interaction possibilities
Encounter Tables: Creature types by biome/terrain combination
Resource Types: Materials, treasures, magical items
Weather/Environmental Effects: How they modify encounters and movement

## 3. Exploration Mechanics Framework

### Visibility and Movement Rules

Adjacent-only movement: Prevents teleportation, creates natural exploration flow
Visibility ranges: Some hexes might be visible but not explorable until you get closer
Terrain-based movement costs: Different terrains take different amounts of "time" to traverse
Line of sight: Hills/mountains might reveal distant hexes without full exploration

### Discovery Progression System

Initial Survey: Basic terrain type visible from adjacent hexes
Surface Exploration: Reveals obvious features, common encounters
Deep Exploration: Requires time investment, reveals hidden features
Seasonal Revisits: Same hex might have different content in different seasons

## 4. AI Integration Architecture

### Knowledge Base Structure

World Bible: Core lore, major NPCs, historical events, political situations
Dynamic Context: Current world state, recent player actions, ongoing storylines
Encounter Templates: Structured prompts for different encounter types
Consistency Rules: Guidelines to maintain narrative coherence

### API Integration Points

Pre-encounter Generation: Create encounters when hexes are first explored
Real-time Narrative: Generate descriptions and NPC dialogue during play
Consequence Processing: How player actions affect future encounters
Story Arc Management: Tracking and advancing longer narrative threads

## 5. Rule System Integration

### GURPS-Compatible Framework

Skill Check Integration: When exploration requires specific skills
Combat Encounter Scaling: Adjust difficulty based on party capabilities
Character Progression Tracking: How exploration contributes to advancement
Equipment/Resource Management: Weight, durability, supply consumption

### Random Generation Tables

Encounter Probability: By terrain type, time of day, weather conditions
Treasure Generation: Appropriate to location and encounter difficulty
NPC Generation: Quick stats and motivations for random encounters
Environmental Hazards: Natural dangers appropriate to each biome

## 6. User Interface Considerations

### Map Display Features

Zoom Levels: Regional overview down to individual hex detail
Layer Toggles: Show/hide different information types
Annotation System: Player notes, markers, waypoints
Path Planning: Visual route planning with movement cost calculation

### Data Management Interface

Hex Detail Panels: Expandable information display
Search/Filter Functions: Find specific locations or encounter types
Export Functions: Generate reports, share discoveries
Backup Management: Save/load different campaign states

## Implementation Phases

### Phase 1: Foundation

Basic hex grid with coordinate system
Simple JSON data storage for hex properties
Adjacent-movement validation
Basic terrain type display

### Phase 2: Content System

Encounter table framework
Dynamic content generation
Discovery state tracking
Simple AI API integration for descriptions

### Phase 3: Advanced Features

Weather and seasonal systems
Complex encounter chains
NPC relationship tracking
Campaign timeline management

### Phase 4: Full Integration

Complete GURPS rule integration
Advanced AI storytelling
Multi-campaign support
Sharing/collaboration features

## Key Design Decisions to Consider

Scalability: How large do you want your world? This affects data storage and loading strategies.
Randomness vs. Authorial Control: Balance between procedural generation and hand-crafted content.
Player Agency: How much should players be able to modify the world permanently?
Campaign Continuity: How to handle world changes across multiple play sessions or different parties.
Performance: Large hex grids with rich data can become memory-intensive.
Would you like me to dive deeper into any of these areas, or shall we start working through the specific data structures you'll need for your hex content system?


## Window/Viewport Management SystemViewport Strategy

Active Grid Window: Load only hexes visible in current viewport (e.g., 21x21 hex grid for detail view)
Buffer Zone: Keep 1-2 hex rings around viewport loaded for smooth scrolling
Zoom Levels:

Regional (1 hex = large area, shows major terrain types)
Local (standard hex detail)
Tactical (if you want sub-hex detail later)


## Memory Management

Lazy Loading: Only load JSON when hex enters buffer zone
Unload Strategy: Remove hex data when it's 3+ rings outside viewport
Cache Recent: Keep recently visited hexes in memory longer
Preload Adjacent: When player moves, preload in movement direction


## Initial File Structure

```
/Worlds/
  /CampaignName/
    /world_config.json          # World generation settings, master data
    /party_state.json     # Current party position and status
    /hexes/
      /0000_0000.json          # Hex at coordinate 0,0
      /0001_0000.json          # Hex at coordinate 1,0
      /-0001_0002.json         # Negative coordinates supported
    /templates/
      /encounters/             # Encounter table templates
      /terrain/               # Terrain type definitions
      /creatures/             # Creature stat blocks
      /settlements/           # Settlement templates
    /campaign_state.json       # Current session, player position, global timers
    /world_timeline.json       # Major events, NPC death/respawn timers
```

## Initial Hex structure

To be adjusted as new data types are understood

```
{
  "coordinate": {"x": 0, "y": 0},
  "terrain": {
    "primary": "forest",
    "secondary": "hills",
    "special_features": ["ancient_ruins", "hidden_spring"]
  },
  "discovery": {
    "visible": true,
    "explored": false,
    "exploration_level": 0,  // 0=unexplored, 1=surface, 2=thorough
    "last_visited": "2024-03-15",
    "discovery_notes": []
  },
  "inhabitants": {
    "permanent": [
      {"id": "orc_tribe_001", "type": "orc_tribe", "status": "active", "population": 45}
    ],
    "temporary": [
      {"id": "traveling_merchant", "expires": "2024-03-20", "type": "merchant"}
    ],
    "respawn_queue": [
      {"original_id": "orc_chief_grimfang", "respawn_date": "2024-04-01", "replacement_type": "orc_chief"}
    ]
  },
  "resources": {
    "harvestable": ["iron_ore", "medicinal_herbs"],
    "treasure": [],
    "consumed": ["silver_vein"]  // Track what's been depleted
  },
  "encounters": {
    "recent": [],  // Track recent encounters to avoid repetition
    "scripted": [], // Special one-time events
    "tables": ["forest_day", "hills_generic"]  // Which encounter tables apply
  },
  "modifications": {
    "player_changes": [],  // Campsites, markers, cleared paths
    "environmental": [],   // Seasonal changes, disasters
    "history": []         // Major events that happened here
  }
}
```

## NPC/Creature Lifecycle System

### Death and Respawn Framework

Individual NPCs: Named characters stay dead unless special resurrection
Organizational Roles: Leadership positions get filled by new randomly generated characters
Population Groups: Tribes/settlements have resilience based on remaining population
Territory Preference: Each creature type has preferred terrain/biome weightings

### Respawn Logic

Immediate: Some creatures respawn quickly (bandits, wild animals)
Seasonal: Migrating creatures return at specific times
Conditional: Some require specific triggers (new orc chief needs 10+ orcs surviving)
Never: Unique NPCs, ancient guardians, plot-critical characters

```
// In world_timeline.json
{
  "events": [
    {
      "date": "2024-04-01",
      "type": "npc_respawn",
      "location": {"x": 5, "y": -3},
      "details": {
        "replacing": "orc_chief_grimfang",
        "new_name": "generated_on_trigger",
        "prerequisites_met": true
      }
    }
  ]
}
```

## File Management

Hex Exists Check: Before generating, check if JSON file exists
Partial Loading: Load only necessary sections for zoom level
Background Saving: Save modified hexes during idle moments
Error Recovery: Backup/restore for corrupted files

## Integration Points for Future Features

AI Story Generation Hooks

Context Building: Gather data from current hex + adjacent hexes + world state
Encounter Seeding: Use hex data to create appropriate AI prompts
Consistency Checking: Track AI-generated content to maintain world coherence

## GURPS Rule Integration Points

Movement Costs: Terrain-based travel time calculations
Encounter Difficulty: Scale based on party level and hex danger rating
Resource Management: Track supplies, equipment wear from terrain

## Campaign Management

Session Boundaries: Save complete world state between sessions
Multiple Parties: Different discovery states for different groups
Time Advancement: Global timeline affecting all hexes

Complete visibility into your world data while keeping memory usage manageable. Each hex is self-contained but references shared templates and world state. You can easily inspect, modify, or debug individual locations, and the system scales well as your world grows.


## UI Design

I'm thinking that a viewport for the hexes with a control panel of sorts on the right that lists the character(s) in the party and possibly a graphic associated with the encounter, table, or terrain.    

We could swap out the hex view port for a combat graphic if there is combat, etc.

We want logic in generation.    For example, a river wouldn't be in a desert.  MOuntains might clump together, then be foothills or rivers, and rivers would lead to lakes, etc.

Procedural Logic should follow something related to normal earth biomes

Basic Types: Plains, Forest, Hills, Mountains, Water, Desert

### Simple Rules:
- Water clusters (lakes, rivers)
- Mountains cluster with hills around edges
- Desert stays away from water
- Forest likes moderate areas
- Plains fill remaining space

### Mountain Rules:
- Mountains cluster together
- Generate foothills 1-2 hexes out from mountains
- Rivers originate in mountains
- Desert unlikely adjacent to mountains

### Water Rules:
- Rivers follow downhill paths (mountains → plains → lakes)
- Lakes form in low areas
- Rivers don't split (except deltas)
- Water bodies connect logically

### Climate Rules:
- Desert clusters together
- Forest avoids desert adjacency
- Swamps near water in warm areas
- Tundra at climate extremes

### Transition Rules:
- Gradual transitions (no desert next to snow)
- Elevation changes gradually
- Climate zones blend at edges

If neighbor is Forest: Forest=40%, Plains=30%, Hills=20%, Other=10%
If neighbor is Mountain: Hills=50%, Mountain=30%, Forest=15%, Other=5%
If neighbor is Water: Plains=40%, Forest=25%, Water=20%, Hills=15%

### Hex Numbering

The MVP is using colored hexes, but eventually we will use tile icons that have much greater detail.

```
// Hex file: 0015_0007.json (coordinates)
{
  "coordinate": {"x": 15, "y": 7},
  "display_id": "015007",  // Generated from your numbering system xxx + yyy
  "terrain": "forest",
  "ambience": "data/forests/forest1.mp3",
  "bg_images": ["001.png", "004.png"],
  "maps":  ["701.png", "714.png"],
  "specials": ["elves","rabid boars", "werewolves"],
  "settlement": "village of ratiki",
  // ... rest of hex data
}
```

## Non Terrain Features

### Density

Each hex is approxiamtely 6 miles.

Medieval Settlement Density
Based on historical medieval demographics:
Rural Areas (Plains/Forest):

1 village (200-800 people) per 2-4 hexes
2-6 farmsteads per hex
1 manor house per 1-2 hexes

### Resource-Rich Areas (Rivers/Crossroads):

1 town (800-3000 people) per 6-12 hexes
More frequent villages
Market towns at river crossings

### Cities (3000+ people):

Very rare - maybe 1 per 50-100 hexes
Always near major resources (rivers, harbors, trade routes)
Regional capitals, major ports, magical centers

### Ruins

LIke manors or farmsteads but with different content such as ghosts, necromancers, etc

### Cave Systems

TBD but would have a more monstrous table such as orcs, goblins, trolls, bears, dragons, etc

### Deep Forest Camps

TBD but could have a table of bandits, monsters, druids, etc

## Details of Non Terrain

Proposed to have UI "popup" when a hex is clicked.    User enters new UI with details such as a map/image of the area and notes.    This allows for cities/mines/ruins/caves/dungeons/camps to be generated or created and persistent with cohesive story lines.

