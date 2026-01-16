# mappings.py

# Standard General MIDI (GM) to rhythm games notes (Expert)
# 96: Kick (Orange/Bar)
# 97: Snare (Red)
# 98: Yellow (Hi-Hat / High Tom)
# 99: Blue (Ride / Mid Tom)
# 100: Green (Crash / Floor Tom)

DRUM_MAPPING = {
    # Kicks
    35: 96, 36: 96,

    # Snares
    37: 97, 38: 97, 40: 97,

    # Toms (Yellow)
    48: 98, 50: 98,  # High Toms

    # Toms (Blue)
    45: 99, 47: 99,  # Low/Mid Toms

    # Toms (Green)
    41: 100, 43: 100,  # Floor Toms

    # Cymbals - Hi-Hat (Yellow)
    42: 98, 44: 98, 46: 98, 55: 98,

    # Cymbals - Ride (Blue)
    51: 99, 53: 99, 59: 99,

    # Cymbals - Crash (Green)
    49: 100, 52: 100, 57: 100
}

# Tom notes
IS_TOM = [
    48, 50,      # High Toms
    45, 47,      # Low/Mid Toms
    41, 43       # Floor Toms
]

# Tom markers map
TOM_MARKERS_MAP = {
    98: 110,
    99: 111,
    100: 112
}

# Humanization Priorities (Higher = Keep)
PRIORITY_MAP = {
    # Snares / Crashes (Keep these)
    38: 3, 40: 3, 49: 3, 57: 3,
    # Toms / Rides (Middle ground)
    51: 2, 59: 2, 41: 2, 43: 2, 45: 2, 47: 2, 48: 2, 50: 2, 
    # Hi-Hats (Drop first)
    42: 1, 44: 1, 46: 1
}

KICK_NOTES = {35, 36}

# Conflict Groups
# Green Collision: Crash vs Floor Tom
GREEN_CRASHES = {49, 52, 55, 57}
GREEN_TOMS = {41, 43}

# Blue Collision: Ride vs Mid Tom
BLUE_CYMBALS = {51, 53, 59} 
BLUE_TOMS = {45, 47}

# Target Colors for Displacement
BLUE_GEM = 99   # Target for displaced Green Tom
YELLOW_GEM = 98 # Target for displaced Blue Tom
GREEN_GEM = 100 # Target for displaced Blue Cymbal