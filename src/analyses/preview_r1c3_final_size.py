"""Reproducible final-size typography trial using unchanged Figure 1 data code.

This produces an exploratory preview only, never overwrites final figures,
and deliberately retains the approved three-column panel arrangement.
"""
from pathlib import Path
import importlib.util
import json
import textwrap

import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.collections import LineCollection
from matplotlib.collections import PathCollection

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/r1c3_readability_trial'
SOURCE = ROOT / 'src/analyses/figure_emergency_care_network_and_population_demand.py'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('figure_one', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = Figure.savefig

    def save(fig, destination, **kwargs):
        # Original artists/data are unchanged; only visual properties change.
        fig.set_size_inches(6, 3.3)
        for artist in fig.findobj(match=Text):
            if artist.get_text():
                artist.set_fontsize(8 if artist.get_text() in ('a', 'b', 'c') else 7)
        for ax in fig.axes:
            # Keep the graticule; label alternate longitudes to avoid crowding.
            east_labels = [t for t in ax.texts if t.get_text().endswith('°E')]
            for index, label in enumerate(east_labels):
                label.set_visible(index % 2 == 0)
            for label in ax.texts:
                if label.get_text() in ('a', 'b', 'c'):
                    label.set_position((-0.04, 1.08))
            if ax.get_xlabel():
                ax.set_xlabel(textwrap.fill(ax.get_xlabel(), 30), fontsize=7)
            for collection in ax.collections:
                if isinstance(collection, LineCollection):
                    widths = collection.get_linewidths()
                    collection.set_linewidth([max(0.15, float(w) * 0.55) for w in widths])
                elif isinstance(collection, PathCollection):
                    collection.set_sizes(collection.get_sizes() * 0.18)
            legend = ax.get_legend()
            if legend:
                handles = legend.legend_handles
                labels = [t.get_text() for t in legend.get_texts()]
                legend.remove()
                fig.axes[-1].legend(handles, [textwrap.fill(t, 24) for t in labels],
                                    loc='upper left', bbox_to_anchor=(0, 1.4),
                                    fontsize=7, frameon=False, handlelength=1.2,
                                    labelspacing=0.3, borderaxespad=0)
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        checks = []
        for ax in fig.axes:
            legend = ax.get_legend()
            if legend:
                box = legend.get_window_extent(renderer)
                map_box = ax.get_window_extent(renderer)
                checks.append({'legend_width_fraction_of_panel': box.width/map_box.width,
                               'legend_height_fraction_of_panel': box.height/map_box.height})
        original(fig, OUT / 'Figure_1_final_size_trial.png', dpi=600, facecolor='white')
        original(fig, OUT / 'Figure_1_final_size_trial.pdf', facecolor='white')
        (OUT / 'layout_checks.json').write_text(json.dumps(checks, indent=2)+'\n')
        print(json.dumps(checks, indent=2))

    Figure.savefig = save
    try:
        module.main()
    finally:
        Figure.savefig = original


if __name__ == '__main__':
    main()
