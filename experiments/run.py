"""Contoh: python -m experiments.run --exp E1 --sizes 1000 10000 --repeats 5."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path

from src.services.benchmark_service import EXPERIMENTS, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exp", choices=EXPERIMENTS, required=True)
    parser.add_argument("--sizes", type=int, nargs="+", required=True)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=Path, default=Path("experiments/results"))
    args = parser.parse_args()
    frame = run_experiment(args.exp, sorted(set(args.sizes)), args.repeats)
    args.output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    prefix = args.output / f"{args.exp}_{stamp}"
    frame.to_csv(prefix.with_suffix(".csv"), index=False, encoding="utf-8-sig")
    environment = {
        "python": platform.python_version(), "os": platform.platform(),
        "processor": platform.processor(), "logical_cpus": os.cpu_count(),
        "ram": "Isi kapasitas RAM secara manual pada laporan",
        "libraries": {name: importlib.metadata.version(name)
                      for name in ("streamlit", "pandas", "altair", "pytest")},
        "seed": 42, "experiment": args.exp, "sizes": args.sizes,
        "repeats": args.repeats, "warmup": 1, "statistic": "median",
        "memory": "Satu run terpisah; setup/index awal tidak termasuk",
    }
    prefix.with_suffix(".json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
    print(frame.to_string(index=False))
    print(f"\nTersimpan: {prefix.with_suffix('.csv')} dan metadata JSON")


if __name__ == "__main__":
    main()
