import ccxt
import pandas as pd
import time


def main():
    bian_exchange = ccxt.binance({
        "timeout": 15000,
        "enableRateLimit": True,
    })

    markets = bian_exchange.load_markets()

    # 选出三角套利的交易市场
    market_a = 'BTC'
    market_b = 'ETH'

    symbols = list(markets.keys())

    symbol_df = pd.DataFrame(data=symbols, columns=['symbol'])

    base_df = symbol_df['symbol'].str.split('/', expand=True)
    base_df.columns = ['base', 'quote']

    base_a_list = base_df[base_df['quote'] == market_a]['base'].values.tolist()
    base_b_list = base_df[base_df['quote'] == market_b]['base'].values.tolist()

    common_list = list(set(base_a_list).intersection(set(base_b_list)))
    print('有%s个计价货币相同' % len(common_list))
    print(common_list)

    columns = ['market_a', 'market_b', 'market_c', 'p1', 'p2', 'p3', 'profit']

    result_df = pd.DataFrame(columns=columns)
    last_min = bian_exchange.milliseconds() - 60 * 1000

    for base_coin in common_list:
        market_c = base_coin
        market_a_b_symbol = '{}/{}'.format(market_b, market_a)
        market_b_c_symbol = '{}/{}'.format(market_c, market_b)
        market_a_c_symbol = '{}/{}'.format(market_c, market_a)

        # 获取行情数据
        a_line = bian_exchange.fetch_ohlcv(market_a_b_symbol, since=last_min, timeframe='1m')
        b_line = bian_exchange.fetch_ohlcv(market_b_c_symbol, since=last_min, timeframe='1m')
        c_line = bian_exchange.fetch_ohlcv(market_a_c_symbol, since=last_min, timeframe='1m')

        if len(a_line) == 0 or len(b_line) == 0 or len(c_line) == 0:
            continue

        # 获取交易对价格
        p1 = a_line[0][4]
        p2 = b_line[0][4]
        p3 = c_line[0][4]

        profit = (p3 / (p2 * p1) - 1) * 1000

        result_df = result_df.append({
            'market_a': market_a,
            'market_b': market_b,
            'market_c': market_c,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'profit': profit
        }, ignore_index=True)

        print(result_df.tail(1))
        time.sleep(1)

    result_df.to_csv('./tri_res,csv')


if __name__ == '__main__':
    main()
