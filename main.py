#!/usr/bin/env python
from urllib.request import urlopen

import certifi
import json
import os

from dotenv import load_dotenv
from poligon_api import get_tickers, get_weekly_bars, get_daily_bars
import technical_analysis

def main():
    load_dotenv()
    symbols = get_tickers()
    for symbol in symbols:
        try:
            print(symbol["ticker"] + "....")
            week_df = get_weekly_bars(symbol["ticker"])
            if technical_analysis.pattern4_check(week_df):
                day_df = get_daily_bars(symbol["ticker"])
                if technical_analysis.pattern4_1_check(week_df):
                    print(symbol["ticker"] + "  wow")
                    return
        except Exception as e:
            print("Error : ", e)

if __name__ == "__main__":
    # execute only if run as a script
    main()
