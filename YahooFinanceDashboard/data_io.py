# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import urllib.request as urllib

import YahooFinanceDashboard.filter_data as filter_data
import YahooFinanceDashboard._data_io.database_manager as database_manager


logger = logging.getLogger(__name__)


def input_data(yahoo_ticker, start=None, end=None, year=None, month=None):
    """Retrieves the stock data in a pandas DataFrame for a given stock, a given timespan,
    and from a chosen source.
    
    Parameters
    ----------
    yahoo_ticker : str
        name of the stock to be retrieved
    start : dt.datetime object
        first date available in the returned DataFrame
    end : dt.datetime object
        last date available in the returned DataFrame
    year : int
        year of data to be parsed.
    month : int
        month of data to be parsed.
        
    Returns
    -------
    data : pd.DataFrame object
    
    Raises
    ------
    ValueError : if the database is not available/the passed name is not recognized
    """
    db_manager = database_manager.DBManager(yahoo_ticker)

    try:
        db_manager.update_prices_db()
    except urllib.URLError:
        logger.warning('Request to YAHOO server unsuccessful. Check internet connection. Using available data')

    data = db_manager.retrieve_prices_db().astype(float)

    data = filter_data.by_datetime_span(data, dt_start=start, dt_end=end)

    if year is not None:
        data = filter_data.by_yearmonth(data, year=year, month=month)

    return data.sort_index()