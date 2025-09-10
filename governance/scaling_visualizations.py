import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

def parse_amount(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "")
    m = re.fullmatch(r'([0-9]*\.?[0-9]*)([kKmM]?)', s)
    if m:
        val = float(m.group(1) or 0.0)
        suf = (m.group(2) or "").lower()
        if suf == 'k':
            val *= 1_000
        elif suf == 'm':
            val *= 1_000_000
        return val
    try:
        return float(s)
    except:
        return np.nan

def w_linear(t): return t
def w_power(t, a): return np.power(t, a)
def w_log(t): return np.log(1.0 + t)

functions = {
    "linear": w_linear,
    "power_0.9": lambda t: w_power(t, 0.9),
    "power_0.8": lambda t: w_power(t, 0.8),
    "power_0.7": lambda t: w_power(t, 0.7),
    "power_0.6": lambda t: w_power(t, 0.6),
    "power_0.5": lambda t: w_power(t, 0.5),
    "log": w_log,
}
order = list(functions.keys())

df = pd.read_csv("prop289_voters.csv")
voter_col, votes_col, side_col = {c.lower(): c for c in df.columns}.values()
df[votes_col] = df[votes_col].apply(parse_amount)
df = df.dropna(subset=[votes_col, side_col]).copy()
df = df[df[votes_col] > 0].copy()

def apply_weighting(df, votes_col, side_col, func_name, func):
    tmp = df[df[side_col].isin(["For","Against"])].copy()
    tmp["weight"] = func(tmp[votes_col].astype(float).values)
    totals = tmp.groupby(side_col)["weight"].sum()
    for_w = float(totals.get("For", 0.0))
    ag_w  = float(totals.get("Against", 0.0))
    s = for_w + ag_w
    return {
        "function": func_name,
        "For_weight": for_w,
        "Against_weight": ag_w,
        "Total_weight": s,
        "For_prop": for_w / s if s>0 else np.nan,
        "Against_prop": ag_w / s if s>0 else np.nan,
        "Margin": for_w - ag_w,
    }

summary = pd.DataFrame([apply_weighting(df, votes_col, side_col, n, f) for n,f in functions.items()])
summary["function"] = pd.Categorical(summary["function"], categories=order, ordered=True)
summary = summary.sort_values("function")

x = np.arange(len(summary))
width = 0.6
lo = min(summary["For_prop"].min(), summary["Against_prop"].min())
hi = max(summary["For_prop"].max(), summary["Against_prop"].max())
pad = (hi - lo) * 0.15 if hi > lo else 0.01

plt.figure(figsize=(10,4))
plt.bar(x, summary["For_prop"], width, label="For")
plt.bar(x, summary["Against_prop"], width, bottom=summary["For_prop"], label="Against")
plt.xticks(x, summary["function"], rotation=0)
plt.ylabel("Proportion (Zoomed)")
plt.ylim(lo - pad, hi + pad)
plt.title("For/Against Proportions with Scaling Functions (Zoomed)")
plt.legend()
plt.tight_layout()
plt.savefig("cast_proportions.png", dpi=220)
plt.show()

is_humpy = df[votes_col] == df[votes_col].max()
is_50k = np.isclose(df[votes_col], 50_000.0, atol=200.0)
is_25k = (df[votes_col] >= 24_400) & (df[votes_col] <= 25_600)

rows = []
for name, func in functions.items():
    w = func(df[votes_col].values.astype(float))
    total = w.sum()
    shares = w / total if total>0 else w
    humpy_share = float(shares[is_humpy].mean()) if is_humpy.any() else np.nan
    avg50_share = float(shares[is_50k].mean()) if is_50k.any() else np.nan
    avg25_share = float(shares[is_25k].mean()) if is_25k.any() else np.nan
    rows.append({"function": name, "Humpy": humpy_share, "Avg_~50k": avg50_share, "Avg_~25k": avg25_share})

shares_df = pd.DataFrame(rows)
shares_df["function"] = pd.Categorical(shares_df["function"], categories=order, ordered=True)
shares_df = shares_df.sort_values("function")

x = np.arange(len(shares_df))
width = 0.25
plt.figure(figsize=(11,5))
plt.bar(x - width, shares_df["Humpy"], width, label="Humpy (~93k)")
plt.bar(x, shares_df["Avg_~50k"], width, label="Avg ~50k voter")
plt.bar(x + width, shares_df["Avg_~25k"], width, label="Avg ~25k voter")
plt.xticks(x, shares_df["function"], rotation=0)
plt.ylabel("Normalized Voting Share")
plt.title("Normalized Voting Share with Scaling Functions")
plt.legend()
plt.tight_layout()
plt.savefig("scaling.png", dpi=220)
plt.show()
