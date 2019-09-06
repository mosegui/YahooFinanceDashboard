# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

from YahooFinanceDashboard._data_io.database_manager import TickersBrowser

def search_tickers(**kwargs):
    """Wrapper around the function in database_manager.TickersBrowser for the
    user now having to acess private functions in private modules
    """
    return TickersBrowser._search_tickers(**kwargs)