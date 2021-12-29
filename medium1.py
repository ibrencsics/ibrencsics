# https://towardsdatascience.com/in-12-minutes-stocks-analysis-with-pandas-and-scikit-learn-a8d8a7b50ee7

import pandas as pd
import datetime
import pandas_datareader.data as web
import math
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from pandas import Series, DataFrame

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl

def load_aapl():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2017, 1, 11)
    df = web.DataReader("AAPL", 'yahoo', start, end)
    close_px = df['Adj Close']
    return df, close_px

def load_aapl_for_prediction():
    start = datetime.datetime(2019, 1, 1)
    end = datetime.datetime(2021, 12, 10)
    df = web.DataReader("PG", 'yahoo', start, end)
    dfreg = df.loc[:, ['Adj Close', 'Volume']]
    dfreg['HL_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
    dfreg['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

    return dfreg

def show_moving_average():
    mavg = close_px.rolling(window=100).mean()

    mpl.rc('figure', figsize=(8, 7))
    style.use('ggplot')

    close_px.plot(label='AAPL')
    mavg.plot(label='mavg')
    plt.legend()
    plt.show()

def show_return():
    rets = close_px / close_px.shift(1) - 1

    mpl.rc('figure', figsize=(8, 7))
    style.use('ggplot')

    rets.plot(label='return')
    plt.legend()
    plt.show()

def load_stocks():
    start = datetime.datetime(2019, 1, 1)
    end = datetime.datetime(2021, 12, 7)
    df = web.DataReader(['AAPL', 'GOOG', 'MSFT', 'PG', 'BRK-B'], 'yahoo', start=start, end=end)['Adj Close']
    # print(df)
    return df

def show_correlation(df):
    retscomp = df.pct_change()
    corr = retscomp.corr()
    print(corr)

    mpl.rc('figure', figsize=(8, 7))
    style.use('ggplot')

    # correlation of two stocks
    # plt.scatter(retscomp.AAPL, retscomp.GOOG)
    # plt.xlabel('Returns AAPL')
    # plt.ylabel('Returns GOOG')

    # correlation of all stocks
    # pd.plotting.scatter_matrix(retscomp, diagonal='kde', figsize=(10, 10));

    # heat map
    plt.imshow(corr, cmap='hot', interpolation='none')
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns)
    plt.yticks(range(len(corr)), corr.columns)

    plt.legend()
    plt.show()

def show_risk_and_return(df):
    retscomp = df.pct_change()

    mpl.rc('figure', figsize=(8, 7))
    style.use('ggplot')

    plt.scatter(retscomp.mean(), retscomp.std())
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')
    for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
        plt.annotate(
            label,
            xy=(x, y), xytext=(20, -20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.legend()
    plt.show()


# df, close_px = load_aapl()
# show_moving_average()
# show_return()

# df = load_stocks()
# show_correlation(df)
# show_risk_and_return(df)

dfpred = load_aapl_for_prediction()
# print(dfpred)

# Drop missing value
dfpred.fillna(value=-99999, inplace=True)

# We want to separate 1 percent of the learn to forecast
forecast_out = int(math.ceil(0.01 * len(dfpred)))
print('learn length: {}, forecast legth: {}'.format(len(dfpred), forecast_out))

# Separating the label here, we want to predict the AdjClose
forecast_col = 'Adj Close'
dfpred['label'] = dfpred[forecast_col].shift(-forecast_out)
print(dfpred.head(10))
print(dfpred.tail(10))

X = np.array(dfpred.drop(['label'], 1))
print(X)

# Scale the X so that everyone can have the same distribution for linear regression
X = preprocessing.scale(X)
print(X)

# Finally We want to find Data Series of late X and early X (train) for model generation and evaluation
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
print('X size: {}, X_lately size: {}'.format(X.size, X_lately.size))

# Separate label and identify it as y
y = np.array(dfpred['label'])
y = y[:-forecast_out]

# Separation of training and testing of model by cross validation train test split
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)
print('X_train size: {}, X_test size: {}, y_train size: {}, y_test size {}'.format(X_train.size, X_test.size, y_train.size, y_test.size))

# Linear regression
clfreg = LinearRegression(n_jobs=-1)
clfreg.fit(X_train, y_train)

# Quadratic Regression 2
clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
clfpoly2.fit(X_train, y_train)

# Quadratic Regression 3
clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
clfpoly3.fit(X_train, y_train)

# KNN Regression
clfknn = KNeighborsRegressor(n_neighbors=2)
clfknn.fit(X_train, y_train)

confidencereg = clfreg.score(X_test, y_test)
confidencepoly2 = clfpoly2.score(X_test,y_test)
confidencepoly3 = clfpoly3.score(X_test,y_test)
confidenceknn = clfknn.score(X_test, y_test)

print("The linear regression confidence is ",confidencereg)
print("The quadratic regression 2 confidence is ",confidencepoly2)
print("The quadratic regression 3 confidence is ",confidencepoly3)
print("The knn regression confidence is ",confidenceknn)

# Printing the forecast
forecast_set = clfreg.predict(X_lately)
dfpred['Forecast'] = np.nan
print(forecast_set, confidencereg, forecast_out)
print(dfpred)


# plot
last_date = dfpred.iloc[-1].name
last_unix = last_date
next_unix = last_unix + datetime.timedelta(days=1)

for i in forecast_set:
    next_date = next_unix
    next_unix += datetime.timedelta(days=1)
    dfpred.loc[next_date] = [np.nan for _ in range(len(dfpred.columns)-1)]+[i]
print(dfpred.tail(10))

dfpred['Adj Close'].tail(500).plot()
dfpred['Forecast'].tail(500).plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
