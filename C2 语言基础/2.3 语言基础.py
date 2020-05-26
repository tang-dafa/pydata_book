"""
    时间：2019/9/23
    作者：大发
    内容：第二章笔记
"""

#由于之前已经过了几遍基础，在学习数据分析这本书中，我只记录之前未见过的语法。


## 用isinstance检查一个对象是否是某类型
# a = 5
# isinstance(a,int)
# Out[3]: True


##检查对象是不是一个你想要的类型，如果不是就转换成你想要的
# if not isinstance(x , list ) and isiterable(x):
#     x = list(x)



## .count()可以计算括号中内容在对象中的数量
# c = """biuehre
# gehnoihm
# iunowoi"""
# c.count('\n')
# Out[7]: 2

###  !!!字符串和元组是不可更改的


##字符串格式化也是一个很重要的主题
# template = '{0 : .2f } {1 : s } are worth US${ 2 : d}'
# {0 : .2f } 把第一个参数格式化成2位小数的浮点数
# {1 : s } 把第二个参数格式化成字符串
# { 2 : d} 把第三个参数格式化成整数
# template.format(4.5560 , 'Argentine Pesos ' , 1)
# .format() 利用上述内容生成新的字符串
# "{0:.2f} {1:s} are worth US${2:d}".format(4.5560 , 'Argentine Pesos ' , 1)
# Out[15]: '4.56Argentine Pesos  are worth US$1'


##用encode方法把字符串转换为 UTF-8 字符   ,   decode 用来解码
# val = "esnnol"
# val_utf8 = val.encode('utf-8')
# val_utf8
# Out[23]: b'esnnol'
# type(val_utf8)
# Out[24]: bytes


## range(起始, 终止， 步进)
# list(range(12,50,5))
# Out[27]: [12, 17, 22, 27, 32, 37, 42, 47]

##三元表达式，存疑