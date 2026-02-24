# client.py

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from planet_overlap.filters import build_filters
from planet_overlap.geometry import load_aoi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_filters(
    geojson_paths: List[str],
    date_ranges: List[Tuple[str, str]],
) -> Dict:
    """
    Build filters for multiple AOIs and date ranges.

    Args:
        geojson_paths: List of file paths to AOI GeoJSONs.
        date_ranges: List of (start_date, end_date) tuples
        as strings.

    Returns:
        Dictionary containing combined filters.
    """
    # Convert string dates to datetime tuples
    parsed_ranges: List[Tuple[datetime, datetime]] = [
        (
            datetime.strptime(start, "%Y-%m-%d"),
            datetime.strptime(end, "%Y-%m-%d"),
        )
        for start, end in date_ranges
    ]

    filters = build_filters(geojson_paths, parsed_ranges)

    logger.info(
        "Filters prepared for %d AOIs/date ranges",
        len(parsed_ranges),
    )

    return filters


def load_aois(geojson_paths: List[str]):
    """
    Load AOIs from GeoJSON files.

    Args:
        geojson_paths: List of AOI GeoJSON paths.

    Returns:
        List of AOI geometries.
    """
    # load_aoi expects List[str | Path]
    path_objects: List[Path] = [Path(p) for p in geojson_paths]

    aois = load_aoi(path_objects)

    logger.info("Loaded %d AOIs", len(aois))

    return aois


def run_client(
    geojson_paths: List[str],
    date_ranges: List[Tuple[str, str]],
):
    """
    Full client workflow: load AOIs, prepare filters.

    Args:
        geojson_paths: List of AOI GeoJSON paths.
        date_ranges: List of (start_date, end_date) tuples.

    Returns:
        Tuple of (filters dict, list of AOI geometries)
    """
    aois = load_aois(geojson_paths)
    filters = prepare_filters(geojson_paths, date_ranges)

    logger.info("Client run complete")

    return filters, aois
