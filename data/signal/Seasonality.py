import pandas as pd

class Seasonality:

    def calculate(self, series):
        monthly_return = series.pct_change()\
            .groupby([series.index.year, series.index.month])\
            .mean()

        montly_return_list = []
        for i in range(len(monthly_return)):
            montly_return_list.append\
                ({'month' : monthly_return.index[i][1],
                  'monthly_return': monthly_return.values[i]})

        montly_return_list = pd.DataFrame(montly_return_list, columns=('month','monthly_return'))
        return montly_return_list


