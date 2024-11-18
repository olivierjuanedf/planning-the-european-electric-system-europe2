import pandas as pd
from typing import Dict, List
from datetime import datetime

from long_term_uc.utils.basic_utils import get_key_of_val


def cast_df_col_as_date(df: pd.DataFrame, date_col: str, date_format: str) -> pd.DataFrame:
    df[date_col] = df[date_col].apply(lambda x: datetime.strptime(x, date_format))
    return df


def selec_in_df_based_on_list(df: pd.DataFrame, selec_col, selec_vals: list, rm_selec_col=False) -> pd.DataFrame:
    val = df.loc[df[selec_col].isin(selec_vals)]
    if rm_selec_col:
        val = val.drop(columns=[selec_col])
    return val


def concatenate_dfs(dfs: List[pd.DataFrame], reset_index: bool = True) -> pd.DataFrame:
    df_concat = pd.concat(dfs, axis=0)
    if reset_index is True:
        df_concat = df_concat.reset_index(drop=True)
    return df_concat


def set_aggreg_col_based_on_corresp(df: pd.DataFrame, col_name: str, created_agg_col_name: str, val_cols: List[str],
                                    agg_corresp: Dict[str, List[str]], common_aggreg_ope, other_col_for_agg: str = None) -> pd.DataFrame:
    df[created_agg_col_name] = df[col_name].apply(get_key_of_val, args=(agg_corresp,)) 
    agg_operations = {col: common_aggreg_ope for col in val_cols}
    if other_col_for_agg is not None:
        gpby_cols = [created_agg_col_name]
        gpby_cols.append(other_col_for_agg)
    else:
        gpby_cols = created_agg_col_name
    df = df.groupby(gpby_cols).agg(agg_operations).reset_index()
    return df


def get_subdf_from_date_range(df: pd.DataFrame, date_col: str, date_min: datetime, date_max: datetime) -> pd.DataFrame:
    """
    Get values in a dataframe from a date range
    """
    df_range = df[(date_min <= df[date_col]) & (df[date_col] < date_max)]
    return df_range


def create_dict_from_cols_in_df(df: pd.DataFrame, key_col, val_col) -> dict:
    df_to_dict = df[[key_col, val_col]]
    return dict(pd.MultiIndex.from_frame(df_to_dict))