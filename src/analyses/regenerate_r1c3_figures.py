"""Render revision figures from existing data code without overwriting originals.

Usage: MPLCONFIGDIR=/private/tmp/ke01b-r1c3-mpl .venv/bin/python
src/analyses/regenerate_r1c3_figures.py 1 2 3 4 5 6 7 8 9
Only display properties are changed; per-artist numeric arrays are hashed.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.legend import Legend
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/r1c3_revised_figures'
NAMES = ['emergency_care_network_and_population_demand',
         'baseline_two_stage_emergency_travel_time', 'failure_severity_response',
         'nested_length_dependent_road_failure_realizations',
         'grid_emergency_access_loss_probability',
         'population_coverage_under_length_dependent_road_failure',
         'hospital_service_reliability_under_road_failure',
         'road_section_accessibility_consequence_and_expected_risk',
         'monte_carlo_convergence_and_stress_sensitivity']
MAPS = {1:3, 2:3, 4:4, 5:3, 7:3, 8:6}


def numeric_fingerprint(fig):
    h = hashlib.sha256()
    for ax in fig.axes:
        for c in ax.collections:
            a = c.get_array()
            if a is not None:
                h.update(np.ma.getdata(a).tobytes())
                h.update(np.ma.getmaskarray(a).tobytes())
            h.update(np.asarray(c.get_offsets()).tobytes())
            if isinstance(c, LineCollection):
                for path in c.get_paths():
                    h.update(path.vertices.tobytes())
        for line in ax.lines:
            h.update(np.asarray(line.get_xydata()).tobytes())
    return h.hexdigest()


def style_maps(fig, number):
    count = MAPS[number]
    maps = fig.axes[:count]
    cols = 3 if number == 8 else 2
    height = {1:6.3, 2:6.9, 4:6.2, 5:6.7, 7:6.7, 8:5.5}[number]
    fig.set_size_inches(6, height)
    fig.set_layout_engine(None)
    # Preserve map extents and frame proportions; notes use in-panel space.
    gap = 0.45
    width = (5.5 - (cols-1)*gap)/cols
    map_h = width*1.04
    inset_notes = number in (4,5,7,8)
    legends = []
    color_axes = fig.axes[count:]
    for i, ax in enumerate(maps):
        row, col = divmod(i, cols)
        y = height - 0.75 - map_h - row*(map_h+0.8)
        if number in (1,2): y = height - 0.25 - map_h - row*(map_h+0.7)
        if number == 8: y = height - 0.75 - map_h - row*(map_h+1.35)
        if number in (4,5,7): y = height-0.25-map_h-row*(map_h+0.30)
        if number == 8: y = height-0.35-map_h-row*(map_h+0.90)
        ax.set_position([(0.43+col*(width+gap))/6, y/height, width/6, map_h/height])
        east = [t for t in ax.texts if t.get_text().endswith('°E')]
        for j, t in enumerate(east): t.set_visible(j % 2 == 0)
        for t in ax.texts:
            s = t.get_text()
            if len(s)==1 and s in 'abcdef':
                t.set_position((-0.02, 1.04)); t.set_fontsize(9)
                if number == 8:
                    t.set_position((0, 1.06))
                    t.set_ha('left'); t.set_va('bottom'); t.set_clip_on(False)
            elif '\n' in s:
                t.set_text('\n'.join(textwrap.fill(line, 30 if cols==2 else 25) for line in s.splitlines()))
                t.set_position((0,1.08)); t.set_ha('left'); t.set_va('bottom')
                t.set_bbox(None); t.set_clip_on(False); t.set_linespacing(1.05)
                if inset_notes:
                    t.set_text('\n'.join(textwrap.fill(line, 28 if cols==2 else 24) for line in s.splitlines()))
                    t.set_position((0.025,0.97));t.set_va('top');t.set_fontsize(5.5 if cols==2 else 4.5)
                    t.set_bbox(dict(facecolor='white',edgecolor='none',alpha=0.75,pad=1.5))
        for c in ax.collections:
            if isinstance(c, LineCollection):
                c.set_linewidth([max(0.10,float(w)*0.55) for w in c.get_linewidths()])
            elif isinstance(c, PathCollection):
                c.set_sizes(c.get_sizes()*(0.2 if number==7 else 0.18))
                if number==7: c.set_linewidth(np.asarray(c.get_linewidths())*np.sqrt(0.2))
        leg=ax.get_legend()
        if leg:
            legends.append((leg.legend_handles,[t.get_text() for t in leg.get_texts()]))
            leg.remove()
    if number in (1,2):
        for i, ax in enumerate(color_axes[:2 if number==1 else 3]):
            box=maps[i].get_position()
            ax.set_position([box.x0,box.y0-0.36/height,width/6,0.10/height])
            ax.set_xlabel(textwrap.fill(ax.get_xlabel(), 25),fontsize=7)
        if number==1: color_axes[-1].set_visible(False)
    elif number==8:
        for ax,y in zip(color_axes,(height-0.35-map_h-0.32,0.74)):
            ax.set_position([0.075,y/height,0.9,0.10/height])
            ax.set_xlabel(textwrap.fill(ax.get_xlabel(),85),fontsize=7)
    elif number in (5,7):
        color_axes[0].set_position([0.075,0.55/height,0.9,0.10/height])
        color_axes[0].set_xlabel(textwrap.fill(color_axes[0].get_xlabel(),80),fontsize=7)
    if number==7:
        color_axes[0].tick_params(axis='x',labelrotation=35)
        color_axes[-1].set_position([0.54,0.16,0.42,0.30])
        for j,legend in enumerate(color_axes[-1].findobj(match=Legend)):
            legend.set_bbox_to_anchor((0.5,0.88-j*0.32))
            for handle in legend.legend_handles:
                if hasattr(handle,'get_markersize'):
                    handle.set_markersize(handle.get_markersize()*np.sqrt(0.2))
                    handle.set_markeredgewidth(handle.get_markeredgewidth()*np.sqrt(0.2))
    if legends:
        handles,labels=legends[0]
        if number==8:
            handles=[Patch(facecolor='white',edgecolor='#555f65') if label=='Zero value' else handle
                     for handle,label in zip(handles,labels)]
        spare = number in (1,2,5)
        fig.legend(handles,[textwrap.fill(t,28) for t in labels],loc='center' if spare else 'lower center',
                   bbox_to_anchor=(0.76,0.29) if spare else (0.52,0.005),ncol=1 if spare else (3 if number==8 else 2),
                   fontsize=7,frameon=False,handlelength=1.5,columnspacing=1.0)


def render(number):
    path=ROOT/'src/analyses'/f'figure_{NAMES[number-1]}.py'
    spec=importlib.util.spec_from_file_location(f'figure_{number}',path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.OUTPUT=OUT/f'Figure_{number:02d}.png'
    original=Figure.savefig
    original_idle=FigureCanvasAgg.draw_idle
    def save(fig,*args,**kwargs):
        before=numeric_fingerprint(fig)
        for text in fig.findobj(match=Text):
            if text.get_text(): text.set_fontsize(6.5 if number in (6,9) else 7)
        if number in MAPS:
            style_maps(fig,number)
        else:
            fig.set_size_inches(6, 5.0 if number==9 else (3.4 if number==6 else 3.1))
            fig.set_layout_engine(None)
            for i,ax in enumerate(fig.axes):
                if number==9:
                    row,col=divmod(i,2)
                    ax.set_position([0.12+col*0.49,0.59-row*0.47,0.36,0.348])
                else:
                    ax.set_position([0.11+i*0.33,0.40 if number==6 else 0.30,0.20,0.506 if number==6 else 0.58])
                ax.set_xlabel(textwrap.fill(ax.get_xlabel(),27),fontsize=7)
                ax.set_ylabel(textwrap.fill(ax.get_ylabel(),38),fontsize=7)
                for line in ax.lines:
                    line.set_linewidth(max(0.5,line.get_linewidth()*0.6))
                    line.set_markersize(line.get_markersize()*0.65)
                for t in ax.texts:
                    if t.get_text() in 'abcd' and len(t.get_text())==1:
                        t.set_position((0,1.05));t.set_ha('left');t.set_va('bottom');t.set_fontsize(8)
                    elif number==6 and '\n' in t.get_text():
                        t.set_text('\n'.join(textwrap.fill(line,28) for line in t.get_text().splitlines()))
                        t.set_position((0.5,-0.40));t.set_ha('center');t.set_va('top');t.set_bbox(None);t.set_fontsize(5.5)
                    elif number==9:
                        t.set_fontsize(5.5)
                if number==9 and i==2:
                    for t in ax.texts:
                        if t.get_text().startswith('Baseline speed'):
                            t.set_text('\n'.join(textwrap.fill(line,30) for line in t.get_text().splitlines()))
                            t.set_transform(ax.transAxes)
                            t.set_position((0.03,0.74));t.set_va('top');t.set_ha('left')
                            t.set_bbox(dict(facecolor='white',edgecolor='none',alpha=0.9,pad=1.5))
            for legend in list(fig.legends):
                handles=legend.legend_handles;labels=[t.get_text() for t in legend.get_texts()]
                legend.remove()
                fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(0.52,0.005),
                           ncol=3,fontsize=6 if number in (6,9) else 7,frameon=False,handlelength=1.4,columnspacing=1)
        fig.canvas.draw()
        # Trim only exterior vertical whitespace, retaining the six-inch width.
        from matplotlib.transforms import Bbox
        tight = fig.get_tightbbox(fig.canvas.get_renderer())
        bottom = max(0, tight.y0-0.04)
        top = min(fig.get_figheight(), tight.y1+0.04)
        export_box = Bbox.from_extents(0, bottom, 6, top)
        # Marker sizes/stroke widths are display properties; data must match.
        after=numeric_fingerprint(fig)
        assert before==after, 'Numeric artist content changed'
        original(fig,module.OUTPUT,dpi=600,facecolor='white',bbox_inches=export_box)
        # PNG is the required replacement; avoid huge vector road collections.
        (OUT/f'Figure_{number:02d}_validation.json').write_text(json.dumps({
            'figure':number,'source_script':str(path.relative_to(ROOT)),
            'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'numeric_artist_sha256_before':before,'numeric_artist_sha256_after':after,
            'width_inches':6,'dpi':600,'visual_review':'pending'},indent=2)+'\n')
    Figure.savefig=save
    FigureCanvasAgg.draw_idle=lambda self,*a,**k: None
    try: module.main()
    finally:
        Figure.savefig=original
        FigureCanvasAgg.draw_idle=original_idle


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('figures',type=int,nargs='+',choices=range(1,10))
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    for number in args.figures: render(number)
