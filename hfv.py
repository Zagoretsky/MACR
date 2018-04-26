from bittrex import Bittrex, API_V2_0
from indicators import Indicators
import telepot
import time

CurrenciesOfInterest = ["BTC-ZEC", "BTC-ETH", "USDT-BTC", "BTC-BCC", "BTC-OMG"]
# "BTC-NEO", "BTC-TRX", "BTC-XRP", "BTC-GNT", "BTC-ADA", "BTC-BTG", "BTC-ETC", "BTC-DASH", "BTC-WAVES", "BTC-XMR", "BTC-DOGE", "BTC-LTC", "BTC-ARK", "BTC-XVG", "BTC-OMG", "BTC-BCC", ]
MA_FAST_PERIOD = 10
MA_SLOW_PERIOD = 100


bi = Bittrex(None, None, api_version=API_V2_0) 
market_sums = bi.get_market_summaries()['result']
markets = list(map(lambda m: m['Market']['MarketName'], market_sums))

def check(bi, market):
	candles = bi.get_candles(market, 'Hour')['result']
	closes = list(map(lambda c: c['C'], candles))

	ind = Indicators()
	maslow = ind.movingAverage(closes, MA_SLOW_PERIOD)
	mafast = ind.movingAverage(closes, MA_FAST_PERIOD)
	if mafast > maslow * 1.015:
		return "UP"
	elif maslow * 0.985 < mafast < maslow * 1.015:
		return "EARLY"
	elif mafast < maslow * 0.985:
		return "DOWN"

def MAoutput(bi, market):
	candles = bi.get_candles(market, 'Hour')['result']
	closes = list(map(lambda c: c['C'], candles))
	ind = Indicators()
	maslow = ind.movingAverage(closes, MA_SLOW_PERIOD)
	mafast = ind.movingAverage(closes, MA_FAST_PERIOD)
	return [mafast, maslow]
					

cyclecounter = 0		

def func():
	bot = telepot.Bot('572875215:AAHeDNnqpu8P5KIKrmeBYM7nx3a9RwZtfz4')
	comparedict = dict.fromkeys(CurrenciesOfInterest, [])
	for marketName in CurrenciesOfInterest:
		if check(bi, marketName) == "UP":
			string = '{} {}'.format(marketName, 'YES')
		elif check(bi, marketName) == "EARLY":
			string = '{} {}'.format(marketName, 'EARLY')
		else:
			string = '{} {}'.format(marketName, 'NO')
		#string = '{} {}'.format(marketName, 'YES' if check(bi, marketName) == "UP" else 'NO')
		comparedict[marketName] = [string, string]
	print(comparedict)	
	while True:
		time.sleep(300)
		global cyclecounter
		cyclecounter += 1
		if cyclecounter == 24:
			bot.sendMessage(-1001169060108, "Buddy, I'm working, hope you are doing well too")
			cyclecounter = 0
		else:
			pass	
		for cur in comparedict:
			if check(bi, cur) == "UP":
				string = '{} {}'.format(cur, 'YES')
			elif check(bi, cur) == "EARLY":
				string = '{} {}'.format(cur, 'EARLY')
			else:
				string = '{} {}'.format(cur, 'NO')		
			# string = '{} {}'.format(cur, 'YES' if check(bi, cur) == "UP" else 'NO')
			if len(comparedict[cur]) > 1:
				comparedict[cur] = comparedict[cur][-1:]
				comparedict[cur].append(string)
				if comparedict[cur][0][-3:] == "YES" and comparedict[cur][1][-2:] == "NO":
					bot.sendMessage(-1001169060108, "{} *sell signal* {} ".format(cur, MAoutput(bi, cur)))			
					print(comparedict[cur])
					print("{} trend has changed".format(cur))
				elif comparedict[cur][0][-2:] == "NO" and comparedict[cur][1][-3:] == "YES":
					bot.sendMessage(-1001169060108, "{} *buy signal* {} ".format(cur, MAoutput(bi, cur)))			
					print(comparedict[cur])
					print("{} trend has changed".format(cur))
				else:
					print("*****")
					print(comparedict[cur])
					print("{} trend is the same".format(cur))
					print("MA_fast {} MA_slow {}".format(MAoutput(bi, cur)[0], MAoutput(bi, cur)[1]))	

def main():
	try:
		func()
	except:
		pass


while True:
	main()