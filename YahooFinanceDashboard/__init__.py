# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""
__version__ = '1.1'  # the current jenkins build id will be appended upon building the package. Format is <major>.<minor>.<build_id>

# A RANDOM CHANGE: DELETE

name = "YahooFinanceDashboard"

import logging

from YahooFinanceDashboard import data_io as io
from YahooFinanceDashboard import plots
from YahooFinanceDashboard._data_io.database_manager import TickersBrowser


logger = logging.getLogger(__name__)


class Historical:
    def __init__(self, yahoo_ticker, start=None, end=None, year=None, month=None):
        self.yahoo_ticker =yahoo_ticker
        self. start = start
        self.end = end
        self.year = year
        self. month = month

        self.data = io.input_data(self.yahoo_ticker, self. start,  self.end, self.year, self.month)

    def __repr__(self):
        return repr(self.data)

    def plot(self, plot_type='candlestick'):
        self.price_axes, self.volume_axes = plots.plot_prices(self.data, plot_type=plot_type)


def search_tickers(**kwargs):
    """Wrapper around the function in database_manager.TickersBrowser for the
    user now having to acess private functions in private modules
    """
    return TickersBrowser._search_tickers(**kwargs)  # TODO: create a signature by hand to enforce *args and **kwargs
