from learn.signal.Ema import Ema

class Apo:

    def __init__(self):
        self.ema = Ema()

    def calculate(self, series, period_fast, period_slow, k):
        ema_fast = self.ema.calculate(series, period_fast, k)
        ema_slow = self.ema.calculate(series, period_slow, k)
        apo = ema_fast - ema_slow
        apo.name = 'apo'
        return ema_fast, ema_slow, apo

    def calculateWithStdev(self, series, period_fast, period_slow, k, period_stdev):
        ema_fast, stdev_factor_fast = self.ema.calculateWithStdev(series, period_fast, k, period_stdev)
        ema_slow, stdev_factor_slow = self.ema.calculateWithStdev(series, period_slow, k, period_stdev)
        apo = ema_fast - ema_slow
        apo.name = 'apo'
        return ema_fast, ema_slow, apo, stdev_factor_fast