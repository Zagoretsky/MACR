from indicators import Indicators
import ccxt
import telepot
import time
import json

CurrenciesOfInterest = ["ZEC/BTC", "ETH/BTC", "BTC/USDT","BCH/BTC","OMG/BTC"]
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 100

def masub(market):
	ind = Indicators()
	binl = binance.fetch_ohlcv(market, timeframe='1h', since=None, limit=None, params={})
	closes = list(map(lambda binl: binl[-2],binl))
	ind = Indicators()
	maslow = ind.movingAverage(closes, MA_SLOW_PERIOD)
	mafast = ind.movingAverage(closes, MA_FAST_PERIOD)
	masub = (mafast/maslow) - 1
	return masub

def signal(currency):
	if masub(currency) > 0.01:
		return "BUY"
	elif masub(currency) < -0.01:
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

CurrentSignals = {}

def SignalDict():
    global CurrentSignals
    try:
        with open("Signals.json") as r:
            CurrentSignals = (json.load(r))
    except:
        CurrentSignals = dict.fromkeys(CurrenciesOfInterest, [])


def Bot():

	bot = telepot.Bot('572875215:AAHeDNnqpu8P5KIKrmeBYM7nx3a9RwZtfz4')

	global comparedict
	global CurrentSignals

	while True:
		DictFormation()
		SignalDict()
		for pair in comparedict:
			if comparedict[pair][0] != "BUY" and comparedict[pair][1] == "BUY" and CurrentSignals[pair] != ["BUY SIGNAL"]:
				string = (pair, "BUY SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["BUY SIGNAL"]
			elif comparedict[pair][0] != "SELL" and comparedict[pair][1] == "SELL" and CurrentSignals[pair] == ["BUY SIGNAL"]:
				string = (pair, "SELL SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["SELL SIGNAL"]
			else:
				print(pair, "Trend is the same")
		print(comparedict)
		print(CurrentSignals)
		with open("Signals.json", 'w') as f:
			json.dump(CurrentSignals, f)
		time.sleep(180)

def main():
	try:
		Bot()
	except:
		pass
while True:
	main()
