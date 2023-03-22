SAFE_DIC =[
        {'danya':'1000kV', "person":8.7, "car": 13},
        {'danya':'220kV', "person":3, "car": 6},
        {'danya':'500kV', "person":5, "car": 8.5}
        ]


def get_safe(dianya):
    for d in SAFE_DIC:
        if dianya == d['danya']:
            return d
    return None