from bittrex import Bittrex, API_V2_0
from indicators import Indicators
import telepot
import time
import json

CurrenciesOfInterest = ["BTC-ZEC", "BTC-ETH", "USDT-BTC", "BTC-BCC", "BTC-OMG"]
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 100

bi = Bittrex(None, None, api_version=API_V2_0)
market_sums = bi.get_market_summaries()['result']
markets = list(map(lambda m: m['Market']['MarketName'], market_sums))

#function returns the result of a substraction of fast and slow MAs of a given pair
def masub(market):
	candles = bi.get_candles(market, 'thirtyMin')['result']
	closes = list(map(lambda c: c['C'], candles))
	ind = Indicators()
	maslow = ind.movingAverage(closes, MA_SLOW_PERIOD)
	mafast = ind.movingAverage(closes, MA_FAST_PERIOD)
	masub = (mafast/maslow) - 1
	return masub


# function determines whether the current trend is negative/positive or negligible
# "Early" is needed to ignore market noise
def signal(currency):
	if masub(currency) > 0.01:
		return "BUY"
	elif masub(currency) < -0.01:
		return "SELL"
	else:
		return "EARLY"


comparedict = dict.fromkeys(CurrenciesOfInterest, [])

# creating and updating dictionary which contains status of a current trend for each pair
def DictFormation():
	global comparedict
	for marketName in CurrenciesOfInterest:
		if len(comparedict[marketName]) == 0:
			comparedict[marketName] = [signal(marketName), signal(marketName)]
		elif len(comparedict[marketName]) == 2:
			comparedict[marketName] = [comparedict[marketName][-1],signal(marketName)]

CurrentSignals = {}

# if there is no file with filled in dictionary, it is created from scratch
# "try" is preventing the function from crashing because of loading a file that is empty/non existent
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
			# if current trend is becoming positive and its current status hasnt't yet reflected this, a buy signal appeares
			if comparedict[pair][0] != "BUY" and comparedict[pair][1] == "BUY" and CurrentSignals[pair] != ["BUY SIGNAL"]:
				string = (pair, "BUY SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				# Status of a given pair is first emptied and then changed to "Buy"
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["BUY SIGNAL"]
			# if current trend is becoming negative and its current status hasnt't yet reflected this, a sell signal appeares
			elif comparedict[pair][0] != "SELL" and comparedict[pair][1] == "SELL" and CurrentSignals[pair] == ["BUY SIGNAL"]:
				string = (pair, "SELL SIGNAL")
				print(string)
				bot.sendMessage(-1001169060108, "{}".format(string))
				CurrentSignals[pair] = []
				CurrentSignals[pair] = ["SELL SIGNAL"]
			else:
				print(pair, "Trend is the same")
				# all print statements are needed to monitor the ongoing procces in console
		print(comparedict)
		print(CurrentSignals)
		# with a cycle ended, an update is made to the signals dictionary
		with open("Signals.json", 'w') as f:
			json.dump(CurrentSignals, f)
		time.sleep(180)

# provides an infinitely running cycle in case there are errors in "Bot" function
def main():
	try:
		Bot()
	except:
		pass
while True:
	main()
