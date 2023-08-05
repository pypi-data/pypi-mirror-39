"""
Basic input and output function for dataset
author: John J. H. Lin  <john.jrhunglin@gmail.com>
"""

import os
import csv
import sys
import pandas as pd
from os.path import dirname, exists, expanduser, isdir, join, splitext
from os import listdir
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def describe_dataset(all_file = None):
    """
    out description of datasets
    :param all_file:
    :return: dataframe for description
    """
    df_columns = ['Data', '#Samples', '# Dimensions', 'Outlier Perc']
    tmp = np.empty((0, 4))
    describ_df = pd.DataFrame(columns  = df_columns)
    for key in all_file:
        x = pd.read_csv(all_file[key], header = 0, delimiter = ',')
        y =x.iloc[:, 0]
        outliers_fraction = np.count_nonzero(y) / len(y)
        outliers_percentage = round(outliers_fraction * 100, ndigits=2)
        tmp_row = np.array([key, x.shape[0], x.shape[1]-1, outliers_percentage])
        tmp_row = np.reshape(tmp_row, (1,4))
        tmp = np.append(tmp, tmp_row, axis = 0)
        o_pct = 0
    df_describe = pd.DataFrame(tmp, columns = df_columns)
    return df_describe


def load_classification_dataset(n_class=2):
    """
    Load all datasets with required number of class,
    :param n_class: number of class (default=2)
    :return: dictionary of required datasets with key (filename without extension) and values (file's relative path)
    """
    y_loc = 0
    parent_d = join(dirname(__file__), 'data')
    folders = [f for f in sorted(listdir(parent_d))
               if isdir(join(parent_d, f))]
    #folders.remove('.ipynb_checkpoints')
    # all_file =[]
    all_file = dict()

    for sub_f in folders:
        sub_f = join(parent_d, sub_f)
        files = sorted(listdir(sub_f))
        for file in files:
            file_path = join(sub_f, file)
            file_id, file_ext = splitext(file)
            # all_file.append(file_path)
            all_file[file_id] = file_path
    ##只保留2類的

    for file_id in all_file.copy():
        y = pd.read_csv(all_file[file_id], header=0, delimiter=',').iloc[:, y_loc]
        n_cls = len(pd.unique(y))
        if n_cls != n_class:
            del all_file[file_id]
    return all_file


def load_phm(return_x_y = False):
    """Load and return the phm dataset (regression).
    ==============     ==============
    Samples total                 200
    Dimensionality               1918
    Features                     real
    Targets     class 0(good), 1(bad)
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename',
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'phm.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/phm', 'phm_RIGHT_RPhase_FB.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'phm_RIGHT_RPhase_FB.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_dna(return_x_y = False):
    """Load and return the dna dataset (classification).
    ==============     ==============
    Samples total                 2586
    Dimensionality               180
    Features                     binary(0,1)
    Targets                  class 0, 1, 2
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename',
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'dna.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/dna', 'dna_0_179.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_usps(return_x_y = False):
    """Load and return the dna dataset (classification).
    ==============     ==============
    Samples total                 9298
    Dimensionality               256
    Features                     real
    Targets             class 0-8
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename'
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/usps', 'usps.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_satimage(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 5104
    Dimensionality               36
    Features                     real
    Targets             class 0-5
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_X_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/satimage', 'satimage.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_letter(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 20000
    Dimensionality               16
    Features                     real
    Targets             class 0-25
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/letter', 'letter.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_letter_2_class(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 1600
    Dimensionality               32
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/letter', 'letter_2_class.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_arrhythmia(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 452
    Dimensionality               274
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/arrhythmia', 'arrhythmia.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_cardio(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 1831
    Dimensionality               21
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/cardio', 'cardio.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_mnist(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 7603
    Dimensionality               100
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/mnist', 'mnist.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_musk(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 3062
    Dimensionality               166
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/musk', 'musk.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_optdigits(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 5216
    Dimensionality               64
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/optdigits', 'optdigits.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_pendigits(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 6870
    Dimensionality               16
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/pendigits', 'pendigits.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_pima(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 768
    Dimensionality               8
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/pima', 'pima.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_satellite(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 6435
    Dimensionality               36
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/satellite', 'satellite.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_shuttle(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 49097
    Dimensionality               9
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/shuttle', 'shuttle.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_speech(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 3686
    Dimensionality               400
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/speech', 'speech.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_vowels(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 1456
    Dimensionality               12
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/vowels', 'vowels.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_phm_outlier_10pct(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 111
    Dimensionality               1918
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/phm', 'phm_outlier_10pct.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data


def load_phm_outlier_20pct(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 125
    Dimensionality               1918
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/phm', 'phm_outlier_20pct.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_phm_outlier_30pct(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 143
    Dimensionality               1918
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/phm', 'phm_outlier_30pct.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data

def load_phm_outlier_40pct(return_x_y = False):
    """Load and return the satimage dataset (classification).
    ==============     ==============
    Samples total                 167
    Dimensionality               1918
    Features                     real
    Targets             class 0-1
    ==============     ==============

    Parameters
    ----------
    return_x_y : boolean, default=False.
        If True, returns ``(data, target)`` instead of a Bunch object.
        See below for more information about the `data` and `target` object.
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the regression targets,
        'DESCR', the full description of the dataset,
        and 'filename', the physical location of boston
    (data, target) : tuple if ``return_x_y`` is True
    Notes
    -----
     Examples
    --------
    """
    module_path = dirname(__file__)

    fdescr_name = join(module_path, 'descr', 'usps.rst')
    with open(fdescr_name, encoding='utf8') as f:
        descr_text = f.read()

    data_file_name = join(module_path, 'data/phm', 'phm_outlier_40pct.csv')
    dataset = pd.read_csv(data_file_name, header=0, delimiter=',')
    dataset_value = dataset.values
    all_feature_name = dataset.columns.values
    feature_name = all_feature_name[1:-1]
    n_sample = int(dataset_value.shape[0])
    x = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    n_feature = int(x.shape[1])

    if return_x_y:
        return x, y
    else:
        img_file_name = join(module_path, 'visualize_data', 'not_available.png')
        plt.figure(figsize=(12, 9))
        img = mpimg.imread(img_file_name)
        imgplot = plt.imshow(img)
        output_data = {'x': x, 'y': y, 'n_feature': n_feature, 'n_sample': n_sample, 'feature_name': feature_name, 'description': descr_text}
        return output_data
