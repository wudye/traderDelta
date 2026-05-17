import pandas as pd
from typing import Optional
from ..core.base import BaseComponent

class DataCleaner(BaseComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.info("DataCleaner initialized")


    def dropna(self, data: pd.DataFrame) -> pd.DataFrame:
        cleaned_data = data.dropna()
        self.logger.info(f"Dropped NaN rows: {len(data)} -> {len(cleaned_data)} rows")
        return cleaned_data

    def fillna(self, data: pd.DataFrame, method: str = "forward") -> pd.DataFrame:

        na_count_before = data.isna().sum().sum()

        if method == "forward":
            fill_data = data.ffill()
        elif method == "backward":
            fill_data = data.bfill()
        else:
            fill_data = data.fillna(0)

        na_count_after = fill_data.isna().sum().sum()
        self.logger.info(f"Filled NaN rows: {na_count_before} -> {na_count_after} rows")
        return fill_data
    