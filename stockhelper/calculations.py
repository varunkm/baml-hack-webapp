import numpy as np
from itertools import combinations
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
from scipy.stats import norm
import random
import pandas as pd


def stock_calculator(sp_index, dataframe):
    # print("Reading sp_index file into pandas Dataframe")
    # df_spindex = pd.read_csv(sp_index)

    # print("Reading stockprice file into dataframe")
    # df = pd.read_csv(csvfile)
    df_spindex = sp_index
    df = dataframe
    df.insert(6, "closeNew", df_spindex["close"])
    df = df[["close", "closeNew"]]
    df.columns = ["close_stocks", "close_benchmark"]

    print("Raveling columns")
    close_stocks_values = df.close_stocks.values
    close_benchmark_values = df.close_benchmark.values

    close_stocks_values = close_stocks_values[::-1]
    close_benchmark_values = close_benchmark_values[::-1]

    # print(" Max Benchmark Values", max(close_benchmark_values))
    # print(" Min Benchmark Values", min(close_benchmark_values))

    # print(close_stocks_values[:100])

    # print("Calculating mean and variance of stock prices")
    # # Variance and mean calculations
    # # stock_var = np.var(close_stocks_values)
    # stock_mean = sum(list(close_stocks_values)) / len(close_stocks_values)
    # stock_var = sum([(i-stock_mean)**2 for i in close_stocks_values])/(len(close_stocks_values)-1)
    #
    # print("Calculating mean and variance of benchmark index")
    # # benchmark_var = np.var(close_benchmark_values)
    # benchmark_mean = sum(list(close_benchmark_values)) / len(close_benchmark_values)
    # benchmark_var = sum([(i-benchmark_mean)**2 for i in close_benchmark_values])/(len(close_benchmark_values)-1)


    close_stocks_change = []
    close_benchmark_change = []

    print("Calculating % change in stock prices")
    for i in range(1, len(close_stocks_values)):
        close_stocks_change.append(
            (close_stocks_values[i] - close_stocks_values[i - 1]) / close_stocks_values[i - 1])

    print("Calculating % change in benchmark values")
    for i in range(1, len(close_benchmark_values)):
        close_benchmark_change.append(
            (close_benchmark_values[i] - close_benchmark_values[i - 1]) / close_benchmark_values[i - 1])

    close_stocks_change = np.array(close_stocks_change)

    close_benchmark_change = np.array(close_benchmark_change)

    print("Calculating mean and variance of close stock prices")
    # Variance and mean calculations
    stock_var = np.var(close_stocks_change)
    stock_mean = sum(list(close_stocks_change)) / len(close_stocks_change)
    # stock_var = sum([(i - stock_mean) ** 2 for i in close_stocks_values]) / (len(close_stocks_values) - 1)

    print("Calculating mean and variance of close benchmark index")
    benchmark_var = np.var(close_benchmark_change)
    benchmark_mean = sum(list(close_benchmark_change)) / len(close_benchmark_change)
    # benchmark_var = sum([(i - benchmark_mean) ** 2 for i in close_benchmark_values]) / (len(close_benchmark_values) - 1)


    df_change = pd.DataFrame(close_stocks_change)
    # print(df_change.head())

    df_change.insert(1, "change_benchmark", close_benchmark_change)

    df_change.columns = ["%change_stocks", "%change_benchmark"]

    # print("Writing % changes to CSV")
    # df_change.to_csv(csvfile.split(".")[0]+ "_percent_change" + ".csv", index=False)

    # print("Calculation on {} complete".format(csvfile))
    return df_change, stock_var, stock_mean, benchmark_var, benchmark_mean








# Function returns Sharpes ratio, Alpha, Beta portfolio,  standard deviation

def get_risk_indicators(list_of_stock_files):
    beta_mean_variance_and_quantity_values = {}
    benchmark_mean = 0
    stocks_change_values = {}
    spindex_file = list_of_stock_files[-1][0]
    stocks = [i[1] for i in list_of_stock_files]


    for dataframe, ticker, quantity in list_of_stock_files[:-1]:
        df, stock_var, stock_mean, benchmark_var, benchmark_mean = stock_calculator(spindex_file, dataframe)

        print("Benchmark variance",benchmark_var)

        # df = pd.read_csv(file.split(".")[0] + "_percent_change.csv")

        stocks_values = df["%change_stocks"].values
        stocks_change_values[ticker] = stocks_values
        benchmark_values = df["%change_benchmark"].values
        cov = np.cov(stocks_values, benchmark_values)
        covariance = cov[0][1]

        print("Stock mean",stock_mean)
        print("Benchmark mean", benchmark_mean)

        # Beta calculation
        print("Beta calculation")
        beta = covariance/benchmark_var
        # print("BETA for {}".format(file), beta)
        beta_mean_variance_and_quantity_values[ticker] = (beta, stock_mean, stock_var, quantity)


    RISK_FREE_RATE = 0.0126/365
    # print(beta_mean_and_variance_values)


    total_capital = sum([i[1]*i[3] for i in beta_mean_variance_and_quantity_values.values()])

    beta_portfolio = sum([i[0]*((i[3]*i[1])/total_capital) for i in beta_mean_variance_and_quantity_values.values()])
    print(beta_portfolio)

    portfolio_mean = sum([i[1]*((i[3]*i[1])/total_capital) for i in beta_mean_variance_and_quantity_values.values()])

    # Alpha calculation
    alpha = portfolio_mean-RISK_FREE_RATE-(beta_portfolio*(benchmark_mean-RISK_FREE_RATE))
    print("ALPHA", alpha)

    weight_array = [(i[3]*i[1])/total_capital for i in beta_mean_variance_and_quantity_values.values()]

    dict_of_weights = {}

    for i in stocks:
        dict_of_weights[i] = weight_array[0]

    # Variance of portfolio

    combinations_of_two = list(combinations(stocks, 2))
    # print("STOCKS ARRAY", stocks_change_values)
    print(combinations_of_two)
    portfolio_of_variance = 0
    for i in combinations_of_two:
        size1 = stocks_change_values[i[0]].size
        size2 = stocks_change_values[i[1]].size
        size = min(size1, size2)

        cov = np.cov(stocks_change_values[i[0]][:size], stocks_change_values[i[1]][:size])
        covariance = cov[0][1]
        print("COVARIANCE:", cov)
        current_pV = dict_of_weights[i[0]]**2 * beta_mean_variance_and_quantity_values[i[0]][2] + dict_of_weights[i[1]]**2 * beta_mean_variance_and_quantity_values[i[1]][2] \
        + 2 * covariance * dict_of_weights[i[0]] * dict_of_weights[i[1]]
        portfolio_of_variance += current_pV

    print("standard deviation of portfolio", math.sqrt(portfolio_of_variance))


    # Sharpes ratio

    sharpes_ratio = (portfolio_mean - RISK_FREE_RATE)/math.sqrt(portfolio_of_variance)
    # sharpes_ratio += 0.5

    standard_deviation = math.sqrt(portfolio_of_variance)

    print(sharpes_ratio)
    return sharpes_ratio, alpha, beta_portfolio,  standard_deviation