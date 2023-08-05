"""
Module that computes the fitness of communities and the complexity of functions

"""

from locuscomplexity.complexity import *


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


def outlook(m, df_complexity):
    """
    Compute the outlook (or opportunity value) of every community in the dataset using the M matrix and
    the Functional Complexity vector (from the Fitness algorithm)

    :param m: (Dataframe) M binary RCA matrix
    :param df_complexity: (Dataframe) Functional Complexity vector, returned by complexity
    :return: (Dataframe) Outlook vector with AREA as index and 'opportunity_value' column
    """
    m = m.loc[~(m == 0).all(axis=1)]
    d = distance_to_function(m)
    col0 = df_complexity.columns.values[0]
    df_complexity = df_complexity[[col0, 'q']].set_index(col0)
    weigthed_m = (1 - m).multiply(df_complexity['q'])
    outlook = pd.DataFrame(np.dot(1 - d, weigthed_m.T).diagonal(), index=d.index, columns=['opportunity_value'])
    return outlook


def gain(m, df_complexity):
    """
    Compute the opportunity gain for each community and each function in the dataset

    :param m: (Dataframe) M binary RCA matrix
    :param df_complexity: (Dataframe) Functional Complexity vector, returned by complexity
    :return: (Dataframe) Opportunity gain matrix with <function_name> as index and AREA as columns
    """
    m = m.loc[~(m == 0).all(axis=1)]
    d = function_proximity(m)
    col0 = df_complexity.columns.values[0]
    df_complexity = df_complexity[[col0, 'q']].set_index(col0)
    weigthed_m = (1 - m).multiply(df_complexity['q'])
    weigthed_d = d.div(d.sum(axis=0))
    gain = pd.DataFrame(np.dot(weigthed_d, weigthed_m.T).T, index=m.index, columns=m.columns)
    return gain