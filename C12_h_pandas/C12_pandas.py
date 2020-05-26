"""

    作者：大发
    日期：2019/11/20
    内容：利用python进行数据分析 12.1 p346 笔记

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
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour,Minute
from pandas.tseries.offsets import Day,MonthEnd
from scipy.stats import percentileofscore

# 12.1 分类数据

## 12.1.1 背景和目标

# values = pd.Series(['apple' , 'orange' , 'apple' , 'apple']*2)
# values
# Out[5]:
# 0     apple
# 1    orange
# 2     apple
# 3     apple
# 4     apple
# 5    orange
# 6     apple
# 7     apple
# dtype: object
# pd.unique(values)
# Out[6]: array(['apple', 'orange'], dtype=object)
# pd.value_counts(values)
# Out[7]:
# apple     6
# orange    2
# dtype: int64
# values = pd.Series([0,1,0,0]*2)
# dim = pd.Series(['apple' , 'orange'])
# values
# Out[10]:
# 0    0
# 1    1
# 2    0
# 3    0
# 4    0
# 5    1
# 6    0
# 7    0
# dtype: int64
# dim
# Out[11]:
# 0     apple
# 1    orange
# dtype: object

# 可以使用take方法存储原始的字符串Series：
# dim.take(values)
# Out[12]:
# 0     apple
# 1    orange
# 0     apple
# 0     apple
# 0     apple
# 1    orange
# 0     apple
# 0     apple
# dtype: object


### 12.1.2 pandas中的Categorical类型
# pandas有一个特殊的分类类型，用于保存使用整数分类表示法的数据。

# fruits = ['apple' , 'orange' , 'apple' , 'apple']*2
# N = len(fruits)
# df = pd.DataFrame({'fruit': fruits ,
#                    'basket_id': np.arange(N) ,
#                    'count': np.random.randint(3,15,size=N) ,
#                    'weight': np.random.uniform(0,4,size=N)} ,
#                   columns=['basket_id' , 'fruit' , 'count' , 'weight'])
# df
# Out[13]:
#    basket_id   fruit  count    weight
# 0          0   apple      9  3.149445
# 1          1  orange     13  2.668208
# 2          2   apple      5  0.357567
# 3          3   apple     12  1.047689
# 4          4   apple     12  3.280273
# 5          5  orange      7  1.465324
# 6          6   apple     13  2.617268
# 7          7   apple     13  2.125068

# 这里，df['fruit']是一个Python字符串对象的数组。
# 我们可以通过调用它，将它转变为分类：
# In[14]: fruit_cat = df['fruit'].astype('category')
# In[15]: fruit_cat
# Out[15]:
# 0     apple
# 1    orange
# 2     apple
# 3     apple
# 4     apple
# 5    orange
# 6     apple
# 7     apple
# Name: fruit, dtype: category
# Categories (2, object): [apple, orange]

# fruit_cat的值不是NumPy数组，而是一个pandas.Categorical实例：
# In[16]: c = fruit_cat.values
# In[17]: type(c)
# Out[17]: pandas.core.arrays.categorical.Categorical

# 分类对象有categories和codes属性：
# In[18]: c.categories
# Out[18]: Index(['apple', 'orange'], dtype='object')
# In[19]: c.codes
# Out[19]: array([0, 1, 0, 0, 0, 1, 0, 0], dtype=int8)

# 可将DataFrame的列通过分配转换结果，转换为分类：
# In[20]: df['fruit'] = df['fruit'].astype('category')
# In[21]: df.fruit
# Out[21]:
# 0     apple
# 1    orange
# 2     apple
# 3     apple
# 4     apple
# 5    orange
# 6     apple
# 7     apple
# Name: fruit, dtype: category
# Categories (2, object): [apple, orange]

# 还可以从其它Python序列直接创建pandas.Categorical：
# my_categories = pd.Categorical(['foo' , 'bar' , 'baz' , 'foo' , 'bar'])
# In[23]: my_categories
# Out[23]:
# [foo, bar, baz, foo, bar]
# Categories (3, object): [bar, baz, foo]

# 如果你已经从其它源获得了分类编码，你还可以使用from_codes构造器：
# In[24]: categories = ['foo' , 'bar' , 'baz']
# In[25]: codes = [0,1,2,0,0,1]
# In[26]: my_cats_2 = pd.Categorical.from_codes(codes , categories)
# In[27]: my_cats_2
# Out[27]:
# [foo, bar, baz, foo, foo, bar]
# Categories (3, object): [foo, bar, baz]

# 与显示指定不同，分类变换不认定指定的分类顺序。
# 因此取决于输入数据的顺序，categories数组的顺序会不同。
# 当使用from_codes或其它的构造器时，你可以指定分类一个有意义的顺序：
# ordered_cat = pd.Categorical.from_codes(codes , categories , ordered =True)
# In[29]: ordered_cat
# Out[29]:
# [foo, bar, baz, foo, foo, bar]
# Categories (3, object): [foo < bar < baz]    ##  输出[foo < bar < baz]指明‘foo’位于‘bar’的前面

# 无序的分类实例可以通过as_ordered排序：
# In[30]: my_cats_2.as_ordered()
# Out[30]:
# [foo, bar, baz, foo, foo, bar]
# Categories (3, object): [foo < bar < baz]

# 12.1.3 使用Categorical对象进行计算
# 使用pandas.qcut面元函数。它会返回pandas.Categorical，
# 我们之前使用过pandas.cut，但没解释分类是如何工作的：
# np.random.seed(12345)
# draws = np.random.randn(1000)
# draws[:5]
# Out[33]: array([-0.20470766,  0.47894334, -0.51943872, -0.5557303 ,  1.96578057])

# 计算这个数据的分位面元，提取一些统计信息：

# bins = pd.qcut(draws , 4)
# bins
# Out[5]:
# [(-0.684, -0.0101], (-0.0101, 0.63], (-0.684, -0.0101],
# (-0.684, -0.0101], (0.63, 3.928], ..., (-0.0101, 0.63],
# (-0.684, -0.0101], (-2.9499999999999997, -0.684],
# (-0.0101, 0.63], (0.63, 3.928]]
# Length: 1000
# Categories (4, interval[float64]):
# [(-2.9499999999999997, -0.684] < (-0.684, -0.0101] < (-0.0101, 0.63]
# <(0.63, 3.928]]

# 虽然有用，确切的样本分位数与分位的名称相比，不利于生成汇总。
# 我们可以使用labels参数qcut，实现目的：
# bins = pd.qcut(draws , 4 , labels = ['Q1' , 'Q2' , 'Q3' , 'Q4'])
# bins
# Out[7]:
# [Q2, Q3, Q2, Q2, Q4, ..., Q3, Q2, Q1, Q3, Q4]
# Length: 1000
# Categories (4, object): [Q1 < Q2 < Q3 < Q4]
# bins.codes[:10]
# Out[8]: array([1, 2, 1, 1, 3, 3, 2, 2, 3, 3], dtype=int8)

# 加上标签的面元分类不包含数据面元边界的信息，
# 因此可以使用groupby提取一些汇总信息：
#
# bins = pd.Series(bins , name='quartile')
# results = (pd.Series(draws)
#           .groupby(bins)
#           .agg(['count' , 'min' , 'max'])
#           .reset_index())
# results
# Out[11]:
#   quartile  count       min       max
# 0       Q1    250 -2.949343 -0.685484
# 1       Q2    250 -0.683066 -0.010115
# 2       Q3    250 -0.010032  0.628894
# 3       Q4    250  0.634238  3.927528

# 分位数列保存了原始的面元分类信息，包括排序：
# results['quartile']
# Out[12]:
# 0    Q1
# 1    Q2
# 2    Q3
# 3    Q4
# Name: quartile, dtype: category
# Categories (4, object): [Q1 < Q2 < Q3 < Q4]

## 12.1.3.1 使用分类提高性能

# DataFrame列的分类使用的内存通常少的多。
# 来看一些包含一千万元素的Series，和一些不同的分类：

# N = 10000000
# draws = pd.Series(np.random.randn(N))
# labels = pd.Series(['foo' , 'bar' , 'baz' , 'qux']* (N//4))
# categories = labels.astype('category')
# 接下来的比较可以发现分类比labels少用很多内存
# labels.memory_usage()
# Out[14]: 80000080
# categories.memory_usage()
# Out[15]: 10000272
# 转换为分类不是没有代价的，但这是一次性的代价：
# %time _  = labels.astype('category')    # 这句可以看到时间
# Wall time: 530 ms
# GroupBy使用分类操作明显更快，是因为底层的算法使用整数编码数组，而不是字符串数组。

# 12.1.4 分类方法
# 包含分类数据的Series有一些特殊的方法，提供了方便的分类和编码的使用方法
# s = pd.Series(['a','b','c','d']*2)
# cat_s = s.astype('category')
# cat_s
# Out[20]:
# 0    a
# 1    b
# 2    c
# 3    d
# 4    a
# 5    b
# 6    c
# 7    d
# dtype: category
# Categories (4, object): [a, b, c, d]

# 特别的cat属性提供了分类方法的入口：
# cat_s.cat.codes
# Out[21]:
# 0    0
# 1    1
# 2    2
# 3    3
# 4    0
# 5    1
# 6    2
# 7    3
# dtype: int8
# cat_s.cat.categories
# Out[22]: Index(['a', 'b', 'c', 'd'], dtype='object')

# 假设我们知道这个数据的实际分类集，超出了数据中的四个值。
# 我们可以使用set_categories方法改变它们：
# cat_s2 = cat_s.cat.set_categories(actual_categories)
# cat_s2
# Out[25]:
# 0    a
# 1    b
# 2    c
# 3    d
# 4    a
# 5    b
# 6    c
# 7    d
# dtype: category
# Categories (5, object): [a, b, c, d, e]


# 虽然数据看起来没变，新的分类将反映在它们的操作中。
# 例如，如果有的话，value_counts表示分类：
# cat_s.value_counts()
# Out[26]:
# d    2
# c    2
# b    2
# a    2
# dtype: int64
# cat_s2.value_counts()
# Out[27]:
# d    2
# c    2
# b    2
# a    2
# e    0
# dtype: int64

# 在大数据集中，分类经常作为节省内存和高性能的便捷工具。
# 过滤完大DataFrame或Series之后，许多分类可能不会出现在数据中。
# 我们可以使用remove_unused_categories方法删除没看到的分类：

# cat_s3 = cat_s[cat_s.isin(['a' ,'b'])]
# cat_s3
# Out[29]:
# 0    a
# 1    b
# 4    a
# 5    b
# dtype: category
# Categories (4, object): [a, b, c, d]
# cat_s3.cat.remove_unused_categories()
# Out[30]:
# 0    a
# 1    b
# 4    a
# 5    b
# dtype: category
# Categories (2, object): [a, b]

# add_categories : 在已存在的分类后面添加（未使用的）分类
# as_ordered : 使分类有序
# as_unordered : 使分类无序
# remove_categories : 移除分类，设置任何被移除的值为null
# remove_unused_categories : 移除任意不出现在数据中的分类值
# rename_categories : 用指定的新分类的名字替换分类；不能改变分类的数目
# reorder_categories : 与上一个很像，但是可以改变结果，是分类有序
# set_categories : 用指定的新分类的名字替换分类；可以添加或删除分类

## 12.1.4.1 为建模创建虚拟变量

# 当你使用统计或机器学习工具时，通常会将分类数据转换为虚拟变量，
# 也称为one-hot编码。这包括创建一个不同类别的列的DataFrame；
# 这些列包含给定分类的1s，其它为0。
# cat_s = pd.Series(['a' , 'b' ,'c' ,'d']*2 , dtype='category')
# pandas.get_dummies函数可以转换这个分类数据为包含虚拟变量的DataFrame：
# pd.get_dummies(cat_s)    # 其实这一步我也没看懂
# Out[33]:
#    a  b  c  d
# 0  1  0  0  0
# 1  0  1  0  0
# 2  0  0  1  0
# 3  0  0  0  1
# 4  1  0  0  0
# 5  0  1  0  0
# 6  0  0  1  0
# 7  0  0  0  1

#### 12.2 GroupBy 高级应用

## 12.2.1 分组转换和展开GroupBy
# tranform 方法：
# • 它可以产生向分组形状广播标量值
# • 它可以产生一个和输入组形状相同的对象
# • 它不能修改输入

# df = pd.DataFrame({'key':['a','b','c']*4 , 'value':np.arange(12.)})
# df
# Out[35]:
#    key  value
# 0    a    0.0
# 1    b    1.0
# 2    c    2.0
# 3    a    3.0
# 4    b    4.0
# 5    c    5.0
# 6    a    6.0
# 7    b    7.0
# 8    c    8.0
# 9    a    9.0
# 10   b   10.0
# 11   c   11.0

# 按键进行分组：
# g = df.groupby('key').value
# g.mean()
# Out[37]:
# key
# a    4.5
# b    5.5
# c    6.5
# Name: value, dtype: float64

# 假设我们想产生一个和df['value']形状相同的Series，但值替换为按键分组的平均值。
# 我们可以传递函数lambda x: x.mean()进行转换：
# g.transform(lambda x:x.mean())
# Out[38]:
# 0     4.5
# 1     5.5
# 2     6.5
# 3     4.5
# 4     5.5
# 5     6.5
# 6     4.5
# 7     5.5
# 8     6.5
# 9     4.5
# 10    5.5
# 11    6.5
# Name: value, dtype: float64

# 对于内置的聚合函数，我们可以传递一个字符串假名作为GroupBy的agg方法：

# g.transform('mean')
# Out[39]:
# 0     4.5
# 1     5.5
# 2     6.5
# 3     4.5
# 4     5.5
# 5     6.5
# 6     4.5
# 7     5.5
# 8     6.5
# 9     4.5
# 10    5.5
# 11    6.5
# Name: value, dtype: float64

# 与apply类似，transform的函数会返回Series，但是结果必须与输入大小相同。
# 举个例子，我们可以用lambda函数将每个分组乘以2：
# g.transform(lambda x:x*2)
# Out[40]:
# 0      0.0
# 1      2.0
# 2      4.0
# 3      6.0
# 4      8.0
# 5     10.0
# 6     12.0
# 7     14.0
# 8     16.0
# 9     18.0
# 10    20.0
# 11    22.0
# Name: value, dtype: float64

# 再举一个复杂的例子，我们可以计算每个分组的降序排名：
# g.transform(lambda x:x.rank(ascending=False))
# Out[41]:
# 0     4.0
# 1     4.0
# 2     4.0
# 3     3.0
# 4     3.0
# 5     3.0
# 6     2.0
# 7     2.0
# 8     2.0
# 9     1.0
# 10    1.0
# 11    1.0
# Name: value, dtype: float64

# 看一个由简单聚合构造的的分组转换函数：
# def normalize(x):
#     return (x - x.mean())/x.std()
# g.transform(normalize)
# Out[42]:
# 0    -1.161895
# 1    -1.161895
# 2    -1.161895
# 3    -0.387298
# 4    -0.387298
# 5    -0.387298
# 6     0.387298
# 7     0.387298
# 8     0.387298
# 9     1.161895
# 10    1.161895
# 11    1.161895
# Name: value, dtype: float64
# .apply方法和上边的方法等同
# g.apply(normalize)
# Out[43]:
# 0    -1.161895
# 1    -1.161895
# 2    -1.161895
# 3    -0.387298
# 4    -0.387298
# 5    -0.387298
# 6     0.387298
# 7     0.387298
# 8     0.387298
# 9     1.161895
# 10    1.161895
# 11    1.161895
# Name: value, dtype: float64

# 内置的聚合函数，比如mean或sum，通常比apply函数快，也比transform快。
# 这允许我们进行一个所谓的解封（unwrapped）分组操作：

# normalized = (df['value'] - g.transform('mean'))/ g.transform('std')
# normalized
# Out[46]:
# 0    -1.161895
# 1    -1.161895
# 2    -1.161895
# 3    -0.387298
# 4    -0.387298
# 5    -0.387298
# 6     0.387298
# 7     0.387298
# 8     0.387298
# 9     1.161895
# 10    1.161895
# 11    1.161895
# Name: value, dtype: float64
# 解封分组操作可能包括多个分组聚合，但是矢量化操作还是会带来收益


### 12.2.2 分组的时间重采样
# 对于时间序列数据，resample方法从语义上是一个基于内在时间的分组操作。
# 下面是一个示例表：
# #
# N = 15
# times = pd.date_range('2017-05-20 00:00' , freq = '1min' , periods = N)
# df = pd.DataFrame({'time':times , 'value':np.arange(N)})
# df
# Out[50]:
#                   time  value
# 0  2017-05-20 00:00:00      0
# 1  2017-05-20 00:01:00      1
# 2  2017-05-20 00:02:00      2
# 3  2017-05-20 00:03:00      3
# 4  2017-05-20 00:04:00      4
# 5  2017-05-20 00:05:00      5
# 6  2017-05-20 00:06:00      6
# 7  2017-05-20 00:07:00      7
# 8  2017-05-20 00:08:00      8
# 9  2017-05-20 00:09:00      9
# 10 2017-05-20 00:10:00     10
# 11 2017-05-20 00:11:00     11
# 12 2017-05-20 00:12:00     12
# 13 2017-05-20 00:13:00     13
# 14 2017-05-20 00:14:00     14

# 可以用time作为索引，然后重采样：
# df.set_index('time').resample('5min').count()
# Out[51]:
#                      value
# time
# 2017-05-20 00:00:00      5
# 2017-05-20 00:05:00      5
# 2017-05-20 00:10:00      5

# 假设DataFrame包含多个时间序列，用一个额外的分组键的列进行标记：
# df2 = pd.DataFrame({'time':times.repeat(3),
#                     'key':np.tile(['a','b','c'],N),
#                     'value':np.arange(N*3.)})

# df2
# Out[53]:
#                   time key  value
# 0  2017-05-20 00:00:00   a    0.0
# 1  2017-05-20 00:00:00   b    1.0
# 2  2017-05-20 00:00:00   c    2.0
# 3  2017-05-20 00:01:00   a    3.0
# 4  2017-05-20 00:01:00   b    4.0
# 5  2017-05-20 00:01:00   c    5.0
# 6  2017-05-20 00:02:00   a    6.0
# 7  2017-05-20 00:02:00   b    7.0
# 8  2017-05-20 00:02:00   c    8.0
# 9  2017-05-20 00:03:00   a    9.0
# 10 2017-05-20 00:03:00   b   10.0
# 11 2017-05-20 00:03:00   c   11.0
# 12 2017-05-20 00:04:00   a   12.0
# 13 2017-05-20 00:04:00   b   13.0
# 14 2017-05-20 00:04:00   c   14.0
# 15 2017-05-20 00:05:00   a   15.0
# 16 2017-05-20 00:05:00   b   16.0
# 17 2017-05-20 00:05:00   c   17.0
# 18 2017-05-20 00:06:00   a   18.0
# 19 2017-05-20 00:06:00   b   19.0
# 20 2017-05-20 00:06:00   c   20.0
# 21 2017-05-20 00:07:00   a   21.0
# 22 2017-05-20 00:07:00   b   22.0
# 23 2017-05-20 00:07:00   c   23.0
# 24 2017-05-20 00:08:00   a   24.0
# 25 2017-05-20 00:08:00   b   25.0
# 26 2017-05-20 00:08:00   c   26.0
# 27 2017-05-20 00:09:00   a   27.0
# 28 2017-05-20 00:09:00   b   28.0
# 29 2017-05-20 00:09:00   c   29.0
# 30 2017-05-20 00:10:00   a   30.0
# 31 2017-05-20 00:10:00   b   31.0
# 32 2017-05-20 00:10:00   c   32.0
# 33 2017-05-20 00:11:00   a   33.0
# 34 2017-05-20 00:11:00   b   34.0
# 35 2017-05-20 00:11:00   c   35.0
# 36 2017-05-20 00:12:00   a   36.0
# 37 2017-05-20 00:12:00   b   37.0
# 38 2017-05-20 00:12:00   c   38.0
# 39 2017-05-20 00:13:00   a   39.0
# 40 2017-05-20 00:13:00   b   40.0
# 41 2017-05-20 00:13:00   c   41.0
# 42 2017-05-20 00:14:00   a   42.0
# 43 2017-05-20 00:14:00   b   43.0
# 44 2017-05-20 00:14:00   c   44.0

# df2[:7]
# Out[54]:
#                  time key  value
# 0 2017-05-20 00:00:00   a    0.0
# 1 2017-05-20 00:00:00   b    1.0
# 2 2017-05-20 00:00:00   c    2.0
# 3 2017-05-20 00:01:00   a    3.0
# 4 2017-05-20 00:01:00   b    4.0
# 5 2017-05-20 00:01:00   c    5.0
# 6 2017-05-20 00:02:00   a    6.0

# 要对每个key值进行相同的重采样，我们引入pandas.Grouper对象：
# time_key = pd.Grouper('5min')
# 我们然后设定时间索引，用key和time_key分组，然后聚合：
# 这里没有运行成功
# resampled = (df2.set_index('time')
#              .groupby(['key' , time_key])
#              .sum())
#
# # 使用TimeGrouper的限制是时间必须是Series或DataFrame的索引
#
#
# ### 12.3 方法链技术
#
# # 当对数据集进行一系列变换时，你可能发现创建的多个临时变量
# # 其实并没有在分析中用到。看下面的例子：
# # df = load_data()
# # df2 = df[df['col2'] < 0]
# # df2['col1_demeaned'] = df2['col1'] - df2['col1'].mean()
# # result = df2.groupby('key').col1_demeaned.std()
#
# # DataFrame.assign方法是一个df[k] = v形式的函数式的列分配方法。
# # 他不是就地修改对象，而是返回一个新的修改过的DataFrame.下边的语句与上边的等价
# # Usual non-functional way
# df2 = df.copy()
# df2['k'] = v
#
# # Functional assign way
# df2 = df.assign(k=v)
#
# # 就地分配可能会比assign快，但是assign可以方便的进行链式编程：
# result = (df2.assign(col1_demeaned = df2.col1 - df2.col2.mean())
#           .groupby('key')
#           .col1_demeaned.std())
#
# df = load_data()
# df2 = df[df['col2']< 0]
# # 可以重写为：
# df = (load_data()
#       [lambda x:x['col2'] < 0])
# # 这里，load_data的结果没有赋值给某个变量，因此传递到[]的函数在这一步被绑定到了对象
# # 我们可以把整个过程写为一个单链表达式
# result = (load_data()
#           [lambda x:x.col2 < 0]
#             .assign(col1_demeaned = lambda x:x.col1 - x.col1.mean())
#           .groupby('key')
#           .col1_demeaned.std())


### 12.3.1 pipe方法 管道方法





