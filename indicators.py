import numpy as np

class Indicators(object):
    def __init__(self):
         pass

    def movingAverage(self, dataPoints, period):
        if len(dataPoints) < period:
            return self.movingAverage(dataPoints, len(dataPoints))
        else:
            return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))

    def momentum (self, dataPoints, period=14):
        if (len(dataPoints) > period -1):
            return dataPoints[-1] * 100 / dataPoints[-period]

    def EMA(self, prices, period):
        if len(prices) < period:
            return self.EMA(prices, len(prices))

        x = numpy.asarray(prices)
        weights = None
        weights = numpy.exp(numpy.linspace(-1., 0., period))
        weights /= weights.sum()

        a = numpy.convolve(x, weights, mode='full')[:len(x)]
        a[:period] = a[period]
        return a

    def sma(self, data, window):
        """
        Calculates Simple Moving Average
        http://fxtrade.oanda.com/learn/forex-indicators/simple-moving-average
        """
        if len(data) < window:
            return None
        return sum(data[-window:]) / float(window)

    def ema(self, data, window):
        if len(data) < 2 * window:
            raise ValueError("data is too short")
        c = 2.0 / (window + 1)
        current_ema = self.sma(data[-window*2:-window], window)
        for value in data[-window:]:
            current_ema = (c * value) + ((1 - c) * current_ema)
        return current_ema

    def MACD(self, prices, nslow=26, nfast=12):
        emaslow = self.EMA(prices, nslow)
        emafast = self.EMA(prices, nfast)
        return emaslow, emafast, emafast - emaslow

    def TR(self, c, h, l, o, yc):
        x = h-l
        y = abs(h-yc)
        z = abs(l-yc)

        return max(x, y, z)          

    def ExpMovingAverage(values, window):
        weights = np.exp(np.linspace(-1., 0., window))
        weights /= weights.sum()
        a =  np.convolve(values, weights, mode='full')[:len(values)]
        a[:window] = a[window]
        return 

        #ATR = ExpMovingAverage(TrueRanges,14)          

    def RSI (self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1. + rs)
 
        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
 
            up = (up*(period - 1) + upval)/period
            down = (down*(period - 1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)
        if len(prices) > period:
            return rsi[-1]
        else:
            return 50 # output a neutral amount until enough prices in list to calculate RSI
