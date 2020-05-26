"""

    作者：大发
    日期：2019/11/17
    内容：利用python进行数据分析 10.1 p274 笔记

"""

import pandas as pd
import numpy as np
from io import StringIO
from lxml import objectify
import requests
import sqlite3
import sqlalchemy as sqla
from io import StringIO
import json
from numpy import nan as NA
import re
import matplotlib.pyplot as plt
from numpy.random import randn
from datetime import datetime
from io import BytesIO
import seaborn as sns
import statsmodels.api as sm

# 10.1 GroupBy机制

# df = pd.DataFrame({'key1': ['a' ,'a' ,'b' ,'b' ,'a'],
#                    'key2': ['one' ,'two' , 'one' ,'two','one'],
#                    'data1':np.random.randn(5) ,
#                    'data2': np.random.randn(5)})
# df
# Out[49]:
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# 4    a  one  0.169965  1.158086

## 按key1进行分组，并计算data1列的平均值
# 访问data1，并根据key1调用groupby
# grouped = df['data1'].groupby(df['key1'])
# grouped             # 变量grouped是一个GroupBy对象。它实际上还没有进行任何计算，只是含
# 有一些有关分组键df['key1']的中间数据而已。
# Out[52]: <pandas.core.groupby.generic.SeriesGroupBy object at 0x000001F6F5D432E8>

# grouped.mean()         # 平均值计算
# Out[53]:
# key1
# a   -0.245220
# b   -1.139282
# Name: data1, dtype: float64

# 根据key1,和key2分组，计算平均值
# means = df['data1'].groupby([df['key1'] , df['key2']]).mean()
# means
# Out[55]:
# key1  key2
# a     one    -0.317482
#       two    -0.100697
# b     one    -0.958730
#       two    -1.319834
# Name: data1, dtype: float64

# means.unstack()        # 内部列转行
# Out[56]:
# key2       one       two
# key1
# a    -0.317482 -0.100697
# b    -0.958730 -1.319834

# states = np.array(['Ohio' , 'California' , 'California' , 'Ohio' ,'Ohio'])
# years = np.array([2005 , 2005 , 2006 , 2005 , 2006])
# df['data1'].groupby([states , years]).mean()
# Out[59]:
# California  2005   -0.100697
#             2006   -0.958730
# Ohio        2005   -1.062382
#             2006    0.169965
# Name: data1, dtype: float64
# df.groupby('key1').mean()
# Out[60]:
#          data1     data2
# key1
# a    -0.245220  0.550057
# b    -1.139282  0.132454
# df.groupby(['key1','key2']).mean()
# Out[61]:
#               data1     data2
# key1 key2
# a    one  -0.317482  0.997484
#      two  -0.100697 -0.344798
# b    one  -0.958730  0.442310
#      two  -1.319834 -0.177402

# GroupBy的size方法，它可以返回一个含有分组大小的Series：
# df.groupby(['key1','key2']).size()
# Out[62]:
# key1  key2
# a     one     2
#       two     1
# b     one     1
#       two     1
# dtype: int64
# 注意，任何分组关键词中的缺失值，都会被从结果中除去。


# # 10.1.1 对分组进行迭代(遍历)
#
# for name , group in df.groupby('key1'):
#     print(name)
#     print(group)
# [out]:
# a
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 4    a  one  0.169965  1.158086
# b
#   key1 key2     data1     data2
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
#
#
# for (k1,k2) , group in df.groupby(['key1' ,'key2']):
#     print((k1,k2))
#     print(group)
#
# ('a', 'one')
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 4    a  one  0.169965  1.158086
# ('a', 'two')
#   key1 key2     data1     data2
# 1    a  two -0.100697 -0.344798
# ('b', 'one')
#   key1 key2    data1    data2
# 2    b  one -0.95873  0.44231
# ('b', 'two')
#   key1 key2     data1     data2
# 3    b  two -1.319834 -0.177402
#
# # 将这些数据片段做成一个字典：
# pieces = dict(list(df.groupby('key1')))
# pieces['b']
# Out[66]:
#   key1 key2     data1     data2
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
#
#
# # groupby默认是在axis=0上进行分组的，通过设置也可以在其他任何轴上进行
# # 分组。拿上面例子中的df来说，我们可以根据dtype对列进行分组
#
# df.dtypes
# Out[67]:
# key1      object
# key2      object
# data1    float64
# data2    float64
# dtype: object
# grouped = df.groupby(df.dtypes,axis=1)
# for dtype , group in grouped :
#     print(dtype)
#     print(group)
# float64
#       data1     data2
# 0 -0.804929  0.836882
# 1 -0.100697 -0.344798
# 2 -0.958730  0.442310
# 3 -1.319834 -0.177402
# 4  0.169965  1.158086
# object
#   key1 key2
# 0    a  one
# 1    a  two
# 2    b  one
# 3    b  two
# 4    a  one

## 10.1.2 选取一列或列的子集


# df.groupby('key1')['data1']
# df.groupby('key1')[['data2']]
#
# df['data1'].groupby(df['key1'])
# df[['data2']].groupby(df['key1'])

# 计算data2列的平均值并以DataFrame形式得到结果，可以这样写：
# df.groupby(['key1' , 'key2'])[['data2']].mean()
# Out[70]:
#               data2
# key1 key2
# a    one   0.997484
#      two  -0.344798
# b    one   0.442310
#      two  -0.177402

# s_grouped = df.groupby(['key1' , 'key2'])['data2']
# s_grouped
# Out[72]: <pandas.core.groupby.generic.SeriesGroupBy object at 0x000001F6F7BD1668>
# s_grouped.mean()
# Out[73]:
# key1  key2
# a     one     0.997484
#       two    -0.344798
# b     one     0.442310
#       two    -0.177402
# Name: data2, dtype: float64

## 10.1.3 通过字典或Series进行分组

# people = pd.DataFrame(np.random.randn(5,5),
#                       columns=['a' , 'b' ,'c' ,'d' ,'e'],
#                       index=['Joe', 'Steve' ,'Wes' ,'Jim' ,'Travis'])
#
# people.iloc[2:3 , [1,2]] = np.nan
# people
# Out[75]:
#                a         b         c         d         e
# Joe    -1.030798 -2.091427  0.845066  0.999099  0.375350
# Steve  -0.913930  1.598747  1.524904  0.331373 -2.018117
# Wes     1.371980       NaN       NaN -0.831736 -1.141324
# Jim    -1.251883  0.508237  0.090224 -0.387719 -1.104174
# Travis  0.922679 -0.127971  0.016176  0.239744 -0.037437

# 构造一个字典
# mapping = {'a':'red' , 'b':'red' ,'c':'blue' ,
#            'd':'blue' , 'e': 'red' ,'f': 'orange'}

# by_column = people.groupby(mapping , axis=1)
# by_column.sum()
# Out[79]:
#             blue       red
# Joe     1.844165 -2.746875
# Steve   1.856277 -1.333300
# Wes    -0.831736  0.230656
# Jim    -0.297495 -1.847820
# Travis  0.255920  0.757271
## Series 也可用
# map_series = pd.Series(mapping)
# map_series
# Out[81]:
# a       red
# b       red
# c      blue
# d      blue
# e       red
# f    orange
# dtype: object
# people.groupby(map_series , axis=1).count()
# Out[82]:
#         blue  red
# Joe        2    3
# Steve      2    3
# Wes        1    2
# Jim        2    3
# Travis     2    3


## 10.1.4 通过函数进行分组

# people.groupby(len).sum()
# Out[83]:
#           a         b         c         d         e
# 3 -0.910701 -1.583190  0.935290 -0.220357 -1.870148
# 5 -0.913930  1.598747  1.524904  0.331373 -2.018117
# 6  0.922679 -0.127971  0.016176  0.239744 -0.037437

# key_list = ['one' , 'one' , 'one' , 'two' , 'two']
# people.groupby([len , key_list]).min()
# Out[85]:
#               a         b         c         d         e
# 3 one -1.030798 -2.091427  0.845066 -0.831736 -1.141324
#   two -1.251883  0.508237  0.090224 -0.387719 -1.104174
# 5 one -0.913930  1.598747  1.524904  0.331373 -2.018117
# 6 two  0.922679 -0.127971  0.016176  0.239744 -0.037437

# 10.1.5  根据索引级别分组

# columns = pd.MultiIndex.from_arrays([['US' , 'US', 'US' , 'JP', 'JP'],
#                                      [1,3,5,1,3]],
#                                      names=['cty' , 'tenor'])
# hier_df = pd.DataFrame(np.random.randn(4,5) , columns=columns)
#
# hier_df
# Out[87]:
# cty          US                            JP
# tenor         1         3         5         1         3
# 0      0.887850  0.682389  1.188287 -1.469968  1.266990
# 1      1.229938 -0.526725 -1.453655 -0.143290 -0.409776
# 2     -1.519164 -0.657476  0.364010 -0.675027 -1.163751
# 3      0.937688  1.306474 -0.180216 -0.595456  0.291138

# 要根据级别分组，使用level关键字传递级别序号或名字：
# hier_df.groupby(level='cty' , axis=1).count()
# Out[88]:
# cty  JP  US
# 0     2   3
# 1     2   3
# 2     2   3
# 3     2   3

##  10.2  数据聚合
#
# df
# Out[49]:
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# 4    a  one  0.169965  1.158086
# grouped = df['data1'].groupby(df['key1'])
# grouped
# Out[51]: <pandas.core.groupby.generic.SeriesGroupBy object at 0x000001F6F7181CC0>
# grouped = df['data1'].groupby(df['key1'])
# grouped
# Out[52]: <pandas.core.groupby.generic.SeriesGroupBy object at 0x000001F6F5D432E8>
# grouped.mean()
# Out[53]:
# key1
# a   -0.245220
# b   -1.139282
# Name: data1, dtype: float64
# means = df['data1'].groupby([df['key1'] , df['key2']]).mean()
# means
# Out[55]:
# key1  key2
# a     one    -0.317482
#       two    -0.100697
# b     one    -0.958730
#       two    -1.319834
# Name: data1, dtype: float64
# means.unstack()
# Out[56]:
# key2       one       two
# key1
# a    -0.317482 -0.100697
# b    -0.958730 -1.319834
# states = np.array(['Ohio' , 'California' , 'California' , 'Ohio' ,'Ohio'])
# years = np.array([2005 , 2005 , 2006 , 2005 , 2006])
# df['data1'].groupby([states , years]).mean()
# Out[59]:
# California  2005   -0.100697
#             2006   -0.958730
# Ohio        2005   -1.062382
#             2006    0.169965
# Name: data1, dtype: float64
# df.groupby('key1').mean()
# Out[60]:
#          data1     data2
# key1
# a    -0.245220  0.550057
# b    -1.139282  0.132454
# df.groupby(['key1','key2']).mean()
# Out[61]:
#               data1     data2
# key1 key2
# a    one  -0.317482  0.997484
#      two  -0.100697 -0.344798
# b    one  -0.958730  0.442310
#      two  -1.319834 -0.177402
# df.groupby(['key1','key2']).size()
# Out[62]:
# key1  key2
# a     one     2
#       two     1
# b     one     1
#       two     1
# dtype: int64
# for name , group in df.groupby('key1'):
#     print(name)
#     print(group)
# a
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 4    a  one  0.169965  1.158086
# b
#   key1 key2     data1     data2
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# for (k1,k2) , group in df.groupby(['key1' ,'key2']):
#     print((k1,k2))
#     print(group)
# ('a', 'one')
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 4    a  one  0.169965  1.158086
# ('a', 'two')
#   key1 key2     data1     data2
# 1    a  two -0.100697 -0.344798
# ('b', 'one')
#   key1 key2    data1    data2
# 2    b  one -0.95873  0.44231
# ('b', 'two')
#   key1 key2     data1     data2
# 3    b  two -1.319834 -0.177402
# pieces = dict(list(df.groupby('key1')))
# pieces['b']
# Out[66]:
#   key1 key2     data1     data2
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# df.dtypes
# Out[67]:
# key1      object
# key2      object
# data1    float64
# data2    float64
# dtype: object
# grouped = df.groupby(df.dtypes,axis=1)
# for dtype , group in grouped :
#     print(dtype)
#     print(group)
# float64
#       data1     data2
# 0 -0.804929  0.836882
# 1 -0.100697 -0.344798
# 2 -0.958730  0.442310
# 3 -1.319834 -0.177402
# 4  0.169965  1.158086
# object
#   key1 key2
# 0    a  one
# 1    a  two
# 2    b  one
# 3    b  two
# 4    a  one
# df.groupby(['key1' , 'key2'])[['data2']].mean()
# Out[70]:
#               data2
# key1 key2
# a    one   0.997484
#      two  -0.344798
# b    one   0.442310
#      two  -0.177402
# s_grouped = df.groupby(['key1' , 'key2'])['data2']
# s_grouped
# Out[72]: <pandas.core.groupby.generic.SeriesGroupBy object at 0x000001F6F7BD1668>
# s_grouped.mean()
# Out[73]:
# key1  key2
# a     one     0.997484
#       two    -0.344798
# b     one     0.442310
#       two    -0.177402
# Name: data2, dtype: float64
# people = pd.DataFrame(np.random.randn(5,5),
#                       columns=['a' , 'b' ,'c' ,'d' ,'e'],
#                       index=['Joe', 'Steve' ,'Wes' ,'Jim' ,'Travis'])
# people.iloc[2:3 , [1,2]] = np.nan
# people
# Out[75]:
#                a         b         c         d         e
# Joe    -1.030798 -2.091427  0.845066  0.999099  0.375350
# Steve  -0.913930  1.598747  1.524904  0.331373 -2.018117
# Wes     1.371980       NaN       NaN -0.831736 -1.141324
# Jim    -1.251883  0.508237  0.090224 -0.387719 -1.104174
# Travis  0.922679 -0.127971  0.016176  0.239744 -0.037437
# mapping = {'a':'red' , 'b':'red' ,'c':'blue' ,}
# mapping = {'a':'red' , 'b':'red' ,'c':'blue' ,
#            'd':'blue' , 'e': 'red' ,'f': 'orange'}
# by_column = people.groupby(mapping , axis=1)
# by_column.sum()
# Out[79]:
#             blue       red
# Joe     1.844165 -2.746875
# Steve   1.856277 -1.333300
# Wes    -0.831736  0.230656
# Jim    -0.297495 -1.847820
# Travis  0.255920  0.757271
# map_series = pd.Series(mapping)
# map_series
# Out[81]:
# a       red
# b       red
# c      blue
# d      blue
# e       red
# f    orange
# dtype: object
# people.groupby(map_series , axis=1).count()
# Out[82]:
#         blue  red
# Joe        2    3
# Steve      2    3
# Wes        1    2
# Jim        2    3
# Travis     2    3
# people.groupby(len).sum()
# Out[83]:
#           a         b         c         d         e
# 3 -0.910701 -1.583190  0.935290 -0.220357 -1.870148
# 5 -0.913930  1.598747  1.524904  0.331373 -2.018117
# 6  0.922679 -0.127971  0.016176  0.239744 -0.037437
# key_list = ['one' , 'one' , 'one' , 'two' , 'two']
# people.groupby([len , key_list]).min()
# Out[85]:
#               a         b         c         d         e
# 3 one -1.030798 -2.091427  0.845066 -0.831736 -1.141324
#   two -1.251883  0.508237  0.090224 -0.387719 -1.104174
# 5 one -0.913930  1.598747  1.524904  0.331373 -2.018117
# 6 two  0.922679 -0.127971  0.016176  0.239744 -0.037437
# columns = pd.MultiIndex.from_arrays([['US' , 'US', 'US' , 'JP', 'JP'],
#                                      [1,3,5,1,3]],
#                                      names=['cty' , 'tenor'])
# hier_df = pd.DataFrame(np.random.randn(4,5) , columns=columns)
# hier_df
# Out[87]:
# cty          US                            JP
# tenor         1         3         5         1         3
# 0      0.887850  0.682389  1.188287 -1.469968  1.266990
# 1      1.229938 -0.526725 -1.453655 -0.143290 -0.409776
# 2     -1.519164 -0.657476  0.364010 -0.675027 -1.163751
# 3      0.937688  1.306474 -0.180216 -0.595456  0.291138
# hier_df.groupby(level='cty' , axis=1).count()
# Out[88]:
# cty  JP  US
# 0     2   3
# 1     2   3
# 2     2   3
# 3     2   3
# df
# Out[89]:
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# 4    a  one  0.169965  1.158086
# grouped = df.groupby('key1')
# grouped['data1'].quantile(0.9)
# Out[91]:
# key1
# a    0.115833
# b   -0.994841
# Name: data1, dtype: float64
# def peak_to_peak(arr):
#     return arr.max()-arr.min()
# grouped.agg(peak_to_peak)
# Out[92]:
#          data1     data2
# key1
# a     0.974895  1.502884
# b     0.361104  0.619712
# grouped
# Out[93]: <pandas.core.groupby.generic.DataFrameGroupBy object at 0x000001F6F7BBCA90>
# grouped.describe()
# Out[94]:
#      data1                      ...     data2
#      count      mean       std  ...       50%       75%       max
# key1                            ...
# a      3.0 -0.245220  0.503260  ...  0.836882  0.997484  1.158086
# b      2.0 -1.139282  0.255339  ...  0.132454  0.287382  0.442310
# [2 rows x 16 columns]


## 10.2.1 逐列及多函数应用
# tips = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\ips.csv')
# tips['tip_pct'] = tips['tip']/tips['total_bill']
# tips[:6]
# Out[97]:
#    total_bill   tip smoker  day    time  size   tip_pct
# 0       16.99  1.01     No  Sun  Dinner     2  0.059447
# 1       10.34  1.66     No  Sun  Dinner     3  0.160542
# 2       21.01  3.50     No  Sun  Dinner     3  0.166587
# 3       23.68  3.31     No  Sun  Dinner     2  0.139780
# 4       24.59  3.61     No  Sun  Dinner     4  0.146808
# 5       25.29  4.71     No  Sun  Dinner     4  0.186240
# grouped = tips.groupby(['day' , 'smoker'])   ## 分组
# grouped_pct = grouped['tip_pct']             # 从各个碎片里选出这一列
# grouped_pct.agg('mean')                  # 单独自定义的算
# Out[100]:
# day   smoker
# Fri   No        0.151650
#       Yes       0.174783
# Sat   No        0.158048
#       Yes       0.147906
# Sun   No        0.160113
#       Yes       0.187250
# Thur  No        0.160298
#       Yes       0.163863
# Name: tip_pct, dtype: float64
# grouped_pct.agg(['mean' , 'std' , peak_to_peak])      # 列表一起算
# Out[101]:
#                  mean       std  peak_to_peak
# day  smoker
# Fri  No      0.151650  0.028123      0.067349
#      Yes     0.174783  0.051293      0.159925
# Sat  No      0.158048  0.039767      0.235193
#      Yes     0.147906  0.061375      0.290095
# Sun  No      0.160113  0.042347      0.193226
#      Yes     0.187250  0.154134      0.644685
# Thur No      0.160298  0.038774      0.193350
#      Yes     0.163863  0.039389      0.151240
#
#
# grouped_pct.agg([('foo' , 'mean') , ('bar' , np.std)])    # 自定义函数命名
# Out[103]:
#                   foo       bar
# day  smoker
# Fri  No      0.151650  0.028123
#      Yes     0.174783  0.051293
# Sat  No      0.158048  0.039767
#      Yes     0.147906  0.061375
# Sun  No      0.160113  0.042347
#      Yes     0.187250  0.154134
# Thur No      0.160298  0.038774
#      Yes     0.163863  0.039389


# 定义一组应用于全部列的一组函数，或不同的列应用不同的函数。
# 假设我们想要对tip_pct和total_bill列计算三个统计信息：

# functions = ['count' , 'mean' , 'max']
# result = grouped['tip_pct' , 'total_bill' ].agg(functions)    # 对这两列数据执行函数
# result
# Out[106]:
#             tip_pct                     total_bill
#               count      mean       max      count       mean    max
# day  smoker
# Fri  No           4  0.151650  0.187735          4  18.420000  22.75
#      Yes         15  0.174783  0.263480         15  16.813333  40.17
# Sat  No          45  0.158048  0.291990         45  19.661778  48.33
#      Yes         42  0.147906  0.325733         42  21.276667  50.81
# Sun  No          57  0.160113  0.252672         57  20.506667  48.17
#      Yes         19  0.187250  0.710345         19  24.120000  45.35
# Thur No          45  0.160298  0.266312         45  17.113111  41.19
#      Yes         17  0.163863  0.241255         17  19.190588  43.11

# 结果DataFrame拥有层次化的列，这相当于分别对各列进行聚合，
# 然后用concat将结果组装到一起，使用列名用作keys参数：

# result['tip_pct']
# Out[107]:
#              count      mean       max
# day  smoker
# Fri  No          4  0.151650  0.187735
#      Yes        15  0.174783  0.263480
# Sat  No         45  0.158048  0.291990
#      Yes        42  0.147906  0.325733
# Sun  No         57  0.160113  0.252672
#      Yes        19  0.187250  0.710345
# Thur No         45  0.160298  0.266312
#      Yes        17  0.163863  0.241255


# 跟前面一样，这里也可以传入带有自定义名称的一组元组：
# ftuples = [('Durchschnitt' , 'mean') ,('Abweichung' , np.var)]
# grouped['tip_pct' , 'total_bill'].agg(ftuples)
# Out[109]:
#                  tip_pct              total_bill
#             Durchschnitt Abweichung Durchschnitt  Abweichung
# day  smoker
# Fri  No         0.151650   0.000791    18.420000   25.596333
#      Yes        0.174783   0.002631    16.813333   82.562438
# Sat  No         0.158048   0.001581    19.661778   79.908965
#      Yes        0.147906   0.003767    21.276667  101.387535
# Sun  No         0.160113   0.001793    20.506667   66.099980
#      Yes        0.187250   0.023757    24.120000  109.046044
# Thur No         0.160298   0.001503    17.113111   59.625081
#      Yes        0.163863   0.001551    19.190588   69.808518

# 假设你想要对一个列或不同的列应用不同的函数。
# 具体的办法是向agg传入一个从列名映射到函数的字典：
# grouped.agg({'tip':np.max , 'size':'sum'})
# Out[110]:
#                tip  size
# day  smoker
# Fri  No       3.50     9
#      Yes      4.73    31
# Sat  No       9.00   115
#      Yes     10.00   104
# Sun  No       6.00   167
#      Yes      6.50    49
# Thur No       6.70   112
#      Yes      5.00    40
# grouped.agg({'tip_pct':['min' , 'max', 'mean', 'std'],'size':'sum'})
# Out[111]:
#               tip_pct                               size
#                   min       max      mean       std  sum
# day  smoker
# Fri  No      0.120385  0.187735  0.151650  0.028123    9
#      Yes     0.103555  0.263480  0.174783  0.051293   31
# Sat  No      0.056797  0.291990  0.158048  0.039767  115
#      Yes     0.035638  0.325733  0.147906  0.061375  104
# Sun  No      0.059447  0.252672  0.160113  0.042347  167
#      Yes     0.065660  0.710345  0.187250  0.154134   49
# Thur No      0.072961  0.266312  0.160298  0.038774  112
#      Yes     0.090014  0.241255  0.163863  0.039389   40

## 10.2.2 返回不含行索引的聚合数据

# 可以向groupby传入as_index=False以禁用分组键作为索引的行为
# tips.groupby(['day' , 'smoker'] , as_index =False).mean()
# Out[112]:
#     day smoker  total_bill       tip      size   tip_pct
# 0   Fri     No   18.420000  2.812500  2.250000  0.151650
# 1   Fri    Yes   16.813333  2.714000  2.066667  0.174783
# 2   Sat     No   19.661778  3.102889  2.555556  0.158048
# 3   Sat    Yes   21.276667  2.875476  2.476190  0.147906
# 4   Sun     No   20.506667  3.167895  2.929825  0.160113
# 5   Sun    Yes   24.120000  3.516842  2.578947  0.187250
# 6  Thur     No   17.113111  2.673778  2.488889  0.160298
# 7  Thur    Yes   19.190588  3.030000  2.352941  0.163863


#### 10.3 apply：一般性的“拆分－应用－合并”

# 选取指定列具有最大值的行
# def top(df , n=5 , column='tip_pct'):
#     return df.sort_values(by=column)[-n:]
#
# top(tips , n=6)
# Out[113]:
#      total_bill   tip smoker  day    time  size   tip_pct
# 109       14.31  4.00    Yes  Sat  Dinner     2  0.279525
# 183       23.17  6.50    Yes  Sun  Dinner     4  0.280535
# 232       11.61  3.39     No  Sat  Dinner     2  0.291990
# 67         3.07  1.00    Yes  Sat  Dinner     1  0.325733
# 178        9.60  4.00    Yes  Sun  Dinner     2  0.416667
# 172        7.25  5.15    Yes  Sun  Dinner     2  0.710345

# 如果对smoker分组并用该函数调用apply，就会得到：
# tips.groupby('smoker').apply(top)
# Out[114]:
#             total_bill   tip smoker   day    time  size   tip_pct
# smoker
# No     88        24.71  5.85     No  Thur   Lunch     2  0.236746
#        185       20.69  5.00     No   Sun  Dinner     5  0.241663
#        51        10.29  2.60     No   Sun  Dinner     2  0.252672
#        149        7.51  2.00     No  Thur   Lunch     2  0.266312
#        232       11.61  3.39     No   Sat  Dinner     2  0.291990
# Yes    109       14.31  4.00    Yes   Sat  Dinner     2  0.279525
#        183       23.17  6.50    Yes   Sun  Dinner     4  0.280535
#        67         3.07  1.00    Yes   Sat  Dinner     1  0.325733
#        178        9.60  4.00    Yes   Sun  Dinner     2  0.416667
#        172        7.25  5.15    Yes   Sun  Dinner     2  0.710345

# tips.groupby(['smoker' , 'day']).apply(top , n=1, column='total_bill')
# Out[115]:
#                  total_bill    tip smoker   day    time  size   tip_pct
# smoker day
# No     Fri  94        22.75   3.25     No   Fri  Dinner     2  0.142857
#        Sat  212       48.33   9.00     No   Sat  Dinner     4  0.186220
#        Sun  156       48.17   5.00     No   Sun  Dinner     6  0.103799
#        Thur 142       41.19   5.00     No  Thur   Lunch     5  0.121389
# Yes    Fri  95        40.17   4.73    Yes   Fri  Dinner     4  0.117750
#        Sat  170       50.81  10.00    Yes   Sat  Dinner     3  0.196812
#        Sun  182       45.35   3.50    Yes   Sun  Dinner     3  0.077178
#        Thur 197       43.11   5.00    Yes  Thur   Lunch     4  0.115982

# result = tips.groupby('smoker')['tip_pct'].describe()
# result
# Out[117]:
#         count      mean       std  ...       50%       75%       max
# smoker                             ...
# No      151.0  0.159328  0.039910  ...  0.155625  0.185014  0.291990
# Yes      93.0  0.163196  0.085119  ...  0.153846  0.195059  0.710345
# [2 rows x 8 columns]

# result.unstack('smoker')
# Out[118]:
#        smoker
# count  No        151.000000
#        Yes        93.000000
# mean   No          0.159328
#        Yes         0.163196
# std    No          0.039910
#        Yes         0.085119
# min    No          0.056797
#        Yes         0.035638
# 25%    No          0.136906
#        Yes         0.106771
# 50%    No          0.155625
#        Yes         0.153846
# 75%    No          0.185014
#        Yes         0.195059
# max    No          0.291990
#        Yes         0.710345
# dtype: float64

#### 10.3.1 禁止(压缩)分组键

# 从上面的例子中可以看出，分组键会跟原始对象的索引共同构成结果对象中的层次化索引。
# 将group_keys=False传入groupby即可禁止该效果：

# tips.groupby('smoker' , group_keys=False).apply(top)
# Out[119]:
#      total_bill   tip smoker   day    time  size   tip_pct
# 88        24.71  5.85     No  Thur   Lunch     2  0.236746
# 185       20.69  5.00     No   Sun  Dinner     5  0.241663
# 51        10.29  2.60     No   Sun  Dinner     2  0.252672
# 149        7.51  2.00     No  Thur   Lunch     2  0.266312
# 232       11.61  3.39     No   Sat  Dinner     2  0.291990
# 109       14.31  4.00    Yes   Sat  Dinner     2  0.279525
# 183       23.17  6.50    Yes   Sun  Dinner     4  0.280535
# 67         3.07  1.00    Yes   Sat  Dinner     1  0.325733
# 178        9.60  4.00    Yes   Sun  Dinner     2  0.416667
# 172        7.25  5.15    Yes   Sun  Dinner     2  0.710345

## 10.3.2 分位数和桶分析

# 利用cut将其装入长度相等的桶中

# frame = pd.DataFrame({'data1': np.random.randn(1000),
#                       'data2': np.random.randn(1000)})
# quartiles = pd.cut(frame.data1 , 4)
# quartiles[:10]
#
# Out[120]:
# 0    (-1.696, -0.0282]
# 1    (-1.696, -0.0282]
# 2      (-0.0282, 1.64]
# 3      (-0.0282, 1.64]
# 4    (-1.696, -0.0282]
# 5    (-1.696, -0.0282]
# 6    (-1.696, -0.0282]
# 7      (-0.0282, 1.64]
# 8    (-1.696, -0.0282]
# 9    (-1.696, -0.0282]
# Name: data1, dtype: category
# Categories (4, interval[float64]): [(-3.371, -1.696] < (-1.696, -0.0282] < (-0.0282, 1.64] <
#                                     (1.64, 3.308]]

# 由cut返回的Categorical对象可直接传递到groupby
# def get_stats(group):
#     return{'min':group.min() , 'max':group.max() ,
#            'count':group.count() , 'mean':group.mean()}
#
# grouped = frame.data2.groupby(quartiles)
#
# grouped.apply(get_stats).unstack()
# Out[121]:
#                    count       max      mean       min
# data1
# (-3.371, -1.696]    25.0  0.937953 -0.527163 -2.293599
# (-1.696, -0.0282]  440.0  3.230200 -0.033814 -2.779937
# (-0.0282, 1.64]    472.0  2.889109 -0.076130 -3.476586
# (1.64, 3.308]       63.0  2.535317  0.242954 -2.064886

# grouping = pd.qcut(frame.data1 , 10 , labels=False)
# grouped = frame.data2.groupby(grouping)
# grouped.apply(get_stats).unstack()
# Out[124]:
#        count       max      mean       min
# data1
# 0      100.0  1.978955 -0.334739 -2.293599
# 1      100.0  3.230200  0.017462 -2.779937
# 2      100.0  2.891592 -0.029558 -2.020534
# 3      100.0  2.474053 -0.003091 -1.936374
# 4      100.0  2.197015  0.069839 -2.591576
# 5      100.0  2.316819 -0.041222 -1.881967
# 6      100.0  1.980845 -0.147302 -2.333208
# 7      100.0  2.263098  0.035961 -2.410611
# 8      100.0  2.501653 -0.094989 -3.002419
# 9      100.0  2.889109  0.040795 -3.476586


## 10.3.3 示例：用特定于分组的值填充缺失值

# 用平均值去填充NA值
# s = pd.Series(np.random.randn(6))
# s[::2] = np.nan
# s
# Out[127]:
# 0         NaN
# 1    0.602224
# 2         NaN
# 3    0.699476
# 4         NaN
# 5   -0.652920
# dtype: float64
# s.fillna(s.mean())
# Out[128]:
# 0    0.216260
# 1    0.602224
# 2    0.216260
# 3    0.699476
# 4    0.216260
# 5   -0.652920
# dtype: float64

# 对不同的分组填充不同的值。
# 一种方法是将数据分组，并使用apply和一个能够对各数据块调用fillna的函数即可。

# states = ['Ohio', 'New York', 'Vermont', 'Florida',
#           'Oregon', 'Nevada', 'California', 'Idaho']
# group_key = ['East']*4 +['West']*4
# data = pd.Series(np.random.randn(8) , index = states)
# data
# Out[133]:
# Ohio          1.617040
# New York      1.729617
# Vermont       0.233488
# Florida      -1.171723
# Oregon       -2.468041
# Nevada       -1.901511
# California   -0.146598
# Idaho        -0.671975
# dtype: float64

# data[['Vermont', 'Nevada', 'Idaho']] = np.nan
# data
# Out[135]:
# Ohio          1.617040
# New York      1.729617
# Vermont            NaN
# Florida      -1.171723
# Oregon       -2.468041
# Nevada             NaN
# California   -0.146598
# Idaho              NaN
# dtype: float64

# data.groupby(group_key).mean()
# Out[136]:
# East    0.724978
# West   -1.307319
# dtype: float64

# 用分组平均值去填充NA值

# fill_mean = lambda g:g.fillna(g.mean())     # lambda 定义一个函数
# data.groupby(group_key).apply(fill_mean)
# Out[138]:
# Ohio          1.617040
# New York      1.729617
# Vermont       0.724978
# Florida      -1.171723
# Oregon       -2.468041
# Nevada       -1.307319
# California   -0.146598
# Idaho        -1.307319
# dtype: float64

# 另外，也可以在代码中预定义各组的填充值。分组具有一个name属性

# fill_values = {'East':0.5 , 'West':-1}
# fill_func = lambda g:g.fillna(fill_values[g.name])
# data.groupby(group_key).apply(fill_func)
# Out[141]:
# Ohio          1.617040
# New York      1.729617
# Vermont       0.500000
# Florida      -1.171723
# Oregon       -2.468041
# Nevada       -1.000000
# California   -0.146598
# Idaho        -1.000000
# dtype: float64

## 10.3.4 示例：随机采样和排列

# 从一个大数据集中随机抽取（进行替换或不替换）样本
# 以进行蒙特卡罗模拟（Monte Carlo simulation）或其他分析工作。
# “抽取”的方式有很多，这里使用的方法是对Series使用sample方法：

# Hearts, Spades, Clubs, Diamonds
# suits = ['H' , 'S' , 'C' , 'D']
# card_val = (list(range(1,11))+[10]*3)*4
# base_names = ['A']+list(range(2,11))+['J' , 'K' , 'Q']
# cards = []
# for suit in ['H' , 'S' , 'C' , 'D'] :
#     cards.extend(str(num)+suit for num in base_names)
# deck = pd.Series(card_val , index=cards)
#
# deck[:13]
# Out[145]:
# AH      1
# 2H      2
# 3H      3
# 4H      4
# 5H      5
# 6H      6
# 7H      7
# 8H      8
# 9H      9
# 10H    10
# JH     10
# KH     10
# QH     10
# dtype: int64

# def draw(deck , n=5):
#     return deck.sample(n)
# draw(deck)
# Out[147]:
# 7H     7
# QH    10
# 7S     7
# 2D     2
# 3S     3
# dtype: int64

# 从每种花色中随机抽取两张牌。
# 由于花色是牌名的最后一个字符，
# 所以我们可以据此进行分组，并使用apply：

# get_suit = lambda card:card[-1]  # last letter is suit
# deck.groupby(get_suit).apply(draw , n=2)
#
# Out[148]:
# C  KC     10
#    9C      9
# D  10D    10
#    6D      6
# H  JH     10
#    9H      9
# S  2S      2
#    JS     10
# dtype: int64

# deck.groupby(get_suit , group_keys = False).apply(draw , n=2)
# Out[149]:
# KC    10
# 7C     7
# 8D     8
# 4D     4
# QH    10
# JH    10
# JS    10
# QS    10
# dtype: int64


## 10.3.5 示例：分组加权平均数和相关系数

# df = pd.DataFrame({'category':['a','a' ,'a','a','b','b','b','b'],
#                    'data':np.random.randn(8),
#                    'weights':np.random.rand(8)})
# df
# Out[151]:
#   category      data   weights
# 0        a -1.212104  0.002279
# 1        a -0.161240  0.284931
# 2        a -0.821587  0.372479
# 3        a  0.110707  0.624479
# 4        b  0.780079  0.155326
# 5        b  0.341591  0.506119
# 6        b -1.597729  0.338060
# 7        b  1.866220  0.111349

# 利用category计算分组加权平均数

# grouped = df.groupby('category')
# get_wavg = lambda g:np.average(g['data'] , weights=g['weights'])
# grouped.apply(get_wavg)
# Out[152]:
# category
# a   -0.222396
# b   -0.034455
# dtype: float64

# close_px = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\stock_px_2.csv',
#                        parse_dates=True , index_col =0)
# close_px.info()
# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 2214 entries, 2003-01-02 to 2011-10-14
# Data columns (total 4 columns):
# AAPL    2214 non-null float64
# MSFT    2214 non-null float64
# XOM     2214 non-null float64
# SPX     2214 non-null float64
# dtypes: float64(4)
# memory usage: 86.5 KB
# close_px[-4:]
# Out[154]:
#               AAPL   MSFT    XOM      SPX
# 2011-10-11  400.29  27.00  76.27  1195.54
# 2011-10-12  402.19  26.96  77.16  1207.25
# 2011-10-13  408.43  27.18  76.37  1203.66
# 2011-10-14  422.00  27.27  78.11  1224.58

# 计算一个由日收益率（通过百分数变化计算）与
# SPX之间的年度相关系数组成的DataFrame。
# spx_corr = lambda x:x.corrwith(x['SPX'])  # 创建一个函数，用它计算每列和SPX列的成对相关系数
# rets = close_px.pct_change().dropna()     # 使用pct_change计算close_px的百分比变化
# get_year = lambda x:x.year
# by_year = rets.groupby(get_year)
# by_year.apply(spx_corr)
# Out[159]:
#           AAPL      MSFT       XOM  SPX
# 2003  0.541124  0.745174  0.661265  1.0
# 2004  0.374283  0.588531  0.557742  1.0
# 2005  0.467540  0.562374  0.631010  1.0
# 2006  0.428267  0.406126  0.518514  1.0
# 2007  0.508118  0.658770  0.786264  1.0
# 2008  0.681434  0.804626  0.828303  1.0
# 2009  0.707103  0.654902  0.797921  1.0
# 2010  0.710105  0.730118  0.839057  1.0
# 2011  0.691931  0.800996  0.859975  1.0

# 计算列与列之间的相关系数
# by_year.apply(lambda g:g['AAPL'].corr(g['MSFT']))
# Out[160]:
# 2003    0.480868
# 2004    0.259024
# 2005    0.300093
# 2006    0.161735
# 2007    0.417738
# 2008    0.611901
# 2009    0.432738
# 2010    0.571946
# 2011    0.581987
# dtype: float64

## 10.3.6 示例：组级别的线性回归

# 可以定义下面这个regress函数（利用statsmodels计量经济学库）
# 对各数据块执行普通最小二乘法（Ordinary Least Squares，OLS）回归：

# def regress(data , yvar , xvars):
#     Y = data[yvar]
#     X = data[xvars]
#     X['intercept'] = 1.
#     result = sm.OLS(Y , X).fit()
#     return result.params

# by_year.apply(regress , 'AAPL' , ['SPX'])
# Out[163]:
#            SPX  intercept
# 2003  1.195406   0.000710
# 2004  1.363463   0.004201
# 2005  1.766415   0.003246
# 2006  1.645496   0.000080
# 2007  1.198761   0.003438
# 2008  0.968016  -0.001110
# 2009  0.879103   0.002954
# 2010  1.052608   0.001261
# 2011  0.806605   0.001514

#### 10.4 透视表和交叉表

# DataFrame有一个pivot_table方法，此外还有一个顶级的pandas.pivot_table函数。
# 除能为groupby提供便利之外，pivot_table还可以添加分项小计，也叫做margins。
# tips.pivot_table(index=['day' , 'smoker'])
# Out[164]:
#                  size       tip   tip_pct  total_bill
# day  smoker
# Fri  No      2.250000  2.812500  0.151650   18.420000
#      Yes     2.066667  2.714000  0.174783   16.813333
# Sat  No      2.555556  3.102889  0.158048   19.661778
#      Yes     2.476190  2.875476  0.147906   21.276667
# Sun  No      2.929825  3.167895  0.160113   20.506667
#      Yes     2.578947  3.516842  0.187250   24.120000
# Thur No      2.488889  2.673778  0.160298   17.113111
#      Yes     2.352941  3.030000  0.163863   19.190588

# 聚合tip_pct和size，并根据time进行分组
# tips.pivot_table(['tip_pct' , 'size'],index=['time' , 'day'],
#                  columns='smoker' , margins=True)     # margins=True 这一行决定的是all的那列

# Out[165]:
#                  size                       tip_pct
# smoker             No       Yes       All        No       Yes       All
# time   day
# Dinner Fri   2.000000  2.222222  2.166667  0.139622  0.165347  0.158916
#        Sat   2.555556  2.476190  2.517241  0.158048  0.147906  0.153152
#        Sun   2.929825  2.578947  2.842105  0.160113  0.187250  0.166897
#        Thur  2.000000       NaN  2.000000  0.159744       NaN  0.159744
# Lunch  Fri   3.000000  1.833333  2.000000  0.187735  0.188937  0.188765
#        Thur  2.500000  2.352941  2.459016  0.160311  0.163863  0.161301
# All          2.668874  2.408602  2.569672  0.159328  0.163196  0.160803
# All值为平均数：不单独考虑烟民与非烟民（All列），
# 不单独考虑行分组两个级别中的任何单项（All行）。

# 使用count或len可以得到有关分组大小的交叉表（计数或频率）
# tips.pivot_table('tip_pct' , index=['time' , 'smoker'],
#                  columns='day' , aggfunc=len , margins=True)
# Out[168]:
# day             Fri   Sat   Sun  Thur    All
# time   smoker
# Dinner No       3.0  45.0  57.0   1.0  106.0
#        Yes      9.0  42.0  19.0   NaN   70.0
# Lunch  No       1.0   NaN   NaN  44.0   45.0
#        Yes      6.0   NaN   NaN  17.0   23.0
# All            19.0  87.0  76.0  62.0  244.0

# 如果存在空的组合（也就是NA），你可能会希望设置一个fill_value：
# tips.pivot_table('tip_pct' , index=['time', 'size','smoker'],
#                  columns='day' , aggfunc='mean' , fill_value=0)
# Out[169]:
# day                      Fri       Sat       Sun      Thur
# time   size smoker
# Dinner 1    No      0.000000  0.137931  0.000000  0.000000
#             Yes     0.000000  0.325733  0.000000  0.000000
#        2    No      0.139622  0.162705  0.168859  0.159744
#             Yes     0.171297  0.148668  0.207893  0.000000
#        3    No      0.000000  0.154661  0.152663  0.000000
#             Yes     0.000000  0.144995  0.152660  0.000000
#        4    No      0.000000  0.150096  0.148143  0.000000
#             Yes     0.117750  0.124515  0.193370  0.000000
#        5    No      0.000000  0.000000  0.206928  0.000000
#             Yes     0.000000  0.106572  0.065660  0.000000
#        6    No      0.000000  0.000000  0.103799  0.000000
# Lunch  1    No      0.000000  0.000000  0.000000  0.181728
#             Yes     0.223776  0.000000  0.000000  0.000000
#        2    No      0.000000  0.000000  0.000000  0.166005
#             Yes     0.181969  0.000000  0.000000  0.158843
#        3    No      0.187735  0.000000  0.000000  0.084246
#             Yes     0.000000  0.000000  0.000000  0.204952
#        4    No      0.000000  0.000000  0.000000  0.138919
#             Yes     0.000000  0.000000  0.000000  0.155410
#        5    No      0.000000  0.000000  0.000000  0.121389
#        6    No      0.000000  0.000000  0.000000  0.173706


## 10.4.1 交叉表：crosstab

# 交叉表（cross-tabulation，简称crosstab）是一种用于计算分组频率的特殊透视表。

# data = pd.DataFrame({'Sample':[1,2,3,4,5,6,7,8,9,10],
#                      'Nationality':['USA','Japan','USA','Japan','Japan','Japan','USA','USA','Japan','USA'],
#                      'Handedness':['Right-handed','Left-handed','Right-handed','Right-handed','Left-handed',
#                                    'Right-handed','Right-handed','Left-handed','Right-handed','Right-handed']})
#
# data
# Out[174]:
#    Sample Nationality    Handedness
# 0       1         USA  Right-handed
# 1       2       Japan   Left-handed
# 2       3         USA  Right-handed
# 3       4       Japan  Right-handed
# 4       5       Japan   Left-handed
# 5       6       Japan  Right-handed
# 6       7         USA  Right-handed
# 7       8         USA   Left-handed
# 8       9       Japan  Right-handed
# 9      10         USA  Right-handed

# 根据国籍和用手习惯对这段数据进行统计汇总
# pd.crosstab(data.Nationality , data.Handedness , margins=True)
# Out[175]:
# Handedness   Left-handed  Right-handed  All
# Nationality
# Japan                  2             3    5
# USA                    1             4    5
# All                    3             7   10

# crosstab的前两个参数可以是数组或Series，或是数组列表。就像小费数据：
# pd.crosstab([tips.time , tips.day] , tips.smoker , margins=True)
# Out[176]:
# smoker        No  Yes  All
# time   day
# Dinner Fri     3    9   12
#        Sat    45   42   87
#        Sun    57   19   76
#        Thur    1    0    1
# Lunch  Fri     1    6    7
#        Thur   44   17   61
# All          151   93  244







