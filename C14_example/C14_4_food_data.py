"""
    作者：大发
    时间：2019/12/21
    功能：有关食物营养信息的数据库,p410
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

### 每种食物都带有若干标识性属性以及两个有关营养成分和分量的列表。
### 这种形式的数据不是很适合分析工作，因此我们需要做一些规整化以使其具有更好用的形式。

### 使用json加载数据 , 数据就是json格式的
db = json.load(open('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\_usda_food\database.json'))
len(db)
# Out[30]: 6636

### db中的每个条目都是一个含有某种食物全部数据的字典。
### nutrients字段是一个字典列表，其中的每个字典对应一种营养成分：

db[0].keys()             # 拿键名
# Out[31]: dict_keys(['id', 'description', 'tags', 'manufacturer', 'group', 'portions', 'nutrients'])

db[0]['nutrients'][0]
# Out[32]:
# {'value': 25.18,
#  'units': 'g',
#  'description': 'Protein',
#  'group': 'Composition'}

nutrients = pd.DataFrame(db[0]['nutrients'])
nutrients[:7]
# Out[33]:
#                    description        group units    value
# 0                      Protein  Composition     g    25.18
# 1            Total lipid (fat)  Composition     g    29.20
# 2  Carbohydrate, by difference  Composition     g     3.06
# 3                          Ash        Other     g     3.28
# 4                       Energy       Energy  kcal   376.00
# 5                        Water  Composition     g    39.28
# 6                       Energy       Energy    kJ  1573.00


### 在将字典列表转换为DataFrame时，可以只抽取其中的一部分字段。
### 这里，我们将取出食物的名称、分类、编号以及制造商等信息：
info_keys = [ 'description','group','id','manufacturer']
info = pd.DataFrame(db , columns=info_keys)
info[:5]
# Out[34]:
#                           description  ... manufacturer
# 0                     Cheese, caraway  ...
# 1                     Cheese, cheddar  ...
# 2                        Cheese, edam  ...
# 3                        Cheese, feta  ...
# 4  Cheese, mozzarella, part skim milk  ...
#
# [5 rows x 4 columns]

info.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 6636 entries, 0 to 6635
# Data columns (total 4 columns):
# description     6636 non-null object
# group           6636 non-null object
# id              6636 non-null int64
# manufacturer    5195 non-null object
# dtypes: int64(1), object(3)
# memory usage: 207.5+ KB

### 通过value_counts，你可以查看食物类别的分布情况：
pd.value_counts(info.group)[:10]
# Out[37]:
# Vegetables and Vegetable Products    812
# Beef Products                        618
# Baked Products                       496
# Breakfast Cereals                    403
# Legumes and Legume Products          365
# Fast Foods                           365
# Lamb, Veal, and Game Products        345
# Sweets                               341
# Pork Products                        328
# Fruits and Fruit Juices              328
# Name: group, dtype: int64

### 为了对全部营养数据做一些分析，最简单的办法是将所有食物的营养成分整合到一个大表中。
### 首先，将各食物的营养成分列表转换为一个DataFrame，并添加一个表示编号的列，
### 然后将该DataFrame添加到一个列表中。最后通过concat将这些东西连接起来就可以了：

long = range(0 , 6636)
pieces = []
for x  in long :
    nutrients = pd.DataFrame(db[x]['nutrients'])
    nutrients['id'] = db[x]['id']
    pieces.append(nutrients)
nutrients_all = pd.concat(pieces , ignore_index=True)

# In[48]: nutrients_all
# Out[62]:
#                                description        group  ...     value     id
# 0                                  Protein  Composition  ...    25.180   1008
# 1                        Total lipid (fat)  Composition  ...    29.200   1008
# 2              Carbohydrate, by difference  Composition  ...     3.060   1008
# 3                                      Ash        Other  ...     3.280   1008
# 4                                   Energy       Energy  ...   376.000   1008
# 5                                    Water  Composition  ...    39.280   1008
# 6                                   Energy       Energy  ...  1573.000   1008
# 7                     Fiber, total dietary  Composition  ...     0.000   1008
# 8                              Calcium, Ca     Elements  ...   673.000   1008
# 9                                 Iron, Fe     Elements  ...     0.640   1008
# 10                           Magnesium, Mg     Elements  ...    22.000   1008
# 11                           Phosphorus, P     Elements  ...   490.000   1008
# 12                            Potassium, K     Elements  ...    93.000   1008
# 13                              Sodium, Na     Elements  ...   690.000   1008
# 14                                Zinc, Zn     Elements  ...     2.940   1008
# 15                              Copper, Cu     Elements  ...     0.024   1008
# 16                           Manganese, Mn     Elements  ...     0.021   1008
# 17                            Selenium, Se     Elements  ...    14.500   1008
# 18                           Vitamin A, IU     Vitamins  ...  1054.000   1008
# 19                                 Retinol     Vitamins  ...   262.000   1008
# 20                          Vitamin A, RAE     Vitamins  ...   271.000   1008
# 21          Vitamin C, total ascorbic acid     Vitamins  ...     0.000   1008
# 22                                 Thiamin     Vitamins  ...     0.031   1008
# 23                              Riboflavin     Vitamins  ...     0.450   1008
# 24                                  Niacin     Vitamins  ...     0.180   1008
# 25                        Pantothenic acid     Vitamins  ...     0.190   1008
# 26                             Vitamin B-6     Vitamins  ...     0.074   1008
# 27                           Folate, total     Vitamins  ...    18.000   1008
# 28                            Vitamin B-12     Vitamins  ...     0.270   1008
# 29                              Folic acid     Vitamins  ...     0.000   1008
#                                     ...          ...  ...       ...    ...
# 389325                        Selenium, Se     Elements  ...     1.100  43546
# 389326                       Vitamin A, IU     Vitamins  ...     5.000  43546
# 389327                             Retinol     Vitamins  ...     0.000  43546
# 389328                      Vitamin A, RAE     Vitamins  ...     0.000  43546
# 389329                      Carotene, beta     Vitamins  ...     2.000  43546
# 389330                     Carotene, alpha     Vitamins  ...     2.000  43546
# 389331        Vitamin E (alpha-tocopherol)     Vitamins  ...     0.250  43546
# 389332                           Vitamin D     Vitamins  ...     0.000  43546
# 389333                 Vitamin D (D2 + D3)     Vitamins  ...     0.000  43546
# 389334                 Cryptoxanthin, beta     Vitamins  ...     0.000  43546
# 389335                            Lycopene     Vitamins  ...     0.000  43546
# 389336                 Lutein + zeaxanthin     Vitamins  ...    20.000  43546
# 389337      Vitamin C, total ascorbic acid     Vitamins  ...    21.900  43546
# 389338                             Thiamin     Vitamins  ...     0.020  43546
# 389339                          Riboflavin     Vitamins  ...     0.060  43546
# 389340                              Niacin     Vitamins  ...     0.540  43546
# 389341                         Vitamin B-6     Vitamins  ...     0.260  43546
# 389342                       Folate, total     Vitamins  ...    17.000  43546
# 389343                        Vitamin B-12     Vitamins  ...     0.000  43546
# 389344                      Choline, total     Vitamins  ...     4.100  43546
# 389345           Vitamin K (phylloquinone)     Vitamins  ...     0.500  43546
# 389346                          Folic acid     Vitamins  ...     0.000  43546
# 389347                        Folate, food     Vitamins  ...    17.000  43546
# 389348                         Folate, DFE     Vitamins  ...    17.000  43546
# 389349                    Vitamin E, added     Vitamins  ...     0.000  43546
# 389350                 Vitamin B-12, added     Vitamins  ...     0.000  43546
# 389351                         Cholesterol        Other  ...     0.000  43546
# 389352        Fatty acids, total saturated        Other  ...     0.072  43546
# 389353  Fatty acids, total monounsaturated        Other  ...     0.028  43546
# 389354  Fatty acids, total polyunsaturated        Other  ...     0.041  43546
# [389355 rows x 5 columns]

nutrients_all.duplicated().sum()    # 重复的数量
# Out[49]: 311192
nutrients = nutrients_all.drop_duplicates()    # 删除重复的数量


### 由于两个DataFrame对象中都有"group"和"description"，
### 所以为了明确到底谁是谁，我们需要对它们进行重命名：
col_mapping = {'description':'food' ,
               'group': 'fgroup'}

info = info.rename(columns = col_mapping , copy=False)
# In[66]: info.info()



col_mapping = {'description' : 'nutrient' ,
               'group' : 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False )

# In[57]: nutrients[:5]
# Out[68]:
#                       nutrient     nutgroup units   value    id
# 0                      Protein  Composition     g   25.18  1008
# 1            Total lipid (fat)  Composition     g   29.20  1008
# 2  Carbohydrate, by difference  Composition     g    3.06  1008
# 3                          Ash        Other     g    3.28  1008
# 4                       Energy       Energy  kcal  376.00  1008


### 将info跟nutrients合并起来:
ndata = pd.merge(nutrients , info , on ='id' , how='outer')
ndata.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 375176 entries, 0 to 375175
# Data columns (total 8 columns):
# nutrient        375176 non-null object
# nutgroup        375176 non-null object
# units           375176 non-null object
# value           375176 non-null float64
# id              375176 non-null int64
# food            375176 non-null object
# fgroup          375176 non-null object
# manufacturer    293054 non-null object
# dtypes: float64(1), int64(1), object(6)
# memory usage: 25.8+ MB
ndata.iloc[30000]
# Out[71]:
# nutrient                                       Glycine
# nutgroup                                   Amino Acids
# units                                                g
# value                                             0.04
# id                                                6158
# food            Soup, tomato bisque, canned, condensed
# fgroup                      Soups, Sauces, and Gravies
# manufacturer
# Name: 30000, dtype: object


### 根据食物分类和营养分类画出一个中位数的图
result = ndata.groupby(['nutrient' , 'fgroup'])['value'].quantile(0.5)

result['Zinc, Zn'].sort_values().plot(kind='barh')

### 发现各营养成分最为丰富的食物是什么:
by_nutrient = ndata.groupby(['nutgroup' , 'nutrient'])
get_maximum = lambda x:x.loc[x.value.idxmax()]
get_minimum = lambda x:x.loc[x.value.idxmin()]

max_foods = by_nutrient.apply(get_maximum)[['value' , 'food']]
max_foods.food = max_foods.food.str[:50]

max_foods.loc['Amino Acids']['food']
