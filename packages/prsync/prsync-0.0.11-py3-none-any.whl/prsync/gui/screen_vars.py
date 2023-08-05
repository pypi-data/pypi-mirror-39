rsync_options_bitwise = {
        "1": {
            "title": "verbose",
            "value": "-v",
            "default_value": 1,
            "element": None
        },
        "2": {
            "title": "archive",
            "value": "-a",
            "default_value": 1,
            "element": None
        },
        "4": {
            "title": "compress",
            "value": "-z",
            "default_value": 1,
            "element": None
        },
        "8": {
                "title": "dry-run",
                "value": "--dry-run",
                "default_value": 1,
                "element": None
        },
        "16": {
            "title": "recursive",
            "value": "-r",
            "default_value": 1,
            "element": None
        },

}

SUCCESS = "success" #green text log row
INFO = 'info' #blue one
ERROR = 'error' #red one