from flask import request
from flask import jsonify
from flask import Request
from config import flask_config
from service.to_graph import graph_init
from config import  process_errors as pe
import requests
import json
from flask import current_app
from config import logging_config
from service.connector import back_end_connector as bnc


logger = logging_config.logging_self_define().log(level='INFO',name="back_end_connector")


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, np.ndarray):
        #     return obj.tolist()
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class back_end_cypher_search_and_theme_return:
    '''
    像后端传入cypher语句 获得结果
    结果有3种情况
    均为列表包裹 但是
        1.列表中只有一个查询结果 --->知识图谱功能侧边栏查询
        2.列表中有多个结果  ---> 智能检索显示项目简介
        3.列表中没有查询结果返回为空 --> 知识图谱功能中 专家不存在
    向后端传输的格式有
    {
        "cypher_str":'',
        "data":{
            '':{},
            '':{}
        }
    }
    '''
    @classmethod
    def cypher_search_Project_Description(cls,cypher_str,code):
        backend_ip = flask_config.Config.BACK_END_URL
        backend_port=flask_config.Config.BACK_END_PORT

        # print('查询项目简介')
        temp_dict={"code":code,"cypher_str":cypher_str}
        # json_temp=jsonify(data=temp_dict)
        '''
        传给后端的数据有:
        {
            "code":200/201/100,  #200表示execute_read 查询数据 execute_write表示更新数据
            "cypher_str":"",
            # "children":[(),(),()]
        }
        
        后端的返回结果包括：
        {
            "code":200,
            "data":[{},{},{}]
            "mag":""
        }
        data中一个列表里面嵌套字典 一个字典就是一个查询结果
        200表示没有给后端的数据
        201表示有给后端的数据
        '''

        #已将转发修改成动态的了
        # url="http://%s:%d/kjxmzstp/graphDatabaseNeo4j/cypher_back_end"%(backend_ip,backend_port)
        try:
            back_end_processing = bnc.back_end_get_data_from_end_end(**temp_dict)  # 字典解包
            json_dict = back_end_processing.back_end_data_return()
            # print(json_dict)
            # res=requests.post(url, json=temp_dict)
            del back_end_processing
        except Exception as e :
            logger.error("自定义模拟后端接口返回错误 --error:{}".format(str(e)))
            return {
                "code":100,
                "data":[],
                "msg":"failed"
            }
        # json_data=res.json()
        # json_dict=json.loads(json_data) #将json 转换成字典 解码

        if json_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
            # 如果查询失败直接返回原前端值
            logger.error("图数据库查询失败,cypher语句可能存在问题  {0} --msg:{1}  --cypher: {2}".format(json_dict["code"], json_dict["msg"],cypher_str))
            # return self.original_front_end_data(), False
        # res = json_dict["data"]
        # if len(res) == 0 and code==pe.Status_codes.cypher_query:  # 查询结果为空直接返回
        #     logger.warning(
        #         "图数据库返回结果为空,cypher语句可能错误  {0} --msg:{1} --cypher:{2}".format(json_dict["code"],
        #                                                                                  json_dict["msg"],
        #                                                                                  cypher_str))
            # return self.original_front_end_data(), False
        # logger.info("图数据库查询成功  {0} --msg:{1}".format(json_dict["code"], json_dict["msg"]))
        return json_dict

#cypher 查询
def cypher_execute_query(g,cypher_str):
    res=g.run(cypher_str).data()  #将neo4j返回的数据类型转换成为可迭代对象 但是内含byte对象
    # res_list=[]
    # for i in res:
    #     for k,v in i:
    #         v=tuple(v)
    #         temp={k:v}
    #         res_list.append(temp)

    # res= [dict(i) for i in res]
    return res
#cypher 更新
def cypher_execute_update(g,cypher_str):
    res=g.run(cypher_str)

    return res


def cypher_execute_add(g, cypher_str):
    res = g.run(cypher_str)

    return res
def cypher_execute_delete(g, cypher_str):
    res = g.run(cypher_str)

    return res
class back_end_get_data_from_end_end:
    
    
    driver = graph_init.ConnectToDatabase.init()
    

    def  __init__(self,code,cypher_str):
        self.code=code
        self.cypher_str=cypher_str
        self.session = self.driver.session()
    

    def back_end_data_return(self) :
        
        

        '''
        后端的返回结果包括：
        {
            "code":200,100  200表示成功 100 表示失败 (没有查询结果不代表查询失败)
            "data":[{},{},{}]
            "msg":""
        }
        data中一个列表里面嵌套字典 一个字典就是一个查询结果
        200表示查询
        201表示更新操作
        :return: dict
        '''
        read_data:None
        write_data=[]
        res=dict()
        # print(self.code)
        # print(self.cypher_str)
        if self.code==200: #表示执行execute_read  查询语句
            if self.cypher_str!="":  #cypher语句不为空
                try:
                    
                    read_data = self.session.read_transaction(cypher_execute_query,self.cypher_str)
                    # print(read_data)
                    res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
                    res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
                except:
                    read_data=[]
                    res["code"] = pe.ProcessInfos.GET_FAILED.status_code
                    res["msg"] = pe.ProcessInfos.GET_FAILED.message
            else:
                # "传输错误 没有cypher语句"
                res["code"]=pe.ProcessInfos.GET_FAILED.status_code
                res["msg"]=pe.ProcessInfos.GET_FAILED.message
                read_data=[]
            res["data"]=read_data
        elif self.code==201: #表示执行execute_write  更新语句
            if self.cypher_str != "":  # cypher语句不为空
                try:
                    self.session.write_transaction(cypher_execute_update,self.cypher_str)
                    res["code"] = pe.ProcessInfos.UPDATE_SUCCEED.status_code
                    res["msg"] = pe.ProcessInfos.UPDATE_SUCCEED.message
                except:
                    res["code"] = pe.ProcessInfos.UPDATE_FAILED.status_code
                    res["msg"] = pe.ProcessInfos.UPDATE_FAILED.message
            else:
                # "传输错误 没有cypher语句"
                res["code"] = pe.ProcessInfos.UPDATE_FAILED.status_code
                res["msg"] = pe.ProcessInfos.UPDATE_FAILED.message
            res["data"]=write_data

        elif self.code==202: #execute_write 添加语句
            if self.cypher_str != "":  # cypher语句不为空
                try:
                    self.session.write_transaction(cypher_execute_add, self.cypher_str)
                    res["code"] = pe.ProcessInfos.ADD_SUCCEED.status_code
                    res["msg"] = pe.ProcessInfos.ADD_SUCCEED.message
                except:
                    res["code"] = pe.ProcessInfos.ADD_FAILED.status_code
                    res["msg"] = pe.ProcessInfos.ADD_FAILED.message
            else:
                # "传输错误 没有cypher语句"
                res["code"] = pe.ProcessInfos.ADD_FAILED.status_code
                res["msg"] = pe.ProcessInfos.ADD_FAILED.message
            res["data"] = write_data

        elif self.code == 203:  # execute_write 删除语句
            if self.cypher_str != "":  # cypher语句不为空
                try:
                    self.session.write_transaction(cypher_execute_delete, self.cypher_str)
                    res["code"] = pe.ProcessInfos.ADD_SUCCEED.status_code
                    res["msg"] = pe.ProcessInfos.ADD_SUCCEED.message
                except:
                    res["code"] = pe.ProcessInfos.ADD_FAILED.status_code
                    res["msg"] = pe.ProcessInfos.ADD_FAILED.message
            else:
                # "传输错误 没有cypher语句"
                res["code"] = pe.ProcessInfos.ADD_FAILED.status_code
                res["msg"] = pe.ProcessInfos.ADD_FAILED.message
            res["data"] = write_data
        else:
            res["code"] = pe.ProcessInfos.GET_FAILED.status_code
            res["msg"] = pe.ProcessInfos.GET_FAILED.message
            res["data"]=[]
        # print(res)
        # print(res["data"])
        # res_json=json.dumps(res,cls=MyEncoder, ensure_ascii=False, indent=4) #将byte对象转换为str 通过自定义类的转换
        #实现对字典数据的成功编码 然后返回
        return res







