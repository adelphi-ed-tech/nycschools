import pandas as pd
from IPython.display import Markdown as md

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
        result = result.rename(columns=demo.col_map)
    return result


def infinite():
    n = 0
    while True:
        n += 1
        yield n


def counter():
    x = infinite()
    return x.__next__
