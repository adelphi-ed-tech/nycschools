# NYC School Data
# Copyright (C) 2022. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU AFFERO GENERAL PUBLIC LICENSE (the "License") as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
import pandas as pd
from IPython.display import Markdown as md
from decimal import *

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import networkx as nx
import folium

import math

def ul(t):

    items =  [f"- {i}" for i in t]
    return str("\n".join(items))


def label_shapes(m, df, col, style={}):
    """Create a function that will add the string of `col`
    to the center of each shape specified by """
    style_str = ";".join([f"{k}:{v}" for k,v in style.items()])
    def label(row):  
        point = row.geometry.centroid
        html=f"""<div style="{style_str}">{row[col]}</div>"""
        folium.Marker(
            location=(point.y, point.x), 
            icon=folium.DivIcon(html=html)).add_to(m)
    df.apply(label, axis=1)
    return m
    


def popup(cols, style={"min-width": "200px"}):
    style_str = ";".join([f"{k}:{v}" for k,v in style.items()])

    def html(row):
        items = "<br>".join([f"{nice_name(c)}: {fmt_num(c, row[c])}" for c in cols])
        return f'<div style="{style_str}">{items}</div>'

    return html


def fmt_num(col, n):
    if col.endswith("_pct"):
        return pct(n)
    try:
        n = float(row[col])
        if round(n) == n:
            return f"{int(n):,}"
        else:
            return f"{n:,.2f}"
    except:
        return n

def hexmap(cmap):

    def f(color):
        return mpl.colors.rgb2hex(cmap(color))

    return f

def pct(n):
    try:
        whole = int(n)
        if whole == float(n):
            return f"{whole}%"
        n = float(n)
        return f"{n:.1%}"
    except:
        return "-"

def commas(n):
    try:
        float(n)
        return f"{round(n, 3):,}"
    except:
        return "-"


def fmt_table(df, col_map=None, pct_cols=[], num_cols=[]):
    result = df.copy()
    for col in pct_cols:
        result[col] = result[col].apply(pct)

    for col in num_cols:
        result[col] = result[col].apply(commas)

    if col_map:
        result = result.rename(columns=col_map)
    return result


def infinite():
    n = 0
    while True:
        n += 1
        yield n


def counter():
    x = infinite()
    return x.__next__

# strips the leading zero from a rounded float
def round_f(f, places):

    s = str(round(f, places))
    if not "." in s:
        return f

    whole, frac = s.split(".")
    if whole == "0":
        whole = ""
    frac = frac.ljust(places, "0")
    return f"{whole}.{frac}"


def fmt_pearson(r):
    """Formats the Pearson's R correlation table returned
    from `pengouin.corr` in the format r(df)={r}, p={p}.
    The r is rounded to 2 decimals, and p is rounded to 3 decimals.
    """
    df = r.n[0] - 2
    p = round_f(r['p-val'][0], 3)
    r_val = round_f(r['r'][0], 2)
    return f"r({df})={r_val}, p={p}"


def edge_label(p, r):
    return f"{p}={round_f(r,2)}"

def nice_name(n):
    allcaps = ["dbn", "beds"]
    if n in allcaps:
        return n.upper()

    return n.replace("_", " ").title()

def plot_model(model):


    # get the data we need from model
    dv = model.model.endog_names

    params = list(model.params.index.values[1:])
    coefs = list(model.params.values[1:],)
    pvalues = list(model.pvalues.round(3).values[1:])


    network_map(dv, params, coefs, pvalues=None)

def network_map(dv, params, coefs, pvalues):

    if not pvalues:
        pvalues = [0 for i in coefs]

    cmap = mpl.cm.seismic
    nodes =  params + [dv]
    plabels = [f"p={p}" for p in pvalues]
    pnodes = list(zip(plabels, params))

    # all targets point to the dv
    targets =  [dv for _ in range(len(params))]
    edges = list(zip(params, targets))
    colors = coefs + [0]

    weights =  [abs(c) for c in coefs]
    weighted_edges = list(zip(params, targets, weights))

    max_node = 2000
    max_size = max(weights)
    node_size = [math.ceil(max_node * (c/max_size)) for c in weights]
    node_size.append(  max_node * 2 )

    labels =  dict([(n, nice_name(n)) for n in nodes])

    edge_labels = dict([(x, edge_label(x[0], y)) for x, y in zip(edges, coefs)])
    node_dict = {}
    for i, n in enumerate(nodes):
        node_dict[n] = {
            "node_size": node_size[i],
            "color": colors[i],
            "pvalue": pvalues[i] if i < len(pvalues) - 1 else 0,
            "weight": weights[i] if i < len(weights) - 1 else 0,
            "scale": node_size[i] / node_size[i],
            "label": nice_name(n)
        }

    draw_model(nodes, pnodes, node_size, weighted_edges, labels, edge_labels, colors, cmap, node_dict)

def draw_model(nodes, pnodes, node_size, edges, labels, edge_labels, colors, cmap, node_dict):

    G = nx.DiGraph()
    G.add_nodes_from(node_dict)
    G.add_weighted_edges_from(edges)

    fig, ax = plt.subplots(figsize=(16,9))

    # pos = nx.spring_layout(G, k=3)
    pos = nx.circular_layout(G)

    nx.draw(G, pos=pos, ax = ax, with_labels=False, node_color=colors, cmap=cmap, node_size=node_size,
            linewidths=2, min_source_margin=2, min_target_margin=2, font_size=14)


    nx.draw_networkx_edge_labels(G,pos, ax=ax, edge_labels=edge_labels, label_pos=.5, font_size=12)

    # draw the node labels separately to put below the nodes
    pos_attrs = {}
    for node, coords in pos.items():

        x, y = coords
        pos_attrs[node] = (x, y - .1)

    nx.draw_networkx_labels(G, pos_attrs, labels=labels)


    # adding p-values as node
    # G.add_nodes_from(pnodes,{"pvalue":True})
    # nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=G.nodes(data=True))




    plt.tight_layout()
    plt.margins(0.05)
    plt.show()
