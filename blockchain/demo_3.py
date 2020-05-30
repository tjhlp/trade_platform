import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from catalyst import run_algorithm
from catalyst.api import record, symbol, order_target_percent
from catalyst.exchange.utils.stats_utils import extract_transactions

NAMESPACE = 'dual_moving_average'
SIGNAL_BUY = 'buy'  # 买入信号
SIGNAL_sell = 'sell'
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


if __name__ == '__main__':
    pass
