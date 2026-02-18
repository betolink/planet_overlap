from typing import Dict

def build_filters(start_date: str,
                  end_date: str,
                  max_cloud: float) -> Dict:
    """
    Build Planet API search filter.
    """

    if not 0 <= max_cloud <= 1:
        raise ValueError("max_cloud must be between 0 and 1.")

    return {
        "type": "AndFilter",
        "config": [
            {
                "type": "DateRangeFilter",
                "field_name": "acquired",
                "config": {
                    "gte": f"{start_date}T00:00:00.000Z",
                    "lte": f"{end_date}T23:59:59.999Z"
                }
            },
            {
                "type": "RangeFilter",
                "field_name": "cloud_cover",
                "config": {"lte": max_cloud}
            }
        ]
    }
