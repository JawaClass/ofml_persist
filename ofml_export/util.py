from enum import Enum
from pathlib import Path
import pandas as pd


def col_enum_extract_value(col: pd.Series):
    return col.apply(lambda x: x.value if isinstance(x, Enum) else x)


def fill_columns(df: pd.DataFrame, columns: list[str]):
    for c in columns:
        if c not in df.columns:
            df[c] = None
    return df


def as_path(path: str | Path):
    if isinstance(path, str):
        path = Path(path)
    return path
