import pandas as pd
from IPython.display import Markdown as md
from decimal import *

def ul(t):

    items =  [f"- {i}" for i in t]
    return str("\n".join(items))



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
        return f"{n:,}"
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
