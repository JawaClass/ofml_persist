import enum
import functools
from pprint import pprint
from typing import Any, TypeVar
import ofml_api.repository as ofml
import pandas as pd


def format_text_table(df: pd.DataFrame):
    df.loc[df["text"].isna(), "text"] = ""
    return df


def extract_single_row(
    df: pd.DataFrame, filter_mask: pd.Series, assert_shape_1: bool = True
):
    result = df.loc[filter_mask]
    if assert_shape_1:
        if not result.shape[0] == 1:
            raise NotOneResultException(
                f"""extract_single_row expected length 1, was {result.shape[0]}:: {result.columns}
{result.to_string()}
! see assert error above
"""
            )
    elif result.empty:
        return None
    row = result.iloc[0]
    return row


class EmptyResultException(Exception):
    pass


class NotOneResultException(Exception):
    pass


def extract_multi_row(
    df: pd.DataFrame, filter_mask: pd.Series, assert_not_empty: bool = True
):
    result = df.loc[filter_mask]
    if assert_not_empty:
        # assert not result.empty
        if result.empty:
            raise EmptyResultException()
    elif result.empty:
        return None
    return result


def make_df_filter_mask(df: pd.DataFrame, filter_mask: dict[str, Any]):
    mask = True
    for k, v in filter_mask.items():
        mask &= df[k] == v
    return mask


def extract_multi_row2(
    table_name: str,
    df: pd.DataFrame,
    filter_mask: dict[str, Any],
    assert_not_empty: bool = True,
):
    mask = make_df_filter_mask(df, filter_mask)
    try:
        return extract_multi_row(df, mask, assert_not_empty)
    except EmptyResultException as e:
        filter_mask_string = ", ".join([f"{k}={v}" for k, v in filter_mask.items()])
        e.add_note(f"No result for {table_name} :: {filter_mask_string}")
        raise


def extract_single_row2(
    table_name: str,
    df: pd.DataFrame,
    filter_mask: dict[str, Any],
    assert_shape_1: bool = True,
):
    mask = make_df_filter_mask(df, filter_mask)
    try:
        return extract_single_row(df, mask, assert_shape_1)
    except NotOneResultException as e:
        filter_mask_string = ", ".join([f"{k}={v}" for k, v in filter_mask.items()])
        e.add_note(
            f"Expected exactly 1 result for {table_name} :: {filter_mask_string}"
        )
        raise


def fmt_tables_na2none(ofml_part: ofml.OFMLPart):
    for table_name, table in ofml_part.tables.items():
        if isinstance(table, ofml.NotAvailable):
            print("table", table_name, "was NotAvailable!")
            input(".")
            continue
        table.df = table.df.where(table.df.notnull(), None)


def make_insert_key(*keys):
    return "::".join(map(str, keys))


def memoize_insert(table_name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cache = self.identy_map_by_key[table_name]

            key = make_insert_key(*args, **kwargs)
            if key in cache:
                return cache[key]
            result = func(self, *args, **kwargs)
            cache[key] = result
            return result

        return wrapper

    return decorator


T = TypeVar("T")


def copy_orm_object(obj: T, no_ids=True) -> T:
    if isinstance(obj, (bool, str, int, float, type(None), enum.Enum)):
        return obj
    if isinstance(obj, list):
        return [copy_orm_object(_) for _ in obj]
    cls = obj.__class__

    print("copy_orm_object...", type(obj))
    print(obj)

    kwargs = {
        k: copy_orm_object(v)
        for k, v in obj.__dict__.items()
        if not k.startswith("_") and (no_ids == False or not k.endswith("id"))
    }

    print("")
    # print(obj)
    return cls(**kwargs)
