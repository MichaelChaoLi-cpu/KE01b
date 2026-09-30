"""Validate study-area denominators and length-weighted road composition."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / 'data/processed'
edges = pd.read_parquet(p / 'kumamoto_routable_road_edges_preprocessed.parquet')
sections = pd.read_parquet(p / 'kumamoto_road_sections_preprocessed.parquet')
demand = pd.read_parquet(p / 'kumamoto_population_mesh_network_access_preprocessed.parquet')
edges = edges.loc[edges['Road Available'].fillna(False) & edges['Network Analysis Eligible'].fillna(False)]
sections = sections.loc[sections['Road Available'].fillna(False) & sections['Network Analysis Eligible'].fillna(False)]
assert edges['Road Edge ID'].is_unique and sections['Road Section ID'].is_unique
assert demand['Analysis Unit ID'].is_unique
assert set(edges['Road Section ID']) == set(sections['Road Section ID'])
by_section = edges.groupby('Road Section ID')['Road Length (m)'].sum()
assert np.allclose(by_section, sections.set_index('Road Section ID').loc[by_section.index, 'Road Section Length (m)'])
lengths = edges.groupby('Road Category', dropna=False)['Road Length (m)'].sum()/1000
assert not lengths.index.isna().any()
result = {'status':'pass','population':int(demand['Total Population'].sum()),'population_meshes':len(demand),'eligible_sections':len(sections),'eligible_edges':len(edges),'network_length_km':float(lengths.sum()),'road_categories':[{'category':k,'length_km':float(v),'length_share_percent':float(100*v/lengths.sum())} for k,v in lengths.items()], 'definition':'Eligible and available represented road geometry, counted once per internal edge; not doubled for directed routing arcs. Category shares use edge attributes, not majority section labels. Population year 2020 is documented in upstream KE01/docs/AnaSOP.md and inherited through prior_ke01 preprocessing.'}
out=ROOT/'data/exp/r1c5_study_context'
out.mkdir(parents=True,exist_ok=True)
(out/'descriptive_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
