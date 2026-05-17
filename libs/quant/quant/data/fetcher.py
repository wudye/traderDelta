
import pandas as pd
import yfinance as yf
import re
import requests
from typing import List, Optional, Dict, Any
from ..core.base import BaseComponent
from .cleaner import DataCleaner
import warnings
warnings.filterwarnings("ignore")

class DataFetcher(BaseComponent):

    def __init__(self, source: str="yahoo", **kwargs:Any) -> None:
        super().__init__(**kwargs)
        self.source = source
        self.cleaner = None
        self.logger.info(f"DataFetcher initialized with source: {self.source}")

    def _ensure_cleaner(self) -> None:
        if self.cleaner is None:
            self.cleaner = DataCleaner()

    def fetch_data(self, symbol: str, start_date: str, end_date: Optional[str] = None, clean: bool = False,
                   interval: str = "1d") -> pd.DataFrame:

        try:
            self.logger.info(f"Fetching data for {symbol} from {self.source} with interval {interval}")
            if self.source == "miniqmt":
                from .miniqmt_xtdata import fetch_miniqmt_bars
                df = fetch_miniqmt_bars(symbol, start_date, end_date, interval=interval)

            elif self.source == "yahoo":
                data = yf.download(symbol, start=start_date, end=end_date, interval=interval, progress=False)
                if isinstance(data.columns, pd.MultiIndex) and data.columns.nlevels > 1:
                    data = data.droplevel(level=1, axis=1)
                if clean:
                    self._ensure_cleaner()
                    data = self.cleaner.dropna(data)
                return data
            else:
                raise ValueError(f"Unsupported data source: {self.source}")

        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol} from {self.source}: {e}")
            raise RuntimeError(f"Failed to fetch data for {symbol} from {self.source}") from e


    def fetch_data_test(self):
        return pd.DataFrame({
            "Open": [100, 102, 101],
            "High": [105, 106, 104],
            "Low": [99, 101, 100],
            "Close": [104, 105, 102],
            "Volume": [1000, 1500, 1200]
        }, index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]))


