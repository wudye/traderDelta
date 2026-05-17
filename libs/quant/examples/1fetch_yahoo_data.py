

from quant.data import DataFetcher


def main():
    fetcher = DataFetcher()
    data = fetcher.fetch_data(symbol="AAPL", start_date="2024-01-01", end_date="2024-01-10")
    print(data)

if __name__ == "__main__":
    main()