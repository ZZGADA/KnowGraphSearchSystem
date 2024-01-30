"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 图数据库所有的添加函数

"""

"""添加结点函数"""


# 添加(团队)结点
def create_entity_team(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:EntityTeam {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(实验室)结点
def create_entity_laboratory(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:EntityLaboratory {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(专家)结点
def create_entity_expert(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:EntityExpert {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(技术标准)结点
def create_entity_technical_standard(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_technical_standard {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(科技项目-省公司项目)结点
def create_entity_project_kjsgs(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_project_kj {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(单位)结点
def create_entity_unit(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:EntityUnit {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-省部级及以上成果)结点
def create_entity_achievement_sbj(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_sbj {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-其他成果)结点
def create_entity_achievement_qt(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_qt {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-省公司成果-标准类)结点
def create_entity_achievement_sgs_bz(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_sgs_bz {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-省公司成果-科学科技进步类)结点
def create_entity_achievement_sgs_kxkj(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_sgs_kxkj {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-省公司成果-技术发明类)结点
def create_entity_achievement_sgs_jsfm(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_sgs_jsfm {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(成果库-省公司成果-专利类)结点
def create_entity_achievement_sgs_zl(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_achievement_sgs_zl {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(知识产权-论文)结点
def create_entity_intellectual_property_paper(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_intellectual_property_paper {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(知识产权-软件著作)结点
def create_entity_intellectual_property_software_works(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_intellectual_property_software_works {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(知识产权-专利)结点
def create_entity_intellectual_property_patent(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_intellectual_property_patent {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(知识产权-专著)结点
def create_entity_intellectual_property_monograph(g, dict):
    res = ""

    for i, k in enumerate(dict.keys()):
        v = dict[k]
        if i == 0:
            res += "MERGE (e:entity_intellectual_property_monograph {" + k + ": " + "'" + v + "'" + "})"
        else:
            res += " SET e." + k + "= " + "'" + v + "'"

    return g.run(res)


# 添加(热词)节点
def create_entity_buzzwords(g):
    res = """
        MERGE (n:entity_buzzwords)
    """

    return g.run(res)
def create_entity_buzzwords_cypher_str():
    res = """
        MERGE (n:entity_buzzwords)
    """
    return res


"""添加边函数"""


# 添加()-[]-()边
def create_relationship(g, s, sp, t, tp):
    res = ""

    res += "MATCH (s:" + s + ")"
    res += " UNWIND s." + sp + " AS sp"
    res += " MATCH (t:" + t + ")"
    res += " WHERE sp =" + " t." + tp
    res += " MERGE (s)-[:R]-(t)"

    return g.run(res)
def init_create_node_cypher_str(label):
    res = "MERGE (n:" + label + ")"
    res += " SET n.name='默认'"
    return res

