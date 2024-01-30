"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 图数据库所有的更新函数

"""


# LLH NEW:
# 补全缺失的数据
def complete_null_data(g, label, property):
    res = "MATCH (n:" + label + ")"
    res += " WHERE n." + property + " IS NULL"
    res += " SET n." + property + " = ''"
    
    res = g.run(res)
    
    return res


def complete_null_data_cypher_str(label, property):
    res = "MATCH (n:" + label + ")"
    res += " WHERE n." + property + " IS NULL"
    res += " SET n." + property + " = ''"
    
    return res


# 设置节点的关键词属性
def set_themes(g, content):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(content["id"])
    res += " SET n.keywords = " + str(content["keywords"])

    res = g.run(res)

    return res
def set_themes_cypher_str(content):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(content["id"])
    res += " SET n.keywords = " + str(content["keywords"])
    return res


# 设置节点的搜索次数属性
def set_search_number(g, key):
    res = "MATCH (n: " + key + ")"
    res += " WHERE n.search_number IS NULL"
    res += " SET n.search_number = 1"

    res = g.run(res)

    return res

def set_search_number_cypher_str( key):
    res = "MATCH (n: " + key + ")"
    res += " WHERE n.search_number IS NULL"
    res += " SET n.search_number = 1"

    return res


# 更新节点的搜索次数属性
def update_search_number(g, gid):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(gid)
    res += " SET n.search_number = n.search_number + 1"

    res = g.run(res)

    return res

def update_search_number_cypher_str( gid):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(gid)
    res += " SET n.search_number = n.search_number + 1"
    return res


# 更新热词节点
def update_entity_buzzwords(g, buzzwords_list):
    res = "MATCH (n:entity_buzzwords)"

    for i, x in enumerate(buzzwords_list):
        string = x[0] + "," + str(x[1])
        res += " SET n.word_" + str(i) + " = " + "'" + string + "'"

    res = g.run(res)

    return res
def update_entity_buzzwords_cypher_str(buzzwords_list):
    res = "MATCH (n:entity_buzzwords)"
    for i, x in enumerate(buzzwords_list):
        string = x[0] + "," + str(x[1])
        res += " SET n.word_" + str(i) + " = " + "'" + string + "'"

    # res = g.run(res)

    return res


# 设置时间字段为字符串类型
def set_time_properties(g, label, property):
    res = "MATCH (n:" + label + ")"
    res += " SET n." + property + " = toString(n." + property + ")"

    res = g.run(res)

    return res
def set_time_properties_cypher_str(label, property):
    res = "MATCH (n:" + label + ")"
    res += " SET n." + property + " = toString(n." + property + ")"

    return res
