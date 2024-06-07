import pandas as pd
import pandas_ta as ta

#이격도
def disparity(df, ndays = 10):
    df["MA"]=df["c"].rolling(ndays).mean()
    df['disparity'] = 100*(df["c"]/df["MA"])
    return df['disparity']

