"""

    作者：大发
    日期：2019/11/16
    内容：利用python进行数据分析 9.1 p245 笔记

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

# Figure和Subplot

# data = np.arange(10)
# data
# Out[5]: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# plt.plot(data)         # 调动图像
# Out[6]: [<matplotlib.lines.Line2D at 0x1bada9d5630>]
# fig = plt.figure()     #

# 用add_subplot创建一个或多个subplot（子图）

# ax1 = fig.add_subplot(2,2,1)
# 图像应该是2×2的（即最多4张图），且当前选中的是4 个subplot中的第一个（编号从1开始）
# ax2 = fig.add_subplot(2,2,2)
# ax3 = fig.add_subplot(2,2,3)

#
# fig = plt.figure()
# ax1 = fig.add_subplot(2,2,1)
# ax2 = fig.add_subplot(2,2,2)
# ax3 = fig.add_subplot(2,2,3)      # 这4条要一起运行，才能得到一个框里3个图

# plt.plot(np.random.randn(50).cumsum() , 'k--') # 这个会绘制在上边出现的3个格子中的最后一个里 ‘k--’指的是一个线型选项

# Out[13]: [<matplotlib.lines.Line2D at 0x1badf0e2a90>]

# 这一行画一个直方图
# _ = ax1.hist(np.random.randn(100) , bins = 20 , color ='k' , alpha = 0.3)
## 这一行画一个散点图
# ax2.scatter(np.arange(30) , np.arange(30)+3*np.random.randn(30))
# Out[15]: <matplotlib.collections.PathCollection at 0x1bad931bf98>

# 这个可以很快速的生成一个2*3矩阵的子图界面，返回一个numpy数组
# fig, axes = plt.subplots(2,3)
# axes
# Out[17]:
# array([[<matplotlib.axes._subplots.AxesSubplot object at 0x000001BADF0A0D30>,
#         <matplotlib.axes._subplots.AxesSubplot object at 0x000001BADC24F780>,
#         <matplotlib.axes._subplots.AxesSubplot object at 0x000001BAD92F10B8>],
#        [<matplotlib.axes._subplots.AxesSubplot object at 0x000001BADF13D668>,
#         <matplotlib.axes._subplots.AxesSubplot object at 0x000001BADF1CCC18>,
#         <matplotlib.axes._subplots.AxesSubplot object at 0x000001BADF20C208>]],
#       dtype=object)

# 利用Figure的subplots_adjust方法可以轻而易举地修改间距，此外，它也是个顶级函数
# subplots_adjust(left = None , bottom = None , right = None , top = None , wspace = None , hspace = None)

# fig , axes = plt.subplots(2,2,sharex=True , sharey=True)
# for i in range(2):
#     for j in range(2):
#         axes[i , j].hist(np.random.randn(500) , bins=50 , color='k' , alpha=0.5)
# plt.subplots_adjust(wspace=0 , hspace=0)   # wspace和hspace是控制宽度高度的百分比



# 颜色、标记、线类型

##matplotlib的plot函数接受一组X和Y坐标，还可以接受一个表示颜色和线型的字符串缩写。

# ax.plot(x,y,'g--')
# ax.plot(x,y,linestyle='--' , color='g') # 这两条等价

# plt.plot(randn(30).cumsum() , 'ko--')
# plot(randn(30).cumsum() , color='k' , linestyle='dashed' , marker='o')
# 以上两条也等价

# data = np.random.randn(30).cumsum()
# plt.plot(data , 'k--' , label = 'Default')
#
# plt.plot(data , 'k-' , drawstyle='steps-post' , label='steps-post')
# plt.legend(loc='best')



# 9.1.3 刻度、标签、图例

## 设置标题、轴标签、刻度以及刻度标签

# 自定义一段随机漫步

# fig = plt.figure()
# # ax = fig.add_subplot(1,1,1)
# # ax.plot(np.random.randn(1000).cumsum())
# # Out[37]: [<matplotlib.lines.Line2D at 0x1bae3f8cf98>]

# 改变x轴刻度，最简单的办法是使用set_xticks和set_xticklabels
# 可以通过set_xticklabels将任何其他的值用作标签
# ticks = ax.set_xticks([0 , 250 , 500 , 750 , 1000])
# rotation选项设定x刻度标签倾斜30度,这个是把标签的字给斜置了，把上边的0换成了one,one是倾斜30度显示的
# labels = ax.set_xticklabels(['one' , 'two' , 'three' , 'four' , 'five' ] , rotation = 30 , fontsize='small')
# 给图表命名
# ax.set_title('My first marplotlib plot')
# Out[40]: Text(0.5, 1, 'My first marplotlib plot')
# 给x轴命名
# ax.set_xlabel('Stages')
# Out[41]: Text(0.5, 10.433891973024506, 'Stages')

# 这一段与上面的功能一致
# props = {
#     'title':'My first matplotlib plot',
#     'xlabel':'Stages'
# }
# ax.set(**props)


## 添加图例


# 先创建3条随机漫步
# fig = plt.figure();ax = fig.add_subplot(1,1,1)
# ax.plot(randn(1000).cumsum() , 'k' , label='one')
# Out[45]: [<matplotlib.lines.Line2D at 0x1bae3fce978>]
# ax.plot(randn(1000).cumsum() , 'k--' , label='two')
# Out[46]: [<matplotlib.lines.Line2D at 0x1bae3fa0eb8>]
# ax.plot(randn(1000).cumsum() , 'k.' , label='three')
# Out[47]: [<matplotlib.lines.Line2D at 0x1bae4a955c0>]

# 调用ax.legend()或plt.legend()来自动创建图例
# loc会设置图例的位置，loc='best'会把图列放在最不碍事的位置
# ax.legend(loc='best')
# legend方法有几个其它的loc位置参数选项。
# 请查看文档字符串（使用ax.legend?）
# 要从图例中去除一个或多个元素，不传入label或传入label='nolegend'即可

## 注解以及在Subplot上绘图
#
# 注解和文字可以通过text、arrow和annotate函数进行添加。
# text可以将文本绘制在图表的指定坐标(x,y)，还可以加上一些自定义格式：
# ax.text(x,y,'Hello world!' , family = 'monospace' , fontsize=10)

# from datetime import datetime
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# data = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\spx.csv',
#                    index_col=0 , parse_dates=True)
#
# spx = data['SPX']
#
# spx.plot(ax=ax , style = 'k-')
#
# crisis_plot = [
#     (datetime(2007, 10, 11), 'Peak of bull market'),
#     (datetime(2008, 3, 12), 'Bear Stearns Fails'),
#     (datetime(2008, 9, 15), 'Lehman Bankruptcy')
# ]
#
# for date, label in crisis_plot:
#     ax.annotate(label , xy=(date, spx.asof(date)+75),
#                 xytext=(date, spx.asof(date)+225),
#                 arrowprops= dict(facecolor = 'black' ,
#                                  headwidth = 4,
#                                  width = 2,
#                                  headlength=4),
#                 horizontalalignment='left' , verticalalignment='top')
#
# # 放大2007年到2010年
# ax.set_xlim(['1/1/2007' , '1/1/2011'])
# ax.set_ylim([600 , 1800])
# ax.set_title('Important dates in the 2008-2009 financial crisis')
#
#
# ax.annotate方法可以在指定的x和y坐标轴绘制标签。
# 我们使用set_xlim和set_ylim人工设定起始和结束边界，而不使用
# matplotlib的默认方法。
# 最后，用ax.set_title添加图标标题。

# 在图表中添加一个图形，你需要创建一个块对象shp，
# 然后通过ax.add_patch(shp)将其添加到subplot中

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# rect = plt.Rectangle((0.2 , 0.75) , 0.4 , 0.15 , color='k', alpha=0.3)
# circ = plt.Circle((0.7 , 0.2) , 0.15 , color='b' , alpha=0.3)
# pgon = plt.Polygon([[0.15 , 0.15] , [0.35 , 0.4] , [0.2 , 0.6]] , color='g' , alpha = 0.5)
# ax.add_patch(rect)
# ax.add_patch(circ)
# ax.add_patch(pgon)

## 利用plt.savefig可以将当前图表保存到文件

# 将图表保存为SVG文件
# plt.savefig('figpath.svg')

# 要得到一张带有最小白边且分辨率为400DPI的PNG图片
# plt.savefig('figpath.png' , dpi=400 , box_inches='tight')
# dpi:控制“每英寸点数”分辨率
# bbox_inches:可以剪除当前图表周围的空白部分
# 写入BytesIO对象
# from io import BytesIO
# buffer = BytesIO()
# plt.savefig(buffer)
# plot_data = buffer.getvalue()


## matplotlib 配置

# 一种Python编程方式配置系统的方法是使用rc方法。
# 例如，要将全局的图像默认大小设置为10×10，你可以执行：

# plt.rc('figure' , figsize=(10,10))
# # 第一个参数是希望自定义的参数，后边是关键字

## 写成一个字典，然后应用成默认
# font_options = {'family':'monospace' ,
#                 'weight':'bold' ,
#                 'size':'small'}
# plt.rc('font',**font_options)

# 要了解全部的自定义选项，请查阅matplotlib的配置文件matplotlibrc（位于
# matplotlib/mpl-data目录中）。如果对该文件进行了自定义，并将其放在你自
# 己的.matplotlibrc目录中，则每次使用matplotlib时就会加载该文件。


## 9.2 使用pandas和seaborn绘图


# 9.2.1 折线图

## plot()默认绘制折线图
# s = pd.Series(np.random.randn(10).cumsum() , index=np.arange(0 , 100 , 10))
# s.plot()

#DataFrame的plot方法会在一个subplot中为各列绘制一条线，并自动创建图例
# df = pd.DataFrame(np.random.randn(10 ,4).cumsum(0),
#                   columns=['A', 'B', 'C','D'],
#                   index=np.arange(0 , 100 , 10))
#
# df.plot()

# 补充有关matplotlib API的知识



## 柱状图
## plot.bar()和plot.barh()分别绘制水平和垂直的柱状图。
## Series和DataFrame的索引将会被用作X（bar）或Y（barh）刻度

# fig,axes = plt.subplots(2,1)
# data = pd.Series(np.random.randn(16) , index = list('abcdefghijklmnop'))
# data.plot.bar(ax=axes[0] , color='k' , alpha=0.7)
#
# data.plot.barh(ax=axes[1] , color='k' , alpha = 0.7)


# 对于DataFrame，柱状图会将每一行的值分为一组，并排显示
#
# df = pd.DataFrame(np.random.randn(6,4) ,
#                   index=['one' , 'two' , 'three' , 'four' , 'five' , 'six'],
#                   columns=pd.Index(['A','B','C','D'] , names = 'Genus'))
# df
# Out[17]:
#               A         B         C         D
# one   -1.198904 -0.665105 -0.590628  0.480832
# two   -0.338580 -1.949920  1.224947  0.277247
# three  1.302162 -0.190733 -0.299809 -0.165985
# four  -0.003440 -1.978005  1.038188 -0.200463
# five   0.990437 -0.777317  1.561968  1.009782
# six   -0.051970 -0.737326  0.279908  0.777146
# df.plot.bar()

# 设置stacked=True即可为DataFrame生成堆积柱状图，这样每行的值就会被堆积在一起

# df.plot.barh(stacked =True , alpha = 0.5)

# 笔记：柱状图有一个非常不错的用法：利用value_counts图形化显示
# Series中各值的出现频率，比如s.value_counts().plot.bar()

# 再以本书前面用过的那个有关小费的数据集为例，假设我们想要做一张堆积
# 柱状图以展示每天各种聚会规模的数据点的百分比。我用read_csv将数据加
# 载进来，然后根据日期和聚会规模创建一张交叉表：

# tips = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\ips.csv')
# party_counts = pd.crosstab(tips['day' ] , tips['size'])
# party_counts
# Out[23]:
# size  1   2   3   4  5  6
# day
# Fri   1  16   1   1  0  0
# Sat   2  53  18  13  1  0
# Sun   0  39  15  18  3  1
# Thur  1  48   4   5  1  3

## .loc[行标签，列标签]    ，  .loc[: ,  2:5  ]  行都要，列要2到5列

# party_counts = party_counts.loc[: , 2:5]
#  标准化至和为1
# party_pcts = party_counts.div(party_counts.sum(1) , axis=0)
# party_pcts
# Out[26]:
# size         2         3         4         5
# day
# Fri   0.888889  0.055556  0.055556  0.000000
# Sat   0.623529  0.211765  0.152941  0.011765
# Sun   0.520000  0.200000  0.240000  0.040000
# Thur  0.827586  0.068966  0.086207  0.017241

# 对于在绘制一个图形之前，需要进行合计的数据，使用seaborn可以减少工作量。
# 用seaborn来看每天的小费比例:

# tips['tip_pct'] = tips['tip'] / (tips['total_bill'] - tips['tip'])
# tips.head()
# Out[30]:
#    total_bill   tip smoker  day    time  size   tip_pct
# 0       16.99  1.01     No  Sun  Dinner     2  0.063204
# 1       10.34  1.66     No  Sun  Dinner     3  0.191244
# 2       21.01  3.50     No  Sun  Dinner     3  0.199886
# 3       23.68  3.31     No  Sun  Dinner     2  0.162494
# 4       24.59  3.61     No  Sun  Dinner     4  0.172069

###  绘制在柱状图上的黑线代表95%置信区间（可以通过可选参数配置）

# seaborn.barplot有hue选项，使我们能够通过一个额外的分类值将数据分离
# sns.barplot(x='tip_pct' , y = 'day' , data = tips , orient='h')

# 用seaborn.set在不同的图形外观之间切换
# sns.set(style = "whitegrid")


## 直方图和密度图

# 直方图（histogram）是一种可以对值频率进行离散化显示的柱状图。
# 数据点被拆分到离散的、间隔均匀的面元中，绘制的是各面元中数据点的数量。
# 再以前面那个小费数据为例，通过在Series使用plot.hist方法，
# 我们可以生成一张“小费占消费总额百分比”的直方图
## bins=50 是说每张图柱子的个数
# tips['tip_pct'].plot.hist(bins=50)


# 密度图也被称作KDE（KernelDensity Estimate，核密度估计）图。
# 使用plot.kde和标准混合正态分布估计即可生成一张密度图

# tips['tip_pct'].plot.density()


# seaborn的distplot方法绘制直方图和密度图更加简单，
# 还可以同时画出直方图和连续密度估计图。
# 作为例子，考虑一个双峰分布，由两个不同的标准正态分布组成:

# comp1 = np.random.normal(0 ,1 ,  size = 200)
# comp2 = np.random.normal(10,2,size=200)
# values = pd.Series(np.concatenate([comp1 , comp2]))
# sns.distplot(values , bins=100 , color ='k')


## 9.2.4 散布图或点图
# 点图或散布图是观察两个一维数据序列之间的关系的有效手段。

# macro = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\macrodata.csv')
# data = macro[['cpi', 'm1', 'tbilrate','unemp']]
# trans_data = np.log(data).diff().dropna()            # 计算对数差
#
# trans_data[-5:]
# Out[40]:
#           cpi        m1  tbilrate     unemp
# 198 -0.007904  0.045361 -0.396881  0.105361
# 199 -0.021979  0.066753 -2.277267  0.139762
# 200  0.002340  0.010286  0.606136  0.160343
# 201  0.008419  0.037461 -0.200671  0.127339
# 202  0.008894  0.012202 -0.405465  0.042560

# # 用seaborn的regplot方法，它可以做一个散布图，并加上一条线性回归的线
# sns.regplot('m1' , 'unemp' , data = trans_data)
# # 给图命名
# plt.title('Changes in log %s versus log %s' % ('m1' , 'unemp'))
# Out[42]: Text(0.5, 1, 'Changes in log m1 versus log unemp')

# 所以seaborn提供了一个便捷的pairplot函数，
# 它支持在对角线上放置每个变量的直方图或密度估计
# sns.pairplot(trans_data , diag_kind='kde' , plot_kws={'alpha':0.2})
# plot_kws参数:它可以让我们传递配置选项到非对角线元素上的图形使用
# 更详细的配置选项，可以查阅seaborn.pairplot文档字符串


## 9.2.5 分面网格和分类数据

# seaborn有一个有用的内置函数factorplot (现在这个函数被命名为catplot)，可以简化制作多种分面图

# 生成的图按日期、时间、是否吸烟划分的小费百分比
# sns.catplot(x='day' , y='tip_pct' , hue='time' , col='smoker',
#                kind='bar' , data = tips[tips.tip_pct < 1])


# 除了在分面中用不同的颜色按时间分组，
# 我们还可以通过给每个时间值添加一行来扩展分面网格：
# sns.catplot(x='day' , y='tip_pct' , row='time',
#             col='smoker',
#             kind='bar' , data=tips[tips.tip_pct<1])

# 也可以更改图的类型
# sns.catplot(x='tip_pct' , y = 'day' , kind='box' ,
#             data=tips[tips.tip_pct < 0.5])
# 使用更通用的seaborn.FacetGrid类，你可以创建自己的分面网格。
# 请查阅seaborn的文档（https://seaborn.pydata.org/）


## 10.2 数据聚合

# df
# Out[89]:
#   key1 key2     data1     data2
# 0    a  one -0.804929  0.836882
# 1    a  two -0.100697 -0.344798
# 2    b  one -0.958730  0.442310
# 3    b  two -1.319834 -0.177402
# 4    a  one  0.169965  1.158086
# grouped = df.groupby('key1')
# grouped['data1'].quantile(0.9)
# Out[91]:
# key1
# a    0.115833
# b   -0.994841
# Name: data1, dtype: float64

# 使用你自己的聚合函数，只需将其传入aggregate或agg方法即可：

# def peak_to_peak(arr):
#     return arr.max()-arr.min()
# grouped.agg(peak_to_peak)
# Out[92]:
#          data1     data2
# key1
# a     0.974895  1.502884
# b     0.361104  0.619712

# grouped.describe()
# Out[94]:
#      data1                      ...     data2
#      count      mean       std  ...       50%       75%       max
# key1                            ...
# a      3.0 -0.245220  0.503260  ...  0.836882  0.997484  1.158086
# b      2.0 -1.139282  0.255339  ...  0.132454  0.287382  0.442310
# [2 rows x 16 columns]

### 10.2.1 逐列及多函数应用

# tips = pd.read_csv('D:\data_py\pydata-book-2nd-edition\examples\ips.csv')
# # 添加了一个小费百分比的列tip_pct：
# tips['tip_pct'] = tips['tip']/tips['total_bill']
# tips[:6]
# Out[97]:
#    total_bill   tip smoker  day    time  size   tip_pct
# 0       16.99  1.01     No  Sun  Dinner     2  0.059447
# 1       10.34  1.66     No  Sun  Dinner     3  0.160542
# 2       21.01  3.50     No  Sun  Dinner     3  0.166587
# 3       23.68  3.31     No  Sun  Dinner     2  0.139780
# 4       24.59  3.61     No  Sun  Dinner     4  0.146808
# 5       25.29  4.71     No  Sun  Dinner     4  0.186240


## 对不同的列使用不同的聚合函数，或一次应用多个函数。
##  根据天和smoker对tips进行分组：

# grouped = tips.groupby(['day' , 'smoker'])     # 以day , smoker分组
# grouped_pct = grouped['tip_pct']               # 对分过的碎片选出tip_pct这一列
# grouped_pct.agg('mean')                        # 对这一列算平均数
# Out[100]:
# day   smoker
# Fri   No        0.151650
#       Yes       0.174783
# Sat   No        0.158048
#       Yes       0.147906
# Sun   No        0.160113
#       Yes       0.187250
# Thur  No        0.160298
#       Yes       0.163863
# Name: tip_pct, dtype: float64

# grouped_pct.agg(['mean' , 'std' , peak_to_peak])   # 把计算函数放进一个列里，一起算
# Out[101]:
#                  mean       std  peak_to_peak
# day  smoker
# Fri  No      0.151650  0.028123      0.067349
#      Yes     0.174783  0.051293      0.159925
# Sat  No      0.158048  0.039767      0.235193
#      Yes     0.147906  0.061375      0.290095
# Sun  No      0.160113  0.042347      0.193226
#      Yes     0.187250  0.154134      0.644685
# Thur No      0.160298  0.038774      0.193350
#      Yes     0.163863  0.039389      0.151240

# 传入的是一个由(name,function)元组组成的列表，
# 则各元组的第一个元素就会被用作DataFrame的列名














