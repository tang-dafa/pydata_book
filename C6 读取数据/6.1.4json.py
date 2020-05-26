"""
    作者：大发
    日期：2019/11/12
    内容：利用python进行数据分析 6.1.4 p176 笔记
    备注：前方内容在 C:\Users\lenovo\Anaconda3
"""

# import json
#
# obj = """
# {"name":"Wes",
# "places_lived":["United States" , "Spain" , "Germany"] ,
# "pet":null ,
# "siblings" : [{"name": "Scott" , "age" : 30 , "pet" : ["Zeus" ,"Zuko" ]},
#               {"name": "Katie" , "age" : 38 , "pet" : ["Sixes" ,"Stache" , "Cisco" ]}]
# }"""
#
# result = json.loads(obj)
# result
# Out[5]:
# {'name': 'Wes',
#  'places_lived': ['United States', 'Spain', 'Germany'],
#  'pet': None,
#  'siblings': [{'name': 'Scott', 'age': 30, 'pet': ['Zeus', 'Zuko']},
#   {'name': 'Katie', 'age': 38, 'pet': ['Sixes', 'Stache', 'Cisco']}]}
#
#
# import pandas as pd
# asjson = json.dumps(result)
# siblings = pd.DataFrame(result['siblings'] , columns = ['name' , 'age'])
# siblings
# Out[11]:
#     name  age
# 0  Scott   30
# 1  Katie   38


# !type "D:\data_py\pydata-book-2nd-edition\examples\example.json"
# Out[11]:
# [{"a": 1, "b": 2, "c": 3},
#  {"a": 4, "b": 5, "c": 6},
#  {"a": 7, "b": 8, "c": 9}]
#
# data = pd.read_json('D:\data_py\pydata-book-2nd-edition\examples\example.json')
#
# data
# Out[14]:
#    a  b  c
# 0  1  2  3
# 1  4  5  6
# 2  7  8  9
#
# print (data.to_json())
# {"a":{"0":1,"1":4,"2":7},"b":{"0":2,"1":5,"2":8},"c":{"0":3,"1":6,"2":9}}
#
# print(data.to_json(orient = 'records'))
# [{"a":1,"b":2,"c":3},{"a":4,"b":5,"c":6},{"a":7,"b":8,"c":9}]


# 6.1.5 XML和HTML：网络抓取

# tables = pd.read_html('D:\data_py\pydata-book-2nd-edition\examples\dic_failed_bank_list.html')
# len(tables)
# Out[22]: 1
# failures = tables[0]
# failures.head()
# Out[24]:
#                       Bank Name  ...       Updated Date
# 0                   Allied Bank  ...  November 17, 2016
# 1  The Woodbury Banking Company  ...  November 17, 2016
# 2        First CornerStone Bank  ...  September 6, 2016
# 3            Trust Company Bank  ...  September 6, 2016
# 4    North Milwaukee State Bank  ...      June 16, 2016
# [5 rows x 7 columns]
# close_timestamp = pd.to_datetime(failures['Closing Date'])
# close_timestamp.dt.year.value_counts()
# Out[27]:
# 2010    157
# 2009    140
# 2011     92
# 2012     51
# 2008     25
# 2013     24
# 2014     18
# 2002     11
# 2015      8
# 2016      5
# 2004      4
# 2001      4
# 2007      3
# 2003      3
# 2000      2
# Name: Closing Date, dtype: int64

# 6.1.5.1 使用lxml.objectify 解析XML

# 使用lxml从更为通用的XML格式解析数据
#
# from lxml import objectify
#
# path = 'D:\data_py\pydata-book-2nd-edition\datasets\mta_perf\Performance_MNR.xml'
# parsed = objectify.parse(open(path))
# root = parsed.getroot
# data = []
# skip_fields = ['PARENT_SEQ' , 'INDICATOR_SEQ' , 'DESIRED_CHANGE' , 'DECIMAL_PLACES']
#
# for elt in root.INDICATOR:              # 这里有问题没有解决
#     el_data ={}
#     for child in elt.getchildren():
#         if child.tag in skip_fields:
#             continue
#         el_data[child.tag] = child.pyval
#     data.append(el_data)
#
# perf = pd.DataFrame(data)
# perf.head()


# from io import StringIO
# tag = '<a herf="http://www.google.com">Google</a>'
# root = objectify.parse(StringIO(tag)).getroot()
# root
# Out[37]: <Element a at 0x1dbb89b2988>
# root.get('herf')
# Out[38]: 'http://www.google.com'
# root.text
# Out[39]: 'Google'



# 6.2

# frame = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\ex1.csv')
# frame
# Out[43]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo
# frame.to_pickle('D:\data_py\pydata-book-2nd-edition\examples\me_pickle')     # 使用to_pickle写入硬盘，pickle短期的储存格式
# pd.read_pickle('D:\data_py\pydata-book-2nd-edition\examples\me_pickle')
# Out[45]:
#    a   b   c   d message
# 0  1   2   3   4   hello
# 1  5   6   7   8   world
# 2  9  10  11  12     foo


# 6.2.1 使用HDF5格式

# import numpy as np
# frame = pd.DataFrame({'a':np.random.randn(100)})
# store = pd.HDFStore('mydata.h5')
# store['obj1'] = frame
# store['obj1_col'] = frame['a']
# store
# Out[53]:
# <class 'pandas.io.pytables.HDFStore'>
# File path: mydata.h5
# store['obj1']
# Out[54]:
#            a
# 0   0.451107
# 1  -1.533654
# 2   1.592731
# 3  -0.522544
# 4  -0.376855
# 5  -0.251318
# 6  -0.643449
# 7   1.424457
# 8   0.091717
# 9  -0.729470
# 10 -0.116514
# 11 -0.667527
# 12  0.780589
# 13 -1.189310
# 14 -0.075752
# 15 -2.005808
# 16  1.153657
# 17 -0.596607
# 18 -0.284290
# 19 -0.672716
# 20 -2.166480
# 21 -0.244957
# 22  0.123113
# 23  0.251980
# 24  0.351958
# 25 -0.493017
# 26  1.613111
# 27 -1.285855
# 28  0.767207
# 29 -0.423906
# ..       ...
# 70 -0.710929
# 71 -0.872290
# 72  0.777574
# 73 -0.601204
# 74 -0.515454
# 75  0.797382
# 76 -0.107307
# 77  0.831799
# 78  0.271206
# 79 -0.868699
# 80 -1.051140
# 81 -0.625513
# 82  1.323332
# 83 -0.958216
# 84  1.395107
# 85  1.140064
# 86  2.285826
# 87 -0.197235
# 88 -0.824921
# 89  0.157117
# 90 -0.071271
# 91  1.293133
# 92 -0.309794
# 93  1.199546
# 94  1.071047
# 95  1.151137
# 96 -0.151846
# 97 -0.449365
# 98  0.641994
# 99  1.920668
# [100 rows x 1 columns]

# store.put('obj2' , frame , format = 'table')
# store.select('obj2' , where=['index >= 10 and index <= 15'])
# Out[56]:
#            a
# 10 -0.116514
# 11 -0.667527
# 12  0.780589
# 13 -1.189310
# 14 -0.075752
# 15 -2.005808

# store.close()
# frame.to_hdf('mydata.h5' , 'obj3' , format='table')
# pd.read_hdf('mydata.h5' , 'obj3' , where=['index < 5'])
# Out[59]:
#           a
# 0  0.451107
# 1 -1.533654
# 2  1.592731
# 3 -0.522544
# 4 -0.376855


# 6.2.2 读取Microsoft Excel 文件
# ExcelFile 和 pandas.read_excel , xlrd和openpyxl，分别读取XLS和XLSX
#
# import pandas as pd
# import numpy as np
# from io import StringIO
# from lxml import objectify
# xlsx = pd.ExcelFile('D:\data_py\pydata-book-2nd-edition\examples\ex1.xlsx')
# pd.read_excel(xlsx , 'Sheet1')             # 通过pandas.read_excel把表中数据读取到DataFrame中
# Out[8]:
#    Unnamed: 0  a   b   c   d message
# 0           0  1   2   3   4   hello
# 1           1  5   6   7   8   world
# 2           2  9  10  11  12     foo
## 方法2 更简介些
# frame = pd.read_excel('D:\data_py\pydata-book-2nd-edition\examples\ex1.xlsx' , 'Sheet1')
# frame
# Out[10]:
#    Unnamed: 0  a   b   c   d message
# 0           0  1   2   3   4   hello
# 1           1  5   6   7   8   world
# 2           2  9  10  11  12     foo
## 把pandas数据写入excel中
# writer = pd.ExcelWriter('D:\data_py\pydata-book-2nd-edition\examples\ex2.xlsx')
# frame.to_excel(writer , 'Sheet1')
# writer.save()
## 第二个方法写，避免直接调用ExcelWriter
# frame.to9_excel('D:\data_py\pydata-book-2nd-edition\examples\ex2.xlsx')

# 6.3 与Web API 交互
# 最简单的是用 requests 包
# 获取GitHub上最新的关于pandas的30条问题

# import requests
#
# url = 'http://api.github.com/repos/pandas-dev/pandas/issues'
# resp = requests.get(url)            # 这里进行不下去
# resp
# data = resp.json()
#

# 使用sqlite3驱动生成一个SQlite
# import sqlite3
#
# query = """
# CREATE TABLE test
# (a VARCHAR(20) , b VARCHAR(20) ,
# c REAL ,         d INTEGER
# );"""
#
# con = sqlite3.connect('mydata.sqlite')
# con.execute(query)
# Out[35]: <sqlite3.Cursor at 0x10872c92730>
# con.commit()
#
# data = [('Atlanta' , 'Georgia' , 1.25 , 6) ,
#         ('Tallahassee' , 'Floida' , 2.6 , 3) ,
#         ('Sacramento' , 'california' , 1.7 , 5)]
#
# stmt = "INSERT INTO test VALUES(?,?,?,?)"
# con.executemany(stmt , data)
# Out[39]: <sqlite3.Cursor at 0x10872c927a0>
# con.commit()

## 从生成的这个数据库中选择数据

# cursor = con.execute('select * from test')
# rows = cursor.fetchall()
# rows
# Out[43]:
# [('Atlanta', 'Georgia', 1.25, 6),
#  ('Tallahassee', 'Floida', 2.6, 3),
#  ('Sacramento', 'california', 1.7, 5)]

# cursor.description
# Out[44]:
# (('a', None, None, None, None, None, None),
#  ('b', None, None, None, None, None, None),
#  ('c', None, None, None, None, None, None),
#  ('d', None, None, None, None, None, None))

# pd.DataFrame(rows , columns=[x[0] for x in cursor.description])
# Out[45]:
#              a           b     c  d
# 0      Atlanta     Georgia  1.25  6
# 1  Tallahassee      Floida  2.60  3
# 2   Sacramento  california  1.70  5

## SQLAlchemy 是一个流行的python SQL工具包 ， read_sql可以从SQLAlchemy中读取数据
# import sqlalchemy as sqla
# db = sqla.create_engine('sqlite:///mydata.sqlite')
# pd.read_sql('select * from test' , db)
# Out[48]:
#              a           b     c  d
# 0      Atlanta     Georgia  1.25  6
# 1  Tallahassee      Floida  2.60  3
# 2   Sacramento  california  1.70  5





























