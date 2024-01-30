from service.to_graph.select_graph import KGraph
from config import logging_config
logger = logging_config.logging_self_define().log(level='INFO',name="k_default.py")
from service.connector import back_end_connector as bnc
from config import process_errors as pe


# LLH: 新增的类
# 知识图谱默认显示的类
class KDefault:
    url="http://172.30.86.10:11623/kjxmprocess/kexportknowledgemapping/getAllRelationValue"
    def __init__(self ):
        self.input = ""
    
    def get_input(self, input):
        self.input = input
    
    def process(self):
        try:
            cur_list = []
            for x in self.input["data"]:
                cur_dict = {
                    "id": "",
                    "gid": "",
                    "label": x["fromEntityCode"],
                    "property": "name",
                    "text": x["fromEntityName"],
                    "first_res": "",
                    "second_res": ""
                }
                cur_list.append(cur_dict)
    
            graph = KGraph()
    
            node_list = []
            relationship_list = []
    
            for x in cur_list:
                graph.input(x)
    
                data, ifSuccess = graph.expand_query_graph_filtered_search()
                
                if not ifSuccess:
                    logger.error("kquery数据查询失败 kDefault数据接口 传入数据可能有误")
                    logger.error("查看数据  --data:{}".format(self.input["data"]))
                    return [],False
                
                for y in self.input["data"]:
                    target_label = y["toEntityCode"]
                    target_text = y["toEntityName"]
    
                    t_gid = ""
                    children = ""
                    for n_second in data["second_res"][0]["nodes"]:
                        if n_second["domain"] == target_label and n_second["name"] == target_text:
                            children = n_second
                            t_gid = n_second["gid"]
                            break
    
                    cur_node = data["first_res"][0]
                    cur_node["children"] = children
    
                    node_list.append(cur_node)
    
                    s_gid = data["first_res"][0]["gid"]
    
                    for r_second in data["second_res"][0]["relations"]:
                        if s_gid == r_second["start"] and t_gid == r_second["end"]:
                            relationship_list.append(r_second)
                            break
    
            res = {"node": node_list, "relationship": relationship_list}
            return res, True
        except Exception as e:
            logger.error("keDefault 执行过程报错  --报错信息{}".format(str(e)))
            return [],False
    
    def query(self):
        output = {}
        output_list = []
        
        # res = self.session.execute_read(get_main_page_node)
        cypher_str="MATCH (n:main_page) RETURN n"
        res=bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
            cypher_str=cypher_str,code=pe.Status_codes.cypher_query
        )
        if res["code"]!=200  :
            return False,[]
        
        res_data=res["data"]
        try:
            data=[x["n"] for x in res_data]
        except Exception as e:
            logger.error("获取数据报错 error:{}".format(e))
            return False,[]
        
        for x in data:
            cur_dict = {}
            for k, v in x.items():
                cur_dict[k] = v
            output_list.append(cur_dict)
        output["data"] = output_list
        
        return True ,output