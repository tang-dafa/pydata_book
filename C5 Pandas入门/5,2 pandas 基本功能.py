"""
    时间：2019/9/30
    作者：大发
    内容：第五章笔记
"""

# import pandas as pd
# from pandas import Series,DataFrame
# import numpy as np
# obj = pd.Series([4.5 , 7.2 , -5.3 , 3.6] , index = ['d' , 'b' , 'a' , 'c'])
# obj
# Out[6]:
# d    4.5
# b    7.2
# a   -5.3
# c    3.6
# dtype: float64
# obj2 = obj.reindex(['a' , 'b' , 'c' , 'd' , 'e'])  ## 按新索引排列
# obj2
# Out[8]:
# a   -5.3
# b    7.2
# c    3.6
# d    4.5
# e    NaN
# dtype: float64
# obj3 = pd.Series(['blue' , 'purple' , 'yellow'] , index = [0 , 2 , 4])
# obj3
# Out[10]:
# 0      blue
# 2    purple
# 4    yellow
# dtype: object
# obj3.reindex(range(6) , method = 'ffill')   ## ffill，插值，向前填充，bfill是向后填充
# Out[11]:
# 0      blue
# 1      blue
# 2    purple
# 3    purple
# 4    yellow
# 5    yellow
# dtype: object

# frame = pd.DataFrame(np.arange(9).reshape((3,3)), index = ['a' , 'c' , 'd'] , columns = ['Ohio' , 'Texas' , 'California'])
# frame
# Out[15]:
#    Ohio  Texas  California
# a     0      1           2
# c     3      4           5
# d     6      7           8

# frame2 = frame.reindex(['a' , 'b' , 'c' , 'd'])    # 重建行标签
# frame2
# Out[17]:
#    Ohio  Texas  California
# a   0.0    1.0         2.0
# b   NaN    NaN         NaN
# c   3.0    4.0         5.0
# d   6.0    7.0         8.0
# states = ['Texas' , 'Utah' , 'California']    # 重建列标签
# frame.reindex(columns = states)
# Out[19]:
#    Texas  Utah  California
# a      1   NaN           2
# c      4   NaN           5
# d      7   NaN           8

# frame.loc[['a' , 'b' , 'c' , 'd'] , states]     # 简便用法，但有危险
# C:\ProgramData\Anaconda3\lib\site-packages\pandas\core\indexing.py:1494: FutureWarning:
# Passing list-likes to .loc or [] with any missing label will raise
# KeyError in the future, you can use .reindex() as an alternative.
# See the documentation here:
# https://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike
#   return self._getitem_tuple(key)
# Out[20]:
#    Texas  Utah  California
# a    1.0   NaN         2.0
# b    NaN   NaN         NaN
# c    4.0   NaN         5.0
# d    7.0   NaN         8.0

# obj = pd.Series(np.arange(5.) , index = ['a' , 'b' , 'c' , 'd' , 'e'])
# obj
# Out[22]:
# a    0.0
# b    1.0
# c    2.0
# d    3.0
# e    4.0
# dtype: float64
# new_obj = obj.drop('c')   # 单删一行
# new_obj
# Out[24]:
# a    0.0
# b    1.0
# d    3.0
# e    4.0
# dtype: float64
# obj.drop(['d' , 'c'])   # 删两行
# Out[25]:
# a    0.0
# b    1.0
# e    4.0
# dtype: float64
# data = pd.DataFrame(np.arange(16).reshape((4,4)),index = ['Ohio' , 'Colarado' , 'Utah' , 'NewYork'], columns = ['one' , 'two' , 'three' , 'four'])
# data
# Out[27]:
#           one  two  three  four
# Ohio        0    1      2     3
# Colarado    4    5      6     7
# Utah        8    9     10    11
# NewYork    12   13     14    15
#
#
# data.drop(['Colarado' , 'Ohio'])            # 二维中删行
# Out[29]:
#          one  two  three  four
# Utah       8    9     10    11
# NewYork   12   13     14    15
# data.drop('two' , axis = 1)              ## 二维删列
# Out[30]:
#           one  three  four
# Ohio        0      2     3
# Colarado    4      6     7
# Utah        8     10    11
# NewYork    12     14    15
# data.drop(['two' , 'four'], axis = 'columns')
# Out[31]:
#           one  three
# Ohio        0      2
# Colarado    4      6
# Utah        8     10
# NewYork    12     14
# obj
# Out[32]:
# a    0.0
# b    1.0
# c    2.0
# d    3.0
# e    4.0
# dtype: float64
# obj.drop('c' , inplace = True)    ## 这个方法直接把原始数据也改了
# obj
# Out[34]:
# a    0.0
# b    1.0
# d    3.0
# e    4.0
# dtype: float64

# data
# Out[35]:
#           one  two  three  four
# Ohio        0    1      2     3
# Colarado    4    5      6     7
# Utah        8    9     10    11
# NewYork    12   13     14    15
# data.loc['Colarado' , ['two' , 'three']]
# Out[36]:
# two      5
# three    6
# Name: Colarado, dtype: int32
# data.iloc[2 ,[3,0,1]]
# Out[37]:
# four    11
# one      8
# two      9
# Name: Utah, dtype: int32
# data.iloc[2]
# Out[38]:
# one       8
# two       9
# three    10
# four     11
# Name: Utah, dtype: int32
# data.iloc[[1,2],[3,0,1]]     # 先行后列
# Out[39]:
#           four  one  two
# Colarado     7    4    5
# Utah        11    8    9

## 可以切片
# data.loc[:'Utah' , 'two']
# Out[40]:
# Ohio        1
# Colarado    5
# Utah        9
# Name: two, dtype: int32
# data.iloc[: , :3][data.three > 5]
# Out[41]:
#           one  two  three
# Colarado    4    5      6
# Utah        8    9     10
# NewYork    12   13     14
# data.iloc[: , :3][data.three > 7]
# Out[42]:
#          one  two  three
# Utah       8    9     10
# NewYork   12   13     14


##  5.2.4 整数索引

# ser = pd.Series(np.arange(3.))
# ser
# Out[4]:
# 0    0.0
# 1    1.0
# 2    2.0
# dtype: float64
# ser2 = pd.Series(np.arange(3.) , index = ['a' , 'b' , 'c'])
# ser2[-1]
# Out[6]: 2.0
# ser[:1]
# Out[7]:
# 0    0.0
# dtype: float64
# ser.loc[:1]                 # 用于标签
# Out[8]:
# 0    0.0
# 1    1.0
# dtype: float64
# ser.iloc[:1]             # 用 iloc[]索引，用于整数
# Out[9]:
# 0    0.0
# dtype: float64

##  算数和数据对齐
# s1 = pd.Series([7.3 , -2.5 , 3.4 , 1.5 ] , index = ['a' , 'c' , 'd' , 'e'])
# s2 = pd.Series([-2.1 , 3.6 , -1.5 , 4 , 3.1], index = ['a' , 'c' , 'e' , 'f' , 'g'])
# s1
# Out[12]:
# a    7.3
# c   -2.5
# d    3.4
# e    1.5
# dtype: float64
# s2
# Out[13]:
# a   -2.1
# c    3.6
# e   -1.5
# f    4.0
# g    3.1
# dtype: float64
# s1 + s2
# Out[14]:
# a    5.2
# c    1.1
# d    NaN           # 在Series中，没有对齐的部分显示缺失值
# e    0.0
# f    NaN
# g    NaN
# dtype: float64

# df1 = pd.DataFrame(np.arange(9.).reshape((3,3)) , columns = list('bcd') , index = ['Ohio' , 'Texas' , 'Colorado'])
# df2 = pd.DataFrame(np.arange(12.).reshape((4,3)) , columns = list('bde') , index = ['Utah' , 'Ohio' , 'Texas' , 'Oregon'])
# df1
# Out[17]:
#             b    c    d
# Ohio      0.0  1.0  2.0
# Texas     3.0  4.0  5.0
# Colorado  6.0  7.0  8.0
# df2
# Out[18]:
#           b     d     e
# Utah    0.0   1.0   2.0
# Ohio    3.0   4.0   5.0
# Texas   6.0   7.0   8.0
# Oregon  9.0  10.0  11.0
# df1 + df2
# Out[19]:
#             b   c     d   e
# Colorado  NaN NaN   NaN NaN        #二维数组也能对齐，非共有的列和行也显示缺失值
# Ohio      3.0 NaN   6.0 NaN
# Oregon    NaN NaN   NaN NaN
# Texas     9.0 NaN  12.0 NaN
# Utah      NaN NaN   NaN NaN

# df1 = pd.DataFrame(np.arange(12.).reshape((3,4)) , columns = list('abcd'))
# df2 = pd.DataFrame(np.arange(20.).reshape((4,5)) , columns = list('abcde'))
# df2.loc[1 ,'b'] =np.nan
# df1
# Out[23]:
#      a    b     c     d
# 0  0.0  1.0   2.0   3.0
# 1  4.0  5.0   6.0   7.0
# 2  8.0  9.0  10.0  11.0
# df2
# Out[24]:
#       a     b     c     d     e
# 0   0.0   1.0   2.0   3.0   4.0
# 1   5.0   NaN   7.0   8.0   9.0
# 2  10.0  11.0  12.0  13.0  14.0
# 3  15.0  16.0  17.0  18.0  19.0
# df1 + df2
# Out[25]:
#       a     b     c     d   e
# 0   0.0   2.0   4.0   6.0 NaN
# 1   9.0   NaN  13.0  15.0 NaN
# 2  18.0  20.0  22.0  24.0 NaN
# 3   NaN   NaN   NaN   NaN NaN        # 非共有的行和列都是缺失值
# df1.add(df2 , fill_value=0)                 # 这个方法把不重叠的位置都放了0
# Out[26]:
#       a     b     c     d     e
# 0   0.0   2.0   4.0   6.0   4.0
# 1   9.0   5.0  13.0  15.0   9.0
# 2  18.0  20.0  22.0  24.0  14.0
# 3  15.0  16.0  17.0  18.0  19.0
# 1 / df1                                    # 和下边的df1.rdiv(1) 一致，方法前加r是反转了参数
# Out[27]:
#        a         b         c         d
# 0    inf  1.000000  0.500000  0.333333
# 1  0.250  0.200000  0.166667  0.142857
# 2  0.125  0.111111  0.100000  0.090909
# df1.rdiv(1)
# Out[28]:
#        a         b         c         d
# 0    inf  1.000000  0.500000  0.333333
# 1  0.250  0.200000  0.166667  0.142857
# 2  0.125  0.111111  0.100000  0.090909

##  Dataframe 和series的操作
# arr = np.arange(12.).reshape((3,4))
# arr
# Out[30]:
# array([[ 0.,  1.,  2.,  3.],
#        [ 4.,  5.,  6.,  7.],
#        [ 8.,  9., 10., 11.]])
# arr[0]
# Out[31]: array([0., 1., 2., 3.])
# arr - arr[0]                   # 这个是他的广播机制
# Out[32]:
# array([[0., 0., 0., 0.],
#        [4., 4., 4., 4.],
#        [8., 8., 8., 8.]])
# frame = pd.DataFrame(np.arange(12.).reshape((4,3)), columns = list('bde') , index = ['Utah' , 'Ohio' , 'Texas' , 'Oregon'])
# series = frame.iloc[0]    # iloc 取行
# frame
# Out[35]:
#           b     d     e
# Utah    0.0   1.0   2.0
# Ohio    3.0   4.0   5.0
# Texas   6.0   7.0   8.0
# Oregon  9.0  10.0  11.0
# series
# Out[36]:
# b    0.0
# d    1.0
# e    2.0
# Name: Utah, dtype: float64

# frame - series                # 广播机制
# Out[37]:
#           b    d    e
# Utah    0.0  0.0  0.0
# Ohio    3.0  3.0  3.0
# Texas   6.0  6.0  6.0
# Oregon  9.0  9.0  9.0

# series2 = pd.Series(range(3) , index = ['b','e', 'f'])  # 如果索引值既不在Dataframe中，也不在series中，会重建索引
# series2
# Out[39]:
# b    0
# e    1
# f    2
# dtype: int64
# frame + series2
# Out[40]:
#           b   d     e   f
# Utah    0.0 NaN   3.0 NaN
# Ohio    3.0 NaN   6.0 NaN
# Texas   6.0 NaN   9.0 NaN
# Oregon  9.0 NaN  12.0 NaN

# series3 = frame['d']
# frame
# Out[42]:
#           b     d     e
# Utah    0.0   1.0   2.0
# Ohio    3.0   4.0   5.0
# Texas   6.0   7.0   8.0
# Oregon  9.0  10.0  11.0
# series3
# Out[43]:
# Utah       1.0
# Ohio       4.0
# Texas      7.0
# Oregon    10.0
# Name: d, dtype: float64
# frame.sub(series3 , axis = 'index')   # axis 用来匹配行
# Out[44]:
#           b    d    e
# Utah   -1.0  0.0  1.0
# Ohio   -1.0  0.0  1.0
# Texas  -1.0  0.0  1.0
# Oregon -1.0  0.0  1.0

# frame = pd.DataFrame(np.random.randn(4,3), columns = list('bde') , index = ['Utah' , 'Ohio' , 'Texas' , 'Oregon'])
# frame
# Out[48]:
#                b         d         e
# Utah   -0.422477 -0.337089  0.327457
# Ohio    0.264294  0.544734  0.197702
# Texas  -0.246607  0.274619  0.137753
# Oregon -0.152574 -0.518362 -0.374587
# np.abs(frame)                            # .abs 取绝对值
# Out[49]:
#                b         d         e
# Utah    0.422477  0.337089  0.327457
# Ohio    0.264294  0.544734  0.197702
# Texas   0.246607  0.274619  0.137753
# Oregon  0.152574  0.518362  0.374587
# f = lambda x:x.max() - x.min()       #  公式
# frame.apply(f)           对每一列用f公式
# Out[51]:
# b    0.686771
# d    1.063096
# e    0.702044
# dtype: float64

# frame.apply(f , axis = 'columns')   # 对每一行用 f 公式
# Out[52]:
# Utah      0.749934
# Ohio      0.347032
# Texas     0.521225
# Oregon    0.365789
# dtype: float64

# def f(x):
#     return pd.Series([x.min() , x.max()] , index = ['min' , 'max'])
# frame.apply(f)
# Out[53]:
#             b         d         e
# min -0.422477 -0.518362 -0.374587
# max  0.264294  0.544734  0.327457
# format = lambda x : '%.2f' % x

# frame.applymap(format)        # 逐个的应用
# Out[55]:
#             b      d      e
# Utah    -0.42  -0.34   0.33
# Ohio     0.26   0.54   0.20
# Texas   -0.25   0.27   0.14
# Oregon  -0.15  -0.52  -0.37
# frame['e'].map(format)           # 单挑一列
# Out[56]:
# Utah       0.33
# Ohio       0.20
# Texas      0.14
# Oregon    -0.37
# Name: e, dtype: object

##  5.2.7 排序和命名

# obj = pd.Series(range(4) , index = ['d' , 'a' , 'b' , 'c'])
# obj
# Out[58]:
# d    0
# a    1
# b    2
# c    3
# dtype: int64
# obj.sort_index()             # .sort_index() 按索引排序
# Out[59]:
# a    1
# b    2
# c    3
# d    0
# dtype: int64

# frame = pd.DataFrame(np.arange(8).reshape((2,4)) , index = ['three' , 'one'] , columns =['d' , 'a' , 'b' , 'c'])
# frame.sort_index()         # 按 行 索引
# Out[61]:
#        d  a  b  c
# one    4  5  6  7
# three  0  1  2  3
# frame.sort_index(axis=1)   # 按 列 索引
# Out[62]:
#        a  b  c  d
# three  1  2  3  0
# one    5  6  7  4
# frame.sort_index(axis = 1 , ascending = False)    # 倒序
# Out[63]:
#        d  c  b  a
# three  0  3  2  1
# one    4  7  6  5

# obj = pd.Series([4, 7, -3, 2])
# obj.sort_values()                   # 按值 排序
# Out[65]:
# 2   -3
# 3    2
# 0    4
# 1    7
# dtype: int64
# obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
# obj.sort_values()                # 缺失值放最后
# Out[67]:
# 4   -3.0
# 5    2.0
# 0    4.0
# 2    7.0
# 1    NaN
# 3    NaN
# dtype: float64

# frame = pd.DataFrame({'b':[4,7,-3,2], 'a':[0,1,0,1]})
# frame
# Out[69]:
#    b  a
# 0  4  0
# 1  7  1
# 2 -3  0
# 3  2  1
# frame.sort_values(by='b')   # 按b排
# Out[70]:
#    b  a
# 2 -3  0
# 3  2  1
# 0  4  0
# 1  7  1
# frame.sort_values(by =['a', 'b'])   ## 多列排序
# Out[71]:
#    b  a
# 2 -3  0
# 0  4  0
# 3  2  1
# 1  7  1

# obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
# obj.rank()        # 平均排名
# Out[73]:
# 0    6.5
# 1    1.0
# 2    6.5
# 3    4.5
# 4    3.0
# 5    2.0
# 6    4.5
# dtype: float64
# obj.rank(method = 'first')  #  根据数据的观察顺序决定同名次的分配
# Out[74]:
# 0    6.0
# 1    1.0
# 2    7.0
# 3    4.0
# 4    3.0
# 5    2.0
# 6    5.0
# dtype: float64

# obj.rank(ascending = False , method = 'max')   # ascending = False 倒序，method = 'max'，同名次的话取名次最靠前的
# Out[75]:
# 0    2.0
# 1    7.0
# 2    2.0
# 3    4.0
# 4    5.0
# 5    6.0
# 6    4.0
# dtype: float64


# frame = pd.DataFrame({'b':[4.3 , 7, -3, 2] , 'a':[0,1,0,1] , 'c':[-2, 5, 8, -2.5]})
# frame
# Out[85]:
#      b  a    c
# 0  4.3  0 -2.0
# 1  7.0  1  5.0
# 2 -3.0  0  8.0
# 3  2.0  1 -2.5
# frame.rank(axis = 'columns')           # 对列排名
# Out[86]:
#      b    a    c
# 0  3.0  2.0  1.0
# 1  3.0  1.0  2.0
# 2  1.0  2.0  3.0
# 3  3.0  2.0  1.0


##  重复索引
# obj = pd.Series(range(5) , index = ['a' , 'a' , 'b' , 'b' , 'c'])
# obj
# Out[88]:
# a    0
# a    1
# b    2
# b    3
# c    4
# dtype: int64
# obj.index.is_unique
# Out[89]: False
# obj['a']
# Out[90]:
# a    0
# a    1
# dtype: int64
# df = pd.DataFrame(np.random.randn(4,3) , index = ['a' , 'a' , 'b' , 'b' ] )
# df
# Out[92]:
#           0         1         2
# a -1.189869  0.052172 -0.839549
# a -2.169752  0.011503 -0.002262
# b  0.436047  2.048463  0.040828
# b -1.740024  1.211339 -0.011339
# df.loc['b']
# Out[93]:
#           0         1         2
# b  0.436047  2.048463  0.040828
# b -1.740024  1.211339 -0.011339





































