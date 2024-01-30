"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 图数据库所有的查询函数

"""

import time

from static.graph_const import GraphConst


def query_types_count(g, label):  # TODO:新增
    res = "MATCH (n:" + str(label) + ")"
    res += " RETURN count(n)"
    # print("-------前置查看-----")
    tempRes = g.run(res)
    tempRes = [dict(i) for i in tempRes]
    # print(tempRes)
    return g.run(res).single()


def query_types_count_cypher_str(label):
    res = "MATCH (n:" + str(label) + ")"
    res += " RETURN count(n)"
    return res


"""查询结点函数"""


# 查看热词节点是否存在
def check_entity_buzzwords(g):
    res = "MATCH (n:entity_buzzwords)"
    res += " RETURN n"

    res = g.run(res)

    return [x["n"] for x in res]


def check_entity_buzzwords_cypher_str():
    res = "MATCH (n:entity_buzzwords)"
    res += " RETURN n"

    return res


# 查询(时间)结点个数
def query_time_num(g, label, property, themes_properties, text, time):
    res = "MATCH (n: " + label + ")"
    res += " WHERE (n." + property + " CONTAINS " + "'" + time + "'" + ")"

    res += " and "

    for i, x in enumerate(themes_properties[label]):
        if i == 0:
            res += " (n." + x + " CONTAINS " + "'" + text + "'"
        else:
            res += " or n." + x + " CONTAINS " + "'" + text + "'"
    res += ")"

    res += " RETURN count(n)"

    return g.run(res).single()


# 查询(类型)结点个数
def query_type_num(g, label, themes_properties, text):
    res = "MATCH (n: " + label + ")"

    res += " WHERE"

    for i, x in enumerate(themes_properties[label]):
        if i == 0:
            res += " n." + x + " CONTAINS " + "'" + text + "'"
        else:
            res += " or n." + x + " CONTAINS " + "'" + text + "'"

    res += " RETURN count(n)"

    return g.run(res).single()


# 查询(主题)节点主题相关文本
def query_theme_name_with_summary(g, themes_properties, themes_type):
    res = ""
    first_union_mark = 0

    for k, v in themes_properties.items():
        if k in themes_type.keys():
            if themes_type[k] == "string":
                if first_union_mark == 0:
                    first_union_mark = 1
                else:
                    res += " UNION "

                res += "MATCH (n:" + k + ")"
                res += " WHERE n.keywords IS NULL"
                res += " RETURN id(n) AS id, n." + v[0] + " AS name"

                if len(v) == 2:
                    res += ", n." + v[1] + " AS summary"
                else:
                    res += ", " + "''" + " AS summary"

            elif themes_type[k] == "list":
                # TODO
                pass

    res = g.run(res)

    return [x for x in res]


def query_theme_name_with_summary_cypher_str(themes_properties, themes_type):
    res = ""
    first_union_mark = 0

    for k, v in themes_properties.items():
        if k in themes_type.keys():
            if themes_type[k] == "string":
                if first_union_mark == 0:
                    first_union_mark = 1
                else:
                    res += " UNION "

                res += "MATCH (n:" + k + ")"
                res += " WHERE n.keywords IS NULL"
                res += " RETURN id(n) AS id, n." + v[0] + " AS name"

                if len(v) == 2:
                    res += ", n." + v[1] + " AS summary"
                else:
                    res += ", " + "''" + " AS summary"

            elif themes_type[k] == "list":
                # TODO
                pass

    return res


# 查询(主题)节点个数
def query_theme_num(g, themes_properties, text):
    res = ""

    first_union_mark = 0

    for k, v in themes_properties.items():

        if first_union_mark == 0:
            first_union_mark = 1
        else:
            res += " UNION ALL "

        res += "MATCH (n:" + k + ") WHERE"

        for i, x in enumerate(v):
            if i == 0:
                res += " n." + x + " CONTAINS " + "'" + text + "'"
            else:
                res += " or n." + x + " CONTAINS " + "'" + text + "'"

        res += " RETURN n.name_theme AS name_theme, n.summary_theme AS summary_theme"

    res = g.run(res)

    return [x for x in res]


# 查询(公司)节点个数
def query_company_num(g):
    res = """
        MATCH (n1:entity_unit)-[*1]-(n2)
        RETURN n1.name AS name, count(n2) AS num
    """

    res = g.run(res)

    return {x["name"]: x["num"] for x in res}


# 查询(公司)第二级的名称
def query_second_rank_company_name(g, name):
    res = "MATCH p=(n3:entity_unit)<-[*0..1]-(n2:entity_unit)<-[*1]-(n1:entity_unit)"
    res += " WHERE n3.name = " + "'" + str(name) + "'"
    res += " RETURN n2.name AS name"

    res = g.run(res)

    return [x["name"] for x in res]


def query_second_rank_company_name_cypher_str(name):
    res = "MATCH p=(n3:entity_unit)<-[*0..1]-(n2:entity_unit)<-[*1]-(n1:entity_unit)"
    res += " WHERE n3.name = " + "'" + str(name) + "'"
    res += " RETURN n2.name AS name"

    return res


# 查询所有热词
def query_all_buzzwords(g, label):
    res = "MATCH (n:" + label + ")"
    res += " RETURN n.keywords AS keywords, n.search_number AS search_number"

    res = g.run(res)

    return [(x["keywords"], x["search_number"]) for x in res]


def query_all_buzzwords_cypher_str(label) -> str:
    res = "MATCH (n:" + label + ")"
    res += " RETURN n.keywords AS keywords, n.search_number AS search_number"
    return res


# 查询热词节点
def query_entity_buzzwords(g):
    res = """
        MATCH (n:entity_buzzwords)
        RETURN n
    """

    res = g.run(res)

    return [x["n"] for x in res]


def query_entity_buzzwords_cypher_str():
    res = "MATCH (n:entity_buzzwords) RETURN n"
    return res


# 知识图谱默认搜索
def query_graph_init(g, label, nodes_init_limit):
    res = "MATCH (n:" + label + ")"
    res += " RETURN n, id(n) AS gid LIMIT " + str(nodes_init_limit)

    res = g.run(res)

    return {x["gid"]: x["n"] for x in res}


def query_graph_init_cypher_str(label, nodes_init_limit):
    res = "MATCH (n:" + label + ")"
    res += " RETURN n, id(n) AS gid LIMIT " + str(nodes_init_limit)
    return res


# 知识图谱搜索二级以上
def following_query_graph_search(g, gid):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(gid)
    res += " RETURN n, id(n) AS gid"

    res = g.run(res)

    return {x["gid"]: x["n"] for x in res}


def following_query_graph_search_cypher_str(gid):
    res = "MATCH (n)"
    res += " WHERE id(n) = " + str(gid)
    res += " RETURN n, id(n) AS gid"

    return res


# <知识图谱>: 搜索范围[0:1], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string)
def query_graph_filtered_search_first(g, label, property, text):
    res = "MATCH (n:" + label + ")"
    res += " WHERE n." + property + " CONTAINS " + "'" + str(text) + "'"
    res += " RETURN n, id(n) AS gid"

    res = g.run(res)

    return {x["gid"]: x["n"] for x in res}


def query_graph_filtered_search_first_cypher_str(g, label, property, text):
    res = "MATCH (n:" + label + ")"
    res += " WHERE n." + property + " CONTAINS " + "'" + str(text) + "'"
    res += " RETURN n, id(n) AS gid"

    return res


# <知识图谱>: 搜索范围[0:1], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string)
def query_graph_filtered_search_second_nodes(g, gid):
    res = "MATCH (n1)"
    res += " WHERE id(n1) = " + str(gid)
    res += " MATCH (n2)-[*1]-(n1)"
    res += " RETURN n2, id(n2) AS gid"

    res = g.run(res)

    return {x["gid"]: x["n2"] for x in res}


def query_graph_filtered_search_second_nodes_cypher_str(gid):
    res = "MATCH (n1)"
    res += " WHERE id(n1) = " + str(gid)
    res += " MATCH (n2)-[*1]-(n1)"
    res += " RETURN n2, id(n2) AS gid"

    return res


# <知识图谱>: 搜索范围[0:1], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string)
def query_graph_filtered_search_second_relations(g, gid):
    res = "MATCH (n1)"
    res += " WHERE id(n1) = " + str(gid)
    res += " MATCH (n2)-[r*1]-(n1)"
    res += " RETURN id(n1) AS start, id(n2) AS end, type(r[0]) AS type"

    res = g.run(res)

    return [(x["start"], x["end"], x["type"]) for x in res]


def query_graph_filtered_search_second_relations_cypher_str(gid):
    res = "MATCH (n1)"
    res += " WHERE id(n1) = " + str(gid)
    res += " MATCH (n2)-[r*1]-(n1)"
    res += " RETURN DISTINCT id(n1) AS start, id(n2) AS end, type(r[0]) AS type"

    return res


# <搜索引擎>: 搜索范围[0:0], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string), 限制条件: ({condition})
def query_tradition_filtered_search(g,
                                    text,
                                    times,
                                    types,
                                    themes,
                                    companies,
                                    times_properties,
                                    types_map,
                                    themes_properties,
                                    companies_properties,
                                    experts_properties,
                                    ):
    # 初始化查询语句
    res = ""
    # 第一个MATCH不需要UNION
    first_union_mark = 0

    # 循环遍历所有类型
    for k, v in types_map.items():
        # 如果有对应的类型
        if k in types:
            # 循环遍历对应类型中的每个子类型
            for x in v:
                # 重置子查询语句
                sub_res = ""
                # 是否有WHERE的筛选条件
                is_valid_x = 0
                # 第一个条件不需要and
                first_and_mark = 0

                # 判断是否需要插入UNION查询关键词
                if first_union_mark == 0:
                    first_union_mark = 1
                else:
                    sub_res += " UNION "
                # 初始化查询语句
                sub_res += "MATCH (n:" + x + ")"
                sub_res += " WHERE"

                # 如果times有值
                if times:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in times_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1
                        for i, time in enumerate(times):
                            if "其他" in time:
                                time = "20"

                                if i == 0:
                                    sub_res += " ((n." + times_properties[x] + " CONTAINS " + "'" + time + "')" + \
                                               " and " + " (NOT n." + times_properties[x] + " CONTAINS " + "'" + "2023" \
                                               + "')" + " and " + " (NOT n." + times_properties[x] + " CONTAINS " + "'" \
                                               + "2022" + "')" + " and " + " (NOT n." + times_properties[x] + \
                                               " CONTAINS " + "'" + "2021" + "')"
                                else:

                                    sub_res += " or (n." + times_properties[x] + " CONTAINS " + "'" + time + "')" + \
                                               " and " + " (NOT n." + times_properties[x] + " CONTAINS " + "'" + "2023" \
                                               + "')" + " and " + " (NOT n." + times_properties[x] + " CONTAINS " + "'" \
                                               + "2022" + "')" + " and " + " (NOT n." + times_properties[x] + \
                                               " CONTAINS " + "'" + "2021" + "')"
                            else:
                                time = time[:4]

                                if i == 0:
                                    sub_res += " (n." + times_properties[x] + " CONTAINS " + "'" + time + "'"
                                else:
                                    sub_res += " or n." + times_properties[x] + " CONTAINS " + "'" + time + "'"
                        sub_res += ")"

                # 如果themes有值
                if themes:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in themes_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1

                        i = 0

                        for theme in themes:
                            if i == 0:
                                sub_res += " (" + "'" + theme + "'" + " IN n.keywords"
                                i = 1
                            else:
                                sub_res += " or" + "'" + theme + "'" + " IN n.keywords"
                        sub_res += ")"

                # 如果companies有值
                if companies:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in companies_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1

                        for i, company in enumerate(companies):
                            if i == 0:
                                sub_res += " (n." + companies_properties[x] + " CONTAINS " + "'" + company + "'"
                            else:
                                sub_res += " or n." + companies_properties[x] + " CONTAINS " + "'" + company + "'"
                        sub_res += ")"

                # 如果text有值
                if text:
                    # 同选项行并集，不同选项行交集
                    if first_and_mark == 0:
                        first_and_mark = 1
                    else:
                        sub_res += " and"

                    is_valid_x = 1

                    for i, y in enumerate(themes_properties[x]):
                        if i == 0:
                            sub_res += " (n." + y + " CONTAINS " + "'" + text + "'"
                        else:
                            sub_res += " or n." + y + " CONTAINS " + "'" + text + "'"
                    sub_res += ")"

                # 如果没有WHERE的筛选条件
                if is_valid_x == 0:
                    # 去除字符串"WHERE"
                    sub_res = sub_res[:-6]

                # 定义返回数据的格式
                sub_res += " RETURN"
                # 定义节点图id
                sub_res += " id(n) AS gid"
                # 定义节点类型
                sub_res += ", " + "'" + str(k) + "'" + " AS type"
                # 定义节点名称
                if x in themes_properties.keys():
                    sub_res += ", n." + themes_properties[x][0] + " AS name"
                else:
                    sub_res += ", " + "'" + "'" + " AS name"
                # 定义节点专家
                if x in experts_properties.keys():
                    sub_res += ", n." + experts_properties[x] + " AS expert"
                else:
                    sub_res += ", " + "'" + "'" + " AS expert"
                # 定义节点公司
                if x in companies_properties.keys():
                    sub_res += ", n." + companies_properties[x] + " AS company"
                else:
                    sub_res += ", " + "'" + "'" + " AS company"
                # 定义节点时间
                if x in times_properties.keys():
                    sub_res += ", n." + times_properties[x] + " AS time"
                else:
                    sub_res += ", " + "'" + "'" + " AS time"
                # 定义节点简介
                if x in themes_properties.keys() and len(themes_properties[x]) == 2:
                    sub_res += ", n." + themes_properties[x][1] + " AS summary"
                else:
                    sub_res += ", " + "'" + "'" + " AS summary"
                # 定义节点主题
                if x in themes_properties.keys():
                    sub_res += ", n." + "keywords" + " AS theme"
                else:
                    sub_res += ", " + "'" + "'" + " AS theme"

                # 将子查询语句拼接到查询语句
                res += sub_res

    # 运行查询语句
    res = g.run(res)

    # 输出查询结果
    return [x for x in res]


def query_tradition_filtered_search_cypher_str(
        text,
        times,
        types,
        themes,
        companies,
        times_properties,
        types_map,
        themes_properties,
        companies_properties,
        experts_properties,
):
    # 初始化查询语句
    res = ""
    # 第一个MATCH不需要UNION
    first_union_mark = 0

    # 循环遍历所有类型
    for k, v in types_map.items():
        # 如果有对应的类型
        if k in types:
            # 循环遍历对应类型中的每个子类型
            for x in v:
                # 重置子查询语句
                sub_res = ""
                # 是否有WHERE的筛选条件
                is_valid_x = 0
                # 第一个条件不需要and
                first_and_mark = 0

                # 判断是否需要插入UNION查询关键词
                if first_union_mark == 0:
                    first_union_mark = 1
                else:
                    sub_res += " UNION "
                # 初始化查询语句
                sub_res += "MATCH (n:" + x + ")-[]-(m)"
                sub_res += " WHERE"

                # 如果times有值
                if times:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in times_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1
                        for i, i_time in enumerate(times):
                            if "其他" in i_time:

                                if i == 0:
                                    sub_res += " (n." + times_properties[x] + " STARTS WITH " + "'" + "" + "'"
                                else:
                                    sub_res += " or n." + times_properties[x] + " STARTS WITH " + "'" + "" + "'"

                                # tar_time = int(time.localtime().tm_year)

                                # if i == 0:
                                #     sub_res += " ((NOT n." + times_properties[x] + " STARTS WITH " + "'" + str(tar_time) \
                                #                + "')" + " and " + " (NOT n." + times_properties[x] + " STARTS WITH " + "'" \
                                #                + str(tar_time - 1) + "')" + " and " + " (NOT n." + times_properties[x] + \
                                #                " STARTS WITH " + "'" + str(tar_time - 2) + "')"
                                #
                                # else:
                                #
                                #     sub_res += " or (NOT n." + times_properties[x] + " STARTS WITH " + "'" + str(tar_time) \
                                #                + "')" + " and " + " (NOT n." + times_properties[x] + " STARTS WITH " + "'" \
                                #                + str(tar_time - 1) + "')" + " and " + " (NOT n." + times_properties[x] + \
                                #                " STARTS WITH " + "'" + str(tar_time - 2) + "')"
                            else:
                                i_time = i_time[:4]

                                if i == 0:
                                    sub_res += " (n." + times_properties[x] + " STARTS WITH " + "'" + i_time + "'"
                                else:
                                    sub_res += " or n." + times_properties[x] + " STARTS WITH " + "'" + i_time + "'"
                        sub_res += ")"
                else:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in times_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1
                        i = 0
                        if i == 0:
                            sub_res += " (n." + times_properties[x] + " STARTS WITH " + "'" + "" + "'"
                        else:
                            sub_res += " or n." + times_properties[x] + " STARTS WITH " + "'" + "" + "'"
                        sub_res += ")"

                # 如果themes有值
                if themes:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in themes_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1

                        i = 0

                        for theme in themes:
                            if i == 0:
                                sub_res += " (" + "'" + theme + "'" + " IN n.keywords"
                                i = 1
                            else:
                                sub_res += " or" + "'" + theme + "'" + " IN n.keywords"
                        sub_res += ")"

                # 如果companies有值
                if companies:
                    # 如果有值并且有对应的属性  TIP:如果有值但是没有对应的属性则当做没有筛选条件
                    if x in companies_properties.keys():
                        # 同选项行并集，不同选项行交集
                        if first_and_mark == 0:
                            first_and_mark = 1
                        else:
                            sub_res += " and"

                        is_valid_x = 1

                        for i, company in enumerate(companies):
                            if i == 0:
                                sub_res += " (n." + companies_properties[x] + " CONTAINS " + "'" + company + "'"
                            else:
                                sub_res += " or n." + companies_properties[x] + " CONTAINS " + "'" + company + "'"
                        sub_res += ")"

                # 如果text有值
                if text:
                    # 同选项行并集，不同选项行交集
                    if first_and_mark == 0:
                        first_and_mark = 1
                    else:
                        sub_res += " and"

                    is_valid_x = 1

                    for i, y in enumerate(themes_properties[x]):

                        if i == 0:
                            sub_res += " (n." + y + " CONTAINS " + "'" + text + "' or " + "'" + text + "' in n.keywords"
                        else:
                            sub_res += " or n." + y + " CONTAINS " + "'" + text + "' or " + "'" + text + "' in n.keywords"

                    # 0125: 新增专家名字检索->属性
                    if x in experts_properties.keys():
                        sub_res += " or n." + experts_properties[x] + " CONTAINS " + "'" + text + "'"
                    # 0125: 新增单位名字检索->属性
                    if x in companies_properties.keys():
                        sub_res += " or n." + companies_properties[x] + " CONTAINS " + "'" + text + "'"

                    # 0125: 新增团队名字检索->关联关系
                    sub_res += " or (m.name CONTAINS " + "'" + text + "' and m: entity_team)"
                    # 0125: 新增实验室名字检索->关联关系
                    sub_res += " or (m.name CONTAINS " + "'" + text + "' and m: entity_laboratory)"

                    sub_res += ")"

                # 如果没有WHERE的筛选条件
                if is_valid_x == 0:
                    # 去除字符串"WHERE"
                    sub_res = sub_res[:-6]

                # 定义返回数据的格式
                sub_res += " RETURN"
                # 定义节点图id
                sub_res += " id(n) AS gid"

                # 添加domain
                sub_res += ", n.domain as domain "
                # 定义节点类型
                sub_res += ", " + "'" + str(k) + "'" + " AS type"
                # 定义节点名称
                if x in themes_properties.keys():
                    sub_res += ", n." + themes_properties[x][0] + " AS name"
                else:
                    sub_res += ", " + "'" + "'" + " AS name"
                # 定义节点专家
                if x in experts_properties.keys():
                    sub_res += ", n." + experts_properties[x] + " AS expert"
                else:
                    sub_res += ", " + "'" + "'" + " AS expert"
                # 定义节点公司
                if x in companies_properties.keys():
                    sub_res += ", n." + companies_properties[x] + " AS company"
                else:
                    sub_res += ", " + "'" + "'" + " AS company"
                # 定义节点时间
                if x in times_properties.keys():
                    sub_res += ", n." + times_properties[x] + " AS time"
                else:
                    sub_res += ", " + "'" + "'" + " AS time"
                # 定义节点简介
                if x in themes_properties.keys() and len(themes_properties[x]) == 2:
                    sub_res += ", n." + themes_properties[x][1] + " AS summary"
                else:
                    sub_res += ", " + "'" + "'" + " AS summary"
                # 定义节点主题
                if x in themes_properties.keys():
                    sub_res += ", n." + "keywords" + " AS theme"
                else:
                    sub_res += ", " + "'" + "'" + " AS theme"

                # 将子查询语句拼接到查询语句
                res += sub_res

    # 输出查询结果
    return res


# LLH: 新增常量字段名查询方法
def check_key(g, label, property):
    res = "MATCH (n:" + label + ")"
    res += " RETURN n." + property

    res = g.run(res)

    return [x for x in res]


def check_key_cypher_str(label, property):
    res = "MATCH (n:" + label + ")"
    res += " RETURN n." + property
    return res


def get_main_page_node(g):
    res = "MATCH (n:main_page)"
    res += " RETURN n"

    res = g.run(res)

    return [x["n"] for x in res]


def get_main_page_node_cypher_str():
    res = "MATCH (n:main_page)"
    res += " RETURN n"

    return res
