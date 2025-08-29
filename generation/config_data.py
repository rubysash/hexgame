"""
generation/config_data.py - Settlement and Terrain Generation data
"""

from data.models import TerrainType, SettlementType

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

# Terrain-based name suffixes  
TERRAIN_SUFFIXES = {
    TerrainType.PLAINS: [
        "field", "meadow", "haven", "vale", "stead", "moor", "lea", "flat", "pasture", "heath",
        "acre", "croft", "down", "plain", "steppe", "wold", "reach", "ward", "bank", "steadings",
        "pastoral", "farm", "lands", "commons", "ham", "wick", "bury", "holm", "gard", "steadholm",
        "holt", "staddle", "glebe", "hollow", "park", "ranch", "grange", "manor", "run", "steadwell",
        "town", "steadgate", "low", "rise", "furlong", "outlands", "fen", "knoll", "brae"
    ],

    TerrainType.FOREST: [
        "wood", "grove", "glade", "hollow", "thicket", "brake", "shaw", "copse", "holt", "spinney",
        "boscage", "chase", "frith", "den", "hurst", "shawden", "glens", "shade", "clearing", "stand",
        "timber", "wilds", "warren", "burrow", "dell", "fen", "marshwood", "briar", "thornwood", "hedge",
        "mire", "holtwood", "lair", "fallow", "watch", "fastness", "woodlands", "brambles", "overgrowth",
        "roots", "underwood", "deepwood", "sylva", "groveland", "twilight", "sward", "feywood", "elderwood"
    ],

    TerrainType.HILLS: [
        "hill", "ridge", "crest", "tor", "mount", "down", "fell", "barrow", "knoll", "tump",
        "brae", "bluff", "escarp", "rise", "heights", "slopes", "crag", "ledge", "overlook", "scaur",
        "rock", "stones", "head", "copsehill", "dun", "fort", "butte", "mound", "knap", "cairn",
        "watch", "seat", "brow", "slope", "cliff", "perch", "spine", "outcrop", "ridgeway", "upland",
        "heaf", "drift", "uplift", "ledgehold", "wildrise", "torfell", "ridgehold", "barrows", "summit"
    ],

    TerrainType.MOUNTAINS: [
        "peak", "fell", "crag", "stone", "hold", "gate", "pass", "spire", "pinnacle", "ridge",
        "summit", "crown", "crest", "horn", "head", "fang", "tooth", "spiregate", "tor", "berg",
        "rock", "buttress", "fastness", "fort", "bastion", "citadel", "keep", "dome", "spirehold",
        "spirefell", "highlands", "palisade", "spirewall", "rampart", "overlook", "ridgekeep", "barrier",
        "heights", "massif", "wildpeak", "gatecrag", "mount", "spirestone", "ridgefort", "stonewall",
        "frosthold", "stormpeak", "dragonspire", "ancienthold"
    ],

    TerrainType.WATER: [
        "ford", "bridge", "port", "bay", "crossing", "mouth", "dock", "wharf", "harbor", "haven",
        "jetty", "quay", "marsh", "lagoon", "estuary", "delta", "inlet", "gulf", "loch", "mere",
        "brook", "stream", "run", "falls", "cascade", "spring", "fountain", "rapids", "shoals", "pool",
        "reach", "channel", "strait", "current", "deep", "shallows", "sands", "beach", "shore", "cliffs",
        "isle", "islet", "atoll", "reef", "sound", "flow", "wash", "drift"
    ],

    TerrainType.DESERT: [
        "well", "springs", "rest", "sanctuary", "refuge", "shade", "rock", "gulch", "dune", "waste",
        "expanse", "flat", "salt", "basin", "sink", "pan", "gorge", "bluff", "cliff", "ridge",
        "hearth", "outcrop", "oasis", "mirage", "mirrors", "winds", "sunlands", "glass", "burn",
        "crust", "sands", "dunes", "stone", "drylands", "steppe", "arid", "lowlands", "scarp",
        "barren", "scour", "ravine", "scrub", "drought", "ash", "ashes", "hollow", "scar", "spire",
        "fane", "bones"
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
        "Brook", "Beck", "Pool", "Well", "Cross", "Howe", "Row", "Hill", "Holt", "Shaw",
        "Wood", "Hatch", "Bridge", "Fell", "Barrow", "Stone", "Gate", "Wall", "Hall", "Stead",
        "Croft", "Holme", "Dale", "Down", "Bend", "Spring", "Burn", "Grange"
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