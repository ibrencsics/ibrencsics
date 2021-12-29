from learn.signal.Apo import Apo
from learn.signal.Ema import Ema


class Macd:

    def __init__(self):
        self.ema = Ema()
        self.apo = Apo()

    def calculate(self, series, period_fast, period_slow, period_macd, k):
        ema_fast, ema_slow, apo = self.apo.calculate(series, period_fast, period_slow, k)

        macd_signal = self.ema.calculate(apo, period_macd, k)
        macd_signal.name = 'MACDSignal'

        macd_histogram = apo - macd_signal
        macd_histogram.name = 'MACDHistogram'

        return ema_fast, ema_slow, apo, macd_signal, macd_histogram