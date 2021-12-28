import pandas as pd

class Mom:

    def calculate(self, series, time_period):
        history = []  # history of observed prices to use in momentum calculation
        mom_values = []  # track momentum values for visualization purposes

        for val in series:
            history.append(val)
            if len(history) > time_period:  # history is at most 'time_period' number of observations
                del (history[0])

            mom = val - history[0]
            mom_values.append(mom)

        return pd.Series(data=mom_values, index=series.index, name='mom' + str(time_period))