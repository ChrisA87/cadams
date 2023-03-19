from datetime import datetime


def to_json_safe(value):
    match value:
        case datetime():
            return value.isoformat()
    return value
