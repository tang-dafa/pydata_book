"""
    作者：大发
    时间：2019/12/21
    功能：p416
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

fec = pd.read_csv('D:\data_py\pydata_book\C14_example\pydata-book-2nd-edition\datasets\_fec\P00000001-ALL.csv')
fec.info()
# <class 'pandas.core.frame.DataFrame'>
# # RangeIndex: 1001731 entries, 0 to 1001730
# # Data columns (total 16 columns):
# # cmte_id              1001731 non-null object
# # cand_id              1001731 non-null object
# # cand_nm              1001731 non-null object
# # contbr_nm            1001731 non-null object
# # contbr_city          1001712 non-null object
# # contbr_st            1001727 non-null object
# # contbr_zip           1001620 non-null object
# # contbr_employer      988002 non-null object
# # contbr_occupation    993301 non-null object
# # contb_receipt_amt    1001731 non-null float64
# # contb_receipt_dt     1001731 non-null object
# # receipt_desc         14166 non-null object
# # memo_cd              92482 non-null object
# # memo_text            97770 non-null object
# # form_tp              1001731 non-null object
# # file_num             1001731 non-null int64
# # dtypes: float64(1), int64(1), object(14)
# # memory usage: 122.3+ MB

fec.iloc[123456]  # 严格用于整数索引，.loc则用于字符索引
# Out[5]:
# cmte_id                             C00431445
# cand_id                             P80003338
# cand_nm                         Obama, Barack
# contbr_nm                         ELLMAN, IRA
# contbr_city                             TEMPE
# contbr_st                                  AZ
# contbr_zip                          852816719
# contbr_employer      ARIZONA STATE UNIVERSITY
# contbr_occupation                   PROFESSOR
# contb_receipt_amt                          50
# contb_receipt_dt                    01-DEC-11
# receipt_desc                              NaN
# memo_cd                                   NaN
# memo_text                                 NaN
# form_tp                                 SA17A
# file_num                               772372
# Name: 123456, dtype: object


### 通过unique，你可以获取全部的候选人名单：
unique_cands = fec.cand_nm.unique()         # .unique 意思是只要唯一， 不要有重复
unique_cands
# Out[6]:
# array(['Bachmann, Michelle', 'Romney, Mitt', 'Obama, Barack',
#        "Roemer, Charles E. 'Buddy' III", 'Pawlenty, Timothy',
#        'Johnson, Gary Earl', 'Paul, Ron', 'Santorum, Rick',
#        'Cain, Herman', 'Gingrich, Newt', 'McCotter, Thaddeus G',
#        'Huntsman, Jon', 'Perry, Rick'], dtype=object)
# In[8]: len(unique_cands)
# Out[8]: 13

unique_cands[2]
# Out[9]: 'Obama, Barack'


### 指明党派信息的方法之一是使用字典：
parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

### 通过这个映射以及Series对象的map方法，你可以根据候选人姓名得到一组党派信息：
fec.cand_nm[123456:123461]
# Out[11]:
# 123456    Obama, Barack
# 123457    Obama, Barack
# 123458    Obama, Barack
# 123459    Obama, Barack
# 123460    Obama, Barack
# Name: cand_nm, dtype: object

fec.cand_nm[123456:123461].map(parties)      # 映射拿到党派列
# Out[13]:
# 123456    Democrat
# 123457    Democrat
# 123458    Democrat
# 123459    Democrat
# 123460    Democrat
# Name: cand_nm, dtype: object

### 增加党派列
fec['party'] = fec.cand_nm.map(parties)
fec['party'].value_counts()              # 用来计数
# Out[15]:
# Democrat      593746
# Republican    407985
# Name: party, dtype: int64

### 赞助款列有正有负，负的是退款
(fec.contb_receipt_amt > 0 ).value_counts()
# Out[16]:
# True     991475
# False     10256
# Name: contb_receipt_amt, dtype: int64

### 为了简化分析过程，我限定该数据集只能有正的出资额：
fec = fec[fec.contb_receipt_amt > 0]       # 利用布尔值筛选数据

### 由于Barack Obama和Mitt Romney是最主要的两名候选人，
### 所以我还专门准备了一个子集，只包含针对他们两人的竞选活动的赞助信息：
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack' , 'Romney, Mitt'])]

### 14.5.1 根据职业和雇主统计赞助信息

fec.contbr_occupation.value_counts()[:10]
# Out[19]:
# RETIRED                                   233990
# INFORMATION REQUESTED                      35107
# ATTORNEY                                   34286
# HOMEMAKER                                  29931
# PHYSICIAN                                  23432
# INFORMATION REQUESTED PER BEST EFFORTS     21138
# ENGINEER                                   14334
# TEACHER                                    13990
# CONSULTANT                                 13273
# PROFESSOR                                  12555
# Name: contbr_occupation, dtype: int64

###不难看出，许多职业都涉及相同的基本工作类型，或者同一样东西有多种变体。
### 下面的代码片段可以清理一些这样的数据（将一个职业信息映射到另一个）。
### 注意，这里巧妙地利用了dict.get，它允许没有映射关系的职业也能“通 过”：
occ_mapping = {
    'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
    'INFORMATION REQUESTED' : 'NOT PROVIDED',
    'INFORMATION REQUESTED (BEST EFFORTS)' : 'NOT PROVIDED',
    'C.E.O.': 'CEO'
}

# 如果没有映射提供的话就返回它本身
f = lambda x:occ_mapping.get(x,x)
fec.contbr_occupation = fec.contbr_occupation.map(f)

# 对雇主的信息也进行同样的处理：
emp_mapping = {
 'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
 'INFORMATION REQUESTED' : 'NOT PROVIDED',
 'SELF' : 'SELF-EMPLOYED',
 'SELF EMPLOYED' : 'SELF-EMPLOYED',
}
# If no mapping provided, return x
f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)

### 可以通过pivot_table根据党派和职业对数据进行聚合，
### 然后过滤掉总出资额不足200万美元的数据：
by_occupation = fec.pivot_table('contb_receipt_amt' ,
                                index = 'contbr_occupation' ,
                                columns='party' , aggfunc=sum)

over_2mm = by_occupation[by_occupation.sum(1) > 2000000]      # .sum(1)是列的和，.sum(0)是行的和
# In[30]: over_2mm
# Out[30]:
# party                 Democrat    Republican
# contbr_occupation
# ATTORNEY           11141982.97  7.477194e+06
# CEO                 2074974.79  4.211041e+06
# CONSULTANT          2459912.71  2.544725e+06
# ENGINEER             951525.55  1.818374e+06
# EXECUTIVE           1355161.05  4.138850e+06
# HOMEMAKER           4248875.80  1.363428e+07
# INVESTOR             884133.00  2.431769e+06
# LAWYER              3160478.87  3.912243e+05
# MANAGER              762883.22  1.444532e+06
# NOT PROVIDED        4866973.96  2.056547e+07
# OWNER               1001567.36  2.408287e+06
# PHYSICIAN           3735124.94  3.594320e+06
# PRESIDENT           1878509.95  4.720924e+06
# PROFESSOR           2165071.08  2.967027e+05
# REAL ESTATE          528902.09  1.625902e+06
# RETIRED            25305116.38  2.356124e+07
# SELF-EMPLOYED        672393.40  1.640253e+06

### 将上图做成柱状图
over_2mm.plot(kind='barh')


### 想了解一下对Obama和Romney总出资额最高的职业和企业。
### 为此，我们先对候选人进行分组，然后使用本章前面介绍的类似top的方法：

def get_top_amounts(group , key , n=5) :
    totals = group.groupby(key)['contb_receipt_amt'].sum()     # 用key分组，算和
    return totals.nlargest(n)                      # 排序

### 根据职业和雇主聚合：
grouped = fec_mrbo.groupby('cand_nm')
grouped.apply(get_top_amounts,'contbr_occupation' , n=7)
# Out[32]:
# cand_nm        contbr_occupation
# Obama, Barack  RETIRED                                   25305116.38
#                ATTORNEY                                  11141982.97
#                INFORMATION REQUESTED                      4866973.96
#                HOMEMAKER                                  4248875.80
#                PHYSICIAN                                  3735124.94
#                LAWYER                                     3160478.87
#                CONSULTANT                                 2459912.71
# Romney, Mitt   RETIRED                                   11508473.59
#                INFORMATION REQUESTED PER BEST EFFORTS    11396894.84
#                HOMEMAKER                                  8147446.22
#                ATTORNEY                                   5364718.82
#                PRESIDENT                                  2491244.89
#                EXECUTIVE                                  2300947.03
#                C.E.O.                                     1968386.11
# Name: contb_receipt_amt, dtype: float64

grouped.apply(get_top_amounts,'contbr_employer' , n=10)
# Out[33]:
# cand_nm        contbr_employer
# Obama, Barack  RETIRED                                   22694358.85
#                SELF-EMPLOYED                             17080985.96
#                NOT EMPLOYED                               8586308.70
#                INFORMATION REQUESTED                      5053480.37
#                HOMEMAKER                                  2605408.54
#                SELF                                       1076531.20
#                SELF EMPLOYED                               469290.00
#                STUDENT                                     318831.45
#                VOLUNTEER                                   257104.00
#                MICROSOFT                                   215585.36
# Romney, Mitt   INFORMATION REQUESTED PER BEST EFFORTS    12059527.24
#                RETIRED                                   11506225.71
#                HOMEMAKER                                  8147196.22
#                SELF-EMPLOYED                              7409860.98
#                STUDENT                                     496490.94
#                CREDIT SUISSE                               281150.00
#                MORGAN STANLEY                              267266.00
#                GOLDMAN SACH & CO.                          238250.00
#                BARCLAYS CAPITAL                            162750.00
#                H.I.G. CAPITAL                              139500.00
# Name: contb_receipt_amt, dtype: float64


### 14.5.2 捐赠金额分桶
### 利用cut函数根据出资额的大小将数据离散化到多个面元中

bins = np.array([0 , 1, 10 , 100 , 1000 , 10000 , 100000 , 1000000 , 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt , bins)

# In[35]: labels
# Out[35]:
# 411           (10, 100]
# 412         (100, 1000]
# 413         (100, 1000]
# 414           (10, 100]
# 415           (10, 100]
# 416           (10, 100]
# 417         (100, 1000]
# 418           (10, 100]
# 419         (100, 1000]
# 420           (10, 100]
# 421           (10, 100]
# 422         (100, 1000]
# 423         (100, 1000]
# 424         (100, 1000]
# 425         (100, 1000]
# 426         (100, 1000]
# 427       (1000, 10000]
# 428         (100, 1000]
# 429         (100, 1000]
# 430           (10, 100]
# 431       (1000, 10000]
# 432         (100, 1000]
# 433         (100, 1000]
# 434         (100, 1000]
# 435         (100, 1000]
# 436         (100, 1000]
# 437           (10, 100]
# 438         (100, 1000]
# 439         (100, 1000]
# 440           (10, 100]
#               ...
# 701356        (10, 100]
# 701357          (1, 10]
# 701358        (10, 100]
# 701359        (10, 100]
# 701360        (10, 100]
# 701361        (10, 100]
# 701362      (100, 1000]
# 701363        (10, 100]
# 701364        (10, 100]
# 701365        (10, 100]
# 701366        (10, 100]
# 701367        (10, 100]
# 701368      (100, 1000]
# 701369        (10, 100]
# 701370        (10, 100]
# 701371        (10, 100]
# 701372        (10, 100]
# 701373        (10, 100]
# 701374        (10, 100]
# 701375        (10, 100]
# 701376    (1000, 10000]
# 701377        (10, 100]
# 701378        (10, 100]
# 701379      (100, 1000]
# 701380    (1000, 10000]
# 701381        (10, 100]
# 701382      (100, 1000]
# 701383          (1, 10]
# 701384        (10, 100]
# 701385      (100, 1000]
# Name: contb_receipt_amt, Length: 694282, dtype: category
# Categories (8, interval[int64]): [(0, 1] < (1, 10] < (10, 100] < (100, 1000] < (1000, 10000] <
#                                   (10000, 100000] < (100000, 1000000] < (1000000, 10000000]]


### 现在可以根据候选人姓名以及面元标签对奥巴马和罗姆尼数据进行分组，以得到一个柱状图：
grouped = fec_mrbo.groupby(['cand_nm' , labels])
grouped.size().unstack(0)
# Out[36]:
# cand_nm              Obama, Barack  Romney, Mitt
# contb_receipt_amt
# (0, 1]                       493.0          77.0
# (1, 10]                    40070.0        3681.0
# (10, 100]                 372280.0       31853.0
# (100, 1000]               153991.0       43357.0
# (1000, 10000]              22284.0       26186.0
# (10000, 100000]                2.0           1.0
# (100000, 1000000]              3.0           NaN
# (1000000, 10000000]            4.0           NaN

###在小额赞助方面，Obama获得的数量比Romney多得多。
# 你还可以对出资额求和并在面元内规格化，
# 以便图形化显示两位候选人各种赞助额度的比例：

bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1) , axis = 0)
# In[38]: normed_sums
# Out[38]:
# cand_nm              Obama, Barack  Romney, Mitt
# contb_receipt_amt
# (0, 1]                    0.805182      0.194818
# (1, 10]                   0.918767      0.081233
# (10, 100]                 0.910769      0.089231
# (100, 1000]               0.710176      0.289824
# (1000, 10000]             0.447326      0.552674
# (10000, 100000]           0.823120      0.176880
# (100000, 1000000]         1.000000           NaN
# (1000000, 10000000]       1.000000           NaN

normed_sums[:-2].plot(kind='barh')


### 14.5.3 根据州统计赞助信息
grouped = fec_mrbo.groupby(['cand_nm' , 'contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
totals[:10]
# Out[40]:
# cand_nm    Obama, Barack  Romney, Mitt
# contbr_st
# AK             281840.15      86204.24
# AL             543123.48     527303.51
# AR             359247.28     105556.00
# AZ            1506476.98    1888436.23
# CA           23824984.24   11237636.60
# CO            2132429.49    1506714.12
# CT            2068291.26    3499475.45
# DC            4373538.80    1025137.50
# DE             336669.14      82712.00
# FL            7318178.58    8338458.81

# 如果对各行除以总赞助额，就会得到各候选人在各州的总赞助额比例：

percent = totals.div(totals.sum(1) , axis = 0)
percent[:10]

# Out[41]:
# cand_nm    Obama, Barack  Romney, Mitt
# contbr_st
# AK              0.765778      0.234222
# AL              0.507390      0.492610
# AR              0.772902      0.227098
# AZ              0.443745      0.556255
# CA              0.679498      0.320502
# CO              0.585970      0.414030
# CT              0.371476      0.628524
# DC              0.810113      0.189887
# DE              0.802776      0.197224
# FL              0.467417      0.532583







