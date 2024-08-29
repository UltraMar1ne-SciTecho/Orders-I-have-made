#!/usr/bin/env python3

import re
import bs4
import requests
import argparse

import pandas as pd

from bs4 import BeautifulSoup


# Define a function to get parsed HTML from the CFTC
def get_parsed(url: str, headers: dict) -> bs4.BeautifulSoup:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Parse the HTML content and return a BeautifulSoup object
    return BeautifulSoup(response.content, 'lxml')


# Cleaning the data from the parsed HTML
def data_cleaning(soup: bs4.BeautifulSoup) -> list:
    # the data is contained in <pre>
    contents = soup.find('pre').contents
    # segment by that, then divided interest document could be gotten
    contents = [e.split('\r\n \r\n \r\n') for e in contents][2: -2][0]
    # clean reluctant symbols
    contents = [e.replace('\r\n', '').strip() for e in contents if e != '']
    return contents


# Extract data from the cleaned contents
def data_extraction(contents: list) -> pd.DataFrame:
    contract_pattern = re.compile(r"^(.*?)\s+-\s+NEW YORK MERCANTILE EXCHANGE", re.MULTILINE)
    interest_pattern = re.compile(r"OPEN INTEREST:\s+(\d{1,3}(?:,\d{3})*)")

    contracts = [contract_pattern.findall(e)[0] for e in contents]
    open_interests = [int(interest_pattern.findall(e)[0].replace(',', '')) for e in contents]

    # Here I use pandas.dataframe, it displays well and
    # if users want to download this csv, they can save csv with df.to_csv()
    result_dataframe = pd.DataFrame({
        'contract': contracts,
        'open_interest': open_interests
    })

    # call the function to display result
    data_display(result_dataframe, ascending=0)
    return result_dataframe


def data_display(result_dataframe: pd.DataFrame, ascending=0) -> None:
    print(','.join(result_dataframe.columns))
    displayed_dataframe = result_dataframe.copy()

    # "-1" means descending
    if ascending == -1:
        displayed_dataframe = result_dataframe.sort_values(by='open_interest', ascending=False)
    # "1" means ascending
    elif ascending == 1:
        displayed_dataframe = result_dataframe.sort_values(by='open_interest', ascending=True)

    # set default as 0, which means display by contract name
    for index, row in displayed_dataframe.iterrows():
        print('{},{}'.format(row['contract'], row['open_interest']))


def get_open_interest():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36'
    }
    url = "https://www.cftc.gov/dea/futures/deanymesf.htm"

    soup = get_parsed(url=url, headers=headers)
    contents = data_cleaning(soup=soup)

    result_dataframe = data_extraction(contents)

    # here's the result dataframe, if users wanna download that csv data
    # they can get the data via:
    # result_dataframe.to_csv('result.csv')


if __name__ == '__main__':
    get_open_interest()
