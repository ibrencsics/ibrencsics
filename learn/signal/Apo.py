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