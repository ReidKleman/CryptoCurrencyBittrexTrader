from bittrex.bittrex import Bittrex
import time as tm
time = 0
ntime = 0
what = None
#your bittrex api secret and key go below
api = Bittrex("secret", "key")
uid = "0"
#base currency
base = "BTC"
#currency selection
user = input("please enter the currency you would like to trade, enter 1 for a list of currencies or enter 2 for us to pick a currency with the highest 1 day change ")
if user == 1:
	for coins in  api.get_currencies()["result"]:
		if coins["CoinType"] == "BITCOIN":
			print coins["Currency"]
	user = input("please type your selected currency")
if user == 2:
	#calculates highest day change
	high = 0
	for cur in api.get_market_summaries()["result"]:
		change = float(cur["PrevDay"])/float(cur["Bid"])
		if change > high:
			high = change
			user = cur["MarketName"].split("-")[1]
	print(user)
#puts base currnecy and market currency in correct format
market = base+"-"+user
percent = int(input("what percent of your bitcion do you want to use per order"))/100
sellp = (int(input("at what percent increase do you want to sell"))/100)+1
while True:
	#gets the pervious order so it knows wether to buy or sell mext
	try:
		history = api.get_order_history(market)
		id = history[unicode("result")][0][unicode("OrderUuid")]
		type = history[unicode("result")][0][unicode("OrderType")]
	except:
		id = 0
		type = "LIMIT_SELL"
	#gets the market cost
	cost = api.get_ticker(market)[unicode("result")][unicode("Ask")]
	#gets how much ti buy
	amount = api.get_balances()[unicode("result")][0][unicode('Available')]/cost *percent
	if uid == id:
		if type == "LIMIT_SELL":
			print("buying")
			#buys at market price
			buy = api.buy_limit(market, amount, cost)
			uid = buy[unicode("result")][unicode("uuid")]
			sell = amount
			what = "buy"
			time = 0
		if type == "LIMIT_BUY":
			print("selling")
			#sells at specified price
			cell = api.sell_limit(market, sell, cost*sellp)
			uid = cell[unicode("result")][unicode("uuid")]
			print uid
			what = "sell"
			time = 0
			#checks if this is forst order
	if uid == "0":
		print("buying")
		#buys at market price
		buy = api.buy_limit(market, amount, cost)
		print(buy)
		uid = buy[unicode("result")][unicode("uuid")]
		sell = amount
		time = 0
		what = "buy"
	print(time)
	time += 1
	tm.sleep(5)
	#how long it waits before just selling at market defualt 4 hours
	if time >= 2880 and what == "buy":
		uid = "0"
		print("canceling")
		api.cancel(uid)
		tm.sleep(10)
		api.sell_market(market, sell)
