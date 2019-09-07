# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

name = "YahooFinanceDashboard"

import logging

from YahooFinanceDashboard import data_io as io
from YahooFinanceDashboard import plots


logger = logging.getLogger(__name__)


class Historical:
    def __init__(self, yahoo_ticker, start=None, end=None, year=None, month=None):
        self.yahoo_ticker =yahoo_ticker
        self. start = start
        self.end = end
        self.year = year
        self. month = month

        self.data = io.input_data(self.yahoo_ticker, self. start,  self.end, self.year, self. month)

    def __repr__(self):
        return repr(self.data)

    def plot(self, plot_type='candlestick'):
        self.price_axes, self.volume_axes = plots.plot_prices(self.data, plot_type=plot_type)
