from bittrex import Bittrex, API_V2_0
from indicators import Indicators
import telepot
import time

CurrenciesOfInterest = ["BTC-ZEC", "BTC-ETH", "USDT-BTC", "BTC-BCC", "BTC-OMG"]
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 100

bi = Bittrex(None, None, api_version=API_V2_0)
market_sums = bi.get_market_summaries()['result']
markets = list(map(lambda m: m['Market']['MarketName'], market_sums))

def masub(market):
	candles = bi.get_candles(market, 'hour')['result']
	closes = list(map(lambda c: c['C'], candles))
	ind = Indicators()
	maslow = ind.movingAverage(closes, MA_SLOW_PERIOD)
	mafast = ind.movingAverage(closes, MA_FAST_PERIOD)
	masub = (mafast/maslow) - 1
	return masub

def signal(currency):
	if masub(currency) > 0.015:
		return "BUY"
	elif masub(currency) < -0.015:
		return "SELL"
	else:
		return "EARLY"

comparedict = dict.fromkeys(CurrenciesOfInterest, [])

def DictFormation():
	global comparedict
	for marketName in CurrenciesOfInterest:
		if len(comparedict[marketName]) == 0:
			comparedict[marketName] = [signal(marketName), signal(marketName)]
		elif len(comparedict[marketName]) == 2:
			comparedict[marketName] = [comparedict[marketName][-1],signal(marketName)]

CurrentSignals = dict.fromkeys(CurrenciesOfInterest, [])
cyclecounter = 0

def Bot():
	while True:
		bot = telepot.Bot('572875215:AAHeDNnqpu8P5KIKrmeBYM7nx3a9RwZtfz4')
		global cyclecounter
		cyclecounter += 1
		if cyclecounter == 30:
			bot.sendMessage(-1001169060108, "Buddy, I'm working, hope you are doing well too")
			cyclecounter = 0
		else:
			pass
		DictFormation()
		global comparedict
		global CurrentSignals
		for pair in comparedict:
			if comparedict[pair][0] != "BUY" and comparedict[pair][1] == "BUY" and CurrentSignals[pair] != ["BUY SIGNAL"]:
				string = (pair, "BUY SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["BUY SIGNAL"]
			elif comparedict[pair][0] != "SELL" and comparedict[pair][1] == "SELL" and CurrentSignals[pair] != ["SELL SIGNAL"]:
				string = (pair, "SELL SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["SELL SIGNAL"]
			else:
				print(pair, "Trend is the same")
		print(comparedict)
		print(CurrentSignals)
		time.sleep(180)

def main():
	try:
		Bot()
	except:
		pass
while True:
	main()
