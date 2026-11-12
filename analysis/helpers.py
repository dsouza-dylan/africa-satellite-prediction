# Imports
import os
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

warnings.filterwarnings("ignore")
pd.set_option("io.parquet.engine", "fastparquet")

# Path variables
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(BASE, "data", "raw")
PROC = os.path.join(BASE, "data", "processed")
OUT  = os.path.join(BASE, "results")
FIG  = os.path.join(BASE, "figures")
MOSAIKS_DIR = os.path.join(RAW, "mosaiks")
GDL_DIR     = os.path.join(RAW, "gdl_indicators")
SHP_DIR     = os.path.join(RAW, "shapefiles")

for d in (PROC, OUT, FIG):
    os.makedirs(d, exist_ok=True)

# Constants
OUTCOMES = ["iwi", "iwipov70", "stunting", "u5mort", "dtp3age1", "gap_eye", "shdi"]

OUTCOME_LABELS = {
    "iwi":       "IWI (Wealth)",
    "iwipov70":  "Poverty rate",
    "stunting":  "Stunting",
    "u5mort":    "U5 mortality",
    "dtp3age1":  "DTP3 coverage",
    "gap_eye":   "Gender schooling gap",
    "shdi":      "SHDI",
}

AFRICA_REGION = {
    # West Africa
    "BEN":"West","BFA":"West","CIV":"West","CPV":"West","GHA":"West","GIN":"West",
    "GMB":"West","GNB":"West","LBR":"West","MLI":"West","MRT":"West","NER":"West",
    "NGA":"West","SEN":"West","SLE":"West","TGO":"West",
    # East Africa
    "BDI":"East","COM":"East","DJI":"East","ERI":"East","ETH":"East","KEN":"East",
    "MDG":"East","MUS":"East","RWA":"East","SDN":"East","SOM":"East","SSD":"East",
    "SYC":"East","TZA":"East","UGA":"East",
    # Central Africa
    "AGO":"Central","CAF":"Central","CMR":"Central","COD":"Central","COG":"Central",
    "GAB":"Central","GNQ":"Central","STP":"Central","TCD":"Central",
    # Southern Africa
    "BWA":"Southern","LSO":"Southern","MOZ":"Southern","MWI":"Southern","NAM":"Southern",
    "SWZ":"Southern","ZAF":"Southern","ZMB":"Southern","ZWE":"Southern",
    # North Africa
    "DZA":"North","EGY":"North","ESH":"North","LBY":"North","MAR":"North","TUN":"North",
}

ALPHAS = np.logspace(-1, 5, 10)


# Helper functions
def load_gdl(filename, cols):
    path = os.path.join(GDL_DIR, filename)
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    keep = ["isocode3","country","continent","datasource","year","gdlcode","level","region"] + cols
    keep = [c for c in keep if c in df.columns]
    df = df[keep]
    df = df[(df["level"] == "Subnat") & (df["continent"] == "Africa")]
    return df


def pick_closest_year(df, value_cols, target_year=2019, max_gap=5):
    df = df.dropna(subset=value_cols, how="all").copy()
    df["year_gap"] = (df["year"] - target_year).abs()
    df["year_off"] = df["year"] - target_year
    df = df.sort_values(["gdlcode", "year_gap", "year_off"])
    df = df.drop_duplicates(subset="gdlcode", keep="first")
    df = df[df["year_gap"] <= max_gap]
    for col in value_cols:
        if col in df.columns:
            df[f"{col}_year"] = df["year"].where(df[col].notna(), pd.NA)
    return df.drop(columns=["year_gap", "year_off"])


def fit_ridge_cv(X_tr, y_tr, groups, X_te, alphas=ALPHAS):
    n_splits = min(5, len(np.unique(groups)))
    gkf = GroupKFold(n_splits=n_splits)
    best_alpha, best_score = alphas[0], -np.inf
    for alpha in alphas:
        scores = []
        for tr, va in gkf.split(X_tr, y_tr, groups):
            m = Ridge(alpha=alpha, solver="lsqr", max_iter=2000)
            m.fit(X_tr[tr], y_tr[tr])
            p = m.predict(X_tr[va])
            if len(np.unique(y_tr[va])) > 1:
                scores.append(r2_score(y_tr[va], p))
        if scores and np.mean(scores) > best_score:
            best_score = np.mean(scores)
            best_alpha = alpha
    model = Ridge(alpha=best_alpha, solver="lsqr", max_iter=2000)
    model.fit(X_tr, y_tr)
    return model.predict(X_te), best_alpha


def compute_metrics(y_true, y_pred):
    if len(y_true) < 2:
        return np.nan, np.nan, np.nan
    r2  = r2_score(y_true, y_pred) if len(np.unique(y_true)) > 1 else np.nan
    mae = mean_absolute_error(y_true, y_pred)
    rho = stats.spearmanr(y_true, y_pred).correlation if len(y_true) > 2 else np.nan
    return r2, mae, rho
