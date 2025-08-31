
# ============================================================================
# MINIMUM VIABLE PRODUCT CHECKLIST
# ============================================================================

"""
MVP FEATURES (Phase 1):
=======================
1. Basic hex grid with coordinate system [hex_grid.py]
2. Simple terrain generation with logical rules [terrain_gen.py]
3. File-based hex data storage [persistence.py]
4. Viewport with adjacent-only movement [viewport.py, movement.py]
5. Basic UI showing hex map and control panel [main_window.py]

MVP Implementation Order:
1. Create HexCoordinate and HexGrid classes
2. Implement basic TerrainGenerator with simple rules
3. Build HexData model with JSON serialization
4. Create simple text/console UI for testing
5. Add Viewport for memory management
6. Implement movement validation
7. Build basic pygame/tkinter UI
8. Add save/load functionality

TERRAIN GENERATION RULES FOR MVP:
=================================
- Use neighbor-based probability weights
- Mountains cluster (30% mountain if neighbor is mountain)
- Water flows downhill (rivers from mountains to plains)
- Forests avoid deserts
- Gradual transitions (no desert next to tundra)

Next Phases:
- Phase 2: AI integration for descriptions
- Phase 3: GURPS combat system
- Phase 4: Advanced world simulation
"""
