import ccxt

# 初始化
bian_exchange = ccxt.binance({
    "timeout": 15000,
    "enableRateLimit": True,

})
# ss = bian_exchange.load_markets()
# 查询账户余额
ba = bian_exchange.fetch_balance()
print(ba['total']['USDT'])
# 可用
print(ba['free']['USDT'])
# 已使用
print(ba['used']['USDT'])


symbol = 'ETH/USDT'
# 买卖订单 buy/sell
# if bian_exchange.has['createLimitOrder']:
#     bian_exchange.create_order(symbol=symbol, side='buy', type='limit', price=100, amount=0.1)
#     bian_exchange.create_order(symbol=symbol, side='buy', type='limit', price=100, amount=0.2)

print(ba['total']['USDT'])
# 可用
print(ba['free']['USDT'])
# 已使用
print(ba['used']['USDT'])

# 获取订单
# print(bian_exchange.fetch_open_orders(symbol))

# 取消订单
# open_orders = bian_exchange.fetch_open_orders(symbol)
# if bian_exchange.has['cancelOrder']:
#     for order in open_orders:
#         orderId = order['info']['orderId']
#         bian_exchange.cancel_order(orderId, symbol)

print(bian_exchange.fetch_open_orders(symbol))
