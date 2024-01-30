"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/9/28
    @Introduction: 存储图数据库相关的常用数学函数

"""


import re


# 默认排序sort的key函数
def re_get_num(x):
    # 正则化匹配"（...）"
    regularization = re.findall("（\d*）", x)
    num = int(regularization[0][1:-1])

    return num
