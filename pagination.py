import logging
import time
import requests
from tqdm import tqdm
from datetime import datetime
from typing import Dict
from .geometry import load_aois, generate_tiles
from .client import create_session
from .filters import build_filters


def fetch_with_retry(session, url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            time.sleep(2 ** attempt)

    raise RuntimeError(f"Failed after {retries} retries: {url}")


def run_pagination(aoi_files,
                   output_dir,
                   start_date,
                   end_date,
                   max_cloud,
                   min_sun_angle,
                   tile_size_deg,
                   point_buffer_deg):

    session = create_session()

    aois = load_aois(aoi_files, point_buffer_deg)

    # Conditional tiling
    date_span = (datetime.fromisoformat(end_date)
                 - datetime.fromisoformat(start_date)).days

    if date_span > 30:
        logging.info("Date range > 30 days, applying tiling")
        tiles = generate_tiles(aois, tile_size_deg)
    else:
        tiles = aois

    logging.info(f"Processing {len(tiles)} spatial units")

    for tile in tqdm(tiles, desc="Processing AOI tiles"):
        # Placeholder API call
        logging.info(f"Would query tile bounds: {tile.bounds}")
