"""
    时间：2019/9/30
    作者：大发
    内容：第五章笔记
"""


#### Series 是一个一维数组，并包含数据标签，能够自动对齐索引
# import pandas as pd
# from pandas import Series,DataFrame
# obj = pd.Series([4,7,-5,3])
# obj
# Out[5]:               ##第一列是index
# 0    4
# 1    7
# 2   -5
# 3    3
# dtype: int64
# obj.values               ## 拿到值
# Out[6]: array([ 4,  7, -5,  3], dtype=int64)
# obj.index                 ## 拿到标签
# Out[7]: RangeIndex(start=0, stop=4, step=1)

## 用语句给标签命名
# obj2 = pd.Series([4,7,-5,3], index = ['d','b','a','c'])
# obj2
# Out[9]:
# d    4
# b    7
# a   -5
# c    3
# dtype: int64
# obj2.index
# Out[10]: Index(['d', 'b', 'a', 'c'], dtype='object')

# obj2['a']
# Out[11]: -5
# obj2[['a','b']]    ##这里一定记得是两个中括号
# Out[13]:
# a   -5
# b    7
# dtype: int64

#### nummpy 风格的数学操作，也可以用，操作时带着索引
# obj2[obj2>0]
# Out[14]:
# d    4
# b    7
# c    3
# dtype: int64
# obj2*2
# Out[15]:
# d     8
# b    14
# a   -10
# c     6
# dtype: int64
# import numpy as np
# np.exp(obj2)         ### numpy 的算法
# Out[18]:
# d      54.598150
# b    1096.633158
# a       0.006738
# c      20.085537
# dtype: float64
# 'b' in obj2           布尔值查索引
# Out[19]: True
# 'e' in obj2
# Out[20]: False

## 把一个字典转换成Series
# sdata = {'Ohio': 3500 , 'Texas': 71000 , 'Oregon':16000 , 'Utah': 5000}
# obj3 = pd.Series(sdata)
# obj3
# Out[23]:
# Ohio       3500
# Texas     71000
# Oregon    16000
# Utah       5000
# dtype: int64

## 指定索引
# states = ['California', 'Ohio','Oregon', 'Texas']
# obj4 = pd.Series(sdata, index= states)
# obj4
# Out[26]:
# California        NaN             ## 标记缺失值
# Ohio           3500.0
# Oregon        16000.0
# Texas         71000.0
# dtype: float64
## isnull 和 notnull 用来检查缺失值
# pd.isnull(obj4)
# Out[27]:
# California     True
# Ohio          False
# Oregon        False
# Texas         False
# dtype: bool
# pd.notnull(obj4)
# Out[28]:
# California    False
# Ohio           True
# Oregon         True
# Texas          True
# dtype: bool
# obj4.notnull()
# Out[29]:
# California    False
# Ohio           True
# Oregon         True
# Texas          True
# dtype: bool

## 给整个数据命名，以及给索引列命名
# obj4.name = 'population'
# obj4.index.name = 'state'
# obj4
# Out[32]:
# state
# California        NaN
# Ohio           3500.0
# Oregon        16000.0
# Texas         71000.0
# Name: population, dtype: float64

##  索引按位置赋值
# obj.index = ['Bob' , 'Steve' , 'Jeff' , 'Ryan']
# obj
# Out[35]:
# Bob      4
# Steve    7
# Jeff    -5
# Ryan     3
# dtype: int64



###  DataFrame
## 这个是一个二维块， 每一个列可以是不同的值类别，既有行索引，也有列索引
# data = {'state' : ['Ohio' , 'Ohio' , 'Ohio' , 'Nevada' , 'Nevada' , 'Nevada'] , 'year' : [2000, 2001 , 2002 , 2001 , 2002 , 2003] , 'pop' : [1.5 , 1.7 , 3.6 , 2.4 ,2.9 , 3.2]}
# frame = pd.DataFrame(data)   ## 自动分配索引， 按照排列的顺序排列
# frame
# Out[39]:
#     state  year  pop
# 0    Ohio  2000  1.5
# 1    Ohio  2001  1.7
# 2    Ohio  2002  3.6
# 3  Nevada  2001  2.4
# 4  Nevada  2002  2.9
# 5  Nevada  2003  3.2

# frame.head()                       ## .head() 的方法可以选出头部的前5行
# Out[40]:
#     state  year  pop
# 0    Ohio  2000  1.5
# 1    Ohio  2001  1.7
# 2    Ohio  2002  3.6
# 3  Nevada  2001  2.4
# 4  Nevada  2002  2.9
# pd.DataFrame(data , columns = ['year' , 'state' , 'pop'])  # 可以按指定的索引顺序排列
# Out[41]:
#    year   state  pop
# 0  2000    Ohio  1.5
# 1  2001    Ohio  1.7
# 2  2002    Ohio  3.6
# 3  2001  Nevada  2.4
# 4  2002  Nevada  2.9
# 5  2003  Nevada  3.2

# frame2 = pd.DataFrame(data , columns = ['year' , 'state' , 'pop' , 'debt'] , index = ['one' , 'two' , 'three' , 'four' , 'five' , 'six'])
# frame2
# Out[43]:
#        year   state  pop debt           ##  如果传入的列，不在字典中，会显示缺失值
# one    2000    Ohio  1.5  NaN
# two    2001    Ohio  1.7  NaN
# three  2002    Ohio  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN
# six    2003  Nevada  3.2  NaN

# frame.columns
# Out[45]: Index(['state', 'year', 'pop'], dtype='object')
# frame2['state']         ##  可以按标记索引
# Out[46]:
# one        Ohio
# two        Ohio
# three      Ohio
# four     Nevada
# five     Nevada
# six      Nevada
# Name: state, dtype: object

# frame2.year               ## 不同的索引方法
# Out[47]:
# one      2000
# two      2001
# three    2002
# four     2001
# five     2002
# six      2003
# Name: year, dtype: int64

##  frame2['state'] 对任意的列名有效， frame2.year  只有在列名是有效的情况下才有效

## 用 .loc 获取行
# frame2.loc['three']   ## 注意是中括号
# Out[51]:
# year     2002
# state    Ohio
# pop       3.6
# debt      NaN
# Name: three, dtype: object


###  修改列的值
# frame2['debt'] = 16.5             ##  修改一列为同一个数值
# frame2
# Out[53]:
#        year   state  pop  debt
# one    2000    Ohio  1.5  16.5
# two    2001    Ohio  1.7  16.5
# three  2002    Ohio  3.6  16.5
# four   2001  Nevada  2.4  16.5
# five   2002  Nevada  2.9  16.5
# six    2003  Nevada  3.2  16.5

# frame2['debt'] = np.arange(6)             # 修改一列为，从0-5
# frame2
# Out[55]:
#        year   state  pop  debt
# one    2000    Ohio  1.5     0
# two    2001    Ohio  1.7     1
# three  2002    Ohio  3.6     2
# four   2001  Nevada  2.4     3
# five   2002  Nevada  2.9     4
# six    2003  Nevada  3.2     5

## 这样赋值的话， 缺失值会自动填充
# val = pd.Series([-1.2 , -1.5 , -1.7] , index = ['two' , 'four' , 'five'])
# frame2['debt'] = val
# frame2
# Out[58]:
#        year   state  pop  debt
# one    2000    Ohio  1.5   NaN
# two    2001    Ohio  1.7  -1.2
# three  2002    Ohio  3.6   NaN
# four   2001  Nevada  2.4  -1.5
# five   2002  Nevada  2.9  -1.7
# six    2003  Nevada  3.2   NaN

# frame2['eastern'] = frame2.state == 'Ohio'        # 创建了一个新的列，布尔值，相比之下，frame2.eastern这个方法是不能建立新的列的
# frame2
# Out[60]:
#        year   state  pop  debt  eastern
# one    2000    Ohio  1.5   NaN     True
# two    2001    Ohio  1.7  -1.2     True
# three  2002    Ohio  3.6   NaN     True
# four   2001  Nevada  2.4  -1.5    False
# five   2002  Nevada  2.9  -1.7    False
# six    2003  Nevada  3.2   NaN    False
# del frame2['eastern']                                 # 删除eastern 这一列
# frame2.columns
# Out[62]: Index(['year', 'state', 'pop', 'debt'], dtype='object')

##  字典的嵌套 ， 外部字典的键为列，内部字典的键为行索引
# pop = {'Nevada' : {2001:2.4 , 2002:2.9}, 'Ohio' : {2000:1.5 , 2001:1.7 , 2002:3.6}}
# frame3 = pd.DataFrame(pop)
# frame3
# Out[65]:
#       Nevada  Ohio
# 2000     NaN   1.5
# 2001     2.4   1.7
# 2002     2.9   3.6

# frame3.T             ##  行列转置
# Out[66]:
#         2000  2001  2002
# Nevada   NaN   2.4   2.9
# Ohio     1.5   1.7   3.6

# pd.DataFrame(pop , index = [2001, 2002, 2003])  ## 指明索引的话， 内部字典的键就不会被自动的排序
# Out[67]:
#       Nevada  Ohio
# 2001     2.4   1.7
# 2002     2.9   3.6
# 2003     NaN   NaN

# pdata = {'Ohio' : frame3['Ohio'][:-1] , 'Nevada':frame3['Nevada'][:2]}  #可以构造DataFrame
# pd.DataFrame(pdata)
# Out[69]:
#       Ohio  Nevada
# 2000   1.5     NaN
# 2001   1.7     2.4

# frame3.index.name = 'year' ; frame3.columns.name = 'state'  加行、列标签
# frame3
# Out[71]:
# state  Nevada  Ohio
# year
# 2000      NaN   1.5
# 2001      2.4   1.7
# 2002      2.9   3.6
# frame3.values      ## 这样可以返回一个 二维ndarray
# Out[72]:
# array([[nan, 1.5],
#        [2.4, 1.7],
#        [2.9, 3.6]])

# frame2.values                 ##  列的属性不同时，values 会自动适配
# Out[74]:
# array([[2000, 'Ohio', 1.5, nan],
#        [2001, 'Ohio', 1.7, -1.2],
#        [2002, 'Ohio', 3.6, nan],
#        [2001, 'Nevada', 2.4, -1.5],
#        [2002, 'Nevada', 2.9, -1.7],
#        [2003, 'Nevada', 3.2, nan]], dtype=object)

###  5.1.3 索引对象

# obj = pd.Series(range(3) , index = ['a' , 'b' , 'c'])
# index=obj.index
# index
# Out[77]: Index(['a', 'b', 'c'], dtype='object')
# index[1:]
# Out[78]: Index(['b', 'c'], dtype='object')
# 索引对象不可变

# labels = pd.Index(np.arange(3))   # 命名标签
# labels
# Out[80]: Int64Index([0, 1, 2], dtype='int64')
# obj2 = pd.Series([1.5 , -2.5 , 0] , index = labels)      #加入数据
# obj2
# Out[82]:
# 0    1.5
# 1   -2.5
# 2    0.0
# dtype: float64
# obj2.index is labels   # 检验标签
# Out[83]: True

# 索引对象还是一个大小固定的集合
# frame3.columns
# Out[85]: Index(['Nevada', 'Ohio'], dtype='object', name='state')
# 'Ohio' in frame3.columns
# Out[86]: True
# 2003 in frame3.index
# Out[87]: False

## pandas 可以有重复标签
# dup_labels = pd.Index(['foo' , 'foo' , 'bar' , 'bar'])
# dup_labels
# Out[89]: Index(['foo', 'foo', 'bar', 'bar'], dtype='object')









