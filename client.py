"""
cli.py
Command-line interface for planet_overlap.
Allows flexible AOI and date inputs, dynamic filters, and output configuration.
"""

import argparse
from pathlib import Path
from datetime import datetime
from planet_overlap import geometry, pagination, filters

def parse_args():
    parser = argparse.ArgumentParser(
        description="planet_overlap: Download and analyze PlanetScope imagery for specified AOIs and dates."
    )

    # AOI input
    parser.add_argument(
        "--aoi",
        nargs="+",
        required=True,
        help="Paths to AOI GeoJSON files or points (lon,lat) separated by space"
    )

    # Date inputs
    parser.add_argument(
        "--dates",
        nargs="+",
        required=True,
        help=(
            "Dates or date ranges. "
            "Single date: 2023-06-21 "
            "Range: 2023-06-01:2023-06-30 "
            "Multiple: 2023-06-01:2023-06-15 2023-07-01:2023-07-15"
        )
    )

    # Output directory
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./planet_output",
        help="Directory to save outputs"
    )

    # Quality settings
    parser.add_argument(
        "--max-cloud",
        type=float,
        default=0.5,
        help="Maximum cloud cover fraction (0.0-1.0)"
    )

    parser.add_argument(
        "--min-sun-angle",
        type=float,
        default=0.0,
        help="Minimum sun angle (degrees)"
    )

    # Optional buffer for point AOIs
    parser.add_argument(
        "--point-buffer",
        type=float,
        default=0.01,
        help="Buffer radius for point AOIs in degrees (~1km default)"
    )

    return parser.parse_args()


def parse_date_input(date_strings):
    """
    Converts CLI date inputs into (start, end) tuples.
    Handles single dates, ranges, and multiple ranges.
    """
    ranges = []
    for ds in date_strings:
        if ":" in ds:
            start_str, end_str = ds.split(":")
            start = datetime.strptime(start_str, "%Y-%m-%d")
            end = datetime.strptime(end_str, "%Y-%m-%d")
        else:
            start = end = datetime.strptime(ds, "%Y-%m-%d")
        ranges.append((start, end))
    return ranges


def prepare_aois(aoi_inputs, point_buffer=0.01):
    """
    Load AOIs and buffer points if needed.
    """
    polygons = []
    geojson_paths = []
    points = []

    for item in aoi_inputs:
        if "," in item:  # assume lon,lat
            lon, lat = map(float, item.split(","))
            points.append(geometry.Point(lon, lat))
        else:
            geojson_paths.append(item)

    # Load polygons from files
    if geojson_paths:
        polygons.extend(geometry.load_aoi(geojson_paths))

    # Buffer points
    if points:
        polygons.extend(geometry.buffer_points(points, buffer_deg=point_buffer))

    # Merge all AOIs into a single polygon
    final_aoi = geometry.unify_aois(polygons)
    return final_aoi


def main():
    args = parse_args()

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare AOIs
    final_aoi = prepare_aois(args.aoi, point_buffer=args.point_buffer)

    # Parse dates
    date_ranges = parse_date_input(args.dates)

    # Log configuration
    print(f"Output directory: {output_dir}")
    print(f"Max cloud: {args.max_cloud}, Min sun angle: {args.min_sun_angle}")
    print(f"AOI area (deg²): {final_aoi.area}")
    print(f"Date ranges: {date_ranges}")

    # Determine if tiling is needed
    total_days = sum((end - start).days + 1 for start, end in date_ranges)
    spatial_tile, temporal_tile = pagination.should_tile(final_aoi.area, total_days)
    print(f"Spatial tiling: {spatial_tile}, Temporal tiling: {temporal_tile}")

    # Build filters dynamically
    search_filters = filters.build_filters([final_aoi], date_ranges,
                                           max_cloud=args.max_cloud,
                                           min_sun_angle=args.min_sun_angle)

    print("Filters prepared and ready for pagination and analysis.")


if __name__ == "__main__":
    main()
