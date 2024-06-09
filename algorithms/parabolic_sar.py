import pandas as pd
import pandas_ta as ta

def parabolic_sar(pd_dataframe):
    df = pd_dataframe
    psar = df.ta.psar(high=df['h'], low=df['l'], close=df['c'], af0=0.02, af=0.02, max_af=0.2)
    print(psar["PSARr_0.02_0.2"])
    return psar