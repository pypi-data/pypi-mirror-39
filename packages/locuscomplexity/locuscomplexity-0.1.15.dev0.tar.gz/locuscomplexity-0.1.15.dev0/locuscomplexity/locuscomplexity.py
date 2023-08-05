"""
Implementation of the Economic Complexity algorithm introduced by Hidalgo and Hausmann


References
----------
See Hidalgo, "The Product Space Conditions the Development of Nations."
    https://arxiv.org/pdf/0708.2090.pdf

See Economic complexity glossary,
    http://atlas.cid.harvard.edu/learn/glossary

See algorithm applied to Locus framework,
    https://drive.google.com/open?id=1jotoaZgVFKd8Il-qzDMP3EBu9NQuRWgR

"""

import pandas as pd
import numpy as np
import os

dirname, filename = os.path.split(os.path.abspath(__file__))


def validate_input(df_data, year):
    """
    Make sure the input data has a column 'AREA', a column 'YEAR' (that contains at least one
    occurence of year and other columns that contains functions

    :param df_data: (Dataframe) input data to validate
    :param year: (int) year of interest, we want to make sure it appears in the dataset
    :return: throw error if not valid, nothing otherwise
    """
    cols = df_data.columns.values
    assert 'AREA' in cols, "Make sure the input data has a column 'AREA' " \
                           "that contains the code or name of each communities"
    assert 'YEAR' in cols, "Make sure the input data has a column 'YEAR' " \
                           "that contains the year of the recorded data in each row"
    YEAR = df_data['YEAR'].astype(int).values
    assert year in YEAR, "Make sure the input data contains data on the year you are interested in. " \
                         "{} doesn't appear in the dataset".format(year)


def build_m(df_data, year, binary=True):
    """
    Build matrix binary M by computing the RCA of every community

    :param df_data: (Dataframe) each row is a community (AREA) in a YEAR, other columns are functions.
    :param year: (int) year of interest
    :param binary : (bool) True to get M matrix, False to get RCA matrix
    :return: (Dataframe) Matrix M
    """
    validate_input(df_data, year)
    df_data['YEAR'] = df_data['YEAR'].astype(int)
    df_nat = df_data[df_data['YEAR'] == year]
    df_cp = df_nat.groupby(by=['AREA', 'YEAR']).sum()

    # Compute num and denom for RCA
    df_nat = df_cp.sum(axis=1)
    df_num = df_cp.astype(float).div(df_nat, axis=0).astype(float)

    df_prod = df_cp.sum(axis=0)
    df_tot = df_prod.sum()
    df_denum = df_prod / df_tot

    # Compute RCA
    df = df_num.div(df_denum).reset_index().drop('YEAR', 1).set_index('AREA')

    # Make matrix binary or keep raw RCA values
    if binary:
        df = df.apply(lambda x: x > 1).astype(int)
    return df


def diversity(m):
    """
    Compute Diversity vector for all communities in the dataset

    :param m: (Dataframe) M RCA, binary matrix
    :return: (Series) d = Diversity vector
    """
    # Taking the sum of each row of the binary M matrix
    return m.sum(axis=1)


def ubiquity(m):
    """
    Compute Ubiquity vector for all functions in the dataset

    :param m: (Dataframe) M RCA, binary matrix
    :return: (Series) Ubiquity vector
    """
    # Taking the sum of each column of the binary M matrix
    return m.sum(axis=0)


def m_dn_un(m):
    """
    From M matrix build both M tilde matrices, first is for Community Complexity Index
    second is for Function Complexity Index

    :param m: (Dataframe) M binary RCA matrix
    :return: (Df, Df) M_tilde for community, M_tilde for functions
    """
    m_dn = m.div(diversity(m), axis='index').replace(np.nan, 0)
    mT_un = (m.T).div(ubiquity(m), axis='index').replace(np.nan, 0)
    m_tilde_community = pd.DataFrame(np.dot(m_dn, mT_un),
                                     index=m_dn.index, columns=m_dn.index)
    m_tilde_function = pd.DataFrame(np.dot(mT_un, m_dn),
                                    index=m_dn.columns, columns=m_dn.columns)

    return m_tilde_community, m_tilde_function


def complexity_indices(df_data, year):
    """
    Computes Community Complexity Indices and Functional Complexity Indices

    :param df_data: (Dataframe) each row is a community (AREA) in a YEAR, other columns are functions.
    :param year: (int) Year of interest
    :return: (Dataframe) Community complexity vector,
             (Dataframe) Functional complexity vector
    """
    m = build_m(df_data, year)
    Mc, Mp = m_dn_un(m)

    # Computes second largest eigenvector of M_tilde for communities
    val, vect = np.linalg.eig(Mc)
    K = vect[:, 1].real
    cci = (K - np.mean(K)) / np.std(K)
    d = diversity(m)
    corr = np.corrcoef(np.squeeze(d.values), np.squeeze(cci))
    if (corr[0, 1] < 0):
        cci = -cci

    # Computes second largest eigenvector of M_tilde for functions
    val, vect = np.linalg.eig(Mp)
    K = vect[:, 1].real
    fci = -(np.mean(K) - K) / np.std(K)
    u = ubiquity(m)
    corr = np.corrcoef(np.squeeze(u.values), np.squeeze(fci))
    if (corr[0, 1] > 0):
        fci = -fci

    return pd.DataFrame(cci, index=Mc.index, columns=['cci']).reset_index(), \
           pd.DataFrame(fci, index=Mp.index, columns=['q']).reset_index()




def iter_fitness(n, m):
    """
    From Tacchella et al., 2012, compute fitness of a community with n iterations

    :param n: (int) number of iteration
    :param m: (Dataframe) Matrix m
    :return: (Series) Fitness vector where [i] is the fitness of community i
    """
    if n == 0:
        return pd.DataFrame(np.ones((len(m.index), 1)), index=m.index, columns=['f'])
    else:
        q = iter_complexity(n - 1, m)
        f = np.dot(m, q)
        return pd.DataFrame(f / np.mean(f), index=m.index, columns=['f'])


def iter_complexity(n, m):
    """
    From Tacchella et al., 2012, compute complexity of a community with n iterations

    :param n: (int) number of iteration
    :param m: (Dataframe) Matrix m
    :return: (Series) Complexity vector where [i] is the fitness of function i
    """
    if n == 0:
        return pd.DataFrame(np.ones((len(m.columns), 1)), index=m.columns, columns=['q'])
    else:
        q = np.dot(m.T, 1 / iter_fitness(n - 1, m))
        q = 1 / q
        return pd.DataFrame(q / np.mean(q), index=m.columns, columns=['q'])


def fitness(m):
    """
    Runs the iteration to compute communities fitness scores

    :param m: (Dataframe) M binary RCA matrix
    :return: (Dataframe) Fitness vector with AREA and 'f' as columns
    """
    areas = pd.DataFrame(list(m.index.values), columns=['AREA'])
    # Remove column and rows with all zeros
    m = m.loc[~(m == 0).all(axis=1)]
    m = m.loc[:, (m != 0).any(axis=0)]
    f = iter_fitness(50, m)
    fit = f.merge(areas, left_index=True, right_on='AREA', how='outer').replace(np.nan, 0)
    return fit


def complexity(m):
    """
    Runs the iteration to compute function complexity scores

    :param m: (Dataframe) M binary RCA matrix
    :return: (Dataframe) Fitness vector with <function_name> and 'q' as columns
    """
    # Remove column and rows with all zeros
    m = m.loc[~(m == 0).all(axis=1)]
    m = m.loc[:, (m != 0).any(axis=0)]
    comp = iter_complexity(50, m)
    return comp.reset_index()

