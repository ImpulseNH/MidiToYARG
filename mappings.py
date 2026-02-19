# =============================================================================
# 1. GENERAL MIDI / SHARED CONSTANTS
# =============================================================================
# Base MIDI Notes for Difficulties
# Base MIDI Notes for Difficulties
BASE_EXPERT = 96
BASE_HARD   = 84
BASE_MEDIUM = 72
BASE_EASY   = 60

# Lane Offsets (0-indexed from Left to Right / Kick to Orange)
LANE_0 = 0  # Green  / Kick
LANE_1 = 1  # Red    / Snare
LANE_2 = 2  # Yellow / Tom1 / HiHat
LANE_3 = 3  # Blue   / Tom2 / Ride
LANE_4 = 4  # Orange / Tom3 / Crash

# 5-Lane Guitar/Bass Mappings (Derived)
GEM_GREEN  = BASE_EXPERT + LANE_0
GEM_RED    = BASE_EXPERT + LANE_1
GEM_YELLOW = BASE_EXPERT + LANE_2
GEM_BLUE   = BASE_EXPERT + LANE_3
GEM_ORANGE = BASE_EXPERT + LANE_4

# =============================================================================
# 2. DRUMS MAPPINGS
# =============================================================================
# Drum Specific Aliases (Mapped to Lanes)
DRUM_KICK   = BASE_EXPERT + LANE_0
DRUM_SNARE  = BASE_EXPERT + LANE_1
DRUM_YELLOW = BASE_EXPERT + LANE_2
DRUM_BLUE   = BASE_EXPERT + LANE_3
DRUM_GREEN  = BASE_EXPERT + LANE_4

# Logical Groups (Used for Conflict Resolution & Identification)
YELLOW_TOMS = {48, 50}
BLUE_TOMS   = {45, 47}
GREEN_TOMS  = {41, 43}
ALL_TOMS    = YELLOW_TOMS | BLUE_TOMS | GREEN_TOMS

BLUE_CYMBALS  = {51, 53, 57, 59} # Added 57 (Crash 2) to Blue
GREEN_CYMBALS = {49, 52}         # Kept 49 (Main Crash) and 52 (China) in Green

DRUM_MAPPING = {
    # Kicks & Snares
    35: DRUM_KICK, 36: DRUM_KICK,
    37: DRUM_SNARE, 38: DRUM_SNARE, 40: DRUM_SNARE,
    
    # Toms (Yellow)
    48: DRUM_YELLOW, 50: DRUM_YELLOW,
    # Toms (Blue)
    45: DRUM_BLUE, 47: DRUM_BLUE,
    # Toms (Green)
    41: DRUM_GREEN, 43: DRUM_GREEN,

    # Cymbals - Hi-Hat (Yellow)
    42: DRUM_YELLOW, 44: DRUM_YELLOW, 46: DRUM_YELLOW, 55: DRUM_YELLOW,

    # Cymbals - Ride & Crash 2 (Blue)
    51: DRUM_BLUE, 53: DRUM_BLUE, 57: DRUM_BLUE, 59: DRUM_BLUE,

    # Cymbals - Crash 1 & China (Green)
    49: DRUM_GREEN, 52: DRUM_GREEN
}

# Derived Sets for Logic
KICK_NOTES = {35, 36}
SPLASH_NOTE = 55
IS_TOM = list(ALL_TOMS)

# Animation Markers
TOM_MARKERS_MAP = {
    DRUM_YELLOW: 110,
    DRUM_BLUE:   111,
    DRUM_GREEN:  112
}

# Humanization Priorities (Higher = Keep)
PRIORITY_MAP = {
    # Snares / Crashes (Priority 3)
    38:3, 40:3, 49:3, 57:3,
    
    # Rides / Toms (Priority 2)
    51:2, 59:2,                            # Rides
    41:2, 43:2, 45:2, 47:2, 48:2, 50:2,    # Toms
    
    # Hi-Hats (Priority 1)
    42:1, 44:1, 46:1
}

# =============================================================================
# 3. 5-LANE INSTRUMENTS CONFIG
# =============================================================================
PROG_GUITAR_MIN, PROG_GUITAR_MAX = 24, 31
PROG_BASS_MIN,   PROG_BASS_MAX   = 32, 39