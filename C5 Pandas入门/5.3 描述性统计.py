"""
    时间：2019/10/2
    作者：大发
    内容：第五章笔记
"""

# import pandas as pd
# from pandas import Series,DataFrame
# import numpy as np
# df = pd.DataFrame([[1.4 , np.nan] , [7.1 , -4.5] , [np.nan , np.nan] , [0.75 , -1.3]] , index = ['a' , 'b' , 'c' , 'd'] , columns = ['one' , 'two'])
# df
# Out[4]:
#     one  two
# a  1.40  NaN
# b  7.10 -4.5
# c   NaN  NaN
# d  0.75 -1.3
# df.sum()           # 没有指定的话，就是加行
# Out[5]:
# one    9.25
# two   -5.80
# dtype: float64
# df.sum(axis = 'columns')        # 指定加列
# Out[6]:
# a    1.40
# b    2.60
# c    0.00
# d   -0.55
# dtype: float64

# df.sum(axis = 'columns' , skipna = False)    # 指定加列，指定不排除nan值
# Out[8]:
# a     NaN
# b    2.60
# c     NaN
# d   -0.55
# dtype: float64

# df
# Out[9]:
#     one  two
# a  1.40  NaN
# b  7.10 -4.5
# c   NaN  NaN
# d  0.75 -1.3
# df.idxmax()           # 间接的搜索，给出索引值
# Out[10]:
# one    b
# two    d
# dtype: object
# df.idxmin()
# Out[11]:
# one    d
# two    b
# dtype: object
# df.cumsum()          # 累计计算
# Out[12]:
#     one  two
# a  1.40  NaN
# b  8.50 -4.5
# c   NaN  NaN
# d  9.25 -5.8
# df.describe()                # 描述统计
# Out[13]:
#             one       two
# count  3.000000  2.000000
# mean   3.083333 -2.900000
# std    3.493685  2.262742
# min    0.750000 -4.500000
# 25%    1.075000 -3.700000
# 50%    1.400000 -2.900000
# 75%    4.250000 -2.100000
# max    7.100000 -1.300000
# obj = pd.Series(['a' , 'a' , 'b' , 'c'] * 4)    # 非数值的描述统计
# obj.describe()
# Out[15]:
# count     16
# unique     3
# top        a
# freq       8
# dtype: object


# import pandas_datareader.data as web

## .corr 给出相关性
## .cor  给出协方差
## .corrwith 给出一个dataframe与另一个的相关性

## 5.3.2 唯一值、计数和成员属性

# obj = pd.Series(['c' , 'a' , 'd' , 'a' , 'a' , 'b' , 'b' , 'c' , 'c'])
# uniques = obj.unique()                 # 给出唯一值
# uniques
# Out[19]: array(['c', 'a', 'd', 'b'], dtype=object)
# obj.value_counts()                   #  计数
# Out[20]:
# a    3
# c    3
# b    2
# d    1
# dtype: int64
# pd.value_counts(obj.values , sort = False)  # 计数加排序
# Out[21]:
# c    3
# b    2
# d    1
# a    3
# dtype: int64
# obj
# Out[22]:
# 0    c
# 1    a
# 2    d
# 3    a
# 4    a
# 5    b
# 6    b
# 7    c
# 8    c
# dtype: object
# mask = obj.isin(['b' , 'c'])     # 取数，布尔值
# mask
# Out[24]:
# 0     True
# 1    False
# 2    False
# 3    False
# 4    False
# 5     True
# 6     True
# 7     True
# 8     True
# dtype: bool
# obj[mask]
# Out[25]:
# 0    c
# 5    b
# 6    b
# 7    c
# 8    c
# dtype: object
# to_match = pd.Series(['c','a' , 'b' , 'b' ,'c' ,'a'])
# unique_val = pd.Series(['c' , 'b' , 'a'])
# pd.Index(unique_val).get_indexer(to_match)
# Out[28]: array([0, 2, 1, 1, 0, 2], dtype=int32)   # 转换成一个数组

# data = pd.DataFrame({'Qu1':[1,3,4,3,4],
#                      'Qu2':[2,3,1,2,3],
#                      'Qu3':[1,5,2,4,4]})
# data
# Out[29]:
#    Qu1  Qu2  Qu3
# 0    1    2    1
# 1    3    3    5
# 2    4    1    2
# 3    3    2    4
# 4    4    3    4
# result = data.apply(pd.value_counts).fillna(0)     # 计数，每个数字在每一列中出现的次数
# result
# Out[31]:
#    Qu1  Qu2  Qu3
# 1  1.0  1.0  1.0
# 2  0.0  2.0  1.0
# 3  2.0  2.0  0.0
# 4  2.0  0.0  2.0
# 5  0.0  0.0  1.0
























