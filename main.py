import time
import binance_api
import ma200_rules
from datetime import datetime

def main():
    last_update_day = None
    ma200_values = {}
    previous_prices = {}

    while True:
        current_day = datetime.now().date()
        if current_day != last_update_day:
            futures_symbols = binance_api.get_futures_symbols()
            ma200_values = ma200_rules.update_ma200_values(futures_symbols)
            previous_prices = {symbol: None for symbol in futures_symbols}
            last_update_day = current_day

        price_ranges = {95: [], 98: [], 100: [], 103: [], 105: []}
        for symbol in futures_symbols:
            ma200 = ma200_values.get(symbol)
            if ma200:
                current_price, _ = binance_api.get_current_and_previous_price(symbol, previous_prices)
                if current_price is not None:
                    ma200_rules.check_price_and_send_email(
                        symbol, ma200, current_price, price_ranges
                    )
                previous_prices[symbol] = current_price

                # 调整MA200的小数位数
                decimal_places = len(str(current_price).split('.')[1]) if '.' in str(current_price) else 0
                ma200_formatted = f"{ma200:.{decimal_places}f}"

                # 打印交易对，最新价和MA200价格
                print(f"交易对: {symbol}, 最新价格: {current_price}, MA200: {ma200_formatted}")

        ma200_rules.send_emails_for_price_ranges(price_ranges)

        time.sleep(60 * 5)  # 每5分钟检查一次

if __name__ == "__main__":
    main()