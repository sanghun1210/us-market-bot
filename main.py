#!/usr/bin/env python
from urllib.request import urlopen

import certifi
import json
import os

from dotenv import load_dotenv
from poligon_api import get_tickers, get_weekly_bars, get_daily_bars
import technical_analysis
from mail import send_mail

def main():
    load_dotenv()
    symbols = get_tickers()
    result_list = []
    mail_count = 0
    for symbol in symbols:
        try:
            print(symbol["ticker"] + "....")
            week_df = get_weekly_bars(symbol["ticker"])
            if technical_analysis.pattern4_check(week_df):
                day_df = get_daily_bars(symbol["ticker"])
                if technical_analysis.pattern4_1_check(day_df) :
                    print(symbol["ticker"] + "  wow")
                    result_list.append(symbol["ticker"])
                    mail_count = mail_count + 1
                    if mail_count == 20:
                        msg = '\r\n'.join(result_list)
                        send_mail(msg, "check stock result")
                        print("send mail...")
                        result_list = []
                        mail_count = 0
        except Exception as e:
            print("Error : ", e)

    msg = '\r\n'.join()
    send_mail(msg, "check stock result")

if __name__ == "__main__":
    # execute only if run as a script
    main()
