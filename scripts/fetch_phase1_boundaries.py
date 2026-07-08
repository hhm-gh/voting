#!/usr/bin/env python3
"""Download Phase 1 boundary files into data/raw/.

Sources are documented in docs/data-sources.md. This script only downloads
raw files as distributed by the source (mostly Shapefile ZIPs, one GeoJSON
API query) and writes a provenance.json sidecar per dataset — it does not
parse, convert, or otherwise process anything (see OVERVIEW.md's
Architecture section: raw stays untouched, Python owns retrieval/storage).

Usage: python3 scripts/fetch_phase1_boundaries.py
"""

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
USER_AGENT = "voting-project-research/1.0 (personal research project)"

DATASETS = [
    {
        "name": "congressional",
        "cycle": "2021",
        "source_page": "https://redistricting.colorado.gov/content/congressional-final-approved",
        "license": "Colorado state government data (public)",
        "files": {
            "2021_Approved_Congressional_Plan_with_Final_Adjustments.zip": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcjBEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--e091bab0fdcc0944ce431ca5708665efb8263228/"
                "2021_Approved_Congressional_Plan_with_Final_Adjustments.zip"
            ),
            "2021_Approved_Congressional_Plan_w_Final_Adjustments.txt": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcjREIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--68c6991842e7dd5bbe287f4ed557e92720c84666/"
                "2021_Approved_Congressional_Plan_w_Final_Adjustments.txt"
            ),
        },
    },
    {
        "name": "state_senate",
        "cycle": "2021",
        "source_page": "https://redistricting.colorado.gov/content/senate-final-approved-errata",
        "license": "Colorado state government data (public)",
        "note": (
            "Use the errata page, not senate-final-approved: that one serves "
            "2021_Final_Approved_Senate_Plan.zip, a differently-named file that "
            "doesn't match the _w_Final_Adjustments pattern the Congressional "
            "and House pages use. The errata page's filename does match, "
            "confirming it's the corrected version consistent with the other "
            "two chambers."
        ),
        "files": {
            "2021_Approved_Senate_Plan_w_Final_Adjustments.zip": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBc0VEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--3e163d6928a7c388874e81cb0dda49ee2b644d33/"
                "2021_Approved_Senate_Plan_w_Final_Adjustments.zip"
            ),
            "2021_Approved_Senate_Plan_w_Final_Adjustments.txt": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBc0lEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--f18cc7e43a16e5051ca0fb102481bca0f25a574e/"
                "2021_Approved_Senate_Plan_w_Final_Adjustments.txt"
            ),
        },
    },
    {
        "name": "state_house",
        "cycle": "2021",
        "source_page": "https://redistricting.colorado.gov/content/house-final-approved",
        "license": "Colorado state government data (public)",
        "files": {
            "2021_Approved_House_Plan_w_Final_Adjustments.zip": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcjhEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--ce9e9fcf6b39c1f7d8ea318e727d1e0ca8f19a92/"
                "2021_Approved_House_Plan_w_Final_Adjustments.zip"
            ),
            "2021_Approved_House_Plan_w_Final_Adjustments.txt": (
                "https://redistricting.colorado.gov/rails/active_storage/blobs/redirect/"
                "eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBc0FEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19"
                "--744738d13feb9f9b4ea15914d1f76101fddedc56/"
                "2021_Approved_House_Plan_w_Final_Adjustments.txt"
            ),
        },
    },
    {
        "name": "counties",
        "cycle": "2024",
        "source_page": "https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=Counties+%28and+equivalent%29",
        "license": "US Census Bureau TIGER/Line (public domain)",
        "note": "National file, all US counties — filter to STATEFP=08 (Colorado) during processing.",
        "files": {
            "tl_2024_us_county.zip": "https://www2.census.gov/geo/tiger/TIGER2024/COUNTY/tl_2024_us_county.zip",
        },
    },
    {
        "name": "denver_council_districts",
        "cycle": "2024",
        "source_page": "https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-council-districts",
        "license": (
            "City and County of Denver — USE CONSTRAINTS: provided as-is, "
            "not for engineering purposes (see source page for full text)"
        ),
        "note": (
            "Fetched directly from the live ArcGIS FeatureServer "
            "(ODC_ADMN_COUNCILDIST_A, layer 3) rather than scraping a download "
            "button, since the Hub page is a JS app with no static download link."
        ),
        "files": {
            "denver_council_districts.geojson": (
                "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/"
                "ODC_ADMN_COUNCILDIST_A/FeatureServer/3/query"
                "?where=1%3D1&outFields=*&f=geojson"
            ),
        },
    },
]


def fetch(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return len(data)


def main() -> None:
    for dataset in DATASETS:
        dir_path = RAW_DIR / dataset["name"] / dataset["cycle"]
        provenance = {
            "source_page": dataset["source_page"],
            "license": dataset["license"],
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "files": {},
        }
        if "note" in dataset:
            provenance["note"] = dataset["note"]

        for filename, url in dataset["files"].items():
            dest = dir_path / filename
            print(f"[{dataset['name']}] downloading {filename} ...")
            size = fetch(url, dest)
            print(f"[{dataset['name']}] saved {dest} ({size:,} bytes)")
            provenance["files"][filename] = {"url": url, "size_bytes": size}

        (dir_path / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        print(f"[{dataset['name']}] wrote provenance.json\n")


if __name__ == "__main__":
    main()
