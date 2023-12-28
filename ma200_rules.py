import email_config
from binance.client import Client
import binance_api

def calculate_ma200(symbol):
    try:
        klines = binance_api.client.futures_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "200 day ago UTC")
        if len(klines) < 200:
            return None
        sum = 0
        for kline in klines:
            sum += float(kline[4]) # 收盘价
        return sum / 200
    except Exception as e:
        print(f"计算MA200时发生错误: {e}")
        return None

def send_emails_for_price_ranges(price_ranges):
    for stage, symbols in price_ranges.items():
        if symbols:
            email_body = f"以下交易对处于MA200的{stage}%区间内：\n" + "\n".join(symbols)
            email_config.send_email(
                f"您的新机会-- MA200的{stage}%",
                email_body,
                email_config.TO_EMAIL,
                email_config.FROM_EMAIL,
                email_config.SMTP_AUTH_PASSWORD
            )
def check_price_and_send_email(symbol, ma200, current_price, price_ranges):
    percentage_of_ma200 = (current_price / ma200) * 100
    symbol_display = symbol.replace('USDT', '')  # 去掉交易对名称中的"USDT"

    # 定义价格区间
    if 95 <= percentage_of_ma200 < 98:
        price_ranges[95].append(symbol_display)
    elif 98 <= percentage_of_ma200 < 99.5:
        price_ranges[98].append(symbol_display)
    elif 99.5 <= percentage_of_ma200 <= 100.5:
        price_ranges[100].append(symbol_display)
    elif 100.5 <= percentage_of_ma200 < 103:
        price_ranges[103].append(symbol_display)
    elif 103 <= percentage_of_ma200 <= 105:
        price_ranges[105].append(symbol_display)

def update_ma200_values(symbols):
    return {symbol: calculate_ma200(symbol) for symbol in symbols}
