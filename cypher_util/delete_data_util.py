"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 图数据库所有的删除函数

"""


"""删除函数"""


# 删除所有结点和边
def delete_all(g):
    res = """
        MATCH (n)
        DETACH DELETE n
    """
    return g.run(res)
