#!/usr/bin/env python3
"""Acquire official source files for the emergency-access study.

The script preserves downloaded archives, extracts analysis-readable members,
copies the two population assets reused from KE01, and writes a checksum
manifest.  It is intentionally separate from later preprocessing: after this
script finishes, ``data/raw/emergency_access`` should be treated as immutable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "emergency_access"
DEFAULT_KE01_ROOT = PROJECT_ROOT.parent / "KE01"


@dataclass(frozen=True)
class Source:
    key: str
    provider: str
    title: str
    url: str
    filename: str
    role: str
    reference_year: str
    extract: bool = False


SOURCES = (
    Source(
        "mlit_ksj_n03_2025_kumamoto",
        "MLIT KSJ",
        "Administrative areas, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N03/N03-2025/N03-20250101_43_GML.zip",
        "N03-20250101_43_GML.zip",
        "Clip road meshes and aggregate results by municipality",
        "2025-01-01",
        True,
    ),
    Source(
        "mlit_ksj_p04_2020_kumamoto",
        "MLIT KSJ",
        "Medical institutions, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/P04/P04-20/P04-20_43_GML.zip",
        "P04-20_43_GML.zip",
        "Hospital emergency/disaster designation baseline",
        "2020",
        True,
    ),
    Source(
        "mlit_ksj_p17_2012_kumamoto",
        "MLIT KSJ",
        "Fire stations and jurisdictions, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/P17/P17-12/P17-12_43_GML.zip",
        "P17-12_43_GML.zip",
        "Candidate ambulance dispatch bases",
        "2012",
        True,
    ),
    Source(
        "mlit_ksj_n10_2024_kumamoto",
        "MLIT KSJ",
        "Emergency transport roads, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N10/N10-24/N10-24_43_GML.zip",
        "N10-24_43_GML.zip",
        "Designated emergency road hierarchy",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_n13_2024_mesh_4829",
        "MLIT KSJ",
        "Road centerlines, mesh 4829",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N13/N13-24/N13-24_4829_GEOJSON.zip",
        "N13-24_4829_GEOJSON.zip",
        "Primary routable road-network input",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_n13_2024_mesh_4830",
        "MLIT KSJ",
        "Road centerlines, mesh 4830",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N13/N13-24/N13-24_4830_GEOJSON.zip",
        "N13-24_4830_GEOJSON.zip",
        "Primary routable road-network input",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_n13_2024_mesh_4831",
        "MLIT KSJ",
        "Road centerlines, mesh 4831",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N13/N13-24/N13-24_4831_GEOJSON.zip",
        "N13-24_4831_GEOJSON.zip",
        "Primary routable road-network input",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_n13_2024_mesh_4930",
        "MLIT KSJ",
        "Road centerlines, mesh 4930",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N13/N13-24/N13-24_4930_GEOJSON.zip",
        "N13-24_4930_GEOJSON.zip",
        "Primary routable road-network input",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_n13_2024_mesh_4931",
        "MLIT KSJ",
        "Road centerlines, mesh 4931",
        "https://nlftp.mlit.go.jp/ksj/gml/data/N13/N13-24/N13-24_4931_GEOJSON.zip",
        "N13-24_4931_GEOJSON.zip",
        "Primary routable road-network input",
        "2024",
        True,
    ),
    Source(
        "mlit_ksj_a33_2025_kumamoto",
        "MLIT KSJ",
        "Landslide disaster warning zones, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/A33/A33-25/A33-25_43_GEOJSON.zip",
        "A33-25_43_GEOJSON.zip",
        "Road-disruption susceptibility overlay",
        "2025",
        True,
    ),
    Source(
        "mlit_ksj_p20_2012_kumamoto",
        "MLIT KSJ",
        "Evacuation facilities, Kumamoto",
        "https://nlftp.mlit.go.jp/ksj/gml/data/P20/P20-12/P20-12_43_GML.zip",
        "P20-12_43_GML.zip",
        "Context only; newer KE01 shelter data remains preferred",
        "2012",
        True,
    ),
    Source(
        "mhlw_hospital_facility_20260601",
        "MHLW",
        "Hospital facility information, nationwide",
        "https://www.mhlw.go.jp/content/11121000/01-1_hospital_facility_info_20260601.csv.zip",
        "hospital_facility_info_20260601.csv.zip",
        "Current hospital identity, location and bed capacity",
        "2026-06-01",
        True,
    ),
    Source(
        "mhlw_hospital_speciality_hours_20260601",
        "MHLW",
        "Hospital specialties and consultation hours, nationwide",
        "https://www.mhlw.go.jp/content/11121000/01-2_hospital_speciality_hours_20260601.csv.zip",
        "hospital_speciality_hours_20260601.csv.zip",
        "Optional hospital service-availability extension",
        "2026-06-01",
        True,
    ),
    Source(
        "fdma_fire_organizations_2024",
        "FDMA",
        "Fire organization status by prefecture",
        "https://www.fdma.go.jp/publication/hakusho/r6/files/excel/shiryo2-1-2.csv",
        "fdma_fire_organizations_2024.csv",
        "Validate completeness of P17 fire-facility points",
        "2024",
    ),
    Source(
        "kumamoto_current_hospitals",
        "Kumamoto Prefecture",
        "Current hospital list",
        "https://www.pref.kumamoto.jp/uploaded/attachment/283141.xlsx",
        "kumamoto_current_hospitals.xlsx",
        "Validate current hospital roster",
        "2026",
    ),
    Source(
        "kumamoto_healthcare_plan_2024_2029",
        "Kumamoto Prefecture",
        "Eighth Kumamoto Prefecture Healthcare Plan",
        "https://www.pref.kumamoto.jp/uploaded/life/202905_529962_misc.pdf",
        "kumamoto_healthcare_plan_2024_2029.pdf",
        "Validate emergency and disaster medical institution roles",
        "2024-2029",
    ),
)

KE01_ASSETS = (
    (
        "kumamoto_population_mesh_125m_preprocessed.parquet",
        "kumamoto_population_mesh_125m.parquet",
        "125 m population mesh for patient-demand origins",
    ),
    (
        "kumamoto_population_disclosure_groups_preprocessed.parquet",
        "kumamoto_population_disclosure_groups.parquet",
        "Disclosure groups containing population age 65+",
    ),
)

EXTRACT_SUFFIXES = {".csv", ".dbf", ".geojson", ".prj", ".shp", ".shx", ".xml"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def acquire(url: str, destination: Path, seed_dir: Path | None) -> str:
    if destination.exists():
        return "existing"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if seed_dir is not None:
        candidate = seed_dir / destination.name
        if candidate.exists():
            shutil.copy2(candidate, destination)
            return "seed-copy"
    request = urllib.request.Request(url, headers={"User-Agent": "KE01b-research/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out)
    return "downloaded"


def extract_selected(archive: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            basename = Path(member.filename).name
            if not basename or Path(basename).suffix.lower() not in EXTRACT_SUFFIXES:
                continue
            target = destination / basename
            with bundle.open(member) as source, target.open("wb") as out:
                shutil.copyfileobj(source, out)
            extracted.append(str(target.relative_to(RAW_ROOT)))
    return sorted(set(extracted))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-dir", type=Path, help="Optional directory containing cached downloads")
    parser.add_argument("--ke01-root", type=Path, default=DEFAULT_KE01_ROOT)
    args = parser.parse_args()

    downloads = RAW_ROOT / "downloads"
    extracted_root = RAW_ROOT / "extracted"
    population_root = RAW_ROOT / "prior_ke01"
    manifest: list[dict[str, object]] = []

    for source in SOURCES:
        target = downloads / source.filename
        acquisition = acquire(source.url, target, args.seed_dir)
        extracted: list[str] = []
        if source.extract:
            extracted = extract_selected(target, extracted_root / source.key)
        record = asdict(source)
        record.update(
            {
                "local_path": str(target.relative_to(PROJECT_ROOT)),
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
                "acquisition": acquisition,
                "extracted_files": extracted,
            }
        )
        manifest.append(record)
        print(f"{source.key}: {acquisition} ({target.stat().st_size:,} bytes)")

    population_root.mkdir(parents=True, exist_ok=True)
    for source_filename, destination_filename, role in KE01_ASSETS:
        source_path = args.ke01_root / "data" / "processed" / source_filename
        if not source_path.exists():
            raise FileNotFoundError(f"Missing reusable KE01 asset: {source_path}")
        destination = population_root / destination_filename
        if not destination.exists():
            shutil.copy2(source_path, destination)
            acquisition = "local-copy"
        else:
            acquisition = "existing"
        manifest.append(
            {
                "key": f"prior_ke01_{destination.stem}",
                "provider": "KE01 project",
                "title": destination.stem,
                "url": str(source_path.resolve()),
                "filename": destination_filename,
                "role": role,
                "reference_year": "KE01 output",
                "extract": False,
                "local_path": str(destination.relative_to(PROJECT_ROOT)),
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
                "acquisition": acquisition,
                "extracted_files": [],
            }
        )
        print(f"prior_ke01_{destination.stem}: {acquisition} ({destination.stat().st_size:,} bytes)")

    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW_ROOT / "source_manifest.json"
    manifest_path.write_text(
        json.dumps({"schema_version": 1, "sources": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
