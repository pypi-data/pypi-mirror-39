"""
Basic input and output function for dataset
author: John J. H. Lin  <john.jrhunglin@gmail.com>
"""

import os
import csv
import sys
import pandas as pd
from os.path import dirname, exists, expanduser, isdir, join, splitext
import copy
import matplotlib.pyplot as plt

def parallel_plot(x, y, pic_size):
    """
    Create parallel_plot of dataset with many features(high dimension),
    This is very useful in visualizing high dimension data
    """
    x_ = copy.copy(x)
    y_ = copy.copy(y)
    if isinstance(x_, pd.DataFrame):
        df_x_test = x_.reset_index(drop = True)
    else:
        raise ValueError("x is not DataFrame!")

    if isinstance(y_, pd.Series):
        y_ = y_.to_frame(name = 'p_pred')
    if not isinstance(y_, pd.DataFrame):
        df_y = pd.DataFrame(y_, columns = ['y_pred'])
    else:
        df_y = y_
    df_all = pd.concat([df_y, df_x_test], sort = False, axis = 1)
    c_name = df_y.columns[0]
    plt.figure(figsize=pic_size)
    pd.plotting.parallel_coordinates(df_all, c_name, axvlines = False, colormap = 'coolwarm')
    plt.show()
    return True

def scatter_plot(x, y, x_label, y_label, title, pic_size, groupby=True):
    """
    scatter plot
    :param x:
    :param y:
    :param x_label:
    :param y_label:
    :param title:
    :param pic_size:
    :param groupby:
    :return:
    """
    fig, ax = plt.subplots(figsize=pic_size)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if groupby:
        plt.scatter(x, y, c=y, cmap=plt.cm.viridis, alpha=.75)
    else:
        plt.scatter(x, y,  marker='o')
        #ax.plot(group.x, group.y, marker = 'o', ms = 3.5,
           #linestyle='',label = name)
    return True

def trend_plot(dset, x_label, y_label, title, pic_size=(8, 6)):
    """
    Trend plot
    :param dset:
    :param x_label:
    :param y_label:
    :param title:
    :param pic_size:
    :return:
    """
    fig, ax = plt.subplots(figsize=pic_size)
    ax.plot(dset, color = 'g', alpha = 0.6)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return True
