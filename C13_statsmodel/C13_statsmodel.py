"""

    作者：大发
    日期：2019/12/19
    内容：利用python进行数据分析 13.1 p364 笔记

"""

import pandas as pd
import numpy as np
import patsy
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


## 13.1 pandas 与建模代码的结合

## 机器学习中，特征工程是模型开发的重要部分之一。
# 特征工程是指从原生数据集中提取可用于模型上下文的有效信息的数据转换过程或分析。
# pandas与其他分析库的结合点通常是numpy数组。
# 将DataFrame转换为NumPy数组，可以使用.values属性
# data = pd.DataFrame({
#     'x0':[1,2,3,4,5],
#     'x1':[0.01,-0.01 , 0.25 , -4.1 , 0.],
#     'y': [-1.5 , 0. , 3.6 , 1.3 , -2.]
# })
# data
# Out[24]:
#    x0    x1    y
# 0   1  0.01 -1.5
# 1   2 -0.01  0.0
# 2   3  0.25  3.6
# 3   4 -4.10  1.3
# 4   5  0.00 -2.0
# data.columns
# Out[26]: Index(['x0', 'x1', 'y'], dtype='object')
# data.values
# Out[27]:
# array([[ 1.  ,  0.01, -1.5 ],
#        [ 2.  , -0.01,  0.  ],
#        [ 3.  ,  0.25,  3.6 ],
#        [ 4.  , -4.1 ,  1.3 ],
#        [ 5.  ,  0.  , -2.  ]])

## 要换成DataFrame，可以传递一个二维ndarray,可带有列名：
# df2 = pd.DataFrame(data.values , columns = ['one' , 'two' , 'three'])
# df2
# Out[29]:
#    one   two  three
# 0  1.0  0.01   -1.5
# 1  2.0 -0.01    0.0
# 2  3.0  0.25    3.6
# 3  4.0 -4.10    1.3
# 4  5.0  0.00   -2.0
## 当数据是均匀的时候使用.values属性，比如当数据全是数值类型。
# 如果数据是不均匀的，结果会是Python对象的ndarray:
# df3 = data.copy()
# df3['strings'] = ['a' ,'b' ,'c' ,'d' ,'e']
# df3
# Out[32]:
#    x0    x1    y strings
# 0   1  0.01 -1.5       a
# 1   2 -0.01  0.0       b
# 2   3  0.25  3.6       c
# 3   4 -4.10  1.3       d
# 4   5  0.00 -2.0       e
# df3.values
# Out[35]:
# array([[1, 0.01, -1.5, 'a'],
#        [2, -0.01, 0.0, 'b'],
#        [3, 0.25, 3.6, 'c'],
#        [4, -4.1, 1.3, 'd'],
#        [5, 0.0, -2.0, 'e']], dtype=object)

## 对于一些模型，你可能只想使用列的子集。
# 建议使用loc， 用values作索引：
# model_col = ['x0' , 'x1']
# data.loc[: , model_col].values
# Out[37]:
# array([[ 1.  ,  0.01],
#        [ 2.  , -0.01],
#        [ 3.  ,  0.25],
#        [ 4.  , -4.1 ],
#        [ 5.  ,  0.  ]])

# 假设数据集中有一个非数值列
# data['category'] = pd.Categorical(['a' ,'b' ,'a' ,'a','b'],categories=['a' ,'b'])
# data
# Out[39]:
#    x0    x1    y category
# 0   1  0.01 -1.5        a
# 1   2 -0.01  0.0        b
# 2   3  0.25  3.6        a
# 3   4 -4.10  1.3        a
# 4   5  0.00 -2.0        b

# 如果我想用虚拟变量替换“category”列 ， 可以先创建虚拟变量，
# 之后删除“category”列，然后联结结果。

# dummies = pd.get_dummies(data.category , prefix='category')
# data_with_dummies = data.drop('category' , axis = 1).join(dummies)
# data_with_dummies
# Out[42]:
#    x0    x1    y  category_a  category_b
# 0   1  0.01 -1.5           1           0
# 1   2 -0.01  0.0           0           1
# 2   3  0.25  3.6           1           0
# 3   4 -4.10  1.3           1           0
# 4   5  0.00 -2.0           0           1



## 13.2 用Patsy创建模型描述

# Patsy 使用简短的字符串公式语法描述统计模型（尤其是线性模型），例如：
# y ~ x0 + x1
# 语法a+b不代表a加b，而是指为模型而创建的设计矩阵中的名词列
# patsy.dmatrices在数据集上使用了一个公式字符串，并未一个线性模型创建一个设计矩阵：
# data = pd.DataFrame({
#     'x0':[1,2,3,4,5],
#     'x1':[0.01,-0.01,0.25,-4.1,0.],
#     'y':[-1.5,0.,3.6,1.3,-2.]
# })
# data
# Out[44]:
#    x0    x1    y
# 0   1  0.01 -1.5
# 1   2 -0.01  0.0
# 2   3  0.25  3.6
# 3   4 -4.10  1.3
# 4   5  0.00 -2.0

# import patsy
# y , X = patsy.dmatrices('y ~ x0 + x1',data)
# y
# Out[48]:
# DesignMatrix with shape (5, 1)
#      y
#   -1.5
#    0.0
#    3.6
#    1.3
#   -2.0
#   Terms:
#     'y' (column 0)

# X
# Out[49]:
# DesignMatrix with shape (5, 3)
#   Intercept  x0     x1
#           1   1   0.01
#           1   2  -0.01
#           1   3   0.25
#           1   4  -4.10
#           1   5   0.00
#   Terms:
#     'Intercept' (column 0)
#     'x0' (column 1)
#     'x1' (column 2)
## 这些Patsy的DesignMatrix的实例是NumPython的ndarray,带有附加元数据：
# np.asarray(y)
# Out[50]:
# array([[-1.5],
#        [ 0. ],
#        [ 3.6],
#        [ 1.3],
#        [-2. ]])
# np.asarray(X)
# Out[51]:
# array([[ 1.  ,  1.  ,  0.01],
#        [ 1.  ,  2.  , -0.01],
#        [ 1.  ,  3.  ,  0.25],
#        [ 1.  ,  4.  , -4.1 ],
#        [ 1.  ,  5.  ,  0.  ]])

## Intercept列(截距)是线性模型的惯例用法。添加 +0 到模型中，就不会显示这列：

# patsy.dmatrices('y ~ x0 + x1 + 0' , data)[1]
# Out[52]:
# DesignMatrix with shape (5, 2)
#   x0     x1
#    1   0.01
#    2  -0.01
#    3   0.25
#    4  -4.10
#    5   0.00
#   Terms:
#     'x0' (column 0)
#     'x1' (column 1)


## patsy对象可以直接传递到算法中（比如numpy.linalg.lstsq） ，
# 它执行普通的最小二乘回归：
# coef, resid, _, _ = np.linalg.lstsq(X , y ,rcond=-1)
## 模型的元数据保留在design_info属性中 ，
# 因此可以重新附加模型列名到拟合系数以获得一个Series，例如：
# coef
# Out[55]:
# array([[ 0.31290976],
#        [-0.07910564],
#        [-0.26546384]])
# coef = pd.Series(coef.squeeze() , index=X.design_info.column_names)
# coef
# Out[57]:
# Intercept    0.312910
# x0          -0.079106
# x1          -0.265464
# dtype: float64

##13.2.1 用Patsy公式进行数据转换

## python代码可以混合到你的Patsy公式中，执行公式时，
# Patsy库将尝试在封闭的作用域中寻找你使用的函数
# y , X = patsy.dmatrices('y ~ x0 + np.log(np.abs(x1) + 1)' , data)
# X
# Out[59]:
# DesignMatrix with shape (5, 3)
#   Intercept  x0  np.log(np.abs(x1) + 1)
#           1   1                 0.00995
#           1   2                 0.00995
#           1   3                 0.22314
#           1   4                 1.62924

## 常见的变量转换包括标准化（平均值为0，方差为1）和中心化（减去平均值）
## Patsy中有内置函数：
# y , X = patsy.dmatrices('y ~ standardize(x0) + center(x1)',data)
# In[62]: X
# Out[62]:
# DesignMatrix with shape (5, 3)
#   Intercept  standardize(x0)  center(x1)
#           1         -1.41421        0.78
#           1         -0.70711        0.76
#           1          0.00000        1.02
#           1          0.70711       -3.33
#           1          1.41421        0.77
#   Terms:
#     'Intercept' (column 0)
#     'standardize(x0)' (column 1)
#     'center(x1)' (column 2)

## 作为建模的一部分，需要在一个数据集上拟合另外一个数据集，之后基于另一个模型评价该模型。
# 这个过程可以保留部分数据或者之后再加入新数据。
# 基于新数据使用模型进行预测时要小心。
# 这些转换是有状态的转换，因为在形成新数据集时必须使用原数据集中的均值或标准差等统计值。

# patsy.build_design_matrices可以使原始样本内数据集中保存的信息
# 将变换应用于新的样本外数据上：
# new_data = pd.DataFrame({
#     'x0':[6,7,8,9],
#     'x1':[3.1,-0.5,0,2.3],
#     'y':[1,2,3,4]
# })
# new_X = patsy.build_design_matrices([X.design_info],new_data)
# new_X
# Out[65]:
# [DesignMatrix with shape (4, 3)
#    Intercept  standardize(x0)  center(x1)
#            1          2.12132        3.87
#            1          2.82843        0.27
#            1          3.53553        0.77
#            1          4.24264        3.07
#    Terms:
#      'Intercept' (column 0)
#      'standardize(x0)' (column 1)
#      'center(x1)' (column 2)]

## 因为Patsy中的加号不是加法的意义，当你按照名称将数据集的列相加时，
## 你必须用特殊I函数将他们封装起来：
# In[66]: y , X = patsy.dmatrices('y ~ I(x0 + x1)' , data)
# In[67]: X
# Out[67]:
# DesignMatrix with shape (5, 2)
#   Intercept  I(x0 + x1)
#           1        1.01
#           1        1.99
#           1        3.25
#           1       -0.10
#           1        5.00
#   Terms:
#     'Intercept' (column 0)
#     'I(x0 + x1)' (column 1)

## Patsy的patsy.builtins模块还有一些其他的内置置换。

## 13.2.2 分类数据与Patsy
## 当在Patsy公式中使用非数值数据时，他们会默认转换为虚拟变量。
##如果有截距，会去掉一个，避免共线性：
# data = pd.DataFrame({
#     'key1':['a','a','b','b','a','b','a','b'],
#     'key2':[0,1,0,1,0,1,0,0],
#     'v1':[1,2,3,4,5,6,7,8],
#     'v2':[-1,0,2.5,-0.5,4.0,-1.2,0.2,-1.7]
# })
#
# y , X =patsy.dmatrices('v2 ~ key1',data)
# X
# Out[69]:
# DesignMatrix with shape (8, 2)
#   Intercept  key1[T.b]
#           1          0
#           1          0
#           1          1
#           1          1
#           1          0
#           1          1
#           1          0
#           1          1
#   Terms:
#     'Intercept' (column 0)
#     'key1' (column 1)

## 如果选择不显示截距列，每个分类值的列都会包括在设计矩阵的模型中：
# y , X =patsy.dmatrices('v2 ~ key1+0',data)
# X
# Out[6]:
# DesignMatrix with shape (8, 2)
#   key1[a]  key1[b]
#         1        0
#         1        0
#         0        1
#         0        1
#         1        0
#         0        1
#         1        0
#         0        1
#   Terms:
#     'key1' (columns 0:2)

### 使用C函数，数值列可以截取分类量
# y , X = patsy.dmatrices('v2 ~ C(key2)' , data)
# X
# Out[8]:
# DesignMatrix with shape (8, 2)
#   Intercept  C(key2)[T.1]
#           1             0
#           1             1
#           1             0
#           1             1
#           1             0
#           1             1
#           1             0
#           1             0
#   Terms:
#     'Intercept' (column 0)
#     'C(key2)' (column 1)

## 当在模型中使用多个分类名，事情就会变复杂，
# 因为会包括key1:key2形式的相交部分，它可以用在方差分析模型中：




### 13.3 statsmodels介绍

## statsmodels的线性模型有两种不同的接口：基于数组和基于公式。
# 它们可以通过API模块引入：

import statsmodels.api as sm
import statsmodels.formula.api as smf

# def dnorm(mean,variance , size=1):
#     if isinstance(size, int):
#         size = size
#     return mean+np.sqrt(variance)*np.random.randn(*size)
#
# # for reproducibility
# np.random.seed(12345)
#
# N=100
#
# X = np.c_[dnorm(0,0.4,size=N),
# dnorm(0,0.6,size=N),
# dnorm(0,0.2,size=N)]
#
# eps = dnorm(0,0.1,size=N )
# beta = [0.1 , 0.3 , 0.5]
# y = np.dot(X , beta) + eps
#
# 这里，我使用了“真实”模型和可知参数beta。
# 此时，dnorm可用来生成正态分布数据，带有特定均值和方差。









