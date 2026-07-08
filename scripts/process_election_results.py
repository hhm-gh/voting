#!/usr/bin/env python3
"""Convert raw election results into data/processed/ working formats.

Currently handles the one results dataset downloaded so far: MEDSL's
2000-2016 county-level presidential returns. Filters to Colorado, derives a
5-digit GEOID matching the county boundaries' GEOID (data/processed/counties)
for joining, and writes a tidy Parquet — same raw-vs-processed split as
scripts/process_phase1_boundaries.py.

Usage: uv run python3 scripts/process_election_results.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "election_results"
PROCESSED = ROOT / "data" / "processed" / "election_results"


def process_president_county() -> None:
    name, cycle = "president_county", "2000-2016"
    src = RAW / name / cycle / "countypres_2000-2016.csv"
    print(f"[{name}] reading {src}")

    df = pd.read_csv(src, encoding="latin-1", dtype={"FIPS": "Int64"})
    co = df[df["state_po"] == "CO"].copy()
    co["geoid"] = co["FIPS"].apply(lambda x: f"{x:05d}")
    co = co.rename(columns={"county": "county_name"})
    co = co[
        ["year", "geoid", "county_name", "office", "candidate", "party",
         "candidatevotes", "totalvotes"]
    ]

    out_dir = PROCESSED / name / cycle
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "results.parquet"
    co.to_parquet(out_path, index=False)

    print(
        f"[{name}] wrote {len(co)} rows, {co['geoid'].nunique()} counties, "
        f"years={sorted(co['year'].unique().tolist())}"
    )
    print(f"[{name}] -> {out_path.relative_to(ROOT)}\n")


def main() -> None:
    process_president_county()


if __name__ == "__main__":
    main()
