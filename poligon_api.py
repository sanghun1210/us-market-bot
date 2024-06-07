#!/usr/bin/env python
from urllib.request import urlopen

import certifi
import json
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

# 특정 키가 존재하는지 확인하는 함수
def check_key_exists(json_dict, key):
    return key in json_dict

def get_period():
    current_date = datetime.now()
    result_date = current_date - timedelta(days=730)

    end_date = current_date.strftime('%Y-%m-%d')
    start_date = result_date.strftime('%Y-%m-%d')
    return start_date, end_date

def get_tickers():
    # 환경 변수에서 API 키 가져오기
    api_key = os.getenv('POLYGON_API_KEY')
    url = ("https://api.polygon.io/v3/reference/tickers?market=stocks&exchange=XNAS&active=true&limit=1000&apiKey={}".format(api_key))

    data_dict = get_jsonparsed_data(url)
    symbols = data_dict["results"]

    for i in range(10):
        if check_key_exists(data_dict, "next_url"):
            nexturl = data_dict["next_url"]+"&apiKey={}".format(api_key)
            data_dict = get_jsonparsed_data(nexturl)
            symbols.extend(data_dict["results"])
        else:
            break

    return symbols


def get_weekly_bars(ticker):
    start_date, end_date = get_period()
    api_key = os.getenv('POLYGON_API_KEY')
    url = ("https://api.polygon.io/v2/aggs/ticker/{}/range/1/week/{}/{}?adjusted=true&sort=asc&apiKey={}".format(ticker, start_date, end_date, api_key))
    data_dict = get_jsonparsed_data(url)
    #print(data_dict)

    # JSON 데이터에서 'results' 키의 값을 추출하여 DataFrame 생성
    data = data_dict['results']
    df = pd.DataFrame(data)

    # 타임스탬프를 날짜로 변환
    df['t'] = pd.to_datetime(df['t'], unit='ms')

    # 데이터프레임 확인
    #print(df.tail())
    return df

def get_daily_bars(ticker):
    start_date, end_date = get_period()
    api_key = os.getenv('POLYGON_API_KEY')
    url = ("https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?adjusted=true&sort=asc&apiKey={}".format(ticker, start_date, end_date, api_key))
    data_dict = get_jsonparsed_data(url)
    #print(data_dict)

    # JSON 데이터에서 'results' 키의 값을 추출하여 DataFrame 생성
    data = data_dict['results']
    df = pd.DataFrame(data)

    # 타임스탬프를 날짜로 변환
    df['t'] = pd.to_datetime(df['t'], unit='ms')

    # 데이터프레임 확인
    #print(df.tail())
    return df

def main():
    load_dotenv()
    #symbols = get_tickers()
    get_weekly_bars("AAPL")


if __name__ == "__main__":
    # execute only if run as a script
    main()
