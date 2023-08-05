
import math
import numpy as np
import pandas as pd
import pickle
import os
import sklearn.metrics as sk_m
import matplotlib.pyplot as plt
import locuscomplexity.fitness as ft
import scipy.stats as stats
import locuscomplexity.process_oecd as oecd

dirname, filename = os.path.split(os.path.abspath(__file__))

with open('../data/raw/oes/ma_locus_3_count_all.pkl', 'rb') as file :
    data = pickle.load(file)

class event:
    '''
    An event describes the state of a community at one point in time in the
    log(GDPpc)-log(Fitness) plan.

    :param area: area code of the community
    :param year: year of interest
    :param r: distance max to find comparatives
    '''

    def __init__(self, area, year, rayon, horizon, fitness_overtime, gdp_overtime):
        self.area = area
        self.year = year
        self.r = rayon
        self.horizon = horizon
        areas = fitness_overtime.index.intersection(gdp_overtime.index)
        self.fitness = fitness_overtime.loc[areas]
        self.gdp = gdp_overtime.loc[areas]
        assert self.gdp.index.equals(self.fitness.index)

    def distance(self):
        '''

        :return: Matrix with the distance to every community at any time
                in the log(GDPpc)-log(Fitness) plan
        '''
        f_area = self.fitness.loc[self.area][self.year]
        d = self.fitness.drop(self.area,0)
        years = [x for x in d.columns if int(x)<self.year]
        fitness = d[years]
        diff_fitness = abs(fitness - f_area)

        y_area = self.gdp.loc[self.area][self.year]
        g = self.gdp.drop(self.area, 0)
        gdps = g[years]
        diff_gdp = abs(gdps - y_area)

        diff_gdp = diff_gdp.apply(pow, args=(2,))
        diff_fitness = diff_fitness.apply(pow, args=(2,))
        som = (diff_gdp.add(diff_fitness))
        self.dist = som.apply(np.sqrt)

    def comparatives(self):
        '''

        :return: Dictionnary of all comparative for the reference community
        '''
        #TODO Add fourth condition
        self.distance()
        fit = self.dist[self.dist < self.r]
        fit = fit.dropna(how='all', axis=0).dropna(how='all', axis=1).replace(np.nan, 0)
        d = {}
        for i in fit.index.unique():
            d[i] = {}
            for c in fit.columns:
                if fit.at[i, c]:
                    d[i][c] = fit.at[i, c]
        self.comp = d


    def is_comparative(self, area,year):
        '''

        :param area:
        :param year:
        :return:
        '''
        self.comparatives()
        return (area in self.comp & year in self.comp[area])


    def average_traj(self):
        '''
        Computes Tc

        :param horizon: horizon for the prediction
        :return:
        '''
        self.comparatives()
        #n_c is the number of comparatives
        n_c = sum(len(values) for values in self.comp.values())
        f_avg = 0
        gdp_avg = 0

        for com in self.comp:
            for year in self.comp[com]:
                future_f = self.fitness.at[com, int(year)+self.horizon]
                future_gdp = self.gdp.at[com, int(year)+self.horizon]
                if int(year)+self.horizon < 2017 :
                    if not math.isnan(future_f):
                        f_avg += (1/n_c)*(future_f-self.fitness.at[com, year])
                    if not math.isnan(future_gdp):
                      gdp_avg += (1/n_c)*(future_gdp-self.gdp.at[com, year])
        return f_avg, gdp_avg

    def predict_growth_rate(self):
        '''

        :param horizon: (int) horizon for the prediction
        :return: predicted annual growth rate over the horizon
        '''
        f_avg, gdp_avg = self.average_traj(self.horizon)
        start_g = self.gdp.at[self.area, self.year]
        end_g = start_g+gdp_avg

        return projected_annual_rate(start_g, end_g, self.horizon)

    def predict_future_gdp(self):
        '''

        :param horizon: (int) horizon for the prediction
        :return: predicted annual growth rate over the horizon
        '''
        f_avg, gdp_avg = self.average_traj()
        start_g = self.gdp.at[self.area, self.year]
        future_g = start_g + gdp_avg
        return future_g

    def plot_growth(self):
        start_f = self.fitness.at[self.area, self.year]
        end_f = self.fitness.at[self.area, self.year+self.horizon]
        start_g = self.gdp.at[self.area, self.year]
        end_g = self.gdp.at[self.area, self.year+self.horizon]
        pred_g = self.predict_future_gdp()
        plt.figure(figsize=(8,8))
        plt.scatter(start_g, start_f, c='b', label=str(self.year))
        plt.scatter(end_g, end_f, c='g', label=str(self.year+self.horizon))
        plt.scatter(pred_g, end_f, c='r', label=str(self.year+self.horizon))
        plt.legend()
        plt.show()


def projected_annual_rate(start_g, end_g, horizon):
    """
    Given the start and end log of gdp with the horizon, computes the annualized growth rate
    :return:
    """
    g = np.exp(end_g-start_g)
    return pow(g, 1 / horizon) - 1


def fitness_series(start,end,  locus=True):
    '''

    :param start: Beginning of the time period
    :param end: End of the time period
    :return: Matrix of the fitness of every community over the time period
    '''
    df = pd.DataFrame()
    for year in range(start,end+1):
        data = oecd.oecd_table(year=year, locus=locus)
        data.to_csv('test.csv')
        m = ft.build_m(data,year)
        fit = ft.fitness(m)
        fit.columns = [year, 'AREA']
        if df.empty :
            df = fit
        else :
            df = df.merge(fit, on='AREA', how='outer')
    c = [x for x in df.columns if x!='AREA']
    df[c]=df[c].apply(np.log)
    return df

def predict(year, horizon, r, locus):
    '''

    :param year: start year
    :param horizon: horizon for the prediction
    :param r: distance max for the comparatives

    '''
    df_fitness = fitness_series(1997, 2016, locus)
    df_gdp = log_gdp()
    df_fitness = df_fitness.set_index('AREA')
    df_gdp = df_gdp.set_index('AREA')

    communities = df_fitness.index.intersection(df_gdp.index)

    pred_gdp = []
    actual_gdp = []

    pred_rate =[]
    actual_rate =[]

    for c in communities :

        e = event(c,year,r,horizon,df_fitness,df_gdp)
        start_g = df_gdp.at[c, year]
        pred_g = e.predict_future_gdp()
        end_g = df_gdp.at[c, year + horizon]

        pred_rate.append(projected_annual_rate(start_g,pred_g,horizon))
        actual_rate.append(projected_annual_rate(start_g,end_g,horizon))

        pred_gdp.append(e.predict_future_gdp())
        actual_gdp.append(end_g)


    print('Predicting GDP')
    print(actual_gdp)
    print(pred_gdp)
    mae = sk_m.mean_absolute_error(actual_gdp, pred_gdp)
    mse = sk_m.mean_squared_error(actual_gdp, pred_gdp)
    corr, p_value = stats.pearsonr(actual_gdp, pred_gdp)
    print('Mean absolute error : {0:.5f}'.format(mae))
    print('Mean squared error : {0:.5f}'.format(mse))
    print('Correlation coefficient : {} ({})\n'.format(corr,p_value))

    print('Predicting annualized growth rate')
    print(actual_rate)
    print(pred_rate)
    mae = sk_m.mean_absolute_error(actual_rate, pred_rate)
    mse = sk_m.mean_squared_error(actual_rate, pred_rate)
    corr, p_value = stats.pearsonr(actual_rate, pred_rate)
    print('Mean absolute error : {0:.5f}'.format(mae))
    print('Mean squared error : {0:.5f}'.format(mse))
    print('Correlation coefficient : {} ({})\n'.format(corr, p_value))

    return communities, actual_gdp, pred_gdp


def log_gdp():
    df_gdp = pd.read_csv(os.path.join(dirname,'../data/raw/gdp_overtime.csv'))
    for c in df_gdp :
        if c != 'AREA':
            df_gdp[int(c)] = df_gdp[c].apply(np.log)
            df_gdp.drop(c, 1, inplace=True)
    return df_gdp


if __name__=='__main__':
    # df_fitness = fitness_series(1997, 2016,locus=True)
    # print(df_fitness.head())
    # df_gdp = log_gdp()
    # df_fitness = df_fitness.set_index('AREA')
    # df_gdp = df_gdp.set_index('AREA')
    # e_c = event('Canada',year=2015,rayon=1, horizon = 1,
    #             fitness_overtime = df_fitness,
    #             gdp_overtime=df_gdp)
    predict(year=2010, horizon=5, r=0.5, locus=True)
    predict(year=2010, horizon=5, r=0.5, locus=False)


