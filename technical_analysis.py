# !pip install prophet
# pip install -U scikit-learn
#from prophet import Prophet
import matplotlib.pyplot as plt
import algorithms
import numpy as np
import technical_analysis

def pattern1_check(daily_df, weekly_df):
    daily_df['SMA1'] = daily_df['c'].rolling(window=42).mean()
    daily_df['SMA2'] = daily_df['c'].rolling(window=252).mean()
    daily_df['position'] = np.where(daily_df['SMA1'] > daily_df['SMA2'], 1, -1)

    cci252 = algorithms.get_current_cci(daily_df, 252)

    if daily_df['position'].iloc[-1] == 1 and cci252 < 50:
        slow_k, slow_d = algorithms.stc_slow(weekly_df, 9, 3, 3)
        if slow_d.iloc[-1] < 35 :
            daily_sma = algorithms.sma(daily_df, 20)
            if algorithms.macd_line_over_than_signal2(daily_df, 12, 26, 9) :
                return True
    return False

def pattern2_check(daily_df, weekly_df):
    res = algorithms.adx(weekly_df['h'], weekly_df['low_price'], weekly_df['c'], 14)
    cci14 = algorithms.get_current_cci(weekly_df, 14)
    if res['DMP_14'].iloc[-1] > res['DMN_14'].iloc[-1] and \
        res['ADX_14'].iloc[-1] < res['DMP_14'].iloc[-1] and \
        algorithms.macd_line_over_than_signal2(weekly_df, 12, 26, 9) and \
        cci14 < 20 :
        res_day = algorithms.adx(daily_df['h'], daily_df['low_price'], daily_df['c'], 14)
        if res_day['DMP_14'].iloc[-1] > res_day['DMN_14'].iloc[-1] and \
            res_day['ADX_14'].iloc[-1] < res_day['DMP_14'].iloc[-1] and \
            res_day['ADX_14'].iloc[-1] > res_day['ADX_14'].iloc[-5] :
            return True
    return False

def pattern3_check(weekly_df) :
    res = algorithms.adx(weekly_df['h'], weekly_df['low_price'], weekly_df['c'], 14)
    cci14 = algorithms.get_current_cci(weekly_df, 14)
    if res['DMP_14'].iloc[-1] > res['DMN_14'].iloc[-1] and \
        res['ADX_14'].iloc[-1] < res['DMP_14'].iloc[-1] and cci14 < 50 :
        return True
    return False

def pattern4_check(df) :
    ema14 = algorithms.ema(df,14)
    if algorithms.macd_line_over_than_signal2(df, 12, 26, 9) and ema14.iloc[-1] < df['c'].iloc[-1] :

        return True
    return False

def pattern4_1_check(df) :
    cci14 = algorithms.get_current_cci(df, 14)
    if cci14 < 80 : 
        slow_k, slow_d = algorithms.stc_slow(df, 14, 5, 5)
        if slow_k.iloc[-1] > slow_d.iloc[-1] and slow_k.iloc[-1] < 55: 
            return True
    return False

def pattern5_1_check(df) :
    res = algorithms.adx(df['h'], df['low_price'], df['c'], 14)
    if res['DMP_14'].iloc[-1] > res['DMN_14'].iloc[-1] and \
        res['ADX_14'].iloc[-1] < res['DMP_14'].iloc[-1] :
        if res['ADX_14'].iloc[-1] <= 30 :
            return True
    return False

def pattern5_check(df) :
    res = algorithms.adx(df['h'], df['low_price'], df['c'], 14)
    slow_k, slow_d = algorithms.stc_slow(df, 9, 3, 3)
    if slow_d.iloc[-1] < 40 :
        if res['DMP_14'].iloc[-1] > res['DMN_14'].iloc[-1] and res['ADX_14'].iloc[-1] < res['DMP_14'].iloc[-1] :
            return True
    return False

def pattern6_check(df) :
    df['SMA200'] = df['c'].rolling(window=200).mean()
    if df['SMA200'].iloc[-1] < df['c'].iloc[-1]:
        if algorithms.get_current_rsi(df, 20) <= 50 :
            return True
    return False
