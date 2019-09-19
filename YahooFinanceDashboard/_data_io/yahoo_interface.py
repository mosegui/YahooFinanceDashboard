# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import datetime as dt

import pandas as pd
import urllib.request as urllib
import bs4

from YahooFinanceDashboard._data_io import _helpers as helpers_io


logger = logging.getLogger(__name__)


class YahooInterface:
    def __init__(self, yahoo_ticker):
        self.yahoo_ticker = yahoo_ticker

    def _get_all_historical_data(self, yahoo_ticker):
        """Scrapes the Yahoo Finance website for a given Yahoo Ticker and returns all the
        available data entries in a list of dictionaries

        Parameters
        ----------
        yahoo_ticker : str
            Yahoo ticker to be embedded in the URL to scrap

        Returns
        -------
        data : list of dicts
            option data retrieved from the Yahoo Finance site
        """
        import yahoofinancials

        yahoo_cursor = yahoofinancials.YahooFinancials(yahoo_ticker)

        # download one day just to have access to the metadata
        today = dt.datetime.today().strftime("%Y-%m-%d")
        yesterday = (dt.datetime.today() - dt.timedelta(1)).strftime("%Y-%m-%d")
        tomorrow = (dt.datetime.today() + dt.timedelta(1)).strftime("%Y-%m-%d")

        one_day_data = yahoo_cursor.get_historical_price_data(yesterday, today, 'daily')
        first_trade_date = one_day_data[yahoo_ticker]['firstTradeDate']['formatted_date']

        # now we can download since the beginning
        data = yahoo_cursor.get_historical_price_data(first_trade_date, tomorrow, 'daily')

        return data[yahoo_ticker]

    def historical_prices_yahoofinancials(self):
        """Wraps a list of dicts in a pandas DataFrame

        Returns
        -------
        data : pd.DataFrame
            stock data retrieved from the Yahoo Finance site
        """
        hist_data = self._get_all_historical_data(self.yahoo_ticker)
        data = pd.DataFrame(hist_data['prices'])
        data.index = data.formatted_date.apply(pd.to_datetime)
        data.index.name = "Date"
        data = data.drop(['date', 'formatted_date'], axis=1)
        data = data[['open', 'high', 'low', 'close', 'adjclose', 'volume']]
        data.columns = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']

        return data


    # def yahoo_prices_scraper(self):
    #     """Wraps a list of dicts in a pandas DataFrame
    #
    #     Returns
    #     -------
    #     data : pd.DataFrame
    #         stock data retrieved from the Yahoo Finance site
    #
    #     Notes
    #     -----
    #     - Deprecated as long as the 3rd-party package 'yahoofinancials' works.
    #     """
    #     def _yahoo_web_scraper(yahoo_ticker):
    #         """Scrapes the Yahoo Finance website for a given Yahoo Ticker and returns all the
    #         available data entries in a list of dictionaries
    #
    #         Parameters
    #         ----------
    #         yahoo_ticker : str
    #             Yahoo ticker to be embedded in the URL to scrap
    #
    #         Returns
    #         -------
    #         data : list of dicts
    #             stock data retrieved from the Yahoo Finance site
    #         """
    #         data = []
    #         url = "https://finance.yahoo.com/quote/" + yahoo_ticker + "/history/"
    #
    #         rows = bs4.BeautifulSoup(urllib.urlopen(url).read(), features="lxml").findAll('table')[0].tbody.findAll('tr')
    #
    #         for each_row in rows:
    #             divs = each_row.findAll('td')
    #             if divs[1].span.text != 'Dividend':  # Ignore this row in the table
    #                 data.append({'Date': divs[0].span.text,
    #                              'Open': float(divs[1].span.text.replace(',', '')),
    #                              'High': float(divs[2].span.text.replace(',', '')),
    #                              'Low': float(divs[3].span.text.replace(',', '')),
    #                              'Close': float(divs[4].span.text.replace(',', '')),
    #                              'Adj_Close': float(divs[5].span.text.replace(',', '')),
    #                              'Volume': float(divs[6].span.text.replace(',', '')), })
    #         return data
    #
    #     data = pd.DataFrame(_yahoo_web_scraper(self.yahoo_ticker))
    #     data.index = data.Date.apply(helpers_io.string_to_dt)
    #     data = data[data.columns.drop('Date')]
    #     data = data[['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']]
    #
    #     return data
