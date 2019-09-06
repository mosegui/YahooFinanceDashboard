# -*- coding: utf-8 -*-
"""
Written by Daniel Moseguí González

GitHub: user:mosegui
LinkedIn: https://www.linkedin.com/in/daniel-moseguí-gonzález-5aa02849/
"""

import logging
import datetime as dt


logger = logging.getLogger(__name__)


def rotate_list(l, n=1):
    """Takes a list and returns it with the last 'n' elements placed in the beginning
    
    Parameters
    ----------
    l : list
        list of elements
    n : int
        number of elements in the end of the list to be moved to the beginning
        
    Returns
    -------
    reordered_list : list
        reordered list
    """
    reordered_list = l[-n:] + l[:-n]
    
    return reordered_list


def get_translation_months():
    """Returns a dictionary with the translations from month acronym to the corresponding
    ordinal number

    Returns
    -------
    months : dict {key=str : value:int}
        correspondences between months acronym and ordinal location in year
    """
    months =  {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
               'Jul':7, 'Ago':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    return months


def string_to_dt(string):
    """Converts a string of the form 'Feb 01, 2013' to a dt.datetime object
    
    Parameters
    ----------
    string : str
        string with date
        
    Returns
    -------
    dt_object : dt.datetime
        dt.datetime object with the date on the string
    """
    translation_months = get_translation_months()
    
    date_time = rotate_list(string.split(' '))
    date_time[1] = translation_months[date_time[1]]
    date_time[2] = date_time[2][:-1]
    
    dt_object = dt.datetime(*[int(item) for item in date_time])
    
    return dt_object
