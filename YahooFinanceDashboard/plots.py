# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""
import logging

import numpy as np
import matplotlib.style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as fnc
from pandas.plotting import register_matplotlib_converters

from YahooFinanceDashboard._plots import _plots_axes


logger = logging.getLogger(__name__)


matplotlib.style.use('ggplot')
register_matplotlib_converters()

def plot_prices(input_data, plot_type='candlestick'):  # TODO: imrpove plot presentation (title, metadata, etc...)
    """Plots the stocks prices day-wise and the traded volume from the inbound data

    Parameters
    ----------
    input_data : pd.DataFrame
        stock price historical data with open, high, low and adj_close values
    plot_type : str {'candlestick', 'ohlc', 'close'}

    Returns
    -------
    price_axes : matplotlib.pyplot.axes object
        the axes in which the historical prices are plotted
    volume_axes : matplotlib.pyplot.axes object
        the axes in which the historical traded volumes are plotted
    """
    plot_data = input_data.copy()
    plot_data.reset_index(inplace=True)
    plot_data['Date'] = plot_data['Date'].map(mdates.date2num)

    sequence = ['Date', 'Open', 'High', 'Low', 'Adj_Close']

    price_axes, volume_axes = _plots_axes.get_pricevolume_axes()

    if plot_type.lower() == 'candlestick':
        fnc.candlestick_ohlc(price_axes, np.array(plot_data[sequence]), width=0.75, colorup='darkgreen')
    elif plot_type.lower() == 'ohlc':
        fnc.plot_day_summary_ohlc(price_axes, np.array(plot_data[sequence]), colorup='darkgreen')
    elif plot_type.lower() == 'close':
        price_axes.plot(plot_data.Date, plot_data.Adj_Close, color='k', linewidth=1)
    else:
        logger.error('invalid plot_type')
        raise ValueError('invalid plot_type')

    volume_axes.bar(plot_data.Date, plot_data.Volume, color='royalblue')

    plt.show()

    return price_axes, volume_axes
