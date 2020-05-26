"""
    作者：大发
    时间：2019/12/20
    功能：p392
"""

import pandas as pd
import numpy as np
import patsy
import json
import seaborn as sns
import statsmodels.api as sm
# from _pydev_bundle._pydev_getopt import gnu_getopt
## MovieLens 1M数据集含有来自6000名用户对4000部电影的100万条评分数据。
## 它分为三个表：评分、用户信息和电影信息。

##将该数据从zip文件中解压出来之后，
## 可以通过pandas.read_table将各个表分别读到一个pandas DataFrame对象中：

pd.options.display.max_rows = 10
unames = ['user_id' , 'gender' , 'age' , 'occupation' , 'zip']
users = pd.read_table('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\movielens\_users.dat' ,
                      sep='::',header=None , names=unames)
#
# users[:5]
# Out[5]:
#    user_id gender  age  occupation    zip
# 0        1      F    1          10  48067
# 1        2      M   56          16  70072
# 2        3      M   25          15  55117
# 3        4      M   45           7  02460
# 4        5      M   25          20  55455


rnames = ['user_id' , 'movie_id' , 'rating' ,'timestamp']
ratings = pd.read_table('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\movielens\_ratings.dat' ,
                      sep='::',header=None , names=rnames)

# In[8]: ratings[:5]
# Out[8]:
#    user_id  movie_id  rating  timestamp
# 0        1      1193       5  978300760
# 1        1       661       3  978302109
# 2        1       914       3  978301968
# 3        1      3408       4  978300275
# 4        1      2355       5  978824291

mnames = ['movie_id' , 'title' , 'genres']
movies = pd.read_table('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\movielens\movies.dat' ,
                      sep='::',header=None , names=mnames)

# In[10]: movies[:5]
# Out[10]:
#    movie_id                               title                        genres
# 0         1                    Toy Story (1995)   Animation|Children's|Comedy
# 1         2                      Jumanji (1995)  Adventure|Children's|Fantasy
# 2         3             Grumpier Old Men (1995)                Comedy|Romance
# 3         4            Waiting to Exhale (1995)                  Comedy|Drama
# 4         5  Father of the Bride Part II (1995)                        Comedy

# In[11]: ratings
# Out[11]:
#          user_id  movie_id  rating  timestamp
# 0              1      1193       5  978300760
# 1              1       661       3  978302109
# 2              1       914       3  978301968
# 3              1      3408       4  978300275
# 4              1      2355       5  978824291
#           ...       ...     ...        ...
# 1000204     6040      1091       1  956716541
# 1000205     6040      1094       5  956704887
# 1000206     6040       562       5  956704746
# 1000207     6040      1096       4  956715648
# 1000208     6040      1097       4  956715569
#
# [1000209 rows x 4 columns]

## 以上显示数据加载完成


### 假设我们要根据性别和年龄计算某部电影的平均得分，将3个表合并为一个就简单多了。
### 首先用pandas的merge函数将ratings和users合并，在将movies也合并进去。
### pandas会根据列名的重叠情况推断出哪些列是合并键：

data = pd.merge(pd.merge(ratings , users),movies)

# In[13]: data
# Out[13]:
#          user_id  ...                genres
# 0              1  ...                 Drama
# 1              2  ...                 Drama
# 2             12  ...                 Drama
# 3             15  ...                 Drama
# 4             17  ...                 Drama
#           ...  ...                   ...
# 1000204     5949  ...           Documentary
# 1000205     5675  ...                 Drama
# 1000206     5780  ...                 Drama
# 1000207     5851  ...  Comedy|Drama|Western
# 1000208     5938  ...           Documentary
#
# [1000209 rows x 10 columns]


# .iloc：根据标签的所在位置，从0开始计数，选取列，如果索引是数字，就使用.iloc
# loc：根据DataFrame的具体标签选取列，.loc主要是针对字符串的，当索引是字符串时可以使用
# In[14]: data.iloc[0]
# Out[14]:
# user_id                                            1
# movie_id                                        1193
# rating                                             5
# timestamp                                  978300760
# gender                                             F
# age                                                1
# occupation                                        10
# zip                                            48067
# title         One Flew Over the Cuckoo's Nest (1975)
# genres                                         Drama
# Name: 0, dtype: object

### 为了按性别计算每部电影的平均得分，可以使用pivot_table方法：
# pivot_table参数含义：
# values：透视表中展示的是有关于Age的数值
# index：按New_Salutation的五个取值（Mr,Mrs,Miss,Master,Other）进行索引排序
# columns：先按照Pclass的三个取值（1,2,3）分成分成三组，每组中再按照Sex的取值（male,female）分成两组，一共是六组。也可以只填Pclass一个值，则只分成三组，不在继续细分。
# aggfunc：透视表中的数值展示的是每组关于Age的均值

mean_ratings = data.pivot_table('rating' , index='title' , columns='gender' , aggfunc='mean' )

# In[18]: mean_ratings[:5]
# Out[18]:
# gender                                F         M
# title
# $1,000,000 Duck (1971)         3.375000  2.761905
# 'Night Mother (1986)           3.388889  3.352941
# 'Til There Was You (1997)      2.675676  2.733333
# 'burbs, The (1989)             2.793478  2.962085
# And Justice for All (1979)  3.828571  3.689024


### 以上操作产生了另一个DataFrame，内容为电影平均得分
### 行标签是电影名字，列标签为性别

### 接下来过滤掉评分数据不够250条的电影（作为一个指标，人为选取的）
### 先对title进行分组，用.size()得到一个含有个电影分组大小的Series对象：

ratings_by_title = data.groupby('title').size()

# In[22]: ratings_by_title[:10]
# Out[22]:
# title
# $1,000,000 Duck (1971)                37
# 'Night Mother (1986)                  70
# 'Til There Was You (1997)             52
# 'burbs, The (1989)                   303
# And Justice for All (1979)        199
# 1-900 (1994)                           2
# 10 Things I Hate About You (1999)    700
# 101 Dalmatians (1961)                565
# 101 Dalmatians (1996)                364
# 12 Angry Men (1957)                  616
# dtype: int64

active_titles = ratings_by_title.index[ratings_by_title>=250] # .index拿的是索引，那索引的标准是索引对应的值的条件
# In[24]: active_titles
# Out[24]:
# Index([''burbs, The (1989)', '10 Things I Hate About You (1999)',
#        '101 Dalmatians (1961)', '101 Dalmatians (1996)', '12 Angry Men (1957)',
#        '13th Warrior, The (1999)', '2 Days in the Valley (1996)',
#        '20,000 Leagues Under the Sea (1954)', '2001: A Space Odyssey (1968)',
#        '2010 (1984)',
#        ...
#        'X-Men (2000)', 'Year of Living Dangerously (1982)',
#        'Yellow Submarine (1968)', 'You've Got Mail (1998)',
#        'Young Frankenstein (1974)', 'Young Guns (1988)',
#        'Young Guns II (1990)', 'Young Sherlock Holmes (1985)',
#        'Zero Effect (1998)', 'eXistenZ (1999)'],
#       dtype='object', name='title', length=1216)

### 利用前面筛选出来的这个名称的列表，摘出平均数中的所需数据

mean_ratings = mean_ratings.loc[active_titles]

# In[26]: mean_ratings
# Out[26]:
# gender                                    F         M
# title
# 'burbs, The (1989)                 2.793478  2.962085
# 10 Things I Hate About You (1999)  3.646552  3.311966
# 101 Dalmatians (1961)              3.791444  3.500000
# 101 Dalmatians (1996)              3.240000  2.911215
# 12 Angry Men (1957)                4.184397  4.328421
#                                      ...       ...
# Young Guns (1988)                  3.371795  3.425620
# Young Guns II (1990)               2.934783  2.904025
# Young Sherlock Holmes (1985)       3.514706  3.363344
# Zero Effect (1998)                 3.864407  3.723140
# eXistenZ (1999)                    3.098592  3.289086
#
# [1216 rows x 2 columns]

### 为了了解女性观众喜欢的电影，可以对F列降序：

top_female_ratings = mean_ratings.sort_values(by='F' , ascending=False)   # ascending上升，False选择不上升

# In[28]: top_female_ratings[:10]
# Out[28]:
# gender                                                     F         M
# title
# Close Shave, A (1995)                               4.644444  4.473795
# Wrong Trousers, The (1993)                          4.588235  4.478261
# Sunset Blvd. (a.k.a. Sunset Boulevard) (1950)       4.572650  4.464589
# Wallace & Gromit: The Best of Aardman Animation...  4.563107  4.385075
# Schindler's List (1993)                             4.562602  4.491415
# Shawshank Redemption, The (1994)                    4.539075  4.560625
# Grand Day Out, A (1992)                             4.537879  4.293255
# To Kill a Mockingbird (1962)                        4.536667  4.372611
# Creature Comforts (1990)                            4.513889  4.272277
# Usual Suspects, The (1995)                          4.513317  4.518248

### 这些技能都是用来为人的目标服务的

### 14.2.1 计算评分 分歧

# 假设我们想要找出男性和女性观众分歧最大的电影。
# 一个办法是给mean_ratings加上一个用于存放均值差的列，并对其进行排序：

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')

# In[31]: sorted_by_diff[:10]
# Out[31]:
# gender                                        F         M      diff
# title
# Dirty Dancing (1987)                   3.790378  2.959596 -0.830782
# Jumpin' Jack Flash (1986)              3.254717  2.578358 -0.676359
# Grease (1978)                          3.975265  3.367041 -0.608224
# Little Women (1994)                    3.870588  3.321739 -0.548849
# Steel Magnolias (1989)                 3.901734  3.365957 -0.535777
# Anastasia (1997)                       3.800000  3.281609 -0.518391
# Rocky Horror Picture Show, The (1975)  3.673016  3.160131 -0.512885
# Color Purple, The (1985)               4.158192  3.659341 -0.498851
# Age of Innocence, The (1993)           3.827068  3.339506 -0.487561
# Free Willy (1993)                      2.921348  2.438776 -0.482573

### 对以上结果取最后10行，就是男性更喜欢的电影：

sorted_by_diff[-10:]
# Out[32]:
# gender                                         F         M      diff
# title
# For a Few Dollars More (1965)           3.409091  3.953795  0.544704
# Caddyshack (1980)                       3.396135  3.969737  0.573602
# Rocky III (1982)                        2.361702  2.943503  0.581801
# Hidden, The (1987)                      3.137931  3.745098  0.607167
# Evil Dead II (Dead By Dawn) (1987)      3.297297  3.909283  0.611985
# Cable Guy, The (1996)                   2.250000  2.863787  0.613787
# Longest Day, The (1962)                 3.411765  4.031447  0.619682
# Dumb & Dumber (1994)                    2.697987  3.336595  0.638608
# Kentucky Fried Movie, The (1977)        2.878788  3.555147  0.676359
# Good, The Bad and The Ugly, The (1966)  3.494949  4.221300  0.726351

sorted_by_diff[::-1][:10]     # [::-1]这个是把前边反序，然后[:10]取前十

# Out[33]:
# gender                                         F         M      diff
# title
# Good, The Bad and The Ugly, The (1966)  3.494949  4.221300  0.726351
# Kentucky Fried Movie, The (1977)        2.878788  3.555147  0.676359
# Dumb & Dumber (1994)                    2.697987  3.336595  0.638608
# Longest Day, The (1962)                 3.411765  4.031447  0.619682
# Cable Guy, The (1996)                   2.250000  2.863787  0.613787
# Evil Dead II (Dead By Dawn) (1987)      3.297297  3.909283  0.611985
# Hidden, The (1987)                      3.137931  3.745098  0.607167
# Rocky III (1982)                        2.361702  2.943503  0.581801
# Caddyshack (1980)                       3.396135  3.969737  0.573602
# For a Few Dollars More (1965)           3.409091  3.953795  0.544704

### 如果只是想找到分歧最大的电影（不考虑性别因素），则可以计算得分的方差和标准差：

ratings_std_by_title = data.groupby('title')['rating'].std()
ratings_std_by_title = ratings_std_by_title.loc[active_titles]
ratings_std_by_title.sort_values(ascending=False)[:10]


# Out[36]:
# title
# Dumb & Dumber (1994)                     1.321333
# Blair Witch Project, The (1999)          1.316368
# Natural Born Killers (1994)              1.307198
# Tank Girl (1995)                         1.277695
# Rocky Horror Picture Show, The (1975)    1.260177
# Eyes Wide Shut (1999)                    1.259624
# Evita (1996)                             1.253631
# Billy Madison (1995)                     1.249970
# Fear and Loathing in Las Vegas (1998)    1.246408
# Bicentennial Man (1999)                  1.245533
# Name: rating, dtype: float64

