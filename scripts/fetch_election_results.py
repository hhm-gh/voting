#!/usr/bin/env python3
"""Download historical election results into data/raw/election_results/.

See docs/election-results-sources.md for the full picture — most sources
(MEDSL's Harvard Dataverse files, CO SoS's historical database, Denver's
Tableau dashboard) can't be scripted yet (gated behind a consent form or a
JS-rendered app with no discoverable API). This script only handles the one
source that's genuinely open: MEDSL's GitHub mirror of pre-2018 presidential
county returns.

Usage: python3 scripts/fetch_election_results.py
"""

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "election_results"
USER_AGENT = "voting-project-research/1.0 (personal research project)"

DATASETS = [
    {
        "name": "president_county",
        "cycle": "2000-2016",
        "source_page": "https://github.com/MEDSL/county-returns",
        "license": "MEDSL (MIT Election Data and Science Lab) — open GitHub mirror, no guestbook gate",
        "note": (
            "Unrestricted mirror of MEDSL's pre-2018 presidential county returns. "
            "Their post-2018 files and all House/Senate files are gated behind a "
            "Harvard Dataverse guestbook (name/email/institution/purpose) that "
            "can't be scripted around honestly — see docs/election-results-sources.md."
        ),
        "files": {
            "countypres_2000-2016.csv": (
                "https://raw.githubusercontent.com/MEDSL/county-returns/master/"
                "countypres_2000-2016.csv"
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
