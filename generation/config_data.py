"""
generation/config_data.py - Settlement and Terrain Generation data
"""

from data.models import TerrainType, SettlementType

# Settlement symbol and color mapping
SETTLEMENT_SYMBOLS = {
    SettlementType.FARMSTEAD: "¤",   # small enclosed mark, evokes a homestead or plot of land
    SettlementType.HAMLET: "h",      # lowercase, simple and small
    SettlementType.VILLAGE: "v",     # lowercase, slightly larger grouping
    SettlementType.TOWN: "◎",        # circle with center, hub of activity
    SettlementType.CITY: "✪",        # star inside circle, major stronghold
    SettlementType.LOGGING_CAMP: "λ", # tree-like shape for logging
    SettlementType.MINING_CAMP: "⛏", # pickaxe symbol, mining
    SettlementType.MONASTERY: "†",   # cross, religious settlement
    SettlementType.WATCHTOWER: "♖",  # rook, tower/fortified structure
    SettlementType.RUINS_VILLAGE: "≈", # broken lines, scattered ruins
    SettlementType.RUINS_KEEP: "☓",    # crossed box, destroyed keep
    SettlementType.ANCIENT_RUINS: "⚑", # tattered flag, ancient fallen site
}

SETTLEMENT_COLORS = {
    SettlementType.FARMSTEAD: (200, 200, 200),      # Light gray
    SettlementType.HAMLET: (200, 200, 200),         # Light gray
    SettlementType.VILLAGE: (200, 200, 200),        # Light gray
    SettlementType.TOWN: (255, 255, 255),           # White for major settlements
    SettlementType.CITY: (255, 255, 255),           # White for major settlements
    SettlementType.LOGGING_CAMP: (184, 134, 11),    # Dark goldenrod for camps
    SettlementType.MINING_CAMP: (184, 134, 11),     # Dark goldenrod for camps
    SettlementType.MONASTERY: (147, 112, 219),      # Light purple
    SettlementType.WATCHTOWER: (255, 100, 100),     # Light red
    SettlementType.RUINS_VILLAGE: (105, 105, 105),  # Gray for ruins
    SettlementType.RUINS_KEEP: (105, 105, 105),     # Gray for ruins
    SettlementType.ANCIENT_RUINS: (105, 105, 105),  # Gray for ruins
}

# Settlement density by terrain (chance per hex)
SETTLEMENT_CHANCES = {
    TerrainType.PLAINS: 0.40,     # Was 0.15
    TerrainType.FOREST: 0.20,     # Was 0.08
    TerrainType.HILLS: 0.30,      # Was 0.12
    TerrainType.MOUNTAINS: 0.10,  # Was 0.05
    TerrainType.WATER: 0.45,      # Was 0.18
    TerrainType.DESERT: 0.05,     # Was 0.02
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

# Terrain-based name prefixes
TERRAIN_PREFIXES = {
    TerrainType.PLAINS: [
        "Green", "Golden", "Fair", "Old", "New", "Dead Man", "Dry", "Raining", "Thunder", "Bandit",
        "Broad", "Rich", "High", "Clear", "Tall", "Wide", "Long", "Open", "Great", "Boundless",
        "Saw", "Reed", "Thatch", "Wheat", "Barley", "Rye", "Grass", "Steppe", "Prairie", "Clover",
        "Heather", "Ash", "Oak", "Elm", "Alder", "Willow", "Beech", "Birch", "Maple", "Hazel",
        "Deer", "Hart", "Stag", "Elk", "Ox", "Bull", "Wolf", "Jackal", "Hound", "Hare", "Fox",
        "Snake", "Viper", "Serpent", "Lark", "Hawk", "Bison", "Horse", "Raven", "Crow",
        "East", "West", "North", "South", "Dawn", "Sunset", "Midday", "Star", "Sun", "Bright",
        "Blue", "Wind", "Storm", "Mana", "Withered", "Shadow", "Giant", "Fey", "Blood", "Ghost",
        "Wraith", "Traveler's", "Lost", "Forsaken"
    ],

    TerrainType.FOREST: [
        "Deep", "Dark", "Green", "Wild", "Hidden", "Lost", "Ancient", "Whispering", "Shadow", "Elder",
        "Wolf", "Boar", "Stag", "Hunter's", "Fey", "Spider", "Serpent", "Owl", "Raven", "Crow",
        "Thorn", "Briar", "Ash", "Oak", "Elm", "Alder", "Willow", "Beech", "Birch", "Maple", "Hazel",
        "Dead Man's", "Cursed", "Haunted", "Moon", "Star", "Sun", "Storm", "Misty", "Foggy", "Enchanted",
        "Dragon", "Goblin", "Bandit", "Witch", "Withered", "Gnarled", "Silent", "Burning", "Blood"
    ],

    TerrainType.HILLS: [
        "High", "Stone", "Wind", "Rolling", "Bright", "Crown", "Eagle", "Hawk", "Raven", "Wolf",
        "Fox", "Boar", "Deer", "Stag", "Serpent", "Dragon", "Storm", "Thunder", "Sunset", "Dawn",
        "Moon", "Star", "Grass", "Heather", "Briar", "Thorn", "Ash", "Oak", "Elm", "Willow",
        "Beech", "Birch", "Maple", "Hazel", "Iron", "Silver", "Gold", "Copper", "Bronze",
        "Cursed", "Lost", "Haunted", "Fey", "Withered", "Traveler's", "Old", "New"
    ],

    TerrainType.MOUNTAINS: [
        "Iron", "Stone", "Peak", "Ridge", "Snow", "Storm", "Dragon", "Thunder", "Lightning", "Cloud",
        "Grim", "Dark", "Shadow", "Frost", "Ice", "Frozen", "Fire", "Ash", "Blood", "Skull",
        "Dead Man's", "Cursed", "Haunted", "Dwarven", "Giant", "Goblin", "Orc", "Troll", "Wraith",
        "Wolf", "Eagle", "Hawk", "Raven", "Vulture", "Serpent", "Wyrm", "Silver", "Gold", "Copper",
        "Crystal", "Gem", "Star", "Moon", "Sun", "Dawn", "Dusk", "Forsaken", "Broken", "Shattered",
        "Withered", "Ancient"
    ],

    TerrainType.WATER: [
        "River", "Lake", "Ford", "Bridge", "Harbor", "Bay", "Shore", "Salt", "Deep", "Dark",
        "Blue", "Green", "Black", "Silver", "Golden", "Crystal", "Frozen", "Storm", "Thunder",
        "Lightning", "Whirlpool", "Foam", "Mist", "Fog", "Moon", "Sun", "Star", "Tide", "Wave",
        "Dragon", "Serpent", "Kraken", "Leviathan", "Mermaid's", "Siren's", "Pirate's", "Fisher's",
        "Dead Man's", "Cursed", "Haunted", "Lost", "Forgotten", "Ancient", "Fey", "Mana", "Withered"
    ],

    TerrainType.DESERT: [
        "Sand", "Sun", "Dry", "Lost", "Mirage", "Bone", "Dune", "Ash", "Scorch", "Red", "Glass", "Dust",
        "Stone", "Salt", "Cracked", "Burning", "Blistering", "Dead", "Forsaken", "Cursed", "Haunted",
        "Phantom", "Ghost", "Wraith", "Nomad's", "Traveler's", "Lost Man's", "Serpent", "Scorpion",
        "Viper", "Jackal", "Hyena", "Buzzard", "Oasis", "Well", "Spring", "Moon", "Sunset", "Dawn",
        "Star", "Ancient", "Withered", "Shattered", "Bleached", "Bonewhite"
    ]
}

# Terrain-Based Name Suffixes  
TERRAIN_SUFFIXES = {
    TerrainType.PLAINS: [
        "Field", "Meadow", "Haven", "Vale", "Stead", "Moor", "Lea", "Flat", "Pasture", "Heath",
        "Acre", "Croft", "Down", "Plain", "Steppe", "Wold", "Reach", "Ward", "Bank", "Steadings",
        "Pastoral", "Farm", "Lands", "Commons", "Ham", "Wick", "Bury", "Holm", "Gard", "Steadholm",
        "Staddle", "Glebe", "Hollow", "Park", "Ranch", "Grange", "Manor", "Run", "Steadwell",
        "Town", "Steadgate", "Low", "Rise", "Furlong", "Outlands", "Fen", "Knoll", "Brae"
    ],

    TerrainType.FOREST: [
        "Wood", "Grove", "Glade", "Hollow", "Thicket", "Brake", "Shaw", "Copse", "Spinney",
        "Boscage", "Chase", "Frith", "Den", "Hurst", "Shawden", "Glens", "Shade", "Clearing", "Stand",
        "Timber", "Wilds", "Warren", "Burrow", "Dell", "Fen", "Marshwood", "Briar", "Thornwood", "Hedge",
        "Mire", "Straightwood", "Lair", "Fallow", "Watch", "Fastness", "Woodlands", "Brambles", "Overgrowth",
        "Roots", "Underwood", "Deepwood", "Sylva", "Groveland", "Twilight", "Sward", "Feywood", "Elderwood"
    ],

    TerrainType.HILLS: [
        "Hill", "Ridge", "Crest", "Tor", "Mount", "Down", "Fell", "Barrow", "Knoll", "Tump",
        "Brae", "Bluff", "Escarp", "Rise", "Heights", "Slopes", "Crag", "Ledge", "Overlook", "Scaur",
        "Rock", "Stones", "Head", "Copsehill", "Dun", "Fort", "Butte", "Mound", "Knap", "Cairn",
        "Watch", "Seat", "Brow", "Slope", "Cliff", "Perch", "Spine", "Outcrop", "Ridgeway", "Upland",
        "Heaf", "Drift", "Uplift", "Ledgehold", "Wildrise", "Torfell", "Ridgehold", "Barrows", "Summit"
    ],

    TerrainType.MOUNTAINS: [
        "Peak", "Fell", "Crag", "Stone", "Hold", "Gate", "Pass", "Spire", "Pinnacle", "Ridge",
        "Summit", "Crown", "Crest", "Horn", "Head", "Fang", "Tooth", "Spiregate", "Tor", "Berg",
        "Rock", "Buttress", "Fastness", "Fort", "Bastion", "Citadel", "Keep", "Dome", "Spirehold",
        "Spirefell", "Highlands", "Palisade", "Spirewall", "Rampart", "Overlook", "Ridgekeep", "Barrier",
        "Heights", "Massif", "Wildpeak", "Gatecrag", "Mount", "Spirestone", "Ridgefort", "Stonewall",
        "Frosthold", "Stormpeak", "Dragonspire", "Ancienthold"
    ],

    TerrainType.WATER: [
        "Ford", "Bridge", "Port", "Bay", "Crossing", "Mouth", "Dock", "Wharf", "Harbor", "Haven",
        "Jetty", "Quay", "Marsh", "Lagoon", "Estuary", "Delta", "Inlet", "Gulf", "Loch", "Mere",
        "Brook", "Stream", "Run", "Falls", "Cascade", "Spring", "Fountain", "Rapids", "Shoals", "Pool",
        "Reach", "Channel", "Strait", "Current", "Deep", "Shallows", "Sands", "Beach", "Shore", "Cliffs",
        "Isle", "Islet", "Atoll", "Reef", "Sound", "Flow", "Wash", "Drift"
    ],

    TerrainType.DESERT: [
        "Well", "Springs", "Rest", "Sanctuary", "Refuge", "Shade", "Rock", "Gulch", "Dune", "Waste",
        "Expanse", "Flat", "Salt", "Basin", "Sink", "Pan", "Gorge", "Bluff", "Cliff", "Ridge",
        "Hearth", "Outcrop", "Oasis", "Mirage", "Mirrors", "Winds", "Sunlands", "Glass", "Burn",
        "Crust", "Sands", "Dunes", "Stone", "Drylands", "Steppe", "Arid", "Lowlands", "Scarp",
        "Barren", "Scour", "Ravine", "Scrub", "Drought", "Ash", "Ashes", "Hollow", "Scar", "Spire",
        "Fane", "Bones"
    ]
}

# Settlement-type specific suffixes
SETTLEMENT_SUFFIXES = {
    SettlementType.FARMSTEAD: [
        "Farm", "Stead", "Homestead", "Ranch", "Croft", "Holding", "Pasture", "Barn", "Fold", "Paddock",
        "Stable", "Grange", "Byre", "Outstead", "Tillage", "Dairy", "Fieldstead", "Sheepfold", "Haystead", "Granary",
        "Millstead", "Thresh", "Piggeries", "Manorstead", "Oxstead", "Cartstead", "Ploughstead", "Cottage", "Lodge", "Lean-to",
        "Ham", "Acrestead", "Yard", "Garth", "Byfarm", "Longstead", "Roodstead", "Shieling", "Shedstead", "Hearthstead",
        "Penstead", "Hovel", "House", "Hallstead", "Kraal", "Outpost", "Steading", "Stableyard"
    ],

    SettlementType.HAMLET: [
        "Hamlet", "Grove", "Glen", "Corner", "Thorp", "Hame", "Nook", "Clachan", "Crook", "Cot",
        "Cote", "Fold", "End", "Row", "Cross", "Wick", "Wich", "Heath", "Lea", "Brook",
        "Beck", "Hollow", "Sted", "Ness", "Croft", "Barrow", "Bend", "Dale", "Holm", "Stead",
        "Yard", "Pightle", "Hill", "Lane", "Mere", "Marsh", "Fen", "Mead", "Low", "Edge",
        "Green", "Drift", "Ridge", "Nest", "Shade", "Gate", "Leys", "Wood"
    ],

    SettlementType.VILLAGE: [
        "Village", "Borough", "Green", "Commons", "Ton", "Sted", "Wick", "Worth", "Wich", "Ford",
        "Ham", "Ferry", "Market", "Yard", "Field", "Lea", "Thwaite", "Kirk", "Minster", "Ness",
        "Brook", "Beck", "Pool", "Well", "Cross", "Howe", "Row", "Hill", "Weed", "Shaw",
        "Wood", "Hatch", "Bridge", "Fell", "Barrow", "Stone", "Gate", "Wall", "Hall", "Stead",
        "Croft", "Holme", "Dale", "Down", "Bend", "Spring", "Burn", "Grange", "Wood"
    ],

    SettlementType.TOWN: [
        "Town", "Market", "Cross", "Mills", "Gate", "Bridge", "Ford", "Port", "Bay", "Harbor",
        "Yard", "Hall", "Square", "Circle", "Court", "Road", "Row", "Street", "Well", "Fountain",
        "Tower", "Keep", "Stone", "Wall", "Watch", "House", "Temple", "Church", "Guild", "Exchange",
        "Mint", "Bazaar", "Dock", "Quay", "Wharf", "Fort", "Castle", "Depot", "Granary", "Vault",
        "Barracks", "Arena", "Theatre", "Garden", "Manor", "Ward", "Quarter", "Plaza"
    ],

    SettlementType.CITY: [
        "City", "Keep", "Hold", "Fortress", "Citadel", "Castle", "Bastion", "Stronghold", "Palisade", "Bulwark",
        "Dome", "Hall", "Tower", "Gate", "Spire", "Temple", "Shrine", "Cathedral", "Vault", "Forum",
        "Market", "Exchange", "Court", "Palace", "Sanctum", "Arena", "Theatre", "Colonnade", "Bridge", "Aqueduct",
        "Wall", "Arch", "Citadelgate", "Highhall", "Stonegate", "Keepgate", "Ward", "Quarter", "Circle", "Square",
        "Manor", "Guildhall", "Library", "Archive", "Observatory", "Monument", "Obelisk", "Colossus"
    ],

    SettlementType.LOGGING_CAMP: [
        "Camp", "Lodge", "Mill", "Clearing", "Cabin", "Hut", "Shanty", "Shack", "Bunkhouse", "Yard",
        "Depot", "Timberyard", "Sawpit", "Sawmill", "Stump", "Coppice", "Hold", "Hutment", "Lean-to", "Campstead",
        "Outcamp", "Logstead", "Woodpile", "Stockpile", "Millstead", "Fell", "Notch", "Grove", "Trailhead", "Firebreak",
        "Palisade", "Fort", "Gate", "Landing", "Dock", "Ramp", "Trestle", "Bridge", "Road", "Track",
        "Path", "Lumberyard", "Backcut", "Crosscut", "Shingle", "Chopstead", "Cleaver", "Splitter"
    ],

    SettlementType.MINING_CAMP: [
        "Mine", "Quarry", "Delve", "Shaft", "Pit", "Tunnel", "Drift", "Stope", "Gallery", "Face",
        "Cut", "Diggings", "Spoil", "Tailings", "Heap", "Workings", "Forge", "Smelter", "Foundry", "Mint",
        "Orehouse", "Store", "Depot", "Camp", "Hollow", "Chasm", "Cleft", "Clough", "Crevasse", "Adits",
        "Cave", "Grotto", "Vault", "Chamber", "Hall", "Forgegate", "Hammer", "Anvil", "Smokeworks", "Ironworks",
        "Copperworks", "Goldstead", "Silverstead", "Coalpit", "Stonecut", "Rockbreak", "Orestead", "Deepstead"
    ],

    SettlementType.MONASTERY: [
        "Abbey", "Monastery", "Priory", "Sanctuary", "Hermitage", "Chapel", "Cloister", "Shrine", "Temple", "Church",
        "Basilica", "Cathedral", "Convent", "Friary", "Oratory", "Minster", "Parish", "Chapterhouse", "Hospice", "Sacristy",
        "Sanctum", "Reliquary", "Hall", "Altar", "Crypt", "Catacomb", "Mausoleum", "Shrinehold", "Refuge", "Retreat",
        "Sanctuarygate", "Pilgrimage", "Processional", "Choir", "Choirhouse", "Liturgy", "Prayerhall", "Scriptorium", "Sacredwell", "Blessing",
        "Font", "Holywell", "Martyrstead", "Angelspire", "Saintstead", "Relicstead", "Reliquaryhall", "Penance"
    ],

    SettlementType.WATCHTOWER: [
        "Watch", "Tower", "Guard", "Beacon", "Keep", "Turret", "Spire", "Fort", "Fortlet", "Lookout",
        "Overlook", "Bastion", "Bulwark", "Outpost", "Signal", "Bell", "Drum", "Fire", "Torch", "Light",
        "Lighthouse", "Lantern", "Pharos", "Citadel", "Garrison", "Blockhouse", "Redoubt", "Palisade", "Stockade", "Wall",
        "Rampart", "Barbican", "Portcullis", "Gate", "Arch", "Gatehouse", "Fortress", "Guardhouse", "Barracks", "Defile",
        "Sentinel", "Cairn", "Monolith", "Obelisk", "Marker", "Pillar", "Post", "Stone"
    ]
}