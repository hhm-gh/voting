#!/usr/bin/env python3
"""Convert Phase 1 raw boundary files into data/processed/ working formats.

Reads the Shapefile/GeoJSON bundles in data/raw/ (see
scripts/fetch_phase1_boundaries.py) and writes each as both GeoParquet and
GeoPackage into data/processed/<dataset>/<cycle>/ — GeoParquet is the
primary processed format per OVERVIEW.md's Architecture section, GeoPackage
is written alongside it as the documented fallback, so we have a real answer
on which one R's `sf` actually prefers rather than guessing.

All layers are reprojected to EPSG:4326 (WGS84 lat/lon) for interoperability
— the source files use a mix of projected Colorado State Plane and native
Census CRSes. Counties are filtered to STATEFP == '08' (Colorado) as flagged
in data/raw/counties/2024/provenance.json.

Usage: uv run python3 scripts/process_phase1_boundaries.py
"""

from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TARGET_CRS = "EPSG:4326"

DATASETS = [
    {
        "name": "congressional",
        "cycle": "2021",
        "path": (
            "zip://" + str(RAW / "congressional" / "2021"
                / "2021_Approved_Congressional_Plan_with_Final_Adjustments.zip")
            + "!2021_Approved_Congressional_Plan_with_Final_Adjustments/"
            "2021_Approved_Congressional_Plan_w_Final_Adjustments.shp"
        ),
    },
    {
        "name": "state_senate",
        "cycle": "2021",
        "path": (
            "zip://" + str(RAW / "state_senate" / "2021"
                / "2021_Approved_Senate_Plan_w_Final_Adjustments.zip")
            + "!2021_Approved_Senate_Plan_w_Final_Adjustments/"
            "2021_Approved_Senate_Plan_w_Final_Adjustments.shp"
        ),
    },
    {
        "name": "state_house",
        "cycle": "2021",
        "path": (
            "zip://" + str(RAW / "state_house" / "2021"
                / "2021_Approved_House_Plan_w_Final_Adjustments.zip")
            + "!2021_Approved_House_Plan_w_Final_Adjustments/"
            "2021_Approved_House_Plan_w_Final_Adjustments.shp"
        ),
    },
    {
        "name": "counties",
        "cycle": "2024",
        "path": "zip://" + str(RAW / "counties" / "2024" / "tl_2024_us_county.zip") + "!tl_2024_us_county.shp",
        "filter": lambda gdf: gdf[gdf["STATEFP"] == "08"],
    },
    {
        "name": "denver_council_districts",
        "cycle": "2024",
        "path": str(RAW / "denver_council_districts" / "2024" / "denver_council_districts.geojson"),
    },
]


def main() -> None:
    for dataset in DATASETS:
        print(f"[{dataset['name']}] reading {dataset['path']}")
        gdf = gpd.read_file(dataset["path"])

        if "filter" in dataset:
            before = len(gdf)
            gdf = dataset["filter"](gdf)
            print(f"[{dataset['name']}] filtered {before} -> {len(gdf)} rows")

        gdf = gdf.to_crs(TARGET_CRS)

        out_dir = PROCESSED / dataset["name"] / dataset["cycle"]
        out_dir.mkdir(parents=True, exist_ok=True)

        parquet_path = out_dir / "boundaries.geoparquet"
        gpkg_path = out_dir / "boundaries.gpkg"

        gdf.to_parquet(parquet_path)
        gdf.to_file(gpkg_path, driver="GPKG")

        print(
            f"[{dataset['name']}] wrote {len(gdf)} features, CRS={gdf.crs.to_string()}, "
            f"columns={list(gdf.columns)}"
        )
        print(f"[{dataset['name']}] -> {parquet_path.relative_to(ROOT)}, {gpkg_path.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
