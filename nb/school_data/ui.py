import pandas as pd
from IPython.display import Markdown as md
from decimal import *

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import networkx as nx

import math

def ul(t):

    items =  [f"- {i}" for i in t]
    return str("\n".join(items))



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
    draw_model(nodes, pnodes, node_size, weighted_edges, labels, edge_labels, colors, cmap)

def draw_model(nodes, pnodes, node_size, edges, labels, edge_labels, colors, cmap):

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    fig, ax = plt.subplots(figsize=(16,9))

    # pos = nx.spring_layout(G, k=3)
    pos = nx.circular_layout(G)

    nx.draw(G, pos=pos, ax = ax, with_labels=True,
            labels=labels, node_color=colors, cmap=cmap, node_size=node_size,
            linewidths=2, min_source_margin=2, min_target_margin=2, font_size=14)

    nx.draw_networkx_edge_labels(G,pos, ax=ax, edge_labels=edge_labels, label_pos=.5, font_size=12)

    # adding p-values as node
    # G.add_nodes_from(pnodes,{"pvalue":True})
    # nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=G.nodes(data=True))




    plt.tight_layout()
    plt.margins(0.05)
    plt.show()
