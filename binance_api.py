from binance.client import Client
from datetime import datetime

# 初始化币安客户端
client = Client(api_key='sHFJLpsVoCNIrRG2sWyM0zUJSrm53FKaIHcsVtrDVVVdvhPifiOVRfZnAdwga3uV',
                api_secret='Q87wvUPzpkBSJDqsupDSNSVXBn5qTIEqSqBgZiGjANspnMmByUmEtmAodrv1s39J')

last_update_day = None
futures_symbols = []

# 要排除的交易对列表
exclude_symbols = [
    "COCOSUSDT", "USDCUSDT", "TOMOUSDT", "SRMUSDT", "HNTUSDT",
    "BTSUSDT", "BTCSTUSDT", "SCUSDT", "BTCDOMUSDT", "RAYUSDT", "ETHBTC"
]

def update_futures_symbols():
    global last_update_day, futures_symbols
    current_day = datetime.now().date()
    if current_day != last_update_day:
        futures_exchange_info = client.futures_exchange_info()
        # 过滤掉不需要的交易对
        futures_symbols = [s['symbol'] for s in futures_exchange_info['symbols'] if s['symbol'] not in exclude_symbols]
        last_update_day = current_day

def get_futures_symbols():
    update_futures_symbols()
    return futures_symbols

def get_current_and_previous_price(symbol, previous_prices):
    ticker = client.futures_ticker(symbol=symbol)
    if 'lastPrice' in ticker:
        current_price = float(ticker['lastPrice'])
        previous_price = previous_prices.get(symbol)
        return current_price, previous_price
    return None, None