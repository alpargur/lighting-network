colors = {
    'russianViolet': (36, 0, 70),
    'safetyOrange': (255, 121, 0),
    'carmineRed': (154, 3, 30),
    'midnightGreen': (15, 76, 92),
    'celeste': (192, 253, 255),
    'greenYellow': (175, 252, 65),
    'cornellRed': (164, 22, 26),
    'neonBlue': (67, 97, 238),
    'harvestGold': (236, 164, 0),
    'richBlack': (17, 14, 27),
}

drum_kit = {
    '51': {
        'name': 'ride',
        'color': colors['russianViolet'],
        'range': range(0, 6)
    },
    '44': {
        'name': 'low-tom',
        'color': colors['richBlack'],
        'range': range(6, 12)
    },
    '43': {
        'name': 'snare-drum',
        'color': colors['midnightGreen'],
        'range': range(12, 18)
    },
    '46': {
        'name': 'open-hi-hat',
        'color': colors['safetyOrange'],
        'range': range(18, 24)
    },
    '36': {
        'name': 'bass-drum',
        'color': colors['carmineRed'],
        'range': range(24, 30)
    },
    '49': {
        'name': 'crash',
        'color': colors['neonBlue'],
        'range': range(30, 36)
    },
    '47': {
        'name': 'high-tom',
        'color': colors['cornellRed'],
        'range': range(36, 42)
    },
    '39': {
        'name': 'clap',
        'color': colors['celeste'],
        'range': range(42, 48)
    },
    '37': {
        'name': 'rim-shot',
        'color': colors['harvestGold'],
        'range': range(48, 54)
    },
    '45': {
        'name': 'mid-tom',
        'color': colors['greenYellow'],
        'range': range(54, 60)
    },
}