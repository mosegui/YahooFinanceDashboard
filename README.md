# YahooFinanceDashboard

API for accessing, synchronizing, managing locally and plotting Yahoo financial data. 

## Description

This Dashboard uses Yahoo ticker symbols for identifying financial securities and fetches the available historical data from Yahoo servers. The downloaded data is returned in the form of a data object wrapping a Pandas DataFrame (Fields: Open, Close, High, Low, Adj_Close, Volume). The downloaded data is stored locally in a series of SQL databases for allowing offline work with known data. When working online with new data flowing in, the Dashboard constantly compares the inbound data with the local copy and keeps updating the SQL databases appending the new points.

The returned data object upon data request offers as well some simple tools/functionalities for requesting filtered data, as well as for rendering different types of financial plots (close, ohlc, candlestick).

The module offers as well a separate basic service for searching and filtering Yahoo ticker symbols by ticker symbol, security name, exchage, type of security, and more. The database of available Yahoo ticker symbols in which the search is carried out gets updated periodically with information of securities in most exchanges worldwide.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

This package works with Python 3 onwards as it uses f-strings

### Installing

```
pip install YahooFinanceDashboard
```

### Basic Usage

Requesting data: Interaction with the data happens mainly over the ```YahooFinanceDashboard.Historical()``` object.

```
>>> import datetime as dt
>>> import YahooFinanceDashboard as yfd
>>>
>>> yahoo_ticker = 'AAPL'
>>>
>>> data = yfd.Historical(yahoo_ticker, start=dt.datetime(2016, 2, 16), end=dt.datetime.today())
>>> print(data.head())
                 Open       High        Low      Close  Adj_Close      Volume
Date                                                                         
2016-02-16  95.019997  96.849998  94.610001  96.639999  91.070045  49057900.0
2016-02-17  96.669998  98.209999  96.150002  98.120003  92.464752  44863200.0
2016-02-18  98.839996  98.889999  96.089996  96.260002  90.711960  39021000.0
2016-02-19  96.000000  96.760002  95.800003  96.040001  90.504639  35374200.0
2016-02-22  96.309998  96.900002  95.919998  96.879997  91.296219  34280800.0
```

Plotting data:

```
>>> data.plot_prices()
>>> data.plot_prices(plot_type='ohlc')
>>> data.plot_prices(plot_type='close')
```

Searching for tickers:

```
>>> similar = tickers_browser.search_tickers(name='Citi group')
>>> print(similar.head())
        index               Name Exchange exchangeDisplay Type TypeDisplay
Ticker                                                                    
C          10     Citigroup Inc.      NYQ            NYSE    S      Equity
QNTQF    4527  QinetiQ Group plc      PNK     OTC Markets    S      Equity
C.BA    13853     Citigroup Inc.      BUE    Buenos Aires    S      Equity
C.MX    13906     Citigroup Inc.      MEX          Mexico    S      Equity
MZ4.F   38981    Mitie Group plc      FRA       Frankfurt    S      Equity

>>> similar = tickers_browser.search_tickers(name='Citi group', exchange='mexico')
>>> print(similar.head())
        index            Name Exchange exchangeDisplay Type TypeDisplay
Ticker                                                                 
C.MX    13906  Citigroup Inc.      MEX          Mexico    S      Equity
```

## Authors

* **Daniel Moseguí González** - *Initial work* - [mosegui](https://github.com/mosegui)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details