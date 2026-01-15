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
    38: 97, 40: 97, 37: 97, 
    
    # Toms (Yellow)
    48: 98, 50: 98, # High Toms
    
    # Toms (Blue)
    45: 99, 47: 99, # Low/Mid Toms
    
    # Toms (Green)
    41: 100, 43: 100, # Floor Toms
    
    # Cymbals - Hi-Hat (Yellow)
    42: 98, 44: 98, 46: 98,
    
    # Cymbals - Ride (Blue)
    51: 99, 59: 99, 53: 99,
    
    # Cymbals - Crash (Green)
    49: 100, 57: 100, 52: 100, 55: 100
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