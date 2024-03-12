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
from IPython.display import display
from decimal import *

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import networkx as nx
import folium
import numpy as np
import random
import math
from shapely import Point
from functools import partial


def ul(t):

    items =  [f"- {i}" for i in t]
    return str("\n".join(items))


def label_shapes(m, df, col, style={}):
    """Create a function that will add the string of `col`
    to the center of each shape in df """
    style_str = ";".join([f"{k}:{v}" for k,v in style.items()])
    def label(row):  
        point = row.geometry.centroid
        html=f"""<div style="{style_str}">{row[col]}</div>"""
        folium.Marker(
            location=(point.y, point.x), 
            icon=folium.DivIcon(html=html)).add_to(m)
    df.apply(label, axis=1)
    return m

def map_legend(m, items, title="", style={}, position="bottomright"):
    """Create a legend for the map with the items listed
    in the order they are passed in. The items should be a list
    of tuples with the first element being the label and the second
    being the html color. The style is a dictionary of css properties
    to apply to the legend. Style properties will replace default
    properties. The title is the title of the legend.

    Parameters
    ----------
    m: folium.Map the map to add the legend to
    items: list of tuples
        The items to include in the legend in the format (label, color)
        they will be displayed in the order they are passed in.
        For example: [("label1", "red"), ("label2", "blue"), ("label3", "#00ff00")]
    title: str
        The title of the legend, appears at the top of the legend (default is "").
    style: dict
        The style of the legend. Default is an empty dictionary. These styles
        will be applied to the <div> element that contains the legend.
        This div also has the css class "MapLegend" which you
        can use to style all of the elements in the legend by adding a custom
        header to the map html file wit the `map_header()` function.
    
    Returns
    -------
    folium.Map
        The map with the legend added to it.
    """

    css = """
.MapLegend {
  position: absolute;
  top: 10px;
  left: 80px;
  width: 200px;
  max-height: 600px;
  background: rgba(255,255,255,.8);
  z-index: 1000;
  padding: 1em;
  border: 2px solid lightgray;
  border-radius: 8px;
  overflow: auto;
  font-size: 14px;
  font-weight: bold;
}
.LegendItem {
    display: flex; 
    align-items: start; 
    margin-bottom: .5em;
}
.LegendMarker {
    width: 12px;
    height: 12px;
}

.LegendLabel {
    line-height: 14px; 
    padding-left: .25em; 
    font-size: 12px;
}
    """
    
    def legend_item(label, color):
        return f"""
        <div class="LegendItem">
          <div class="LegendMarker" style="background:{color};">&nbsp;</div>
          <div class="LegendLabel"><strong>{label}</strong></div>
        </div>
"""
    
    html = f"""
<div class="MapLegend">
  <style>{css}</style>
  <h4><strong>{title}</strong></h4>
  {"".join([legend_item(label, color) for label, color in items])}
</div>
"""

    m.get_root().html.add_child(folium.Element(html))
    return m

def map_layers(m, df, radius=5):

    def create_layer(df, name, color="color", popup="popup", radius=5):
        layer = folium.FeatureGroup(name=name)

        def marker(row):
            if popup in row:
                info = row[popup]
            else:
                info = ""
            return folium.Circle(
                location=(row['geometry'].y, row['geometry'].x),
                radius=20,
                color=row["color"],
                fill=True,
                fill_color=row[color],
                fill_opacity=1,
                opacity=1,
                popup=info,
                className=f"layer-{name} zoomable"
            )
        df.apply(lambda row: marker(row).add_to(layer), axis=1)

        layer.add_to(m)

        return layer

    groups = df.groupby("layer")
    for name, group in groups:
        create_layer(group, name, radius=radius)
        # print(name, len(group), group["color"].unique())
    # folium.LayerControl().add_to(m)
    return m


def rand_points(geometry, n, max_conflicts=100):
    """
    Create n random points within the bounds of the geometry.
    
    Parameters
    ----------
    geometry: shapely.geometry
        The geometry to create points within
    n: int
        The number of points to create

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame with n random points within the geometry

    """
    minx, miny, maxx, maxy = geometry.bounds

    occupied = set()
    conflicts = 0

    def is_occupied(p):
        if p in occupied:
            conflicts += 1
            return True or conflicts > max_conflicts
        occupied.add(p)
        return False

    def rand_point():

        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        p = Point(x, y)
        if p.within(geometry):
            return p
        return rand_point()

    points = [rand_point() for i in range(n)]
    if conflicts > 0:
        print(f"Conflicts in plotting {n} points:", conflicts)
    # create a GeoDataFrame from the points
    points = pd.DataFrame({"geometry": points})
    return points

def map_js(m, file_path, js):
    """Add the custom javascript to the map
    that will load after the body is rendered
    and all other map elements are ready.
    Do not wrap js in <script> tags."""
    m.save(file_path)

    html = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {""" + js + """

    });
    </script>
    """

    # open the map html and insert the footer at the bottom of page
    with open(file_path, 'r') as file:
        content = file.read()

    with open(file_path, 'w') as file:
        file.write(content.replace('</html>', f"{html}</html>"))
    
    return file_path


def map_footer(m, file_path, html):
    """Add the html to the bottom of the map html file"""
    m.save(file_path)

    # open the map html and insert the footer at the bottom of page
    with open(file_path, 'r') as file:
        content = file.read()

    with open(file_path, 'w') as file:
        file.write(content.replace('</body>', f"{html}</body>"))
    
    return file_path

def map_header(m, file_path, html):
    """Add the html to the top of the map html file"""
    m.save(file_path)

    # open the map html and insert the header at the top of page
    with open(file_path, 'r') as file:
        content = file.read()

    with open(file_path, 'w') as file:
        file.write(content.replace('<body>', f"<body>{html}"))
    
    return file_path


def create_layer(m, data, name, style={"color": "blue", "weight": 0, "opacity": 0},tooltip=None,radius=2):
    """Create a folium layer from the data. A new CircleMarker is created for
    each row in the DataFrame and added to map `m`.
    Parameters
    ----------
    m: folium.Map
        The map to add the layer to
    data: GeoDataFrame
        The data to plot
    name: str
        The name of the layer
    style: dict
        The style of the layer. Default is {"color": "blue", "weight": 0, "opacity": 0}
    tooltip: str
        The column name to use for the tooltip. Default is None.
    radius: int
        The radius of the circle markers. Default is 2.

    Returns
    -------
    folium.FeatureGroup
        The layer created from the data
    """
    layer = folium.FeatureGroup(name=name)

    def marker(row):
        tool = row[tooltip] if tooltip else False
        return folium.CircleMarker(
            location=(row['geometry'].y, row['geometry'].x),
            radius=radius,
            style=style,
            fill=True,
            popup=tool
        )
    data.apply(lambda row: marker(row).add_to(layer), axis=1)

    layer.add_to(m)

    return layer


def popup(cols, style={"min-width": "200px"}, fmt_funcs={}):
    style_str = ";".join([f"{k}:{v}" for k,v in style.items()])

    def html(row):
        def content(c):
            if c == "----":
                return """<hr style="padding: 0;margin:0; margin-bottom: .25em; border: none; border-top: 2px solid black;">"""
            # make a partial of fmt_num that includes the column name

            f = fmt_funcs.get(c, partial(fmt_num, c))
            return f"{nice_name(c)}: {f(row[c])}<br>"
        
        items = [content(c) for c in cols]
        items[0] = f"<strong>{items[0]}</strong>"
        items = "".join(items)
        return f'<div style="{style_str}">{items}</div>'

    return html


def fmt_num(col, n):
    if col.endswith("_pct"):
        return pct(n)
    try:
        n = float(n)
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


def show_md(s):
    display(md(s))

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
