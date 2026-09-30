"""Export and round-trip verify the GIS features underlying manuscript Figure 8."""
from pathlib import Path
import hashlib
import json
import shutil
import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/tranfer'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    gpkg = OUT / 'Figure8_road_importance.gpkg'
    if gpkg.exists():
        raise FileExistsError(f'Refusing to overwrite {gpkg}')
    sources = [ROOT / 'data/processed/kumamoto_road_sections_preprocessed.parquet',
               ROOT / 'data/exp/road_section_accessibility_consequence/road_section_accessibility_consequence.parquet',
               ROOT / 'data/processed/kumamoto_administrative_areas_preprocessed.parquet']
    roads = gpd.read_parquet(sources[0])
    result = pd.read_parquet(sources[1])
    base = {'Road Section ID': 'section_id', 'Route Name': 'route_name',
            'Road Category': 'road_category', 'Road Section Length (m)': 'length_m'}
    metrics = {f'Potential Access Loss {t} Minutes': f'loss_{t}min' for t in (15, 30, 45)}
    metrics.update({f'Expected Risk 30 Minutes {s} Percent': f'risk_30min_{s}pct' for s in (1, 3, 5)})
    probs = {f'Section Failure Probability {s} Percent': f'failure_prob_{s}pct' for s in (1, 3, 5)}
    for df in (roads, result):
        df['Road Section ID'] = df['Road Section ID'].astype(str)
        assert df['Road Section ID'].is_unique
    assert set(roads['Road Section ID']) == set(result['Road Section ID'])
    full = roads[[*base, 'Geometry']].merge(result[['Road Section ID', *metrics, *probs]], on='Road Section ID', validate='one_to_one')
    full = full.rename(columns=base | metrics | probs).rename_geometry('geometry')
    assert len(full) == 343844
    numeric = [*metrics.values(), *probs.values()]
    assert np.isfinite(full[numeric].to_numpy()).all()
    assert full[numeric].ge(0).all().all()
    assert full[list(probs.values())].le(1).all().all()
    for s in (1, 3, 5):
        np.testing.assert_allclose(full[f'risk_30min_{s}pct'], full.loss_30min * full[f'failure_prob_{s}pct'], rtol=1e-12, atol=1e-12)
    assert full.geometry.notna().all() and (~full.geometry.is_empty).all() and full.geometry.is_valid.all()
    assert full.geom_type.isin(['LineString', 'MultiLineString']).all()
    layers = {'roads_all_sections': full}
    panel_fields = dict(zip('abcdef', metrics.values()))
    for panel, field in panel_fields.items():
        layers[f'panel_{panel}_{field}'] = full.loc[full[field].gt(0), [*base.values(), field, 'geometry']].copy()
    boundary = gpd.read_parquet(sources[2]).rename(columns={
        'Municipality Code': 'municipality_code', 'Municipality Label': 'municipality_label'})
    layers['administrative_boundaries'] = boundary[['municipality_code', 'municipality_label', 'Geometry']].rename_geometry('geometry').to_crs(full.crs)
    report = {'source_crs': full.crs.to_string(), 'sources': {}, 'layers': {}, 'risk_formula_check': 'PASS'}
    for source in sources:
        report['sources'][str(source.relative_to(ROOT))] = hashlib.sha256(source.read_bytes()).hexdigest()
    for name, frame in layers.items():
        assert frame.geometry.notna().all() and (~frame.geometry.is_empty).all() and frame.geometry.is_valid.all()
        frame.to_file(gpkg, layer=name, driver='GPKG', engine='pyogrio', index=False, promote_to_multi=False)
        back = gpd.read_file(gpkg, layer=name, engine='pyogrio')
        assert len(back) == len(frame) and back.crs == frame.crs
        assert np.array_equal(back.geometry.to_wkb().to_numpy(), frame.geometry.to_wkb().to_numpy())
        for col in frame.columns.drop('geometry'):
            pd.testing.assert_series_equal(back[col].reset_index(drop=True), frame[col].reset_index(drop=True), check_dtype=False)
        report['layers'][name] = {'features': len(frame), 'geometry_types': frame.geom_type.value_counts().to_dict(),
            'missing_attributes': frame.drop(columns='geometry').isna().sum().to_dict(), 'round_trip': 'PASS'}
        if name.startswith('panel_'):
            field = panel_fields[name.split('_')[1]]
            report['layers'][name].update(value_field=field, minimum=float(frame[field].min()), maximum=float(frame[field].max()))
        print(name, len(frame), 'PASS', flush=True)
    shutil.copy2(ROOT / 'data/results/figures/Figure_road_section_accessibility_consequence_and_expected_risk.png', OUT / 'Figure8_reference.png')
    dictionary = [
        '| Field | Definition | Unit |', '|---|---|---|',
        '| section_id | Stable study section identifier; not an official road number | ID |',
        '| route_name | Source route name; preserved as supplied, including Japanese | text |',
        '| road_category | Source road classification | text |',
        '| length_m | Original analytical section length, retained without recalculation | m |',
        '| loss_15min / loss_30min / loss_45min | Baseline timely-access population lost when this section alone is closed; time is fire-base to grid plus grid to eligible hospital | people |',
        '| failure_prob_1pct / 3pct / 5pct | Length-dependent section failure probability under the specified expected failed road-length scenario | 0–1 |',
        '| risk_30min_1pct / 3pct / 5pct | loss_30min × corresponding section failure probability | probability-weighted people |',
        '| municipality_code / municipality_label | Administrative identifier and source label | text |',
        '| geometry | Original unsimplified feature geometry in JGD2011 | EPSG:6668 |']
    (OUT / 'FIELD_DICTIONARY.md').write_text('\n'.join(dictionary) + '\n', encoding='utf-8')
    (OUT / 'validation_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False, default=int), encoding='utf-8')
    lines = ['# Figure 8 GIS Delivery', '',
        'Study: Length-Dependent Road Failure and Two-Stage Emergency Medical Access in Kumamoto Prefecture.', '',
        'Open Figure8_road_importance.gpkg in QGIS or ArcGIS. It contains eight separately named layers. GeoPackage preserves long field names, Unicode route names, and multipart lines without Shapefile truncation.', '',
        'Load the complete road network, the six panel layers, and the administrative boundaries separately as needed.', '',
        '## Layers', '', '| Layer | Features | Meaning |', '|---|---:|---|']
    for name, frame in layers.items():
        meaning = 'All sections, including zero values; all six Figure 8 metrics' if name == 'roads_all_sections' else ('Context boundaries' if name == 'administrative_boundaries' else 'Positive-valued features only; zero-valued roads remain in roads_all_sections')
        lines.append(f'| {name} | {len(frame):,} | {meaning} |')
    lines += ['', 'Panels a–c: potential population access loss at 15, 30, 45 minutes. Panels d–f: probability-weighted 30-minute loss under 1%, 3%, 5% expected failed road-length scenarios.', '',
        'The six panel layers contain only roads with positive values for the corresponding metric. All 343,844 sections, including zero-valued sections, are retained in roads_all_sections. No top-ranked subset was imposed, and no road geometry was simplified or clipped.', '',
        '## Interpretation', '',
        'Values describe modelled emergency-access consequences, not observed road damage, verified closures, casualty counts, or engineering failure probabilities. Zero means no loss for this metric in this calculation, not that a road is unimportant for every purpose. Section-level risks must not be summed as the total loss from simultaneous closures.', '',
        'When using these data to identify filming locations, verify road names, current conditions, and site access locally. The section_id field is an internal study identifier, not an official road number. Source road and administrative names are retained in their original language for location matching. Road names are missing for 333,366 sections in the source data; their geometries, identifiers, and importance metrics remain complete.', '',
        'Original geometry CRS: EPSG:6668 (JGD2011, longitude/latitude degrees). Figure 8 display CRS: EPSG:6670 (JGD2011 / Japan Plane Rectangular CS II). Set the GIS project to EPSG:6670 to reproduce the map projection. Geometry is not shifted or simplified.', '',
        'For Figure 8 styling: zero = white; positive = logarithmic blue (#2166ac), green (#1a9850), yellow (#fee08b), red (#d73027). Panels a–c share limits [1, maximum of the three loss fields]; panels d–f share the minimum positive and maximum across the three risk fields. Do not classify zero as missing.', '',
        'Sources are the exact processed road geometry, consequence results and administrative polygons used by the Figure 8 script. Source file paths and SHA-256 hashes, geometry/attribute round-trip checks, counts and value ranges are in validation_report.json. The export preserves original route metadata; see per-field null counts before using names as location identifiers.', '',
        'Retain attribution to the study and the underlying geographic-data providers. This package does not grant a new license over third-party base data; confirm applicable source attribution and reuse terms before public redistribution.', '',
        'FIELD_DICTIONARY.md explains every field. Figure8_reference.png is the original figure. Reproduce with src/analyses/export_figure8_gis.py in the project environment (the exporter refuses to overwrite an existing GeoPackage).']
    (OUT / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    manifest = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in OUT.iterdir() if p.is_file()}
    (OUT / 'checksums.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
