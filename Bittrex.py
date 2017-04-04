from bittrex.bittrex import Bittrex
import time as tm
time = 0
ntime = 0
what = None
api = Bittrex('secret', 'key')
uid = "0"
bit = 'BTC'
currency = 'DRACO'
market = '{0}-{1}'.format(bit, currency)
while True:
	history = api.get_order_history(market)
	id = history[unicode("result")][0][unicode("OrderUuid")]
	type = history[unicode("result")][0][unicode("OrderType")]
	dogecost = api.get_ticker(market)[unicode("result")][unicode("Ask")]
	amount = api.get_balances()[unicode("result")][0][unicode('Available')]/dogecost *.75
	if uid == id:
		if type == "LIMIT_SELL":
			print("buying")
			buy = api.buy_limit(market, amount, dogecost)
			uid = buy[unicode("result")][unicode("uuid")]
			sell = amount
			what = "buy"
			time = 0
		if type == "LIMIT_BUY":
			print("selling")
			cell = api.sell_limit(market, sell, dogecost*1.0125)
			uid = cell[unicode("result")][unicode("uuid")]
			print uid
			what = "sell"
			time = 0
	if uid == "0":
		print("buying")
		buy = api.buy_limit(market, amount, dogecost)
		print(buy)
		uid = buy[unicode("result")][unicode("uuid")]
		sell = amount
		time = 0
		what = "buy"
	print(time)
	time += 1
	tm.sleep(10)
	if time >= 6 and what == "buy":
		uid = "0"
		print("canceling")
		print(api.cancel(uid))
		tm.sleep(10)
