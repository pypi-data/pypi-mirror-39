# weighting_fxns.py
# MIT license 2018
# Francis C. Motta

"""
Functions which weight the birth-persistence plane. To ensure stability, functions should vanish continuously at the
line persistence = 0 (see [PI] for details).
"""

import numpy as np


def linear_ramp(birth, pers, low=0.0, high=1.0, start=0.0, end=1.0):
    """
    continuous peicewise linear ramp function which is constant below and above specified input values
    :param birth: birth coordinates
    :param pers: persistence coordinates
    :param low: minimal weight
    :param high: maximal weight
    :param start: start persistence value of linear transition from low to high weight
    :param end: end persistence value of linear transition from low to high weight
    :return: weight at persistence pair
    """
    n = birth.shape[0]
    w = np.zeros((n,))
    for i in range(n):
        if pers[i] < start:
            w[i] = low
        elif pers[i] > end:
            w[i] = high
        else:
            w[i] = (pers[i] - start) * (high - low) / (end - start) + low

    return w


def persistence(birth, pers, n=1.0):
    """
    :param birth: birth coordinates
    :param pers: persistence coordinates
    :return: weight at persistence pair
    """
    return pers ** n