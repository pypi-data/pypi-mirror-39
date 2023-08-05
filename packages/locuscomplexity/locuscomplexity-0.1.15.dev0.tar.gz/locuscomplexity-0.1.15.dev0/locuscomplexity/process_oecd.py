"""
Processing OECD data file
"""

import pandas as pd
import numpy as np
import os
import sys
import locuscomplexity.file_handler as fh
dirname, filename = os.path.split(os.path.abspath(__file__))



def clean_oecd(year):
    df = pd.read_csv(os.path.join(dirname, '../data/raw/OECD1980.csv'))
    df = df[(df['Transaction']=='Total employment') & (df['Year']==year) & (df['MEASURE']=='PER')]
    df = df[['Country', 'ACTIVITY',  'Value']]
    df['ACTIVITY'] = df['ACTIVITY'].apply(lambda x : x[1:])
    # df['Value'] = df['Value'].apply(lambda x : ''.join(str(x).split('.')))
    df['Value'] = df['Value'].astype(float).apply(lambda x : x*1000)
    df.columns = ['Country', 'ISIC',  'Employment']
    return df


def mapping_isic():
    mapping = fh.get_mapping(os.path.join(dirname, '../data/external/isic2locus.csv'), 'ISIC 4.0', 'Enterprise_Locus',
                             '36x6x4x3', dr=False, io=False)
    mapping['ISIC 4.0'] = mapping['ISIC 4.0'].apply(lambda x : str(x).zfill(4)[:2])
    mapping.drop_duplicates(subset=['ISIC 4.0'], inplace=True)
    return mapping

def oecd_table(granularity =['a1','a2','a3','r1','r2','r3'], year=2016, locus = True):
    df_oecd = clean_oecd(year)
    df_oecd['Employment'] = df_oecd['Employment'].astype(float)
    df_oecd = pd.pivot_table(df_oecd, values='Employment', columns='ISIC', index='Country')
    df_oecd.dropna(axis=1, thresh=0.25 * df_oecd.shape[1], inplace=True)
    if not locus:
        df_oecd.index.name = 'AREA'
        df_oecd = df_oecd.reset_index()
        df_oecd['YEAR'] = year
        return df_oecd
    df_oecd=df_oecd.reset_index().melt('Country', var_name='ISIC', value_name='Employment')
    df_map = mapping_isic()
    df_oecd = df_oecd.merge(df_map, left_on='ISIC', right_on='ISIC 4.0').drop(['ISIC','ISIC 4.0'], 1)
    df_oecd = df_oecd.groupby(by=granularity+['Country'], as_index=False)['Employment'].sum()
    act = [x for x in granularity if x.startswith('a')]
    res = [x for x in granularity if x.startswith('r')]
    df_oecd['act'] = df_oecd[act].astype(str).apply(lambda x: '.'.join(x), axis=1)
    df_oecd['res'] = df_oecd[res].astype(str).apply(lambda x: ''.join(x), axis=1)
    df_oecd.replace(np.nan, '', inplace=True)
    df_oecd['Locus'] = df_oecd[['act', 'res']].astype(str).apply(lambda x: ' '.join(x), axis=1).apply(lambda x: x.strip())
    df_oecd.drop(granularity + ['act', 'res'], axis=1, inplace=True)
    df_oecd = pd.pivot_table(df_oecd, values = 'Employment', columns ='Locus', index='Country')
    df_oecd.index.name='AREA'
    df_oecd = df_oecd.reset_index()
    df_oecd['YEAR']=year
    df_oecd.dropna(axis=1, thresh=0.25 * df_oecd.shape[1], inplace=True)
    return df_oecd

