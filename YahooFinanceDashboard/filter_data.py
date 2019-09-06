# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import datetime as dt
import calendar
import logging


logger = logging.getLogger(__name__)


def by_datetime_span(data_df, dt_start=None, dt_end=None):
    """Slices a copy the inbound dataframe to the passed start and/or dates and returns it.
    
    Parameters
    ----------
    data_df : pd.DataFrame object
        single-indexed pandas DataFrame object with timestamp objects in index
    dt_start : dt.datetime object
        first date available in the returned DataFrame
    dt_end : dt.datetime object
        last date available in the returned DataFrame
        
    Returns
    -------
    df : d.DataFrame object
        sliced DataFrame object
        
    Raises
    ------
    TypeError : if 'dt_start' or 'dt_end' are not dt.datetime objects
    """
    df = data_df.copy()
    
    if isinstance(dt_start, dt.datetime):
        df = df[df.index >= dt_start]
    elif dt_start is None:
        pass
    else:
        raise TypeError("'start' must be a datetime.datetime object ")
        
    if isinstance(dt_end, dt.datetime):
        df = df[df.index <= dt_end]
    elif dt_start is None:
        pass
    else:
        raise TypeError("'start' must be a datetime.datetime object ")
        
    return df


def by_yearmonth(data, year=None, month=None):
    """High-level function to select a month or a year period from a dictionary containing
    single-indexed Datafaframes with timestamp indices. Wrapper around'by_datetime_span()'

    Parameters
    ----------
    data : 'pandas.DataFrame' object
        multi-indexed dataframe
    year : int
        year of data to be parsed.
    month : int
        month of data to be parsed.

    Returns
    -------
    dataframe : 'pandas.core.frame.DataFrame' object
        sliced multi-indexed dataframe

    Raises
    ------
    NotImplementedError: If the user wants to select a month throughout several years
    """
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                   'September', 'October', 'November', 'December']

    slice_df = data.copy()

    if year is None and month is not None:
        logger.warning("Using {month_names[month-1]} data for all available years")
        raise NotImplementedError('Data slicing method not yet implemented')
    elif year is None and month is None:
        logger.info(f'Using all-time data')
        pass
    elif year is not None and month is None:
        logger.info(f'Using data for the year {year}')
        slice_df = by_datetime_span(data, dt.datetime(year, 1, 1),
                                          dt.datetime(year, 12, 31, 23, 59, 59))

    elif year is not None and month is not None:
        logger.info(f'Using {month_names[month-1]} {year} data')
        slice_df = by_datetime_span(data, dt.datetime(year, month, 1),
                                          dt.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59))

    return slice_df
