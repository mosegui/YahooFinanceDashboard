# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)


def get_pricevolume_axes():
    """Creates the figure with the axes designed for plotting the historical prices
    and volumnes, and retuns both axes to the user

    Returns
    -------
    ax1, ax2 : matplotlib.Axes object
    """
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    ax2.xaxis_date()
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.xticks(rotation=20)

    return ax1, ax2
