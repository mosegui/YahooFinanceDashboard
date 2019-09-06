# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import datetime as dt

from YahooFinanceDashboard import data_io as io
from YahooFinanceDashboard import plots
from YahooFinanceDashboard import tickers_browser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


yahoo_ticker = 'AAPL'


# data = io.input_data(yahoo_ticker, start=dt.datetime(2016, 2, 16), end=dt.datetime.today())
#
# price_axes, volume_axes = plots.plot_prices(data, plot_type='candlestick')

# similar = tickers_browser.search_tickers(ticker=yahoo_ticker)
#
# similar2 = tickers_browser.search_tickers(ticker=yahoo_ticker, type='Equity')
#
similar3 = tickers_browser.search_tickers(ticker=yahoo_ticker, exchange='NASDAQ')

# similar4 = tickers_browser.search_tickers(ticker='AAPL')
