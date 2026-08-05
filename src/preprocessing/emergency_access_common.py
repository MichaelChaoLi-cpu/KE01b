#!/usr/bin/env python3
"""Shared preprocessing functions for the emergency-access source datasets."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "emergency_access"
PROCESSED = ROOT / "data" / "processed"
TARGET_CRS = "EPSG:6668"


def _save(df: pd.DataFrame, filename: str) -> None:
    path = PROCESSED / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"Saved {len(df):,} rows x {len(df.columns)} cols -> {path.relative_to(ROOT)}")


def _strip(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})


def _code(series: pd.Series, width: int | None = None) -> pd.Series:
    out = _strip(series).str.replace(r"\.0$", "", regex=True)
    return out.str.zfill(width) if width else out


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(_strip(series).str.replace(",", "", regex=False), errors="coerce")


def _rename_geometry(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.geometry.name != "Geometry":
        gdf = gdf.rename_geometry("Geometry")
    return gdf


def _geo(path: Path, assumed_crs: str | None = None, **kwargs) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path, **kwargs)
    if gdf.crs is None:
        if assumed_crs is None:
            raise ValueError(f"CRS missing and no assumption supplied: {path}")
        gdf = gdf.set_crs(assumed_crs)
    return gdf.to_crs(TARGET_CRS)


def _add_labels(df: pd.DataFrame, code_col: str, label_col: str, labels: dict[int, str]) -> None:
    values = pd.to_numeric(df[code_col], errors="coerce").astype("Int64")
    df[code_col] = values
    df[label_col] = values.map(labels).astype("string")


def preprocess_administrative_areas() -> None:
    path = RAW / "extracted/mlit_ksj_n03_2025_kumamoto/N03-20250101_43.geojson"
    gdf = _geo(path).rename(columns={
        "N03_001": "Prefecture Name",
        "N03_002": "Subprefecture Name",
        "N03_003": "District Name",
        "N03_004": "Municipality Name",
        "N03_005": "Ward Name",
        "N03_007": "Municipality Code",
    })
    for col in ["Prefecture Name", "Subprefecture Name", "District Name", "Municipality Name", "Ward Name"]:
        gdf[col] = _strip(gdf[col])
    gdf["Municipality Code"] = _code(gdf["Municipality Code"], 5)
    gdf["Municipality Label"] = gdf["Municipality Name"].fillna("") + gdf["Ward Name"].fillna("")
    gdf = gdf.dissolve(by="Municipality Code", as_index=False, aggfunc="first")
    gdf = _rename_geometry(gdf)
    cols = ["Municipality Code", "Prefecture Name", "Subprefecture Name", "District Name", "Municipality Name", "Ward Name", "Municipality Label", "Geometry"]
    _save(gdf[cols], "kumamoto_administrative_areas_preprocessed.parquet")


def preprocess_medical_facilities() -> None:
    path = RAW / "extracted/mlit_ksj_p04_2020_kumamoto/P04-20_43.geojson"
    gdf = _geo(path).rename(columns={
        "P04_001": "Medical Facility Class Code",
        "P04_002": "Facility Name",
        "P04_003": "Address",
        "P04_004": "Medical Departments 1",
        "P04_005": "Medical Departments 2",
        "P04_006": "Medical Departments 3",
        "P04_007": "Operator Class Code",
        "P04_008": "Bed Count",
        "P04_009": "Emergency Designation Code",
        "P04_010": "Disaster Base Designation Code",
    })
    for col in ["Facility Name", "Address", "Medical Departments 1", "Medical Departments 2", "Medical Departments 3"]:
        gdf[col] = _strip(gdf[col])
    for col in ["Medical Facility Class Code", "Operator Class Code", "Bed Count", "Emergency Designation Code", "Disaster Base Designation Code"]:
        gdf[col] = pd.to_numeric(gdf[col], errors="coerce").astype("Int64")
    _add_labels(gdf, "Medical Facility Class Code", "Medical Facility Class", {1: "Hospital", 2: "General Clinic", 3: "Dental Clinic"})
    _add_labels(gdf, "Emergency Designation Code", "Emergency Designation", {1: "Designated", 9: "Not Designated"})
    _add_labels(gdf, "Disaster Base Designation Code", "Disaster Base Designation", {1: "Core Disaster Base", 2: "Regional Disaster Base", 9: "Not Designated"})
    gdf["Eligible Emergency Hospital"] = (
        gdf["Medical Facility Class Code"].eq(1)
        & (gdf["Emergency Designation Code"].eq(1) | gdf["Disaster Base Designation Code"].isin([1, 2]))
    )
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_medical_facilities_2020_preprocessed.parquet")


def preprocess_fire_stations() -> None:
    path = RAW / "extracted/mlit_ksj_p17_2012_kumamoto/P17-12_43_FireStation.shp"
    gdf = _geo(path, assumed_crs="EPSG:4612").rename(columns={
        "P17_001": "Fire Facility Name",
        "P17_002": "Municipality Code",
        "P17_003": "Fire Facility Type Code",
        "P17_004": "Address",
    })
    gdf["Fire Facility Name"] = _strip(gdf["Fire Facility Name"])
    gdf["Address"] = _strip(gdf["Address"])
    gdf["Municipality Code"] = _code(gdf["Municipality Code"], 5)
    _add_labels(gdf, "Fire Facility Type Code", "Fire Facility Type", {1: "Fire Headquarters", 2: "Fire Station", 3: "Branch or Outpost"})
    gdf["Candidate Dispatch Base"] = gdf["Fire Facility Type Code"].isin([2, 3])
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_fire_stations_2012_preprocessed.parquet")


def preprocess_fire_jurisdictions() -> None:
    path = RAW / "extracted/mlit_ksj_p17_2012_kumamoto/P17-12_43_FireStationJurisdiction.shp"
    gdf = _geo(path, assumed_crs="EPSG:4612")
    mapping = {"P17_005": "Fire Station Name"}
    mapping.update({f"P17_{i:03d}": f"Jurisdiction Area {i - 5}" for i in range(6, 27)})
    gdf = gdf.rename(columns=mapping)
    for col in mapping.values():
        gdf[col] = _strip(gdf[col])
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_fire_jurisdictions_2012_preprocessed.parquet")


def preprocess_emergency_transport_roads() -> None:
    path = RAW / "extracted/mlit_ksj_n10_2024_kumamoto/N10-24_43.geojson"
    gdf = _geo(path).rename(columns={
        "N01_001": "Prefecture Code",
        "N01_002": "Emergency Road Class Code",
        "N01_003": "Road Type Code",
        "N01_004": "Route Name",
        "N01_005": "Route ID",
        "N01_006": "Branch ID",
        "N01_007": "Source Name",
        "N01_008": "Source Date",
        "N01_009": "Service Status",
        "N01_010": "Notes",
    })
    gdf["Prefecture Code"] = _code(gdf["Prefecture Code"], 2)
    gdf["Route ID"] = _code(gdf["Route ID"])
    gdf["Branch ID"] = _code(gdf["Branch ID"])
    for col in ["Route Name", "Source Name", "Service Status", "Notes"]:
        gdf[col] = _strip(gdf[col])
    gdf["Source Date"] = pd.to_datetime(_strip(gdf["Source Date"]).str.replace(" ", "-") + "-01", errors="coerce")
    _add_labels(gdf, "Emergency Road Class Code", "Emergency Road Class", {1: "Primary Emergency Road", 2: "Secondary Emergency Road", 3: "Tertiary Emergency Road", 9: "Other or Unspecified"})
    _add_labels(gdf, "Road Type Code", "Road Type", {1: "National Expressway", 2: "Urban Expressway", 3: "National Highway", 4: "Major Prefectural Road", 5: "Major Designated-City Road", 6: "General Prefectural Road", 7: "Municipal Road", 8: "Other Road", 9: "Unknown"})
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_emergency_transport_roads_2024_preprocessed.parquet")


def preprocess_road_centerlines() -> None:
    boundary_path = RAW / "extracted/mlit_ksj_n03_2025_kumamoto/N03-20250101_43.geojson"
    boundary = _geo(boundary_path).geometry.union_all()
    frames: list[gpd.GeoDataFrame] = []
    for mesh in ["4829", "4830", "4831", "4930", "4931"]:
        path = RAW / f"extracted/mlit_ksj_n13_2024_mesh_{mesh}/N13-24_{mesh}.geojson"
        frame = _geo(path, mask=boundary)
        # Preserve full segments selected by the N03 spatial mask. Exact polygon
        # intersection is prohibitively slow for this 1.18-million-feature
        # source and would sever cross-boundary links needed for routing.
        frames.append(frame)
    gdf = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=TARGET_CRS)
    gdf = gdf.rename(columns={
        "N13_001": "Registration Date",
        "N13_002": "Road Centerline Type Code",
        "N13_003": "Road Category Code",
        "N13_004": "Road State Code",
        "N13_005": "Vertical Level",
        "N13_006": "Width Category Code",
        "N13_007": "Toll Category Code",
        "N13_008": "Secondary Mesh Code",
    })
    gdf["Registration Date"] = pd.to_datetime(gdf["Registration Date"], errors="coerce")
    gdf["Secondary Mesh Code"] = _code(gdf["Secondary Mesh Code"])
    gdf["Vertical Level"] = pd.to_numeric(gdf["Vertical Level"], errors="coerce").astype("Int64")
    _add_labels(gdf, "Road Centerline Type Code", "Road Centerline Type", {1: "Standard Road", 2: "Garden Path", 3: "Pedestrian Path", 4: "Steps", 5: "Unknown"})
    _add_labels(gdf, "Road Category Code", "Road Category", {1: "National Highway", 2: "Prefectural Road", 3: "Municipal Road or Equivalent", 4: "National Expressway or Equivalent", 5: "Other", 6: "Unknown"})
    _add_labels(gdf, "Road State Code", "Road State", {1: "At Grade", 2: "Bridge or Elevated", 3: "Tunnel", 4: "Snow Shelter", 5: "Under Construction", 6: "Other", 7: "Unknown"})
    _add_labels(gdf, "Width Category Code", "Width Category", {1: "Under 3 m", 2: "3 to Under 5.5 m", 3: "5.5 to Under 13 m", 4: "13 to Under 19.5 m", 5: "19.5 m or More", 6: "Unknown"})
    _add_labels(gdf, "Toll Category Code", "Toll Category", {1: "Free", 2: "Toll"})
    gdf["_wkb"] = gdf.geometry.to_wkb()
    gdf = gdf.drop_duplicates(subset=["_wkb", "Road Centerline Type Code", "Road Category Code", "Road State Code", "Vertical Level", "Width Category Code", "Toll Category Code"]).drop(columns="_wkb")
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_road_centerlines_2024_preprocessed.parquet")


def preprocess_landslide_zones() -> None:
    path = RAW / "extracted/mlit_ksj_a33_2025_kumamoto/A33-25_43Polygon.geojson"
    gdf = _geo(path).rename(columns={
        "A33_001": "Hazard Type Code",
        "A33_002": "Warning Zone Class Code",
        "A33_003": "Prefecture Code",
        "A33_004": "Zone ID",
        "A33_005": "Zone Name",
        "A33_006": "Address",
        "A33_007": "Designation Date",
        "A33_008": "Special Warning Zone Pending Code",
    })
    gdf["Prefecture Code"] = _code(gdf["Prefecture Code"], 2)
    for col in ["Zone ID", "Zone Name", "Address"]:
        gdf[col] = _strip(gdf[col])
    gdf["Designation Date"] = pd.to_datetime(gdf["Designation Date"], errors="coerce")
    _add_labels(gdf, "Hazard Type Code", "Hazard Type", {1: "Steep-Slope Collapse", 2: "Debris Flow", 3: "Landslide"})
    _add_labels(gdf, "Warning Zone Class Code", "Warning Zone Class", {1: "Warning Zone", 2: "Special Warning Zone"})
    _add_labels(gdf, "Special Warning Zone Pending Code", "Special Warning Zone Pending", {0: "No", 1: "Yes"})
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_landslide_warning_zones_2025_preprocessed.parquet")


def preprocess_evacuation_facilities() -> None:
    path = RAW / "extracted/mlit_ksj_p20_2012_kumamoto/P20-12_43.shp"
    gdf = _geo(path, assumed_crs="EPSG:4612").rename(columns={
        "P20_001": "Municipality Code", "P20_002": "Facility Name", "P20_003": "Address",
        "P20_004": "Facility Type", "P20_005": "Capacity", "P20_006": "Facility Area m2",
        "P20_007": "Earthquake Hazard", "P20_008": "Tsunami Hazard", "P20_009": "Flood Hazard",
        "P20_010": "Volcanic Hazard", "P20_011": "Other Hazard", "P20_012": "No Hazard Specified",
        "レベル": "Location Accuracy Level", "備考": "Notes", "緯度": "Latitude", "経度": "Longitude", "NO": "Source Record ID",
    })
    gdf["Municipality Code"] = _code(gdf["Municipality Code"], 5)
    gdf["Source Record ID"] = _code(gdf["Source Record ID"])
    for col in ["Facility Name", "Address", "Facility Type", "Notes"]:
        gdf[col] = _strip(gdf[col])
    for col in ["Capacity", "Facility Area m2", "Earthquake Hazard", "Tsunami Hazard", "Flood Hazard", "Volcanic Hazard", "Other Hazard", "No Hazard Specified", "Location Accuracy Level", "Latitude", "Longitude"]:
        gdf[col] = _numeric(gdf[col])
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_evacuation_facilities_2012_preprocessed.parquet")


def preprocess_population_mesh() -> None:
    path = RAW / "prior_ke01/kumamoto_population_mesh_125m.parquet"
    gdf = gpd.read_parquet(path)
    gdf = gdf.to_crs(TARGET_CRS)
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_population_mesh_125m_preprocessed.parquet")


def preprocess_population_groups() -> None:
    path = RAW / "prior_ke01/kumamoto_population_disclosure_groups.parquet"
    gdf = gpd.read_parquet(path)
    gdf = gdf.to_crs(TARGET_CRS)
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_population_disclosure_groups_preprocessed.parquet")


WEEKDAYS = [("月", "Monday"), ("火", "Tuesday"), ("水", "Wednesday"), ("木", "Thursday"), ("金", "Friday"), ("土", "Saturday"), ("日", "Sunday")]


def hospital_facility_mapping() -> dict[str, str]:
    mapping = {
        "ID": "Hospital ID", "正式名称": "Hospital Name", "正式名称（フリガナ）": "Hospital Name Kana",
        "略称": "Short Name", "略称（フリガナ）": "Short Name Kana", "英語表記（ローマ字表記）": "Hospital Name Romanized",
        "機関区分": "Institution Type Code", "都道府県コード": "Prefecture Code", "市区町村コード": "Municipality Code",
        "所在地": "Address", "所在地座標（緯度）": "Latitude", "所在地座標（経度）": "Longitude",
        "案内用ホームページアドレス": "Website",
    }
    for jp, en in WEEKDAYS:
        mapping[f"毎週決まった曜日に休診（{jp}）"] = f"Weekly Closed {en}"
    for week in range(1, 6):
        for jp, en in WEEKDAYS:
            mapping[f"決まった週に休診（定期週）第{week}週（{jp}）"] = f"Week {week} Closed {en}"
    mapping.update({
        "祝日に休診": "Closed on Holidays", "その他の休診日（gw、お盆等）": "Other Closure Dates",
        "一般病床": "General Beds", "療養病床": "Long-Term Care Beds",
        "療養病床のうち医療保険適用": "Insured Long-Term Care Beds", "療養病床のうち介護保険適用": "Nursing-Care Long-Term Beds",
        "精神病床": "Psychiatric Beds", "結核病床": "Tuberculosis Beds", "感染症病床": "Infectious Disease Beds", "合計病床数": "Total Beds",
    })
    return mapping


def preprocess_mhlw_hospitals() -> None:
    path = RAW / "extracted/mhlw_hospital_facility_20260601/01-1_hospital_facility_info_20260601.csv"
    df = pd.read_csv(path, dtype="string", encoding="utf-8-sig", low_memory=False)
    mapping = hospital_facility_mapping()
    df = df[list(mapping)].rename(columns=mapping)
    df["Prefecture Code"] = _code(df["Prefecture Code"], 2)
    df = df[df["Prefecture Code"].eq("43")].copy()
    df["Hospital ID"] = _code(df["Hospital ID"])
    df["Municipality Code"] = _code(df["Municipality Code"], 5)
    for col in ["Hospital Name", "Hospital Name Kana", "Short Name", "Short Name Kana", "Hospital Name Romanized", "Address", "Website", "Other Closure Dates"]:
        df[col] = _strip(df[col])
    for col in ["Latitude", "Longitude", "General Beds", "Long-Term Care Beds", "Insured Long-Term Care Beds", "Nursing-Care Long-Term Beds", "Psychiatric Beds", "Tuberculosis Beds", "Infectious Disease Beds", "Total Beds"]:
        df[col] = _numeric(df[col])
    geometry = gpd.points_from_xy(df["Longitude"], df["Latitude"], crs="EPSG:4326")
    gdf = gpd.GeoDataFrame(df, geometry=geometry).to_crs(TARGET_CRS)
    gdf = _rename_geometry(gdf)
    _save(gdf, "kumamoto_hospitals_2026_preprocessed.parquet")


def speciality_hours_mapping() -> dict[str, str]:
    mapping = {"ID": "Hospital ID", "診療科目コード": "Specialty Code", "診療科目名": "Specialty Name", "診療時間帯": "Consultation Time Band Code"}
    for jp, en in WEEKDAYS + [("祝", "Holiday")]:
        mapping[f"{jp}_診療開始時間"] = f"{en} Consultation Start"
        mapping[f"{jp}_診療終了時間"] = f"{en} Consultation End"
        mapping[f"{jp}_外来受付開始時間"] = f"{en} Reception Start"
        mapping[f"{jp}_外来受付終了時間"] = f"{en} Reception End"
    return mapping


def preprocess_mhlw_speciality_hours() -> None:
    facility_path = RAW / "extracted/mhlw_hospital_facility_20260601/01-1_hospital_facility_info_20260601.csv"
    facility = pd.read_csv(facility_path, dtype="string", usecols=["ID", "都道府県コード"], encoding="utf-8-sig")
    ids = set(_code(facility.loc[_code(facility["都道府県コード"], 2).eq("43"), "ID"]))
    path = RAW / "extracted/mhlw_hospital_speciality_hours_20260601/01-2_hospital_speciality_hours_20260601.csv"
    df = pd.read_csv(path, dtype="string", encoding="utf-8-sig", low_memory=False)
    mapping = speciality_hours_mapping()
    df = df[list(mapping)].rename(columns=mapping)
    df["Hospital ID"] = _code(df["Hospital ID"])
    df = df[df["Hospital ID"].isin(ids)].copy()
    df["Specialty Code"] = _code(df["Specialty Code"])
    df["Consultation Time Band Code"] = _code(df["Consultation Time Band Code"])
    df["Specialty Name"] = _strip(df["Specialty Name"])
    for col in [c for c in df if c.endswith("Start") or c.endswith("End")]:
        df[col] = _strip(df[col])
    _save(df, "kumamoto_hospital_speciality_hours_2026_preprocessed.parquet")


def preprocess_fdma_validation() -> None:
    path = RAW / "downloads/fdma_fire_organizations_2024.csv"
    raw = pd.read_csv(path, header=None, dtype="string", encoding="utf-8-sig")
    row = raw.loc[_strip(raw[0]).eq("熊本")].copy()
    names = ["Prefecture Name", "Fire Headquarters Total", "Municipal Headquarters", "Town Headquarters", "Village Headquarters", "Joint Headquarters", "Fire Stations", "Fire Outposts", "Fire Service Personnel", "Volunteer Fire Corps", "Volunteer Fire Divisions", "Volunteer Firefighters"]
    row = row.iloc[:, :12]
    row.columns = names
    row["Prefecture Name"] = _strip(row["Prefecture Name"])
    for col in names[1:]:
        row[col] = _numeric(row[col])
    _save(row, "kumamoto_fire_organization_validation_2024_preprocessed.parquet")


PREFECTURE_HOSPITAL_COLUMNS = [
    "Unused", "Health Office", "Hospital Name", "Postal Code", "Address", "Phone", "Operator Name", "Opening Date", "Opening Status",
    "Total Beds", "General Beds", "Long-Term Care Beds", "Psychiatric Beds", "Tuberculosis Beds", "Infectious Disease Beds",
    "Internal Medicine", "Psychosomatic Medicine", "Psychiatry", "Neurology", "Neurological Medicine", "Respiratory Medicine", "Gastroenterology", "Gastrointestinal Medicine", "Cardiology", "Allergy", "Rheumatology", "Pediatrics", "Surgery", "Orthopedics", "Plastic Surgery", "Cosmetic Surgery", "Neurosurgery", "Thoracic Surgery", "Cardiovascular Surgery", "Pediatric Surgery", "Venereology", "Proctology", "Dermatology and Urology", "Dermatology", "Urology", "Obstetrics and Gynecology", "Obstetrics", "Gynecology", "Ophthalmology", "Otolaryngology", "Tracheoesophageal Medicine", "Rehabilitation Medicine", "Radiology", "Dentistry", "Orthodontic Dentistry", "Pediatric Dentistry", "Oral Surgery", "Anesthesiology", "Other Specialties",
]


def _era_date(value: object) -> pd.Timestamp | pd.NaT:
    if pd.isna(value):
        return pd.NaT
    match = re.fullmatch(r"([SHR])(\d{1,2})\.(\d{1,2})\.(\d{1,2})", str(value).strip())
    if not match:
        return pd.to_datetime(value, errors="coerce")
    base = {"S": 1925, "H": 1988, "R": 2018}[match.group(1)]
    return pd.Timestamp(base + int(match.group(2)), int(match.group(3)), int(match.group(4)))


def preprocess_prefecture_hospital_registry() -> None:
    path = RAW / "downloads/kumamoto_current_hospitals.xlsx"
    raw = pd.read_excel(path, header=None, dtype=object)
    df = raw.iloc[3:, :54].copy()
    df.columns = PREFECTURE_HOSPITAL_COLUMNS
    df = df.drop(columns="Unused")
    df = df[df["Hospital Name"].notna()].copy()
    for col in ["Health Office", "Hospital Name", "Postal Code", "Address", "Phone", "Operator Name", "Opening Status", "Other Specialties"]:
        df[col] = _strip(df[col])
    df["Opening Date"] = df["Opening Date"].map(_era_date)
    for col in ["Total Beds", "General Beds", "Long-Term Care Beds", "Psychiatric Beds", "Tuberculosis Beds", "Infectious Disease Beds"]:
        df[col] = _numeric(df[col])
    for col in PREFECTURE_HOSPITAL_COLUMNS[15:53]:
        df[col] = _numeric(df[col]).fillna(0).astype("Int8")
    _save(df, "kumamoto_prefecture_hospital_registry_2025_preprocessed.parquet")


TERTIARY_HOSPITALS = ["熊本赤十字病院", "熊本医療センター", "済生会熊本病院", "熊本大学病院"]
ROTATION_HOSPITALS = [
    "荒尾市立有明医療センター", "くまもと県北病院", "和水町立病院", "川口病院", "菊池郡市医師会立病院", "菊池中央病院", "岸病院", "再春医療センター", "熊本セントラル病院", "熊本リハビリテーション病院", "東熊本第二病院", "熊本市立植木病院", "保利病院", "山鹿市民医療センター", "山鹿中央病院", "熊本医療センター", "熊本市民病院", "熊本赤十字病院", "熊本地域医療センター", "済生会熊本病院", "阿蘇医療センター", "阿蘇温泉病院", "阿蘇立野病院", "大阿蘇病院", "小国公立病院", "山都町包括医療センターそよう病院", "矢部広域病院", "熊本総合病院", "熊本労災病院", "八代北部地域医療センター", "岡部病院", "国保水俣市立総合医療センター", "球磨郡公立多良木病院", "人吉医療センター", "天草慈恵病院", "天草市立牛深市民病院", "天草市立河浦病院", "天草第一病院", "天草地域医療センター", "天草中央総合病院", "上天草市立上天草総合病院", "済生会みすみ病院", "苓北医師会病院",
]
EMERGENCY_HOSPITALS = [
    "荒尾市立有明医療センター", "くまもと県北病院", "和水町立病院", "米の山病院", "川口病院", "菊池郡市医師会立病院", "菊池中央病院", "菊陽台病院", "岸病院", "再春医療センター", "熊本セントラル病院", "熊本リハビリテーション病院", "東熊本第二病院", "保利病院", "三森循環器科・呼吸器科病院", "山鹿市民医療センター", "山鹿中央病院",
    "朝日野総合病院", "東病院", "植木病院", "宇城総合病院", "帯山中央病院", "表参道吉田病院", "上代成城病院", "川野病院", "菊南病院", "九州記念病院", "熊本医療センター", "熊本機能病院", "熊本市民病院", "くまもと森都総合病院", "熊本整形外科病院", "くまもと成城病院", "熊本赤十字病院", "熊本大学病院", "熊本中央病院", "くまもと南部広域病院", "熊本脳神経外科病院", "熊本南病院", "くわみず病院", "江南病院", "済生会熊本病院", "済生会みすみ病院", "桜十字病院", "慈恵病院", "嶋田病院", "十善病院", "水前寺とうや病院", "杉村病院", "整形外科井上病院", "青磁野リハビリテーション病院", "大腸肛門病センター高野病院", "寺尾病院", "南部中央病院", "にしくまもと病院", "西日本病院", "比企病院", "平成とうや病院", "御幸病院", "武蔵ヶ丘病院", "山口病院",
    "阿蘇医療センター", "阿蘇温泉病院", "阿蘇立野病院", "大阿蘇病院", "小国公立病院", "山都町包括医療センターそよう病院", "熊本総合病院", "熊本労災病院", "岡部病院", "国保水俣市立総合医療センター", "愛生記念病院", "球磨郡公立多良木病院", "球磨病院", "外山胃腸病院", "人吉医療センター", "天草慈恵病院", "天草市立牛深市民病院", "天草市立河浦病院", "天草市立新和病院", "天草市立栖本病院", "天草第一病院", "天草地域医療センター", "天草中央総合病院", "上天草市立上天草総合病院",
]


def _normalize_name(value: str) -> str:
    out = unicodedata.normalize("NFKC", value)
    out = re.sub(r"[\s・･（）()\-－]", "", out)
    return out.replace("独立行政法人国立病院機構", "").replace("国立病院機構", "").replace("国保", "")


HOSPITAL_NAME_ALIASES = {
    "和水町立病院": "国民健康保険　和水町立病院",
    "植木病院": "熊本市立植木病院",
    "熊本市民病院": "熊本市立熊本市民病院",
    "済生会熊本病院": "社会福祉法人恩賜財団済生会熊本病院",
    "熊本労災病院": "独立行政法人労働者健康安全機構熊本労災病院",
    "人吉医療センター": "独立行政法人地域医療機能推進機構人吉医療センター",
    "天草市立河浦病院": "国民健康保険天草市立河浦病院",
    "天草市立新和病院": "国民健康保険天草市立新和病院",
}


def preprocess_emergency_hospital_roles() -> None:
    hospital_path = PROCESSED / "kumamoto_hospitals_2026_preprocessed.parquet"
    hospitals = pd.read_parquet(hospital_path, columns=["Hospital ID", "Hospital Name"])
    candidates = {row["Hospital ID"]: (row["Hospital Name"], _normalize_name(row["Hospital Name"])) for _, row in hospitals.iterrows()}
    all_names = list(dict.fromkeys(EMERGENCY_HOSPITALS + ROTATION_HOSPITALS + TERTIARY_HOSPITALS))
    rows = []
    for plan_name in all_names:
        normalized = _normalize_name(plan_name)
        alias = HOSPITAL_NAME_ALIASES.get(plan_name)
        scores = [
            (
                1.0 if alias == hospital_name else SequenceMatcher(None, normalized, candidate_norm).ratio(),
                hospital_id,
                hospital_name,
            )
            for hospital_id, (hospital_name, candidate_norm) in candidates.items()
        ]
        score, hospital_id, hospital_name = max(scores)
        external = plan_name == "米の山病院"
        matched = (score >= 0.78) and not external
        rows.append({
            "Plan Hospital Name": plan_name,
            "Hospital ID": hospital_id if matched else pd.NA,
            "Matched Hospital Name": hospital_name if matched else pd.NA,
            "Name Match Score": score if not external else pd.NA,
            "Match Status": "Matched" if matched else ("Outside Kumamoto" if external else "Review Required"),
            "Emergency Designated": (plan_name in EMERGENCY_HOSPITALS) and not external,
            "Rotation Hospital": plan_name in ROTATION_HOSPITALS,
            "Tertiary Emergency Hospital": plan_name in TERTIARY_HOSPITALS,
            "External Reference": external,
            "Reference Date": pd.Timestamp("2023-09-01"),
        })
    _save(pd.DataFrame(rows), "kumamoto_emergency_hospital_roles_2023_preprocessed.parquet")
