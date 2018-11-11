filter_cols = ['base_mr']

cont_variables = [
    'agi_gain',
    'attack_range',
    'attack_rate',
    'base_agi',
    'base_armor',
    'base_attack_max',
    'base_attack_min',
    'base_health_regen',
    'base_int',
    'base_mr',
    'base_str',
    'int_gain',
    'legs',
    'move_speed',
    'pro_ban',
    'pro_pick',
    'pro_win',
    'projectile_speed',
    'str_gain',
    'turn_rate',
]

unique_roles = [
    'Carry',
    'Disabler',
    'Durable',
    'Escape',
    'Initiator',
    'Jungler',
    'Nuker',
    'Pusher',
    'Support'
]

unique_primary_attrs = [
    'agi',
    'int',
    'str'
]

feature_names = cont_variables + \
    ['min_' + col for col in cont_variables if col not in filter_cols] + \
    ['max_' + col for col in cont_variables if col not in filter_cols] + [
        'no_agi',
        'no_int',
        'no_str',
        'no_melees',
        'no_Carry',
        'no_Disabler',
        'no_Durable',
        'no_Escape',
        'no_Initiator',
        'no_Jungler',
        'no_Nuker',
        'no_Pusher',
        'no_Support',
    ]
