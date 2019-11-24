# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import os
import datetime as dt
import sys
from contextlib import contextmanager

import pandas as pd
import sqlite3

from YahooFinanceDashboard._data_io import YahooTickerDownloader
from YahooFinanceDashboard._data_io import difflib
from YahooFinanceDashboard._data_io import yahoo_interface


logger = logging.getLogger(__name__)


@contextmanager
def _connect_db(database_dir, yahoo_ticker):
    """Manages the connection (I/O) to the corresponding DB

    Parameters
    ----------
    database_dir : str
        path pointing to the location of the BD to connect to
    yahoo_ticker : str
        name of the DB to connect to
    """
    db = sqlite3.connect(os.path.join(database_dir, f"{yahoo_ticker}.sqlite"))
    yield db
    db.close()


def prev_weekday(adate):
    """
    """
    adate -= dt.timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= dt.timedelta(days=1)
    return adate


def get_db_location(db_name):
    """Searches the passed filename in the whole package tree and returns the
    absolute path or paths of the coincident filenames

    Parameters
    ----------
    filename : str
        basename of the file to be searched

    Returns
    -------
    filename_location : str
        absolute path of the found file

    Raises
    ------
    NotImplementedError : If more than one file matches the passed filename
    """
    db_filename = f"{db_name}.sqlite"

    matching_files = []

    for root, dirs, files in os.walk(os.path.abspath(os.path.dirname(__file__))):
        if '__pycache__' in root:
            continue

        if db_filename in files:
            matching_files.append(os.path.join(root, db_filename))
    if len(matching_files) > 1:
        raise NotImplementedError(f'More than one file in tree matches filename: {matching_files}')

    filename_location = matching_files[0]
    return os.path.dirname(filename_location)


class TickersBrowser:

    def __need_update(path):
        """Checks the last time the 'generic' tickers DB was updated. If it has been
        updated in the last 'updating_threshold', returns False. Otherwise True

        Parameters
        ----------
        path : str
            path pointing to the 'generic' DB

        Returns
        -------
        bool
        """
        last_update_filename = '__last_update.log'
        update_timestamp_string_format = '%Y%m%d'
        updating_threshold = 7  # number of days allowed since last DB update

        last_update_path = os.path.join(os.path.normpath(path), last_update_filename)

        if os.path.exists(last_update_path):
            with open(last_update_path, 'r') as f:
                last_db_update = dt.datetime.strptime(f.read(), update_timestamp_string_format)

            if abs((last_db_update - dt.datetime.now()).days) > updating_threshold:
                logger.info('Tickers DB is being updated....')
                new_update = dt.datetime.strftime(dt.datetime.now(), update_timestamp_string_format)
                with open(last_update_path, 'w') as f:
                    f.write(new_update)
                return True
            else:
                return False
        else:
            new_update = dt.datetime.strftime(dt.datetime.now(), update_timestamp_string_format)
            with open(last_update_path, 'w') as f:
                f.write(new_update)
            return True

    def __update_tickers_db(path):
        """Updates the local Yahoo Securities Tickers DB by using the library
        YahooTickerDownloader
        """
        if TickersBrowser.__need_update(path):
            try:
                wdir = os.getcwd()
                os.chdir(path)

                YahooTickerDownloader.main()

                os.chdir(wdir)
            except:
                logger.error('Error updating Yahoo tickers DB')

    def _search_tickers(**kwargs):
        """Browses the securities DB searching for entries matching or close to the passed criteria.
        Input can be approximate

        Parameters:
        ----------
        'name': str
            Security name (e.g.: Lindblad Expeditions, Santander, ...)
        'ticker': str
            Security Yahoo Ticker Identifier (e.g.: AAPL, SAN.MC)
        'exchange': str
            Name of the exchange in which the security is traded (e.g.: Munich, NYSE, NASDAQ)
        'type': str
            Type of security (e.g.: Equity, Index, Fund)
        'exchange_symbol': str
            Abbrebiation of the exchange name (e.g.: MUN, NYQ, NAS)
        'type_symbol': str
            abbreviation fo the type of security (e.g.: S, M, B, ...)
        'index': str
            numeric security index identifier (e.g.: 106782, 48875, ...)
        Notes:
        ------
        Input can be approximate
        """
        # check and set arguments
        security_arguments = {'name': 'Name',
                              'ticker': 'Ticker',
                              'exchange': 'exchangeDisplay',
                              'type': 'TypeDisplay',
                              'exchange_symbol': 'Exchange',
                              'type_symbol': 'Type',
                              'index': 'index'}

        search_arguments = {'cutoff': 0.5,
                            'number_results': 20}

        for argument in search_arguments.keys():
            if argument in kwargs.keys():
                search_arguments[argument] = kwargs[argument]

        # get paths and connect to db
        pd.set_option('display.expand_frame_repr', False)

        tickers_db = 'generic'

        tickers_path = get_db_location(tickers_db)

        TickersBrowser.__update_tickers_db(tickers_path)

        with _connect_db(tickers_path, tickers_db) as db:
            df = pd.read_sql('select * from YAHOO_TICKERS', db, index_col='Ticker')

        # search candidates and intersect
        comparison_dimensions = {}

        for argument in kwargs.keys():
            if argument not in list(security_arguments.keys()) + list(search_arguments.keys()):
                raise ValueError(f'unexpected argument {argument}')

        for argument in [item for item in kwargs.keys() if item not in search_arguments.keys()]:
            if argument is 'ticker':
                close_matches_idx = difflib.get_close_matches(kwargs[argument],
                                                          df.index,
                                                          n=search_arguments['number_results'],
                                                          cutoff=search_arguments['cutoff'])
            else:
                close_matches = difflib.get_close_matches(kwargs[argument],
                                                          df[security_arguments[argument]],
                                                          n=search_arguments['number_results'],
                                                          cutoff=search_arguments['cutoff'])

                close_matches_idx = [index for index in df.T if df[security_arguments[argument]].loc[index] in close_matches]

            comparison_dimensions[argument] = df.loc[close_matches_idx].reindex(close_matches_idx)

        compared_dimensions = list(comparison_dimensions.keys())

        if len(compared_dimensions) == 1:
            intersection = comparison_dimensions[compared_dimensions[0]]
        elif len(compared_dimensions) >= 2:

            intersection = \
                comparison_dimensions[compared_dimensions[0]].loc[comparison_dimensions[compared_dimensions[0]].index.intersection(comparison_dimensions[compared_dimensions[1]].index)]
            for key in compared_dimensions[2:]:
                intersection = intersection.loc[intersection.index.intersection(comparison_dimensions[key].index)]

        # TODO: Return results in order of 'closeness'

        return intersection


class DBManager:
    def __init__(self, yahoo_ticker):
        """Class responsible for acting as middleman between the sqlite
        databases and other functions in the software

        Parameters
        ----------
        yahoo_ticker : str
            index/option/etc. name (e.g. IBEX35) whose associated database must be
            interacted with
        """
        self.yahoo_ticker = yahoo_ticker

        try:
            self.database_dir = get_db_location(self.yahoo_ticker)
        except IndexError:
            logger.warning('DB not found in local filesystem. Downloading from Yahoo server...')
            self.database_dir = get_db_location('__dummy')
            try:
                self.create_new_prices_db()
            except:
                logger.warning('Ticker not found in Yahoo DB. Browsing Yahoo tickers list...')
                self.get_similar_tickers()

    def create_new_prices_db(self):
        """Downloads from Yahoo Server the historical prices of the passed ticker
        and stores them in a freshly created DB

        Returns
        -------
        all_prices : pandas.DataFrame object
            historical prices of the passed ticker
        """
        web_interface = yahoo_interface.YahooInterface(self.yahoo_ticker)

        # TODO: check here if ticker does not exist and log/raise error and return list of
        #  availbale tickers (via YahooTickerDowloader file)

        all_prices = web_interface.historical_prices_yahoofinancials()

        with _connect_db(self.database_dir, self.yahoo_ticker) as db:
            all_prices.to_sql('HIST_PRICES', db, if_exists='replace')
            db.commit()

        return all_prices

    def get_similar_tickers(self):
        """Searches in the securities DB tickers similar to the passed one
        """
        logger.info('searching for Yahoo tickers similar to the input query...')

        similar = TickersBrowser._search_tickers(ticker=self.yahoo_ticker, number_results=10)

        if similar.empty:
            logger.error('The passed ticker does not appear in the Yahoo database. No similar tickers could be found')
        else:
            logger.error('The passed ticker does not appear in the Yahoo database. Do you maybe mean one of the following?')
            logger.info(f"\n{similar}")

        sys.exit(1)

    def retrieve_prices_db(self):
        """Connects to the SQLITE IBEX35 database and returns the historical
        prices in a pandas DataFrame object

        Parameters
        ----------
        file : str
            absolute path of the database location to be queried

        Returns
        -------
        df : pd.DataFrame
            DataFrame object with retrieved data
        """

        with _connect_db(self.database_dir, self.yahoo_ticker) as db:
            df = pd.read_sql('select * from HIST_PRICES', db, parse_dates=['Date'], index_col='Date')

        df = df[['Open','High','Low','Close','Adj_Close','Volume']]

        return df

    def update_prices_db(self):
        """Connects to the SQLITE IBEX35 database and updates it with new data entries
        taken from the Yahoo Finance website

        Parameters
        ----------
        file : str
            absolute path of the database location to be queried
        """
        historical = self.retrieve_prices_db()

        # check for new entries
        web_interface = yahoo_interface.YahooInterface(self.yahoo_ticker)
        from_yahoo = web_interface.historical_prices_yahoofinancials()
        new_date_times = [item for item in from_yahoo.index if item not in historical.index]

        if prev_weekday(dt.date.today() + dt.timedelta(days=1)) == dt.date.today():
            if dt.datetime.now().hour < 18.:
                new_date_times = new_date_times[:-1]

        if new_date_times:
            historical = historical.append(from_yahoo.loc[new_date_times])
            historical = historical.sort_index()

            with _connect_db(self.database_dir, self.yahoo_ticker) as db:
                historical.to_sql('HIST_PRICES', db, if_exists='replace')
