"""

    作者：大发
    日期：2019/11/15
    内容：利用python进行数据分析 8.1 p216 笔记

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

# 8.1 分层索引 pandas

# data = pd.Series(np.random.randn(9) , index = [['a','a','a','b','b','c','c','d','d'] , [1,2,3,1,3,1,2,2,3]])
# data
# Out[34]:
# a  1    0.086525
#    2    0.635653
#    3    0.854132
# b  1   -0.711350
#    3    1.377424
# c  1   -1.204218
#    2    1.854289
# d  2    1.678305
#    3    1.158985
# dtype: float64

# data.index
# Out[35]:
# MultiIndex(levels=[['a', 'b', 'c', 'd'], [1, 2, 3]],
#            codes=[[0, 0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 2, 0, 2, 0, 1, 1, 2]])

# data['b']     # 部分索引
# Out[36]:
# 1   -0.711350
# 3    1.377424
# dtype: float64

# data['b':'c']
# Out[37]:
# b  1   -0.711350
#    3    1.377424
# c  1   -1.204218
#    2    1.854289
# dtype: float64

# data.loc[['b' , 'd']]
# Out[38]:
# b  1   -0.711350
#    3    1.377424
# d  2    1.678305
#    3    1.158985
# dtype: float64


# data.loc[: , 2]        # 在内部层级中选择
# Out[39]:
# a    0.635653
# c    1.854289
# d    1.678305
# dtype: float64


# data.unstack()              # 改变排列方式
# Out[40]:
#           1         2         3
# a  0.086525  0.635653  0.854132
# b -0.711350       NaN  1.377424
# c -1.204218  1.854289       NaN
# d       NaN  1.678305  1.158985

#
# data.unstack().stack()
# Out[41]:
# a  1    0.086525
#    2    0.635653
#    3    0.854132
# b  1   -0.711350
#    3    1.377424
# c  1   -1.204218
#    2    1.854289
# d  2    1.678305
#    3    1.158985
# dtype: float64


# frame = pd.DataFrame(np.arange(12).reshape((4,3)),
#                      index=[['a' , 'a', 'b' , 'b'] , [1,2,1,2]],
#                      columns=[['Ohio' , 'Ohio' , 'Colorado'] ,
#                               ['Green' , 'Red' , 'Green']])
#
# frame
# Out[43]:
#      Ohio     Colorado
#     Green Red    Green
# a 1     0   1        2
#   2     3   4        5
# b 1     6   7        8
#   2     9  10       11

#
# frame.index.names = ['key1' , 'key2']              # 层级命名
# frame.columns.names = ['state' , 'color']
# frame
# Out[46]:
# state      Ohio     Colorado
# color     Green Red    Green
# key1 key2
# a    1        0   1        2
#      2        3   4        5
# b    1        6   7        8
#      2        9  10       11

# frame['Ohio']            # 部分索引可以从中取出组
# Out[47]:
# color      Green  Red
# key1 key2
# a    1         0    1
#      2         3    4
# b    1         6    7
#      2         9   10

# MultiIndex.from_arrays([['Ohio' , 'Ohio' , 'Colorado'] ,['Green' , 'Red' , 'Green']] ,
#                        names = ['state' , 'color'])                             # 另一个层级命名的方法


# CSDN MultiIndex内容补充

##  from_tuples接受的是行参数
# arrays = [['bar' , 'bar' , 'baz' , 'baz' , 'foo' , 'foo' , 'qux' , 'qux' ] ,
#           ['one' , 'two' , 'one' , 'two' , 'one' , 'two' , 'one' , 'two' ]]
# tuples = list(zip(*arrays))
# print(tuples)
# [('bar', 'one'), ('bar', 'two'), ('baz', 'one'), ('baz', 'two'), ('foo', 'one'), ('foo', 'two'), ('qux', 'one'), ('qux', 'two')]
# index = pd.MultiIndex.from_tuples(tuples , names = ['first' , 'second'])
# print(index)
# MultiIndex(levels=[['bar', 'baz', 'foo', 'qux'], ['one', 'two']],
#            codes=[[0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 0, 1, 0, 1, 0, 1]],
#            names=['first', 'second'])


#  from_arrays 用的是列参数
# rays =[['bar' , 'bar' , 'baz' , 'baz' , 'foo' , 'foo' , 'qux' , 'qux' ] ,
#           ['one' , 'two' , 'one' , 'two' , 'one' , 'two' , 'one' , 'two' ]]
# index =  pd.MultiIndex.from_arrays(rays)
#
# s = pd.Series(np.random.randn(8) , index = index)
# print(s)
# bar  one    1.226214
#      two   -0.212676
# baz  one    0.623232
#      two   -1.038306
# foo  one    0.298606
#      two    1.244629
# qux  one    0.225832
#      two   -1.490807
# dtype: float64


# arrays = [['bar' , 'bar' , 'baz' , 'baz' , 'foo' , 'foo' , 'qux' , 'qux' ] ,
#           ['one' , 'two' , 'one' , 'two' , 'one' , 'two' , 'one' , 'two' ]]
# s = pd.Series(np.random.randn(8) , index = arrays)             # 简便一点的方法就这么写了
# print(s)
# bar  one    1.975517
#      two    2.592364
# baz  one    0.944408
#      two    0.687803
# foo  one    0.741554
#      two   -1.776272
# qux  one   -0.923540
#      two    0.053036
# dtype: float64

# lists = [['bar' , 'baz' , 'foo' , 'qux'] , ['one' , 'two']]
# index = pd.MultiIndex.from_product(lists , names = ['first' , 'second'])
# s = pd.Series(np.random.randn(len(index)) , index = index)
# s
# Out[77]:
# first  second
# bar    one       0.521267
#        two      -1.479631
# baz    one      -0.252994
#        two       0.438816
# foo    one      -0.427805
#        two      -1.314504
# qux    one      -0.393890
#        two      -0.034324
# dtype: float64
# print(s.index.names)
# ['first', 'second']
# s.index.names = ['first level' , 'second level']
# print(s.index.names)
# ['first level', 'second level']
#
# df = pd.DataFrame(np.random.randn(3,8) , index = ['A' , 'B' , 'C'] , columns = index)
# print(df)
# first level        bar                 baz  ...       foo       qux
# second level       one       two       one  ...       two       one       two
# A             0.326439 -0.397437  0.825262  ... -0.845274  0.670085 -0.706082
# B             1.503496  0.448118  1.356014  ...  0.505521 -0.663821  1.025939
# C             0.332731  1.124880  1.351024  ...  0.111717  0.233027 -0.000402
# [3 rows x 8 columns]


# 8.1.1 重排序和层级排序

# frame.swaplevel('key1' , 'key2')        # 把层级变换了
# Out[90]:
# state      Ohio     Colorado
# color     Green Red    Green
# key2 key1
# 1    a        0   1        2
# 2    a        3   4        5
# 1    b        6   7        8
# 2    b        9  10       11


# frame.sort_index(level=1)            # 使用.sort_index在单一层级上对数据排序
# Out[91]:
# state      Ohio     Colorado
# color     Green Red    Green
# key1 key2
# a    1        0   1        2
# b    1        6   7        8
# a    2        3   4        5
# b    2        9  10       11



# frame.swaplevel(0,1).sort_index(level = 0)
# Out[92]:
# state      Ohio     Colorado
# color     Green Red    Green
# key2 key1
# 1    a        0   1        2
#      b        6   7        8
# 2    a        3   4        5
#      b        9  10       11


# 8.1.2 按照层级进行汇总统计
# frame.sum(level = 'key2')       # 按指定聚合
# Out[93]:
# state  Ohio     Colorado
# color Green Red    Green
# key2
# 1         6   8       10
# 2        12  14       16
# frame.sum(level = 'color' , axis = 1)
# Out[94]:
# color      Green  Red
# key1 key2
# a    1         2    1
#      2         8    4
# b    1        14    7
#      2        20   10



# 8.1.3 使用DataFrame的列进行索引

# frame = pd.DataFrame({'a':range(7) , 'b':range(7 , 0 , -1) ,
#                       'c':['one' , 'one' , 'one' , 'two' ,'two' , 'two' , 'two'] ,
#                       'd' : [0,1,2,0,1,2,3]})
# frame
# Out[96]:
#    a  b    c  d
# 0  0  7  one  0
# 1  1  6  one  1
# 2  2  5  one  2
# 3  3  4  two  0
# 4  4  3  two  1
# 5  5  2  two  2
# 6  6  1  two  3
# frame2 = frame.set_index(['c' , 'd'])    # .set_index 会生成一个新的DataFrame，使用多个列做索引 ， 默认把这些做索引的列删除了
# frame2
# Out[98]:
#        a  b
# c   d
# one 0  0  7
#     1  1  6
#     2  2  5
# two 0  3  4
#     1  4  3
#     2  5  2
#     3  6  1
#
# frame.set_index(['c' , 'd'] , drop = False)     # drop = False 参数设置后，不删除设为索引的列
# Out[99]:
#        a  b    c  d
# c   d
# one 0  0  7  one  0
#     1  1  6  one  1
#     2  2  5  one  2
# two 0  3  4  two  0
#     1  4  3  two  1
#     2  5  2  two  2
#     3  6  1  two  3
#
# frame2.reset_index()  # .reset_index()反操作
# Out[100]:
#      c  d  a  b
# 0  one  0  0  7
# 1  one  1  1  6
# 2  one  2  2  5
# 3  two  0  3  4
# 4  two  1  4  3
# 5  two  2  5  2
# 6  two  3  6  1



## 8.2 联合与合并数据集

# pandas.merge # 链接行，数据库的链接
# pandas.connect # 允许在轴向上进行粘合或“堆叠”
# combine_first #把重叠的对象拼接在一起

# 8.2.1 数据库风格的DataFrame连接

# df1 = pd.DataFrame({'key':['b' , 'b' , 'a' , 'c' , 'a' , 'a' , 'b'] , 'data1':range(7)})
# df2 = pd.DataFrame({'key':['a' , 'b' , 'd'] , 'data2':range(3)})
# df1
# Out[102]:
#   key  data1
# 0   b      0
# 1   b      1
# 2   a      2
# 3   c      3
# 4   a      4
# 5   a      5
# 6   b      6
# df2
# Out[103]:
#   key  data2
# 0   a      0
# 1   b      1
# 2   d      2
# pd.merge(df1,df2)
# Out[104]:
#   key  data1  data2
# 0   b      0      1
# 1   b      1      1
# 2   b      6      1
# 3   a      2      0
# 4   a      4      0
# 5   a      5      0
# pd.merge(df1 ,df2,on='key')     # 显式的指定连接键
# Out[105]:
#   key  data1  data2
# 0   b      0      1
# 1   b      1      1
# 2   b      6      1
# 3   a      2      0
# 4   a      4      0
# 5   a      5      0
# df3 = pd.DataFrame({'lkey':['b' , 'b' , 'a' , 'c' , 'a' , 'a' , 'b'] , 'data1' :range(7)})
# df4 = pd.DataFrame({'rkey':['a' , 'b' , 'd'] , 'data2': range(3)})
# pd.merge(df3 , df4 , left_on = 'lkey' , right_on = 'rkey')      # 分别指定列名
# Out[109]:
#   lkey  data1 rkey  data2
# 0    b      0    b      1
# 1    b      1    b      1
# 2    b      6    b      1
# 3    a      2    a      0
# 4    a      4    a      0
# 5    a      5    a      0
#
#  pd.merge(df1, df2 , how = 'outer')  # merge默认内连接，就是取交集 ， 引入how = 'outer',设置为外连接就可以去并集
# Out[110]:
#   key  data1  data2
# 0   b    0.0    1.0
# 1   b    1.0    1.0
# 2   b    6.0    1.0
# 3   a    2.0    0.0
# 4   a    4.0    0.0
# 5   a    5.0    0.0
# 6   c    3.0    NaN
# 7   d    NaN    2.0

# df1 = pd.DataFrame({'key':['b' , 'b' , 'a' , 'c' , 'a' , 'b'] , 'data1': range(6)})
# df2 = pd.DataFrame({'key':['a' , 'b' , 'a' , 'b' , 'd'] , 'data2':range(5)})
# df1
# Out[113]:
#   key  data1
# 0   b      0
# 1   b      1
# 2   a      2
# 3   c      3
# 4   a      4
# 5   b      5
# df2
# Out[114]:
#   key  data2
# 0   a      0
# 1   b      1
# 2   a      2
# 3   b      3
# 4   d      4
# pd.merge(df1 , df2 , on = 'key' , how = 'left')
# Out[115]:
#    key  data1  data2
# 0    b      0    1.0
# 1    b      0    3.0
# 2    b      1    1.0
# 3    b      1    3.0
# 4    a      2    0.0
# 5    a      2    2.0
# 6    c      3    NaN
# 7    a      4    0.0
# 8    a      4    2.0
# 9    b      5    1.0
# 10   b      5    3.0
# pd.merge(df1,df2,how='inner')
# Out[116]:
#   key  data1  data2
# 0   b      0      1
# 1   b      0      3
# 2   b      1      1
# 3   b      1      3
# 4   b      5      1
# 5   b      5      3
# 6   a      2      0
# 7   a      2      2
# 8   a      4      0
# 9   a      4      2
# left = pd.DataFrame({'key1':['foo' , 'foo' , 'bar'] , 'key2':['one' , 'two' , 'one'] , 'lval':[1,2,3]})
# right = pd.DataFrame({'key1':['foo' , 'foo' , 'bar' , 'bar'] , 'key2':['one','one', 'one' , 'two' ] , 'rval':[4,5,6,7]})
# pd.merge(left , right , on = ['key1' , 'key2'] , how = 'outer')
# Out[119]:
#   key1 key2  lval  rval
# 0  foo  one   1.0   4.0
# 1  foo  one   1.0   5.0
# 2  foo  two   2.0   NaN
# 3  bar  one   3.0   6.0
# 4  bar  two   NaN   7.0

# pd.merge(left , right , on = 'key1')
# Out[120]:
#   key1 key2_x  lval key2_y  rval
# 0  foo    one     1    one     4
# 1  foo    one     1    one     5
# 2  foo    two     2    one     4
# 3  foo    two     2    one     5
# 4  bar    one     3    one     6
# 5  bar    one     3    two     7
# pd.merge(left , right , on='key1' , suffixes = ('_left' , '_right'))    # suffixes = ('_left' , '_right')可以给重叠的列名指定后缀
# Out[121]:
#   key1 key2_left  lval key2_right  rval
# 0  foo       one     1        one     4
# 1  foo       one     1        one     5
# 2  foo       two     2        one     4
# 3  foo       two     2        one     5
# 4  bar       one     3        one     6
# 5  bar       one     3        two     7

# 8.2.2 根据索引合并

# left1 = pd.DataFrame({'key':['a' , 'b' , 'a' , 'a' , 'b' , 'c'],
#                       'value' : range(6)})
# right1 = pd.DataFrame({'group_val':[3.5 , 7]} , index=['a' ,'b'])
#
# left1 = pd.DataFrame({'key':['a' , 'b' , 'a' , 'a' , 'b' , 'c'],
#                       'value' : range(6)})
# right1 = pd.DataFrame({'group_val':[3.5 , 7]} , index=['a' ,'b'])
# left1
# Out[122]:
#   key  value
# 0   a      0
# 1   b      1
# 2   a      2
# 3   a      3
# 4   b      4
# 5   c      5
# right1
# Out[123]:
#    group_val
# a        3.5
# b        7.0
# pd.merge(left1 , right1 , left_on = 'key' , right_index = True)    # 使用索引作为合并的键，传入right_index = True或者left_index = True
# Out[124]:
#   key  value  group_val
# 0   a      0        3.5
# 2   a      2        3.5
# 3   a      3        3.5
# 1   b      1        7.0
# 4   b      4        7.0
# pd.merge(left1 , right1 , left_on = 'key' , right_index = True , how = 'outer')
# Out[125]:
#   key  value  group_val
# 0   a      0        3.5
# 2   a      2        3.5
# 3   a      3        3.5
# 1   b      1        7.0
# 4   b      4        7.0
# 5   c      5        NaN

# 多层索引

# lefth = pd.DataFrame({'key1':['Ohio' , 'Ohio' , 'Ohio' , 'Nevada' , 'Nevad'] ,
#                       'key2':[2000 , 2001, 2002 , 2001, 2002] ,
#                       'data':np.arange(5.)})
# righth = pd.DataFrame(np.arange(12).reshape((6,2)) ,
#                       index=[['Nevada' , 'Nevada' , 'Ohio' , 'Ohio' , 'Ohio' , 'Ohio'] ,
#                              [2001 , 2000 , 2000 , 2000 , 2001 , 2002]],
#                       columns=['event1' , 'event2'])
# lefth
# Out[127]:
#      key1  key2  data
# 0    Ohio  2000   0.0
# 1    Ohio  2001   1.0
# 2    Ohio  2002   2.0
# 3  Nevada  2001   3.0
# 4   Nevad  2002   4.0
# righth
# Out[128]:
#              event1  event2
# Nevada 2001       0       1
#        2000       2       3
# Ohio   2000       4       5
#        2000       6       7
#        2001       8       9
#        2002      10      11

# pd.merge(lefth , righth , left_on = ['key1' , 'key2'] , right_index = True)
# Out[129]:
#      key1  key2  data  event1  event2
# 0    Ohio  2000   0.0       4       5
# 0    Ohio  2000   0.0       6       7
# 1    Ohio  2001   1.0       8       9
# 2    Ohio  2002   2.0      10      11
# 3  Nevada  2001   3.0       0       1

# pd.merge(lefth , righth , left_on = ['key1' , 'key2'] , right_index = True , how = 'outer')
# Out[130]:
#      key1  key2  data  event1  event2
# 0    Ohio  2000   0.0     4.0     5.0
# 0    Ohio  2000   0.0     6.0     7.0
# 1    Ohio  2001   1.0     8.0     9.0
# 2    Ohio  2002   2.0    10.0    11.0
# 3  Nevada  2001   3.0     0.0     1.0
# 4   Nevad  2002   4.0     NaN     NaN
# 4  Nevada  2000   NaN     2.0     3.0

# 两边都用索引

# left2 = pd.DataFrame([[1. ,2.] , [3. ,4.] , [5. ,6.]] ,
#                      index=['a' , 'c' , 'e'] ,
#                      columns=['Ohio' , 'Nevada'])
#
# right2 = pd.DataFrame([[7.,8.] , [9.,10.] , [11. ,12.] , [13. ,14.]],
#                       index=['b' , 'c' , 'd' , 'e'],
#                       columns=['Missouri' , 'Alabama'])
# left2
# Out[132]:
#    Ohio  Nevada
# a   1.0     2.0
# c   3.0     4.0
# e   5.0     6.0
# right2
# Out[133]:
#    Missouri  Alabama
# b       7.0      8.0
# c       9.0     10.0
# d      11.0     12.0
# e      13.0     14.0
# pd.merge(left2 , right2 , how='outer' , left_index =True , right_index = True)
# Out[134]:
#    Ohio  Nevada  Missouri  Alabama
# a   1.0     2.0       NaN      NaN
# b   NaN     NaN       7.0      8.0
# c   3.0     4.0       9.0     10.0
# d   NaN     NaN      11.0     12.0
# e   5.0     6.0      13.0     14.0
#
#
# left2.join(right2 , how='outer')        # .join的方法是相同的效果
# Out[135]:
#    Ohio  Nevada  Missouri  Alabama
# a   1.0     2.0       NaN      NaN
# b   NaN     NaN       7.0      8.0
# c   3.0     4.0       9.0     10.0
# d   NaN     NaN      11.0     12.0
# e   5.0     6.0      13.0     14.0

# left1.join(right1 , on='key')
# Out[136]:
#   key  value  group_val
# 0   a      0        3.5
# 1   b      1        7.0
# 2   a      2        3.5
# 3   a      3        3.5
# 4   b      4        7.0
# 5   c      5        NaN



# another = pd.DataFrame([[7. , 8.] , [9.,10.] , [11.,12.] , [16.,17.]] ,
#                        index=['a','c','e','f'],
#                        columns=['New York' , 'Oregon'])
#
# another
# Out[139]:
#    New York  Oregon
# a       7.0     8.0
# c       9.0    10.0
# e      11.0    12.0
# f      16.0    17.0
# left2.join([right2 , another])
# Out[140]:
#    Ohio  Nevada  Missouri  Alabama  New York  Oregon
# a   1.0     2.0       NaN      NaN       7.0     8.0
# c   3.0     4.0       9.0     10.0       9.0    10.0
# e   5.0     6.0      13.0     14.0      11.0    12.0
#


# left2.join([right2 , another] , how='outer')
#
# Out[141]:
#    Ohio  Nevada  Missouri  Alabama  New York  Oregon
# a   1.0     2.0       NaN      NaN       7.0     8.0
# b   NaN     NaN       7.0      8.0       NaN     NaN
# c   3.0     4.0       9.0     10.0       9.0    10.0
# d   NaN     NaN      11.0     12.0       NaN     NaN
# e   5.0     6.0      13.0     14.0      11.0    12.0
# f   NaN     NaN       NaN      NaN      16.0    17.0



# 8.2.3 沿轴方向连接

#
# arr = np.arange(12).reshape((3,4))
# arr
# Out[143]:
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]])
# np.concatenate([arr,arr],axis = 1)     #
# Out[144]:
# array([[ 0,  1,  2,  3,  0,  1,  2,  3],
#        [ 4,  5,  6,  7,  4,  5,  6,  7],
#        [ 8,  9, 10, 11,  8,  9, 10, 11]])


# s1 = pd.Series([0,1] , index=['a','b'])
# s2 = pd.Series([2,3,4] , index=['c','d','e'])
# s3 = pd.Series([5,6],index=['f','g'])
# pd.concat([s1,s2,s3])            # 用concat可以将值和索引粘合在一起,默认axis=0
# Out[148]:
# a    0
# b    1
# c    2
# d    3
# e    4
# f    5
# g    6
# dtype: int64

# pd.concat([s1,s2,s3] , axis=1)   # 列上相加
# Out[149]:
#      0    1    2
# a  0.0  NaN  NaN
# b  1.0  NaN  NaN
# c  NaN  2.0  NaN
# d  NaN  3.0  NaN
# e  NaN  4.0  NaN
# f  NaN  NaN  5.0
# g  NaN  NaN  6.0

# s4 = pd.concat([s1,s3])
# s4
# Out[151]:
# a    0
# b    1
# f    5
# g    6
# dtype: int64
# pd.concat([s1,s4] , axis=1)
# Out[152]:
#      0  1
# a  0.0  0
# b  1.0  1
# f  NaN  5
# g  NaN  6
# pd.concat([s1,s4] , axis=1 , join='inner')
# Out[153]:
#    0  1
# a  0  0
# b  1  1

#通过join_axes指定要在其它轴上使用的索引
# pd.concat([s1,s4] , axis=1 , join_axes = [['a','c' , 'b' , 'e']])
# Out[154]:
#      0    1
# a  0.0  0.0
# c  NaN  NaN
# b  1.0  1.0
# e  NaN  NaN

# 在连接轴上创建一个层次化索引
# result = pd.concat([s1,s1,s3],keys=['one','two','three'])
# result
# Out[156]:
# one    a    0
#        b    1
# two    a    0
#        b    1
# three  f    5
#        g    6
# dtype: int64
#
# result.unstack()
# Out[157]:
#          a    b    f    g
# one    0.0  1.0  NaN  NaN
# two    0.0  1.0  NaN  NaN
# three  NaN  NaN  5.0  6.0
# result.unstack().stack()
# Out[158]:
# one    a    0.0
#        b    1.0
# two    a    0.0
#        b    1.0
# three  f    5.0
#        g    6.0
# dtype: float64

# 如果沿着axis=1对Series进行合并，则keys就会成为DataFrame的列头：
# pd.concat([s1,s2,s3],axis=1,keys=['one','two','three'])
#
# out[159]:
#    one  two  three
# a  0.0  NaN    NaN
# b  1.0  NaN    NaN
# c  NaN  2.0    NaN
# d  NaN  3.0    NaN
# e  NaN  4.0    NaN
# f  NaN  NaN    5.0
# g  NaN  NaN    6.0


# df1=pd.DataFrame(np.arange(6).reshape(3,2),
#                  index=['a','b','c'],
#                  columns=['one','two'])
# df2 = pd.DataFrame(5 + np.arange(4).reshape(2,2) ,
#                    index=['a','c'],
#                    columns=['three' , 'four'])
# df1
# Out[161]:
#    one  two
# a    0    1
# b    2    3
# c    4    5
# df2
# Out[162]:
#    three  four
# a      5     6
# c      7     8
#
# pd.concat([df1,df2],axis=1,keys=['level1' , 'level2'])
#
# Out[163]:
#   level1     level2
#      one two  three four
# a      0   1    5.0  6.0
# b      2   3    NaN  NaN
# c      4   5    7.0  8.0


# 如果传入的不是列表而是一个字典，则字典的键就会被当做keys选项的值：

# pd.concat({'level1':df1 , 'level2':df2} , axis=1,sort=False)
#
# Out[164]:
#   level1     level2
#      one two  three four
# a      0   1    5.0  6.0
# b      2   3    NaN  NaN
# c      4   5    7.0  8.0

# 用names参数命名创建的轴级别
# pd.concat([df1,df2] , axis=1 ,
#           keys=['level1' , 'level2'] ,
#           names =['upper' , 'lower'] ,
#           sort=True)
# Out[169]:
# upper level1     level2
# lower    one two  three four
# a          0   1    5.0  6.0
# b          2   3    NaN  NaN
# c          4   5    7.0  8.0

# df1 = pd.DataFrame(np.random.randn(3,4) , columns=['a' , 'b', 'c' , 'd'])
# df2 = pd.DataFrame(np.random.randn(2,3) , columns=['b' , 'd' , 'a'])
# df1
# Out[173]:
#           a         b         c         d
# 0 -1.182773  0.877331 -0.161098 -0.221907
# 1  0.623180 -1.334489  0.726187 -0.115448
# 2  0.345934 -1.262575 -2.406897  0.463520
# df2
# Out[174]:
#           b         d         a
# 0  1.336895 -0.732482 -0.026555
# 1  1.040371 -0.730539  1.013456

# pd.concat([df1 , df2] , ignore_index = True , sort=True)
# 引入ignore_index = True ，意思是不保留连接轴上的索引，产生一组新索引
# Out[176]:
#           a         b         c         d
# 0 -1.182773  0.877331 -0.161098 -0.221907
# 1  0.623180 -1.334489  0.726187 -0.115448
# 2  0.345934 -1.262575 -2.406897  0.463520
# 3 -0.026555  1.336895       NaN -0.732482
# 4  1.013456  1.040371       NaN -0.730539


## 8.2.4   合并重叠数据

# a = pd.Series([np.nan , 2.5 , np.nan , 3.5 , 4.5 , np.nan] ,
#               index= ['f' , 'e' , 'd' , 'c' , 'b' , 'a'])
#
# b = pd.Series(np.arange(len(a) , dtype = np.float64) ,
#               index=['f' , 'e' , 'd' , 'c' , 'b' , 'a'])
#
# a
# Out[179]:
# f    NaN
# e    2.5
# d    NaN
# c    3.5
# b    4.5
# a    NaN
# dtype: float64
# b
# Out[180]:
# f    0.0
# e    1.0
# d    2.0
# c    3.0
# b    4.0
# a    5.0
# dtype: float64
# b[-1] = np.nan
# b
# Out[182]:
# f    0.0
# e    1.0
# d    2.0
# c    3.0
# b    4.0
# a    NaN
# dtype: float64
# np.where(pd.isnull(a) , b , a)
# pd.isnull(a)判断a中是否有空值
# np.where是条件，a中是空值，就放进b中值，a中不是空值，就放进a中值
# Out[183]: array([0. , 2.5, 2. , 3.5, 4.5, nan])

# combine_first方法，实现的也是一样的功能，还带有pandas的数据对齐
# b[:2].combine_first(a[2:])
# Out[184]:
# a    NaN
# b    4.5
# c    3.5
# d    NaN
# e    1.0
# f    0.0
# dtype: float64

# b[:-2].combine_first(a[2:])
# Out[185]:
# a    NaN
# b    4.5
# c    3.0
# d    2.0
# e    1.0
# f    0.0
# dtype: float64

# 对于DataFrame，combine_first自然也会在列上做同样的事情，
# 因此你可以将其看做：用传递对象中的数据为调用对象的缺失数据“打补丁”：

# df1 = pd.DataFrame({'a':[1. , np.nan , 5. , np.nan],
#                     'b':[np.nan , 2. , np.nan , 6.],
#                     'c':range(2,18,4)})
# df2 = pd.DataFrame({'a':[5. , 4. , np.nan , 3. , 7.],
#                     'b':[np.nan , 3. ,4. ,6. ,8.]})
#
# df1
# Out[187]:
#      a    b   c
# 0  1.0  NaN   2
# 1  NaN  2.0   6
# 2  5.0  NaN  10
# 3  NaN  6.0  14
# df2
# Out[188]:
#      a    b
# 0  5.0  NaN
# 1  4.0  3.0
# 2  NaN  4.0
# 3  3.0  6.0
# 4  7.0  8.0
# df1.combine_first(df2)
# Out[189]:
#      a    b     c
# 0  1.0  NaN   2.0
# 1  4.0  2.0   6.0
# 2  5.0  4.0  10.0
# 3  3.0  6.0  14.0
# 4  7.0  8.0   NaN

# 8.3重塑和轴向旋转（透视）

# stack：将数据的列“旋转”为行
# unstack：将数据的行“旋转”为列

# data = pd.DataFrame(np.arange(6).reshape((2,3)),
#                     index=pd.Index(['Ohio' , 'Colorado'],name='state'),
#                     columns=pd.Index(['one' , 'two' , 'three'],
#                     name = 'number'))
# data
# Out[192]:
# number    one  two  three
# state
# Ohio        0    1      2
# Colorado    3    4      5

# 使用stack方法即可将列转换为行，得到一个Series：
# result = data.stack()
# result
# Out[194]:
# state     number
# Ohio      one       0
#           two       1
#           three     2
# Colorado  one       3
#           two       4
#           three     5
# dtype: int32

# 对于一个层次化索引的Series，你可以用unstack将其重排为一个
# DataFrame：

# result.unstack()
# Out[195]:
# number    one  two  three
# state
# Ohio        0    1      2
# Colorado    3    4      5

# 默认情况下，unstack操作的是最内层（stack也是如此）。
# 传入分层级别的编号或名称即可对其它级别进行unstack操作
#
# result.unstack(0)
# Out[196]:
# state   Ohio  Colorado
# number
# one        0         3
# two        1         4
# three      2         5

# result.unstack('state')
# Out[197]:
# state   Ohio  Colorado
# number
# one        0         3
# two        1         4
# three      2         5



# 如果不是所有的级别值都能在各分组中找到的话
# 则unstack操作可能会引入缺失数据：

# s1 = pd.Series([0,1,2,3] , index=['a','b','c','d'])
# s2 = pd.Series([4,5,6] , index=['c','d','e'])
# data2 = pd.concat([s1,s2], keys=['one' , 'two'])
# data2
# Out[200]:
# one  a    0
#      b    1
#      c    2
#      d    3
# two  c    4
#      d    5
#      e    6
# dtype: int64

# stack默认会滤除缺失数据，因此该运算是可逆的：
# data2.unstack().stack()
# Out[202]:
# one  a    0.0
#      b    1.0
#      c    2.0
#      d    3.0
# two  c    4.0
#      d    5.0
#      e    6.0
# dtype: float64

# data2.unstack().stack(dropna=False)
# Out[203]:
# one  a    0.0
#      b    1.0
#      c    2.0
#      d    3.0
#      e    NaN
# two  a    NaN
#      b    NaN
#      c    4.0
#      d    5.0
#      e    6.0
# dtype: float64

# 在对DataFrame进行unstack操作时
# 作为旋转轴的级别将会成为结果中的最低级别：

# df = pd.DataFrame({'left': result ,'right':result + 5},
#                   columns=pd.Index(['left' , 'right'],
#                                    name = 'side'))
# df
# Out[205]:
# side             left  right
# state    number
# Ohio     one        0      5
#          two        1      6
#          three      2      7
# Colorado one        3      8
#          two        4      9
#          three      5     10

# df.unstack('state')
# Out[207]:
# side   left          right
# state  Ohio Colorado  Ohio Colorado
# number
# one       0        3     5        8
# two       1        4     6        9
# three     2        5     7       10

# df.unstack('state').stack('side')
# Out[208]:
# state         Colorado  Ohio
# number side
# one    left          3     0
#        right         8     5
# two    left          4     1
#        right         9     6
# three  left          5     2
#        right        10     7


# 8.3.2   将长格式旋转为宽格式

# data = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\macrodata.csv')
# data.head()
# Out[210]:
#      year  quarter   realgdp  realcons  ...  unemp      pop  infl  realint
# 0  1959.0      1.0  2710.349    1707.4  ...    5.8  177.146  0.00     0.00
# 1  1959.0      2.0  2778.801    1733.7  ...    5.1  177.830  2.34     0.74
# 2  1959.0      3.0  2775.488    1751.8  ...    5.3  178.657  2.74     1.09
# 3  1959.0      4.0  2785.204    1753.7  ...    5.6  179.386  0.27     4.06
# 4  1960.0      1.0  2847.699    1770.5  ...    5.2  180.007  2.31     1.19
# [5 rows x 14 columns]

# periods = pd.PeriodIndex
# periods = pd.PeriodIndex(year = data.year , quarter = data.quarter,name='date')
# columns = pd.Index(['realgdp' , 'infl' , 'unemp'] , name='item')
# data = data.reindex(columns = columns)
# data.index = periods.to_timestamp('D' , 'end')
# ldata = data.stack().reset_index().rename(columns={0:'value'})
# ldata
#
# Out[217]:
#                              date     item      value
# 0   1959-03-31 23:59:59.999999999  realgdp   2710.349
# 1   1959-03-31 23:59:59.999999999     infl      0.000
# 2   1959-03-31 23:59:59.999999999    unemp      5.800
# 3   1959-06-30 23:59:59.999999999  realgdp   2778.801
# 4   1959-06-30 23:59:59.999999999     infl      2.340
# 5   1959-06-30 23:59:59.999999999    unemp      5.100
# 6   1959-09-30 23:59:59.999999999  realgdp   2775.488
# 7   1959-09-30 23:59:59.999999999     infl      2.740
# 8   1959-09-30 23:59:59.999999999    unemp      5.300
# 9   1959-12-31 23:59:59.999999999  realgdp   2785.204
# 10  1959-12-31 23:59:59.999999999     infl      0.270
# 11  1959-12-31 23:59:59.999999999    unemp      5.600
# 12  1960-03-31 23:59:59.999999999  realgdp   2847.699
# 13  1960-03-31 23:59:59.999999999     infl      2.310
# 14  1960-03-31 23:59:59.999999999    unemp      5.200
# 15  1960-06-30 23:59:59.999999999  realgdp   2834.390
# 16  1960-06-30 23:59:59.999999999     infl      0.140
# 17  1960-06-30 23:59:59.999999999    unemp      5.200
# 18  1960-09-30 23:59:59.999999999  realgdp   2839.022
# 19  1960-09-30 23:59:59.999999999     infl      2.700
# 20  1960-09-30 23:59:59.999999999    unemp      5.600
# 21  1960-12-31 23:59:59.999999999  realgdp   2802.616
# 22  1960-12-31 23:59:59.999999999     infl      1.210
# 23  1960-12-31 23:59:59.999999999    unemp      6.300
# 24  1961-03-31 23:59:59.999999999  realgdp   2819.264
# 25  1961-03-31 23:59:59.999999999     infl     -0.400
# 26  1961-03-31 23:59:59.999999999    unemp      6.800
# 27  1961-06-30 23:59:59.999999999  realgdp   2872.005
# 28  1961-06-30 23:59:59.999999999     infl      1.470
# 29  1961-06-30 23:59:59.999999999    unemp      7.000
# ..                            ...      ...        ...
# 579 2007-06-30 23:59:59.999999999  realgdp  13203.977
# 580 2007-06-30 23:59:59.999999999     infl      2.750
# 581 2007-06-30 23:59:59.999999999    unemp      4.500
# 582 2007-09-30 23:59:59.999999999  realgdp  13321.109
# 583 2007-09-30 23:59:59.999999999     infl      3.450
# 584 2007-09-30 23:59:59.999999999    unemp      4.700
# 585 2007-12-31 23:59:59.999999999  realgdp  13391.249
# 586 2007-12-31 23:59:59.999999999     infl      6.380
# 587 2007-12-31 23:59:59.999999999    unemp      4.800
# 588 2008-03-31 23:59:59.999999999  realgdp  13366.865
# 589 2008-03-31 23:59:59.999999999     infl      2.820
# 590 2008-03-31 23:59:59.999999999    unemp      4.900
# 591 2008-06-30 23:59:59.999999999  realgdp  13415.266
# 592 2008-06-30 23:59:59.999999999     infl      8.530
# 593 2008-06-30 23:59:59.999999999    unemp      5.400
# 594 2008-09-30 23:59:59.999999999  realgdp  13324.600
# 595 2008-09-30 23:59:59.999999999     infl     -3.160
# 596 2008-09-30 23:59:59.999999999    unemp      6.000
# 597 2008-12-31 23:59:59.999999999  realgdp  13141.920
# 598 2008-12-31 23:59:59.999999999     infl     -8.790
# 599 2008-12-31 23:59:59.999999999    unemp      6.900
# 600 2009-03-31 23:59:59.999999999  realgdp  12925.410
# 601 2009-03-31 23:59:59.999999999     infl      0.940
# 602 2009-03-31 23:59:59.999999999    unemp      8.100
# 603 2009-06-30 23:59:59.999999999  realgdp  12901.504
# 604 2009-06-30 23:59:59.999999999     infl      3.370
# 605 2009-06-30 23:59:59.999999999    unemp      9.200
# 606 2009-09-30 23:59:59.999999999  realgdp  12990.341
# 607 2009-09-30 23:59:59.999999999     infl      3.560
# 608 2009-09-30 23:59:59.999999999    unemp      9.600
# [609 rows x 3 columns]

# pivoted = ldata.pivot('date' , 'item' , 'value')
# 前两个传递的值分别用作行和列索引，最后一个可选值则是用于填充DataFrame的数据列。
# pivoted
# Out[219]:
# item                           infl    realgdp  unemp
# date
# 1959-03-31 23:59:59.999999999  0.00   2710.349    5.8
# 1959-06-30 23:59:59.999999999  2.34   2778.801    5.1
# 1959-09-30 23:59:59.999999999  2.74   2775.488    5.3
# 1959-12-31 23:59:59.999999999  0.27   2785.204    5.6
# 1960-03-31 23:59:59.999999999  2.31   2847.699    5.2
# 1960-06-30 23:59:59.999999999  0.14   2834.390    5.2
# 1960-09-30 23:59:59.999999999  2.70   2839.022    5.6
# 1960-12-31 23:59:59.999999999  1.21   2802.616    6.3
# 1961-03-31 23:59:59.999999999 -0.40   2819.264    6.8
# 1961-06-30 23:59:59.999999999  1.47   2872.005    7.0
# 1961-09-30 23:59:59.999999999  0.80   2918.419    6.8
# 1961-12-31 23:59:59.999999999  0.80   2977.830    6.2
# 1962-03-31 23:59:59.999999999  2.26   3031.241    5.6
# 1962-06-30 23:59:59.999999999  0.13   3064.709    5.5
# 1962-09-30 23:59:59.999999999  2.11   3093.047    5.6
# 1962-12-31 23:59:59.999999999  0.79   3100.563    5.5
# 1963-03-31 23:59:59.999999999  0.53   3141.087    5.8
# 1963-06-30 23:59:59.999999999  2.75   3180.447    5.7
# 1963-09-30 23:59:59.999999999  0.78   3240.332    5.5
# 1963-12-31 23:59:59.999999999  2.46   3264.967    5.6
# 1964-03-31 23:59:59.999999999  0.13   3338.246    5.5
# 1964-06-30 23:59:59.999999999  0.90   3376.587    5.2
# 1964-09-30 23:59:59.999999999  1.29   3422.469    5.0
# 1964-12-31 23:59:59.999999999  2.05   3431.957    5.0
# 1965-03-31 23:59:59.999999999  1.28   3516.251    4.9
# 1965-06-30 23:59:59.999999999  2.54   3563.960    4.7
# 1965-09-30 23:59:59.999999999  0.89   3636.285    4.4
# 1965-12-31 23:59:59.999999999  2.90   3724.014    4.1
# 1966-03-31 23:59:59.999999999  4.99   3815.423    3.9
# 1966-06-30 23:59:59.999999999  2.10   3828.124    3.8
#                              ...        ...    ...
# 2002-06-30 23:59:59.999999999  1.56  11538.770    5.8
# 2002-09-30 23:59:59.999999999  2.66  11596.430    5.7
# 2002-12-31 23:59:59.999999999  3.08  11598.824    5.8
# 2003-03-31 23:59:59.999999999  1.31  11645.819    5.9
# 2003-06-30 23:59:59.999999999  1.09  11738.706    6.2
# 2003-09-30 23:59:59.999999999  2.60  11935.461    6.1
# 2003-12-31 23:59:59.999999999  3.02  12042.817    5.8
# 2004-03-31 23:59:59.999999999  2.35  12127.623    5.7
# 2004-06-30 23:59:59.999999999  3.61  12213.818    5.6
# 2004-09-30 23:59:59.999999999  3.58  12303.533    5.4
# 2004-12-31 23:59:59.999999999  2.09  12410.282    5.4
# 2005-03-31 23:59:59.999999999  4.15  12534.113    5.3
# 2005-06-30 23:59:59.999999999  1.85  12587.535    5.1
# 2005-09-30 23:59:59.999999999  9.14  12683.153    5.0
# 2005-12-31 23:59:59.999999999  0.40  12748.699    4.9
# 2006-03-31 23:59:59.999999999  2.60  12915.938    4.7
# 2006-06-30 23:59:59.999999999  3.97  12962.462    4.7
# 2006-09-30 23:59:59.999999999 -1.58  12965.916    4.7
# 2006-12-31 23:59:59.999999999  3.30  13060.679    4.4
# 2007-03-31 23:59:59.999999999  4.58  13099.901    4.5
# 2007-06-30 23:59:59.999999999  2.75  13203.977    4.5
# 2007-09-30 23:59:59.999999999  3.45  13321.109    4.7
# 2007-12-31 23:59:59.999999999  6.38  13391.249    4.8
# 2008-03-31 23:59:59.999999999  2.82  13366.865    4.9
# 2008-06-30 23:59:59.999999999  8.53  13415.266    5.4
# 2008-09-30 23:59:59.999999999 -3.16  13324.600    6.0
# 2008-12-31 23:59:59.999999999 -8.79  13141.920    6.9
# 2009-03-31 23:59:59.999999999  0.94  12925.410    8.1
# 2009-06-30 23:59:59.999999999  3.37  12901.504    9.2
# 2009-09-30 23:59:59.999999999  3.56  12990.341    9.6
# [203 rows x 3 columns]


# ldata['value2'] = np.random.randn(len(ldata))
# ldata[:10]
# Out[221]:
#                            date     item     value    value2
# 0 1959-03-31 23:59:59.999999999  realgdp  2710.349  0.105432
# 1 1959-03-31 23:59:59.999999999     infl     0.000 -0.951959
# 2 1959-03-31 23:59:59.999999999    unemp     5.800  1.866561
# 3 1959-06-30 23:59:59.999999999  realgdp  2778.801 -0.717398
# 4 1959-06-30 23:59:59.999999999     infl     2.340  0.939747
# 5 1959-06-30 23:59:59.999999999    unemp     5.100  0.421197
# 6 1959-09-30 23:59:59.999999999  realgdp  2775.488  0.222969
# 7 1959-09-30 23:59:59.999999999     infl     2.740 -0.898276
# 8 1959-09-30 23:59:59.999999999    unemp     5.300 -0.653408
# 9 1959-12-31 23:59:59.999999999  realgdp  2785.204 -0.811388

# pivoted = ldata.pivot('date' , 'item')
# 再次使用.pivot，但是不放如第三个参数，value和value2就被提出，是数据变得层次化
# pivoted[:5]
# Out[223]:
#                               value            ...    value2
# item                           infl   realgdp  ...   realgdp     unemp
# date                                           ...
# 1959-03-31 23:59:59.999999999  0.00  2710.349  ...  0.105432  1.866561
# 1959-06-30 23:59:59.999999999  2.34  2778.801  ... -0.717398  0.421197
# 1959-09-30 23:59:59.999999999  2.74  2775.488  ...  0.222969 -0.653408
# 1959-12-31 23:59:59.999999999  0.27  2785.204  ... -0.811388  0.110364
# 1960-03-31 23:59:59.999999999  2.31  2847.699  ...  0.651897 -0.793677
# [5 rows x 6 columns]

# pivoted['value'][:5]
# Out[224]:
# item                           infl   realgdp  unemp
# date
# 1959-03-31 23:59:59.999999999  0.00  2710.349    5.8
# 1959-06-30 23:59:59.999999999  2.34  2778.801    5.1
# 1959-09-30 23:59:59.999999999  2.74  2775.488    5.3
# 1959-12-31 23:59:59.999999999  0.27  2785.204    5.6
# 1960-03-31 23:59:59.999999999  2.31  2847.699    5.2


# pivot其实就是用set_index创建层次化索引，再用unstack重塑:

# unstacked = ldata.set_index(['date' , 'item']).unstack('item')
# unstacked[:7]
# Out[226]:
#                               value            ...    value2
# item                           infl   realgdp  ...   realgdp     unemp
# date                                           ...
# 1959-03-31 23:59:59.999999999  0.00  2710.349  ...  0.105432  1.866561
# 1959-06-30 23:59:59.999999999  2.34  2778.801  ... -0.717398  0.421197
# 1959-09-30 23:59:59.999999999  2.74  2775.488  ...  0.222969 -0.653408
# 1959-12-31 23:59:59.999999999  0.27  2785.204  ... -0.811388  0.110364
# 1960-03-31 23:59:59.999999999  2.31  2847.699  ...  0.651897 -0.793677
# 1960-06-30 23:59:59.999999999  0.14  2834.390  ... -0.069367 -1.573119
# 1960-09-30 23:59:59.999999999  2.70  2839.022  ...  0.551373 -0.501898
# [7 rows x 6 columns]


# 8.3.3 将宽旋转为长

# 旋转DataFrame的逆运算是pandas.melt。
# 它不是将一列转换到多个新的DataFrame，而是合并多个列成为一个，产生一个比输入长的DataFrame。

# df = pd.DataFrame({'key':['foo' , 'bar' , 'baz'],
#                    'A':[1,2,3],
#                    'B':[4,5,6],
#                    'C':[7,8,9]})
#
# df
# Out[230]:
#    key  A  B  C
# 0  foo  1  4  7
# 1  bar  2  5  8
# 2  baz  3  6  9
# 当使用pandas.melt，我们必须指明哪些列是分组指标。
# melted = pd.melt(df , ['key'])
# melted
# Out[232]:
#    key variable  value
# 0  foo        A      1
# 1  bar        A      2
# 2  baz        A      3
# 3  foo        B      4
# 4  bar        B      5
# 5  baz        B      6
# 6  foo        C      7
# 7  bar        C      8
# 8  baz        C      9
#
# reshaped = melted.pivot('key' , 'variable' , 'value')
# reshaped
# Out[235]:
# variable  A  B  C
# key
# bar       2  5  8
# baz       3  6  9
# foo       1  4  7

# reshaped.reset_index()
# Out[236]:
# variable  key  A  B  C
# 0         bar  2  5  8
# 1         baz  3  6  9
# 2         foo  1  4  7

# 指定列的子集，作为值的列
# pd.melt(df, id_vars=['key'] , value_vars=['A' , 'B'])
# Out[237]:
#    key variable  value
# 0  foo        A      1
# 1  bar        A      2
# 2  baz        A      3
# 3  foo        B      4
# 4  bar        B      5
# 5  baz        B      6

# pandas.melt也可以不用分组指标：

# pd.melt(df , value_vars = ['A' , 'B' , 'C'])
# Out[238]:
#   variable  value
# 0        A      1
# 1        A      2
# 2        A      3
# 3        B      4
# 4        B      5
# 5        B      6
# 6        C      7
# 7        C      8
# 8        C      9

# pd.melt(df , value_vars=['key' , 'A' , 'B'])
# Out[239]:
#   variable value
# 0      key   foo
# 1      key   bar
# 2      key   baz
# 3        A     1
# 4        A     2
# 5        A     3
# 6        B     4
# 7        B     5
# 8        B     6






