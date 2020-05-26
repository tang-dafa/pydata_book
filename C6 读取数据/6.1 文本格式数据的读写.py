"""
    时间：2019/10/2
    作者：大发
    内容：第六章笔记
"""

import pandas as pd
from pandas import Series,DataFrame
import numpy as np
#
# !type "D:\ex1.csv"             # windows下导入数据
# ﻿a,b,c,d,message
# 1,2,3,4,hello
# 5,6,7,8,world
# 9,10,11,12,foo

# df = pd.read_csv('D:\ex1.csv')      # 读入一个dataframe
# df
# Out[5]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo
# pd.read_table('D:\ex1.csv' , sep = ',')      # 用table打开，用 ， 分割
# C:\Program Files\JetBrains\PyCharm Community Edition 2019.1.3\helpers\pydev\pydevconsole.py:1: FutureWarning: read_table is deprecated, use read_csv instead.
#   '''
# Out[6]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo

# !type "D:\ex2.csv"
# ﻿1,2,3,4,hello
# 5,6,7,8,world
# 9,10,11,12,foo
# pd.read_csv('D:\ex2.csv' , header = None)       ## 加上头
# Out[9]:
#    0   1   2   3      4
# 0  1   2   3   4  hello
# 1  5   6   7   8  world
# 2  9  10  11  12    foo

# pd.read_csv('D:\ex2.csv' , names = ['a' , 'b' , 'c' , 'd' , 'message'])
# Out[10]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo
# names = ['a' , 'b' , 'c' , 'd' , 'message']
# pd.read_csv('D:\ex2.csv' , names = names , index_col = 'message')   # 指定一个为索引
# Out[12]:
#          a   b   c   d
# message
# hello    1   2   3   4
# world    5   6   7   8
# foo      9  10  11  12


# !type "D:\csv_mindex.csv"
# ﻿key1,key2,value1,value2
# one,a,1,2
# one,b,3,4
# one,c,5,6
# one,d,7,8
# two,a,9,10
# two,b,11,12
# two,c,13,14
# two,d,15,16
# parsed = pd.read_csv('D:\csv_mindex.csv', index_col = ['key1','key2']) # 分层索引
# parsed
# Out[15]:
#            value1  value2
# key1 key2
# one  a          1       2
#      b          3       4
#      c          5       6
#      d          7       8
# two  a          9      10
#      b         11      12
#      c         13      14
#      d         15      16

# !type "D:\ex4.csv"
# ﻿##h,,,,
# a,b,c,d,message
# ####dgyj ,,,,
# ###ttyu,,,,
# 1,2,3,4,hello
# 5,6,7,8,world
# 9,10,11,12,foo
#
# pd.read_csv('D:\ex4.csv', skiprows = [0,2,3])   ## skiprows 用来跳过不要的行
# Out[19]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo


# !type "D:\ex5.csv"
# ﻿something,a,b,c,d,message
# one,1,2,3,4,                        # 这里有一个不显示的缺失值
# two,5,6,7,8,world
# three,9,10,11,12,foo
# result = pd.read_csv('D:\ex5.csv')
# result
# Out[22]:
#   something  a   b   c   d message
# 0       one  1   2   3   4     NaN
# 1       two  5   6   7   8   world
# 2     three  9  10  11  12     foo
# pd.isnull(result)                              ## 布尔值辨认是否为 缺失值
# Out[23]:
#    something      a      b      c      d  message
# 0      False  False  False  False  False     True
# 1      False  False  False  False  False    False
# 2      False  False  False  False  False    False

# result = pd.read_csv('D:\ex5.csv' , na_values = ['NULL'])
# result
# Out[25]:
#   something  a   b   c   d message
# 0       one  1   2   3   4     NaN
# 1       two  5   6   7   8   world
# 2     three  9  10  11  12     foo
# sentinels = {'message':['foo', 'NA'] , 'something':['two']}      ## 指定缺失值
# pd.read_csv('D:\ex5.csv' , na_values = sentinels)
# Out[27]:
#   something  a   b   c   d message
# 0       one  1   2   3   4     NaN
# 1       NaN  5   6   7   8   world
# 2     three  9  10  11  12     NaN



###    6.1.1 分块读取文本文件

# pd.options.display.max_rows = 10          ## 这句可以让数据的显示更紧凑
# result = pd.read_csv('D:\examples\ex6.csv')
# result
# Out[32]:
#            one       two     three      four key
# 0     0.467976 -0.038649 -0.295344 -1.824726   L
# 1    -0.358893  1.404453  0.704965 -0.200638   B
# 2    -0.501840  0.659254 -0.421691 -0.057688   G
# 3     0.204886  1.074134  1.388361 -0.982404   R
# 4     0.354628 -0.133116  0.283763 -0.837063   Q
#         ...       ...       ...       ...  ..
# 9995  2.311896 -0.417070 -1.409599 -0.515821   L
# 9996 -0.479893 -0.650419  0.745152 -0.646038   E
# 9997  0.523331  0.787112  0.486066  1.093156   K
# 9998 -0.362559  0.598894 -1.843201  0.887292   G
# 9999 -0.096376 -1.012999 -0.657431 -0.573315   0
# [10000 rows x 5 columns]


# pd.read_csv('D:\examples\ex6.csv', nrows = 5)    ## 读取一小部分的行 ，指定 nrows
# Out[33]:
#         one       two     three      four key
# 0  0.467976 -0.038649 -0.295344 -1.824726   L
# 1 -0.358893  1.404453  0.704965 -0.200638   B
# 2 -0.501840  0.659254 -0.421691 -0.057688   G
# 3  0.204886  1.074134  1.388361 -0.982404   R
# 4  0.354628 -0.133116  0.283763 -0.837063   Q


# chunker = pd.read_csv('D:\examples\ex6.csv' , chunksize = 1000)
# chunker
# Out[4]: <pandas.io.parsers.TextFileReader at 0x45dfd90>   # 指定chunksize为每一块的行数
# chunker = pd.read_csv('D:\examples\ex6.csv' , chunksize = 1000)
# tot = pd.Series([])
# for piece in chunker :
#     tot = tot.add(piece['key'].value_counts() , fill_value=0)      #  对k列聚合获得技术值
# tot = tot.sort_values(ascending = False)
# tot[:10]
# Out[8]:
# E    368.0
# X    364.0
# L    346.0
# O    343.0
# Q    340.0
# M    338.0
# J    337.0
# F    335.0
# K    334.0
# H    330.0
# dtype: float64


##  6.1.2 将数据写入文本格式

# data = pd.read_csv('D:\examples\ex5.csv')
# data
# Out[10]:
#   something  a   b     c   d message
# 0       one  1   2   3.0   4     NaN
# 1       two  5   6   NaN   8   world
# 2     three  9  10  11.0  12     foo
# data.to_csv('D:\examples\ex_out.csv')   # to_csv 将数据导出成逗号分隔的数据，但这种方法缺失值没有被标出
# !type "D:\examples\ex_out.csv"
# ,something,a,b,c,d,message
# 0,one,1,2,3.0,4,
# 1,two,5,6,,8,world
# 2,three,9,10,11.0,12,foo
# data.to_csv('D:\examples\ex_out1.csv' , na_rep = 'NULL')   ## na_rep 用来标志缺失值
# !type "D:\examples\ex_out1.csv"
# ,something,a,b,c,d,message
# 0,one,1,2,3.0,4,NULL
# 1,two,5,6,NULL,8,world
# 2,three,9,10,11.0,12,foo
# data.to_csv('D:\examples\ex_out2.csv' , na_rep = 'NULL', index = False , header = False ) # 也可以控制标题行、索引是否被写入
# !type "D:\examples\ex_out2.csv"
# one,1,2,3.0,4,NULL
# two,5,6,NULL,8,world
# three,9,10,11.0,12,foo
# data.to_csv('D:\examples\ex_out3.csv' , na_rep = 'NULL', index = False , columns = ['a' , 'b'] )  # 控制要写入的列
# !type "D:\examples\ex_out3.csv"
# a,b
# 1,2
# 5,6
# 9,10

## 6.1.3 使用分隔符 P174

# import pandas as pd
# from pandas import Series, DataFrame
# import numpy as np
# !type
# "D:\examples\ex7.csv"
# "a", "b", "c"
# "1", "2", "3"
# "1", "2", "3"
# import csv

# f = open("D:\examples\ex7.csv")
# reader = csv.reader(f)
# for line in reader:
#     print(line)
#
# ['a', 'b', 'c']
# ['1', '2', '3']
# ['1', '2', '3']


# with open("D:\examples\ex7.csv") as f:
#     lines = list(csv.reader(f))
#
# header, values = lines[0], lines[:1]            # 分出头和值
# data_dict = {h: v for h, v in zip(header, zip(*values))}                # ，生成一个字典，把行转成列
# data_dict
# Out[12]: {'a': ('a',), 'b': ('b',), 'c': ('c',)}
# header, values = lines[0], lines[1:]
# data_dict = {h: v for h, v in zip(header, zip(*values))}
# data_dict
# Out[13]: {'a': ('1', '1'), 'b': ('2', '2'), 'c': ('3', '3')}

# class my_dialect(csv.Dialect):            # 用来定义一个简单的子类
#     lineterminator = '\n'
#     delimiter = ';'
#     quotechar = '"'
#     quoting = csv.QUOTE_MINIMAL
# reader = csv.reader(f , dialect = my_dialect)
# reader = csv.reader(f , dialect ='|')


# 6.1.4 JSON P176

# obj = """
# {"name":"Wes",
# "places_lived":["United States" , "Spain" , "Germany"],
# "pet" : null
# "siblings":[{"name":"Scott" , "age" :30 , "pet":["Zeus","Zuke"]},
# {"name":"Katie" , "age" :38,
# "pet":["Zeus","Zuke"]}]
# """
import json
result = json.loads(obj)          # 将JSON字符串转换为python形式
result


















