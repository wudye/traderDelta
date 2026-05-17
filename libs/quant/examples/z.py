from quant.data import fetch_miniqmt_bars

df = fetch_miniqmt_bars(
    symbol="000001.SZ",
    start_date="2024-01-01",
    end_date="2024-12-31",
    interval="1d",
    use_mock=True  # 设置为 True 以使用模拟数据
)

print(df.head())
