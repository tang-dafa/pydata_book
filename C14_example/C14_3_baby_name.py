"""
    作者：大发
    时间：2019/12/20
    功能：p397
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import patsy
import json
import seaborn as sns
import statsmodels.api as sm

names1880 = pd.read_csv('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\_babynames\yob1880.txt',
                        names=['name' , 'sex' , 'births'])

### 按性别列出的出生总和作为当年的出生总数

names1880.groupby('sex').births.sum()
# Out[39]:
# sex
# F     90993
# M    110493
# Name: births, dtype: int64

### 由于该数据集按年度被分隔成了多个文件，
### 所以第一件事情就是要将所有数据都组装到一个DataFrame里面，并加上一个year字段。
### 使用pandas.concat即可达到这个目的：

years = range(1880 , 2011)
pieces = []
columns = ['name' , 'sex' , 'births']

for year in years:
    path = 'D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\_babynames\yob%d.txt' % year
    frame = pd.read_csv(path , names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat( pieces , ignore_index=True)

### 这里需要注意几件事情。
# 第一，concat默认是按行将多个DataFrame组合到一起的；
# 第二，必须指定ignore_index=True，因为我们不希望保留read_csv所返回的原始行号。

names

# Out[41]:
#               name sex  births  year
# 0             Mary   F    7065  1880
# 1             Anna   F    2604  1880
# 2             Emma   F    2003  1880
# 3        Elizabeth   F    1939  1880
# 4           Minnie   F    1746  1880
#             ...  ..     ...   ...
# 1690779    Zymaire   M       5  2010
# 1690780     Zyonne   M       5  2010
# 1690781  Zyquarius   M       5  2010
# 1690782      Zyran   M       5  2010
# 1690783      Zzyzx   M       5  2010
#
# [1690784 rows x 4 columns]

### 有了这些数据之后，我们就可以利用groupby或pivot_table
### 在year和sex级别上对其进行聚合了

total_births = names.pivot_table('births' , index='year' ,
                                 columns='sex' , aggfunc=sum)           # index 是行头，行标题，columns 是列头，列标题，aggfunc是计算方法
# .tail()与head()函数类似，默认是取dataframe中的最后五行。
total_births.tail()
total_births.head()

total_births.plot(title='Total births by sex and year')     # 画图

### 插入一个prop列，用于存放指定名字的婴儿数相对于总出生数的比例。
### prop值为0.02表示每100名婴儿中有2名取了当前这个名字。
### 因此，我们先按year和sex分组，然后再将新列加到各个分组上：

def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group

names = names.groupby(['year' , 'sex']).apply(add_prop)

# In[48]: names
# Out[48]:
#               name sex  births  year      prop
# 0             Mary   F    7065  1880  0.077643
# 1             Anna   F    2604  1880  0.028618
# 2             Emma   F    2003  1880  0.022013
# 3        Elizabeth   F    1939  1880  0.021309
# 4           Minnie   F    1746  1880  0.019188
#             ...  ..     ...   ...       ...
# 1690779    Zymaire   M       5  2010  0.000003
# 1690780     Zyonne   M       5  2010  0.000003
# 1690781  Zyquarius   M       5  2010  0.000003
# 1690782      Zyran   M       5  2010  0.000003
# 1690783      Zzyzx   M       5  2010  0.000003
#
# [1690784 rows x 5 columns]

### 执行这样的分组处理时，要做一些有效性检查，比如验证所有分组的prop和是否为1

names.groupby(['year' , 'sex']).prop.sum()      ## 算的是每个名字在组内占的比例

# In[49]: names.groupby(['year' , 'sex']).prop.sum()
# Out[49]:
# year  sex
# 1880  F      1.0
#       M      1.0
# 1881  F      1.0
#       M      1.0
# 1882  F      1.0
#             ...
# 2008  M      1.0
# 2009  F      1.0
#       M      1.0
# 2010  F      1.0
#       M      1.0
# Name: prop, Length: 262, dtype: float64


### 为了便于实现更进一步的分析，我需要取出该数据的一个子集：
### 每对sex/year组合的前1000个名字。

def get_top1000(group):
    return group.sort_values(by='births' , ascending=False)[:1000]
grouped = names.groupby(['year' , 'sex'])
top1000 = grouped.apply(get_top1000)

### 删除组索引，不需要它
top1000.reset_index(inplace=True , drop=True)
top1000

### 以下方法也合适
pieces = []
for year,group in names.groupby(['year' , 'sex']):
    pieces.append(group.sort_values(by='births' , ascending=False)[:1000])
top1000 = pd.concat(pieces , ignore_index=True)

#   ...: top1000
# Out[8]:
#              name sex  births  year      prop
# 0            Mary   F    7065  1880  0.077643
# 1            Anna   F    2604  1880  0.028618
# 2            Emma   F    2003  1880  0.022013
# 3       Elizabeth   F    1939  1880  0.021309
# 4          Minnie   F    1746  1880  0.019188
# 5        Margaret   F    1578  1880  0.017342
# 6             Ida   F    1472  1880  0.016177
# 7           Alice   F    1414  1880  0.015540
# 8          Bertha   F    1320  1880  0.014507
# 9           Sarah   F    1288  1880  0.014155
# 10          Annie   F    1258  1880  0.013825
# 11          Clara   F    1226  1880  0.013474
# 12           Ella   F    1156  1880  0.012704
# 13       Florence   F    1063  1880  0.011682
# 14           Cora   F    1045  1880  0.011484
# 15         Martha   F    1040  1880  0.011429
# 16          Laura   F    1012  1880  0.011122
# 17         Nellie   F     995  1880  0.010935
# 18          Grace   F     982  1880  0.010792
# 19         Carrie   F     949  1880  0.010429
# 20          Maude   F     858  1880  0.009429
# 21          Mabel   F     808  1880  0.008880
# 22         Bessie   F     794  1880  0.008726
# 23         Jennie   F     793  1880  0.008715
# 24       Gertrude   F     787  1880  0.008649
# 25          Julia   F     783  1880  0.008605
# 26         Hattie   F     769  1880  0.008451
# 27          Edith   F     768  1880  0.008440
# 28         Mattie   F     704  1880  0.007737
# 29           Rose   F     700  1880  0.007693
#            ...  ..     ...   ...       ...
# 261847       Yair   M     201  2010  0.000106
# 261848      Talan   M     201  2010  0.000106
# 261849      Keyon   M     201  2010  0.000106
# 261850       Kael   M     201  2010  0.000106
# 261851   Demarion   M     200  2010  0.000105
# 261852     Gibson   M     200  2010  0.000105
# 261853     Reagan   M     200  2010  0.000105
# 261854  Cristofer   M     199  2010  0.000105
# 261855     Daylen   M     199  2010  0.000105
# 261856     Jordon   M     199  2010  0.000105
# 261857    Dashawn   M     198  2010  0.000104
# 261858      Masen   M     198  2010  0.000104
# 261859      Rowen   M     197  2010  0.000104
# 261860     Yousef   M     197  2010  0.000104
# 261861   Thaddeus   M     197  2010  0.000104
# 261862      Kadin   M     197  2010  0.000104
# 261863     Dillan   M     197  2010  0.000104
# 261864   Clarence   M     197  2010  0.000104
# 261865      Slade   M     196  2010  0.000103
# 261866    Clinton   M     196  2010  0.000103
# 261867    Sheldon   M     196  2010  0.000103
# 261868    Keshawn   M     195  2010  0.000103
# 261869   Menachem   M     195  2010  0.000103
# 261870     Joziah   M     195  2010  0.000103
# 261871     Bailey   M     194  2010  0.000102
# 261872     Camilo   M     194  2010  0.000102
# 261873     Destin   M     194  2010  0.000102
# 261874     Jaquan   M     194  2010  0.000102
# 261875     Jaydan   M     194  2010  0.000102
# 261876     Maxton   M     193  2010  0.000102
#
# [261877 rows x 5 columns]

### 14.3.1 分析名字的趋势

### 首先把前1000 的名字分成男女两部分：

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

### 这是两个简单的时间序列，只需稍作整理即可绘制出相应的图表（比如每年叫做John和Mary的婴儿数）。
### 我们可以生成一张按year和name统计的总出生数透视表：
total_births = top1000.pivot_table('births' , index='year' ,
                                   columns='name' , aggfunc=sum)

### 用DataFrame的plot方法绘制几个名字的曲线图:
total_births.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 131 entries, 1880 to 2010
# Columns: 6868 entries, Aaden to Zuri
# dtypes: float64(6868)
# memory usage: 6.9 MB

subset = total_births[['John' , 'Harry' , 'Mary' , 'Marilyn']]
subset.plot(subplots=True , figsize=(12,10) , grid=False ,
            title = "Number of births per year")

### 14.3.1.1 计量命名多样性的增加

### 一种解释是父母愿意给小孩起常见的名字越来越少。
### 这个假设可以从数据中得到验证。一个办法是计算最流行的1000个名字所占的比例，
### 按year和sex进行聚合并绘图：

table = top1000.pivot_table('prop' , index='year' ,
                            columns='sex' , aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0,1.2,13) , xticks=range(1880,2020,10) )

### 从上式所得图中前1000所占比例下降，说明多样性降低
### 另一个办法是计算占总出生人数前50%的不同名字的数量，这个数字不太好计算。
### 我们只考虑2010年男孩的名字：

df = boys[boys.year == 2010]

### 在对prop降序排列之后，我们想知道前面多少个名字的人数加起来才够50%。
### 先计算prop的累计和cumsum，然后再通过searchsorted方法找出0.5应该
### 被插入在哪个位置才能保证不破坏顺序：
prop_cumsum = df.sort_values(by='prop' , ascending=False).prop.cumsum()
# prop_cumsum[:10]
#    ...: prop_cumsum[:10]
# Out[21]:
# 260877    0.011523
# 260878    0.020934
# 260879    0.029959
# 260880    0.038930
# 260881    0.047817
# 260882    0.056579
# 260883    0.065155
# 260884    0.073414
# 260885    0.081528
# 260886    0.089621
# Name: prop, dtype: float64

prop_cumsum.values.searchsorted(0.5)      # .searchsorted()查找0.5位置，返回索引值
# Out[22]: 116

### 拿1900年的数据来做个比较，这个数字要小得多

df = boys[boys.year == 1900 ]
prop_cumsum = df.sort_values(by='prop' , ascending=False).prop.cumsum()
prop_cumsum.values.searchsorted(0.5)
# Out[23]: 24      # 24小于116+1


### 现在就可以对所有year/sex组合执行这个计算了。
### 按这两个字段进行groupby处理，然后用一个函数计算各分组的这个值：

def get_quantile_count(group , q=0.5):
    group = group.sort_values(by='prop' , ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1

diversity = top1000.groupby(['year' , 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

# diversity.head()
# Out[25]:
# sex    F   M
# year
# 1880  38  14
# 1881  38  14
# 1882  38  15
# 1883  39  15
# 1884  39  16

diversity.plot(title='Number of popular names in top 50%')      # 这个本质是求中位数


### 14.3.1.2 “最后一个字母”的变革

### 从name列提取最后一个字母
get_last_letter = lambda  x:x[-1]

###​ map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，
### 并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回
last_letters = names.name.map(get_last_letter)    #映射，
last_letters.name = 'last_letter'

table = names.pivot_table('births' , index=last_letters ,
                          columns=['sex' ,'year'] , aggfunc=sum)   # 按人数排列，行号是最后一个字母

### 选出最有代表性的3年

subtable = table.reindex(columns=[1910 , 1960 , 2010] , level='year')
# subtable.head()

# Out[6]:
# sex                 F                            M
# year             1910      1960      2010     1910      1960      2010
# last_letter
# a            108376.0  691247.0  670605.0    977.0    5204.0   28438.0
# b                 NaN     694.0     450.0    411.0    3912.0   38859.0
# c                 5.0      49.0     946.0    482.0   15476.0   23125.0
# d              6750.0    3729.0    2607.0  22111.0  262112.0   44398.0
# e            133569.0  435013.0  313833.0  28655.0  178823.0  129012.0


### 接下来我们需要按总出生数对该表进行规范化处理，
### 以便计算出各性别各末字母占总出生人数的比例：

subtable.sum()
# Out[8]:
# sex  year
# F    1910     396416.0
#      1960    2022062.0
#      2010    1759010.0
# M    1910     194198.0
#      1960    2132588.0
#      2010    1898382.0
# dtype: float64

letter_prop = subtable / subtable.sum()
letter_prop

# Out[10]:
# sex                 F                             M
# year             1910      1960      2010      1910      1960      2010
# last_letter
# a            0.273390  0.341853  0.381240  0.005031  0.002440  0.014980
# b                 NaN  0.000343  0.000256  0.002116  0.001834  0.020470
# c            0.000013  0.000024  0.000538  0.002482  0.007257  0.012181
# d            0.017028  0.001844  0.001482  0.113858  0.122908  0.023387
# e            0.336941  0.215133  0.178415  0.147556  0.083853  0.067959
# f                 NaN  0.000010  0.000055  0.000783  0.004325  0.001188
# g            0.000144  0.000157  0.000374  0.002250  0.009488  0.001404
# h            0.051529  0.036224  0.075852  0.045562  0.037907  0.051670
# i            0.001526  0.039965  0.031734  0.000844  0.000603  0.022628
# j                 NaN       NaN  0.000090       NaN       NaN  0.000769
# k            0.000121  0.000156  0.000356  0.036581  0.049384  0.018541
# l            0.043189  0.033867  0.026356  0.065016  0.104904  0.070367
# m            0.001201  0.008613  0.002588  0.058044  0.033827  0.024657
# n            0.079240  0.130687  0.140210  0.143415  0.152522  0.362771
# o            0.001660  0.002439  0.001243  0.017065  0.012829  0.042681
# p            0.000018  0.000023  0.000020  0.003172  0.005675  0.001269
# q                 NaN       NaN  0.000030       NaN       NaN  0.000180
# r            0.013390  0.006764  0.018025  0.064481  0.031034  0.087477
# s            0.039042  0.012764  0.013332  0.130815  0.102730  0.065145
# t            0.027438  0.015201  0.007830  0.072879  0.065655  0.022861
# u            0.000684  0.000574  0.000417  0.000124  0.000057  0.001221
# v                 NaN  0.000060  0.000117  0.000113  0.000037  0.001434
# w            0.000020  0.000031  0.001182  0.006329  0.007711  0.016148
# x            0.000015  0.000037  0.000727  0.003965  0.001851  0.008614
# y            0.110972  0.152569  0.116828  0.077349  0.160987  0.058168
# z            0.002439  0.000659  0.000704  0.000170  0.000184  0.001831

letter_prop.sum()        # 作用是验证
# Out[12]:
# sex  year
# F    1910    1.0
#      1960    1.0
#      2010    1.0
# M    1910    1.0
#      1960    1.0
#      2010    1.0
# dtype: float64

### 有了letter_prop之后可以画一个各年度各性别的条形图

fig , axes = plt.subplots(2,1,figsize=(10,8))
letter_prop['M'].plot(kind='bar' , rot=0 , ax=axes[0] , title='Male')
letter_prop['F'].plot(kind='bar' , rot=0 , ax=axes[1] , title='Female' ,
                      legend=False)

### 从20世纪60年代开始，以字母"n"结尾的男孩名字出现了显著的增长。
### 回到之前创建的那个完整表，按年度和性别对其进行规范化处理，
### 并在男孩名字中选取几个字母，最后进行转置以便将各个列做成一个时间序列:

letter_prop = table / table.sum()
dny_ts = letter_prop.loc[['d' , 'n' , 'y'] , 'M'].T     # .T是转置的意思

# In[17]: dny_ts.head()
# Out[17]:
# last_letter         d         n         y
# year
# 1880         0.083055  0.153213  0.075760
# 1881         0.083247  0.153214  0.077451
# 1882         0.085340  0.149560  0.077537
# 1883         0.084066  0.151646  0.079144
# 1884         0.086120  0.149915  0.080405

### 画一张趋势图

dny_ts.plot()  # 趋势图表明，用n做结尾的递增

### 14.3.1.3 男孩名字变成女孩名

### 回到top1000数据集，找出其中以"lesl"开头的一组名字：
### unique函数去除其中重复的元素，并按元素由大到小返回一个新的无元素重复的元组或者列表:

all_names = pd.Series(top1000.name.unique())
lesley_like = all_names[all_names.str.lower().str.contains('lesl')]
lesley_like
# Out[21]:
# 632     Leslie
# 2294    Lesley
# 4262    Leslee
# 4728     Lesli
# 6103     Lesly
# dtype: object

### 利用这个结果过滤其他名字，并按名字计算出生数和相对频数

filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
# Out[22]:
# name
# Leslee      1082
# Lesley     35022
# Lesli        929
# Leslie    370429
# Lesly      10067
# Name: births, dtype: int64

### 按性别和年度进行聚合，并按年度进行规范化处理:

table = filtered.pivot_table('births' , index='year' ,
                             columns='sex' , aggfunc=sum)
table = table.div(table.sum(1) , axis=0)
table.tail()
# Out[26]:
# sex     F   M
# year
# 2006  1.0 NaN
# 2007  1.0 NaN
# 2008  1.0 NaN
# 2009  1.0 NaN
# 2010  1.0 NaN


### 画一张按性别区分的年度曲线
table.plot(style = {'M':'k-' , 'F':'k--'})












