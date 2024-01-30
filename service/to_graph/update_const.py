from service.to_graph import graph_init
from static.graph_const import GraphConst
from cypher_util.query_data_util import *
from service.connector import back_end_connector as bnc
from config import  process_errors as pe
from config import logging_config
logger = logging_config.logging_self_define().log(level='INFO',name="update_const.py")


# LLH: 新增常量更新类
class UpdateConst:
    # 图数据库初始化
    

    def __init__(self):
        
        self.graph_const = GraphConst()

    def update(self):
        # 获取需要检查的字典
        times_properties = self.graph_const.get_times_properties()
        themes_properties = self.graph_const.get_themes_properties()
        companies_properties = self.graph_const.get_companies_properties()
        experts_properties = self.graph_const.get_experts_properties()

        check_list = [
            times_properties,
            themes_properties,
            companies_properties,
            experts_properties
        ]

        new_list = []
    
        # 检查各个字段名是否存在于数据库中
        for check in check_list:
            cur_dict = {}
            for k, v in check.items():
                if isinstance(v, list):
                    cur_list = []
                    flag = False
                    for x in v:
                        
                        # res = session.execute_read(check_key, k, x)
                        check_key_str=check_key_cypher_str(k,x)
                        
                        res_dict=bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                            code=pe.Status_codes.cypher_query,
                            cypher_str=check_key_str
                        )
                        if res_dict["code"]!=pe.Status_codes.GET_OK:
                            logger.error("执行check_key1时出现问题 cypher_str1{}".format(check_key_str))
                            return
                        logger.info("check_key1语句执行成功 k:{} x:{} ".format(k,x))
                        res_data1=res_dict["data"]
                        try:
                            res = [x for x in res_data1]
                        except Exception as e:
                            logger.error("报错信息如下  --error{]".format(str(e)))

                        if res:
                            flag = True
                            cur_list.append(x)
                    if flag:
                        cur_dict[k] = cur_list
                else:
                    check_key_str2 = check_key_cypher_str(k, v)
                    # res = session2.execute_read(check_key, k, v)\
                    res_dict2 = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                        code=pe.Status_codes.cypher_query,
                        cypher_str=check_key_str2
                    )
                    if res_dict2["code"] != pe.Status_codes.GET_OK:
                        logger.error("执行check_key2时出现问题 cypher_str2{}".format(check_key_str2))
                        return
                    logger.info("check_key2语句执行成功 k:{} v:{} ".format(k,v))
                    res_data2 = res_dict2["data"]
                    try:
                        res2 = [x for x in res_data2]
                    except Exception as e:
                        logger.error("报错信息如下  --error{]".format(str(e)))

                    if res2:
                        cur_dict[k] = v
            new_list.append(cur_dict)

        # 更新常量类字典
        self.graph_const["times_properties"] = new_list[0]
        self.graph_const["themes_properties"] = new_list[1]
        self.graph_const["companies_properties"] = new_list[2]
        self.graph_const["experts_properties"] = new_list[3]

