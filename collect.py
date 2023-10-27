# script to collect injury data 
# https://gist.github.com/maxwellbade/f33431383c466a7b70b386422c4b5e57#file-nfl-py

import bs4
import requests
import pandas as pd
import itertools
from ast import literal_eval
import ast
import math
import re
from difflib import SequenceMatcher
from collections import Counter
import collections

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

#data through week 10 of each year
url_list_2012 = ['https://www.nfl.com/injuries/league/2012/REG1','https://www.nfl.com/injuries/league/2012/REG2','https://www.nfl.com/injuries/league/2012/REG3','https://www.nfl.com/injuries/league/2012/REG4','https://www.nfl.com/injuries/league/2012/REG5','https://www.nfl.com/injuries/league/2012/REG6','https://www.nfl.com/injuries/league/2012/REG7','https://www.nfl.com/injuries/league/2012/REG8','https://www.nfl.com/injuries/league/2012/REG9','https://www.nfl.com/injuries/league/2012/REG10']
url_list_2013 = ['https://www.nfl.com/injuries/league/2013/REG1','https://www.nfl.com/injuries/league/2013/REG2','https://www.nfl.com/injuries/league/2013/REG3','https://www.nfl.com/injuries/league/2013/REG4','https://www.nfl.com/injuries/league/2013/REG5','https://www.nfl.com/injuries/league/2013/REG6','https://www.nfl.com/injuries/league/2013/REG7','https://www.nfl.com/injuries/league/2013/REG8','https://www.nfl.com/injuries/league/2013/REG9','https://www.nfl.com/injuries/league/2013/REG10']
url_list_2014 = ['https://www.nfl.com/injuries/league/2014/REG1','https://www.nfl.com/injuries/league/2014/REG2','https://www.nfl.com/injuries/league/2014/REG3','https://www.nfl.com/injuries/league/2014/REG4','https://www.nfl.com/injuries/league/2014/REG5','https://www.nfl.com/injuries/league/2014/REG6','https://www.nfl.com/injuries/league/2014/REG7','https://www.nfl.com/injuries/league/2014/REG8','https://www.nfl.com/injuries/league/2014/REG9','https://www.nfl.com/injuries/league/2014/REG10']
url_list_2015 = ['https://www.nfl.com/injuries/league/2015/REG1','https://www.nfl.com/injuries/league/2015/REG2','https://www.nfl.com/injuries/league/2015/REG3','https://www.nfl.com/injuries/league/2015/REG4','https://www.nfl.com/injuries/league/2015/REG5','https://www.nfl.com/injuries/league/2015/REG6','https://www.nfl.com/injuries/league/2015/REG7','https://www.nfl.com/injuries/league/2015/REG8','https://www.nfl.com/injuries/league/2015/REG9','https://www.nfl.com/injuries/league/2015/REG10']
url_list_2016 = ['https://www.nfl.com/injuries/league/2016/REG1','https://www.nfl.com/injuries/league/2016/REG2','https://www.nfl.com/injuries/league/2016/REG3','https://www.nfl.com/injuries/league/2016/REG4','https://www.nfl.com/injuries/league/2016/REG5','https://www.nfl.com/injuries/league/2016/REG6','https://www.nfl.com/injuries/league/2016/REG7','https://www.nfl.com/injuries/league/2016/REG8','https://www.nfl.com/injuries/league/2016/REG9','https://www.nfl.com/injuries/league/2016/REG10']
url_list_2017 = ['https://www.nfl.com/injuries/league/2017/REG1','https://www.nfl.com/injuries/league/2017/REG2','https://www.nfl.com/injuries/league/2017/REG3','https://www.nfl.com/injuries/league/2017/REG4','https://www.nfl.com/injuries/league/2017/REG5','https://www.nfl.com/injuries/league/2017/REG6','https://www.nfl.com/injuries/league/2017/REG7','https://www.nfl.com/injuries/league/2017/REG8','https://www.nfl.com/injuries/league/2017/REG9','https://www.nfl.com/injuries/league/2017/REG10']
url_list_2018 = ['https://www.nfl.com/injuries/league/2018/REG1','https://www.nfl.com/injuries/league/2018/REG2','https://www.nfl.com/injuries/league/2018/REG3','https://www.nfl.com/injuries/league/2018/REG4','https://www.nfl.com/injuries/league/2018/REG5','https://www.nfl.com/injuries/league/2018/REG6','https://www.nfl.com/injuries/league/2018/REG7','https://www.nfl.com/injuries/league/2018/REG8','https://www.nfl.com/injuries/league/2018/REG9','https://www.nfl.com/injuries/league/2018/REG10']
url_list_2019 = ['https://www.nfl.com/injuries/league/2019/REG1','https://www.nfl.com/injuries/league/2019/REG2','https://www.nfl.com/injuries/league/2019/REG3','https://www.nfl.com/injuries/league/2019/REG4','https://www.nfl.com/injuries/league/2019/REG5','https://www.nfl.com/injuries/league/2019/REG6','https://www.nfl.com/injuries/league/2019/REG7','https://www.nfl.com/injuries/league/2019/REG8','https://www.nfl.com/injuries/league/2019/REG9','https://www.nfl.com/injuries/league/2019/REG10']
url_list_2020 = ['https://www.nfl.com/injuries/league/2020/REG1','https://www.nfl.com/injuries/league/2020/REG2','https://www.nfl.com/injuries/league/2020/REG3','https://www.nfl.com/injuries/league/2020/REG4','https://www.nfl.com/injuries/league/2020/REG5','https://www.nfl.com/injuries/league/2020/REG6','https://www.nfl.com/injuries/league/2020/REG7','https://www.nfl.com/injuries/league/2020/REG8','https://www.nfl.com/injuries/league/2020/REG9','https://www.nfl.com/injuries/league/2020/REG10']
url_list_2021 = ['https://www.nfl.com/injuries/league/2021/REG1','https://www.nfl.com/injuries/league/2021/REG2','https://www.nfl.com/injuries/league/2021/REG3','https://www.nfl.com/injuries/league/2021/REG4','https://www.nfl.com/injuries/league/2021/REG5','https://www.nfl.com/injuries/league/2021/REG6','https://www.nfl.com/injuries/league/2021/REG7','https://www.nfl.com/injuries/league/2021/REG8','https://www.nfl.com/injuries/league/2021/REG9','https://www.nfl.com/injuries/league/2021/REG10']
url_list_2022 = ['https://www.nfl.com/injuries/league/2022/REG1','https://www.nfl.com/injuries/league/2022/REG2','https://www.nfl.com/injuries/league/2022/REG3','https://www.nfl.com/injuries/league/2022/REG4','https://www.nfl.com/injuries/league/2022/REG5','https://www.nfl.com/injuries/league/2022/REG6','https://www.nfl.com/injuries/league/2022/REG7','https://www.nfl.com/injuries/league/2022/REG8','https://www.nfl.com/injuries/league/2022/REG9','https://www.nfl.com/injuries/league/2022/REG10']

def injury_data(url_list,year):
    df_list = []
    df = pd.DataFrame()

    for i in url_list:
        alpha = requests.get(i)
        beta = bs4.BeautifulSoup(alpha.text)
        tables = beta.findAll("table")

        for table in tables:
             if table.findParent("table") is None:
                for tr in table:
                    if isinstance(tr, bs4.NavigableString):
                        continue
                    td = tr.find_all('td')
                    rows = [tr.text.strip() for tr in td if tr is not None and len(tr) > 0]
                    for i in rows:
                        df_list.append(i)

    df['data'] = df_list
    df = df[
        (df['data'].str.contains('Out'))
         | (df['data'].str.contains('Questionable'))
         ]
    df['year'] = str(year)

    return df
        
#concat all dfs
df1 = injury_data(url_list_2012,'2012')
df2 = injury_data(url_list_2013,'2013')
df3 = injury_data(url_list_2014,'2014')
df4 = injury_data(url_list_2015,'2015')
df5 = injury_data(url_list_2016,'2016')
df6 = injury_data(url_list_2017,'2017')
df7 = injury_data(url_list_2018,'2018')
df8 = injury_data(url_list_2019,'2019')
df9 = injury_data(url_list_2020,'2020')
df10 = injury_data(url_list_2021,'2021')
df11 = injury_data(url_list_2022,'2022')
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11], ignore_index=True)

display('semi raw data:', df.shape)

# create row number col
df['row_number'] = df.sort_values(['data','year'], ascending=[True,True]) \
             .groupby(['year']) \
             .cumcount() + 1
display('df with rownumber:', df.sort_values(by=['row_number','year'],ascending=True).head())

df.to_csv("nfl-injuries.csv")
