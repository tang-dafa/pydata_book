"""
    时间：2019/9/23
    作者：大发
    功能：练习用 导入
"""

# import c2_some_module
# result = c2_some_module.f(5)
# pi = c2_some_module.PI

# from c2_some_module import f , g , PI
# result = g (5 , PI )

import c2_some_module as csm
from c2_some_module import PI as pi , g as gf

r1 = csm.f(pi)
r2 = gf(6 , pi)