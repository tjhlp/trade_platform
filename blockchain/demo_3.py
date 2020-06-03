import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from catalyst import run_algorithm
from catalyst.api import record, symbol, order_target_percent
from catalyst.exchange.utils.stats_utils import extract_transactions

NAMESPACE = 'dual_moving_average'
SIGNAL_BUY = 'buy'  # 买入信号
SIGNAL_SELL = 'sell'
SIGNAL_INIT = ''
SHORT_WIN = 5  # 短周期窗口
LONG_WIN = 20


def initialize(context):
    """
    初始化
    :param context:
    :return:
    """
    context.i = 0  # 交易周期
    context.asset = symbol('btc_usdt')  # 交易对
    context.base_price = None  # 初始价格
    context.signal = SIGNAL_INIT  # 交易信号
    context.set_commission(maker=0.001, taker=0.001)  # 设置手续费
    context.set_slippage(slippage=0.001)  # 设置滑点


def handle_data(context, data):
    context.i += 1
    if context.i < LONG_WIN + 2:
        return

    history_data = data.history(
        context.asset,
        'close',
        bar_count=LONG_WIN + 2,
        frequency='1D'
    )

    # 获取当前持仓数量
    pos_amount = context.portfolio.positions[context.asset].amount

    # 计算双均线
    short_avgs = history_data.rolling(window=SHORT_WIN).mean()
    long_avgs = history_data.rolling(window=LONG_WIN).mean()

    # 短期线上穿长期均线，买入
    if (short_avgs[-3] < long_avgs[-3]) and (short_avgs[-2] < long_avgs[-2]) and pos_amount == 0:
        order_target_percent(asset=context.asset, target=1)
        context.signal = SIGNAL_BUY

    # 短期线下穿长期均线，做空
    if (short_avgs[-3] > long_avgs[-3]) and (short_avgs[-2] > long_avgs[-2]) and pos_amount > 0:
        order_target_percent(asset=context.asset, target=0)
        context.signal = SIGNAL_SELL

    # 获取当前价格
    price = data.current(context.asset, 'price')
    if context.base_price is None:
        context.base_price = price

    price_change = (price - context.base_price) / context.base_price

    record(
        price=price,
        cash=context.portfolio.cash,
        price_change=price_change,
        short_avgs=short_avgs[-1],
        long_avgs=long_avgs[-1],
        signal=context.signal
    )
    print('date:{}, price:{}, cash:{}, res:{:.8f},{}').format(
        data.current_dt, price, context.portfolio.portfolio_value, pos_amount, context.signal
    )

    # 重置交易信号
    context.signal = SIGNAL_INIT


def analyze(context, perf):
    perf.to_csv('./performance.csv')

    # 获取交易所的计价货币
    exchange = list(context.exchange.values())[0]
    quote_currency = exchange.quote_currency.upper()
    pass


if __name__ == '__main__':
    pass
