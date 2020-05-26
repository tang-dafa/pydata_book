"""
    时间：2019/9/23
    作者：大发
    内容：第三章笔记
"""

##  tuple()  把别的转换成元组   元组用的是（）圆括号
#  元组不可改，但元组内部的对象的内部是可更改的
# tup = tuple(['foo',[1,2],True])
# tup[1].append(3)
# tup
# Out[4]: ('foo', [1, 2, 3], True)


##  元组拆包
# tup = (4, 5, 6)
# a, b, c =tup
# b
# Out[7]: 5

# a,b = 3,4
# a
# Out[9]: 3

#利用拆包遍历元组或列表组成的序列
# seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
# for a, b, c in seq:
#     print('a={0},b={1},c={2}'.format(a, b, c))
#
# a = 1, b = 2, c = 3
# a = 4, b = 5, c = 6
# a = 7, b = 8, c = 9

#  *rest 或  *_   用来在拆包中表示不想要的变量
# values = 1,2,3,4,5
# a,b,*rest = values
# rest
# Out[16]: [3, 4, 5]


## 列表list  用[]中括号  可修改， 用法与元组一致
# gen = range (10)
# gen
# Out[18]: range(0, 10)
# list(gen)
# Out[19]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# .append('x')在列表尾部加入一个x元素
# .extend() 可以向列表添加多个元素   （ 运算代价较小的一种方式 ）
# .insert(a, 'b')  在列表指定的a位置， 加入b元素
# .pop(2)  移除位置2上的元素，并返回该元素
# .remove('X') 也是移除对象用的，但它查找的是元素，列表中的对象，而且只移除它查找到的第一个对象

# .sort() 可以对列表排序
# .sort(key = len)  按列表中字符串的长度排序
# import bisect
# c = [1,2,2,2,4,6,8,9]
# bisect.bisect(c,7)    #  找到元素应被插入的位置  但没有将元素插入
# Out[22]: 6
# bisect.insort(c,1)    # 将元素插入
# c
# Out[24]: [1, 1, 2, 2, 2, 4, 6, 8, 9]

#切片
# seq = [1, 2, 2, 2, 4, 6, 8, 9]
# seq[1:3]
# Out[28]: [2, 2]
# seq[5:7] = [0 ,0]     #切片替换
# seq
# Out[30]: [1, 2, 2, 2, 4, 0, 0, 9]
#  seq[-6:-2]  #负向切片
#  seq[::2]     #第二个冒号后，是表示步进值，隔几个数取一次值
#  seq[::-1]    #步进值为-1， 则是把元素或列表进行反转   #  矩阵可能会用到

## enumerate  遍历一个序列的同时追踪当前元素的索引
# some_list = ['ffo', 'bwu' , 'booo']
# mapping = {}
# for i , v in enumerate(some_list):
#     mapping[v] = i
# mapping
# Out[4]: {'ffo': 0, 'bwu': 1, 'booo': 2}

## sorted 函数
# sorted([1,9,3,7,6,8,4,9,5,0,3])
# Out[6]: [0, 1, 3, 3, 4, 5, 6, 7, 8, 9, 9]
# sorted ('amount number')
# Out[7]: [' ', 'a', 'b', 'e', 'm', 'm', 'n', 'n', 'o', 'r', 't', 'u', 'u']

##  zip  可以将列表，元组与其他序列的元素配对，新建一个元组构成的列表
# seq1 = ['fofo', 'wii' , 'aof']
# seq2 = ['one' , 'two', 'three']
# zipped = zip(seq1 , seq2)
# list(zipped)
# Out[11]: [('fofo', 'one'), ('wii', 'two'), ('aof', 'three')]
##  如果列表的长度不一致，按最短的
# for i,(a,b) in enumerate(zip(seq1 , seq2)) :
#     print('{0}:{1},{2}'.format(i , a, b))
# 0:fofo,one
# 1:wii,two
# 2:aof,three
## 这个方法可以用来形成矩阵
## 拆分序列
# pitcher = [('fofo', 'one'), ('wii', 'two'), ('aof', 'three')]
# add_names , ass_names = zip(*pitcher)
# add_names
# Out[15]: ('fofo', 'wii', 'aof')
# ass_names
# Out[16]: ('one', 'two', 'three')

##  reversed  将元素倒序排列
# list(reversed(range(10)))
# Out[17]: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

##  dict 字典{}，键值对集合（大概可以，一个键是指一个被试，值对应一个被试的所有数据）
##  del   或 pop 方法删除键值对

##由首字母分类
# words = ['apple' , 'bat' , 'bar' , 'atom' , 'cook']
# by_letter = {}
# for word in words :
#     letter = word[0]
#     if letter not in by_letter :
#         by_letter[letter] = [word]
#     else :
#         by_letter[letter].append(word)
# by_letter
# Out[20]: {'a': ['apple', 'atom'], 'b': ['bat', 'bar'], 'c': ['cook']}
##这个步骤简化为  setdefault  方法:
# for word in words :
#     letter = word[0]
#     by_letter.setdefault(letter, []).append(word)
##  defaultdict  方法
# from colllections import defaultdict
# by_letter = defaultdict(list)
# for word in words :
#     by_letter[word[0]].append(word)

##列表推导式 [expe for val in collection if condition] 而且把字母该为大写了
# strings = ['a', 'ass', 'hu', 'ouw', 'pqos']
# [x.upper() for x in strings if len(x)>2]
# Out[3]: ['ASS', 'OUW', 'PQOS']

# 集合推导式 set_comp = {expe for val in collection if condition}

## map()函数的使用
# strings = ['a', 'ass', 'hu', 'ouw', 'pqos']
# set(map(len,strings))
# Out[4]: {1, 2, 3, 4}

# 字典推导式 dict_comp = {key-expr : value-expr for value in collection if condition}
# strings = ['a', 'ass', 'hu', 'ouw', 'pqos']
# loc_mapping = {val : index   for  index, val  in  enumerate(strings)}
# loc_mapping
# Out[8]: {'a': 0, 'ass': 1, 'hu': 2, 'ouw': 3, 'pqos': 4}

##嵌套推导式
# some_tuples = [(1,2,3),(4,5,6),(7,8,9)]
# flattended = [x for tup in some_tuples for x in tup]
# flattended
# Out[11]: [1, 2, 3, 4, 5, 6, 7, 8, 9]
## 主要看嵌套的顺序 ， 先从大列表中取元组，从元组中取值，当然也不一定非得是元组
# 也可以    [ [ x for x in tup ] for tup in some_tuples]

##清洗数据，去掉符号，统一大小写，去除空格
# states = ['  ajWSXbw', ' 87vuEw!', 'jhGSdi0']
# import re
# def remove_punc(value):
#     return re.sub('[!?#]', ' ', value)
# clean_ops = [str.strip, remove_punc, str.title]
# def clean_strings(strings, ops):
#     result = []
#     for value in strings:
#         for function in ops :
#             value = function(value)
#         result.append(value)
#     return result
# clean_strings(states, clean_ops)
# Out[15]: ['Ajwsxbw', '87Vuew ', 'Jhgsdi0']


# for x in map(remove_punc, states):
#     print(x)
#
# ajWSXbw
# 87
# vuEw
# jhGSdi0


###  匿名函数  Lambda函数
###  部分参数应用

##生成器
# def squares(n = 10) :
#     print('Generating squares from 1 to {0}'.format(n ** 2))
#     for i in range(1,n+1):
#         yield i**2     ## 把return转换成 yield，就是生成器了
# gen = squares()
# for x in gen :        ##必须请求生成器中的元素才会执行它的代码
#     print(x, end=' , ')
#
# Generating squares from 1 to 100
# 1, 4, 9, 16, 25, 36, 49, 64, 81, 100,

###一个简单的生成器表达式
# gen = (x**2 for x in range(100))
##一个用法
# dict((i, i**2) for x in range(5))   ##括号里边是一个简单的生成器表达式，整个是一个字典


###  打开读取，关闭
# path = '     .txt'
# f = open(path)
# f.close()                ##使用with语句，会自动关闭

# f = open(path , 'w')   ##一个新文件会被创建并覆盖原文件
# f = open(path , 'x')   ##也能创建一个可写的文件
