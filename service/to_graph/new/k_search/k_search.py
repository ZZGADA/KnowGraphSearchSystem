import copy

import flask

from config import flask_config
from flask import request
import requests
from collections import Counter
from service.connector import back_end_connector as bnc
from config import process_errors as pe
from flask import current_app
import neo4j._sync.work.result
from service.to_graph import graph_init
from cypher_util.query_data_util import *
from cypher_util.update_data_util import *
from cypher_util.add_data_util import *
from static.graph_const import *
from model.KeyBERT import KeyBERTModel
from static.common_func import *
import threading
from multiprocessing import Process
from config import process_errors as pe
import json

from config import logging_config

logger = logging_config.logging_self_define().log(level='INFO',name="k_search.py")


# LLH: 新增类
# 知识图谱图的默认类
class KSearch:
    # 图数据库初始化
    # driver = graph_init.ConnectToDatabase.driver()

    def __init__(self):
        # 创建连接
        # self.sesssion = self.driver.session()
        # 实例化图的常量类
        self.graph_const = GraphConst()
        # 定义查询id
        self.id = ""
        # 定义节点gid
        self.gid = ""
        # 定义初始查询的节点标签
        self.label = ""
        # 定义初始查询的节点的对应属性
        self.property = ""
        # 定义初始查询的关键词
        self.text = ""
        # 定义第一级节点搜索结果
        self.first_res = []
        # 定义第二级节点搜索结果
        self.second_res = []

    def __del__(self):
        logger.info("kGraph缓存清理")

    # 输入查询数据
    def input(self, dict):
        # 传入输入的值
        # 循环遍历字典
        for k, v in dict.items():
            # 存储数据
            if k == "label":
                self.label = v
            elif k == "property":
                self.property = v
            elif k == "text":
                self.text = v
            elif k == "gid":
                self.gid = v

    # 判断是否为默认值(空值)
    def is_default(self):
        if (not self.text) and self.gid=="":
            return True
        else:
            return False

    # 知识图谱默认搜索
    def query_graph_init(self)->(dict,bool):

        final_res_dict=None
        # 定义范围1内的结果
        first_res = []

        # 获取知识图谱的type中文名和对应节点名的映射关系
        labels = self.graph_const.get_graph_types_map()[self.label]
        # 获取知识图谱搜索初始显示个数
        nodes_init_limit = self.graph_const.get_nodes_init_limit()

        # 循环遍历所有节点类别
        for label in labels:
            logger.info("知识图谱默认搜索 --label:{}".format(label))
            # 获取范围1内的原生结果
            # raw_res_1 = self.session.execute_read(query_graph_init, label, nodes_init_limit)
            cypher_str1=query_graph_init_cypher_str(label, nodes_init_limit)
            res_dict=bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str1,code=pe.Status_codes.cypher_query
            )
            if res_dict["code"]!=pe.ProcessInfos.GET_SUCCEED.status_code:
                logger.error(
                    "图数据库查询失败,cypher语句可能错误  --cypher:{0} ".format(cypher_str1))
                final_res_dict=self.output()
                return final_res_dict,False

            res_data=res_dict["data"]
            try:
                raw_res_1={x["gid"]: x["n"] for x in res_data}
            #     知识图谱默认搜索不会发生异常  因为text为空
            except:
                logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str1,res_data))
                final_res_dict = self.output()
                return final_res_dict, False


            # 范围1内结果的后处理
            for k, v in raw_res_1.items():
                cur_dict = dict(v.items())
                cur_dict["gid"] = k
                first_res.append(cur_dict)

        self.first_res = first_res
        final_res_dict=self.output()

        return final_res_dict,True

    # [含处理]<知识图谱>: 搜索范围[0:1], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string)
    def expand_query_graph_filtered_search(self):
        # 定义范围1内的结果
        first_res = []
        # 定义范围2内的结果
        second_res = []

        final_res_dict={}
        
        # 如果没有点击特定节点并获取了对应的gid
        if self.gid=="":
            # 获取知识图谱的type中文名和对应节点名的映射关系
            labels = self.graph_const.get_graph_types_map()[self.label]
            
            for label in labels:
                # 获取范围1内的原生结果
                # res_1 = self.session.execute_read(query_graph_filtered_search_first, label, self.property, self.text)
                logger.info("知识图谱非默认搜索 --label:{}".format(label))
                cypher_str2 = query_graph_filtered_search_first_cypher_str(label, label, self.property, self.text)
                res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                    cypher_str=cypher_str2, code=pe.Status_codes.cypher_query
                )
                if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                    final_res_dict = self.output()
                    return final_res_dict, False

                res_data = res_dict["data"]
                if not res_data:
                    logger.warning("返回结果为空 当前阶段的label不可用 没有遍历到目标label  --label:{}  --text:{}".format(label,self.text))
                    continue
                try:
                    res_1 = {x["gid"]: x["n"] for x in res_data}
                    logger.info("知识图谱非默认搜索 res_1返回正确")
                except:
                    logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str2,
                                                                                                           res_data))
                    final_res_dict = self.output()
                    return final_res_dict, False

                # {x["gid"]: x["n"] for x in res}
                if not res_1:
                    logger.warning("kquery非默认搜索中res_1为空 表示当前label和text是不匹配的 跳过  --label:{}  --text:{}".format(label,self.text))
                #   跳过
                    continue
                # 范围1内结果的后处理
                try:
                    gid_1 = [x for x in res_1.keys()][0]
                except Exception as e:
                    logger.error("获取gid_1的结果为空  -- 报错:{}  --cypher:{}".format(e,cypher_str2))
                    return final_res_dict,False

                single_first_res = dict(res_1[gid_1].items())
                single_first_res["gid"] = gid_1

                # 定义范围2内结果的所有节点列表
                res_2_nodes = []

                # 获取原生的范围2内结果的所有节点列表
                # raw_res_2_nodes = self.session.execute_read(query_graph_filtered_search_second_nodes, gid_1)
                cypher_str3=query_graph_filtered_search_second_nodes_cypher_str(gid_1)
                res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                    cypher_str=cypher_str3, code=pe.Status_codes.cypher_query
                )
                if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                    final_res_dict = self.output()
                    return final_res_dict, False

                res_data = res_dict["data"]
                try:
                    #后处理
                    raw_res_2_nodes = {x["gid"]: x["n2"] for x in res_data}

                except:
                    logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str3,
                                                                                                           res_data))
                    final_res_dict = self.output()
                    return final_res_dict, False


                # {x["gid"]: x["n2"] for x in res}

                # 范围2内结果的后处理
                for k, v in raw_res_2_nodes.items():
                    cur_dict = dict(v.items())
                    cur_dict["gid"] = k
                    res_2_nodes.append(cur_dict)

                # 定义范围2内结果的所有关系列表
                # res_2_relations = self.session.execute_read(query_graph_filtered_search_second_relations, gid_1)
                cypher_str4=query_graph_filtered_search_second_relations_cypher_str(gid_1)
                res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                    cypher_str=cypher_str4, code=pe.Status_codes.cypher_query
                )
                if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                    final_res_dict = self.output()
                    return final_res_dict, False

                res_data = res_dict["data"]

                try:
                    # 后处理
                    res_2_relations = [(x["start"], x["end"], x["type"]) for x in res_data]

                except:
                    logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str4,
                                                                                                           res_data))
                    final_res_dict = self.output()
                    return final_res_dict, False

                new_res_2_relations = []

                # LLH: 下面一段已修改
                # ======================================================================================

                for i in range(len(res_2_relations)):
                    if res_2_relations[i][2] in self.graph_const.get_graph_chinese_types().keys():
                        new_res_2_relations.append({
                            "start": res_2_relations[i][0],
                            "end": res_2_relations[i][1],
                            "name": res_2_relations[i][2],
                            "Chinese": self.graph_const.get_graph_chinese_types()[res_2_relations[i][2]]
                        })
                    else:
                        new_res_2_relations.append({
                            "start": res_2_relations[i][0],
                            "end": res_2_relations[i][1],
                            "name": res_2_relations[i][2],
                            "Chinese": ""
                        })

                # ======================================================================================

                # [(x["start"], x["end"], x["type"]) for x in res]

                # 合并范围2内结果的所有节点和关系列表为一个字典
                single_second_res = {
                    "nodes": res_2_nodes,
                    "relations": new_res_2_relations
                }

                first_res.append(single_first_res)
                second_res.append(single_second_res)

        # 如果有点击特定节点并获取了对应的gid
        else:
            # 获取范围1内的原生结果
            # res_1 = self.session.execute_read(following_query_graph_search, self.gid)
            # print("uuuuuuuuuuuuuuuuu")
            cypher_str5 = following_query_graph_search_cypher_str(self.gid)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str5, code=pe.Status_codes.cypher_query
            )
            if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                final_res_dict = self.output()
                return final_res_dict, False

            res_data = res_dict["data"]
            
            
            
            try:
                # 后处理
                res_1= {x["gid"]: x["n"] for x in res_data}

            except:
                logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str5,
                                                                                                       res_data))
                final_res_dict = self.output()
                return final_res_dict, False

            # {x["gid"]: x["n"] for x in res}
            
            # 范围1内结果的后处理
            try:
                gid_1 = [x for x in res_1.keys()][0]
            except Exception as e:
                logger.error("结果为空  -- {}".format(e))
                return final_res_dict,False


            single_first_res = dict(res_1[gid_1].items())
            single_first_res["gid"] = gid_1

            # 定义范围2内结果的所有节点列表
            res_2_nodes = []

            # 获取原生的范围2内结果的所有节点列表
            # raw_res_2_nodes = self.session.execute_read(query_graph_filtered_search_second_nodes, gid_1)

            cypher_str6=query_graph_filtered_search_second_nodes_cypher_str(gid_1)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str6, code=pe.Status_codes.cypher_query
            )
            if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                final_res_dict = self.output()
                return final_res_dict, False

            res_data = res_dict["data"]
            # print(res_data)
            try:
                # 后处理
                raw_res_2_nodes= {x["gid"]: x["n2"] for x in res_data}

            except:
                logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str6,
                                                                                                       res_data))
                final_res_dict = self.output()
                return final_res_dict, False

            # 范围2内结果的后处理
            for k, v in raw_res_2_nodes.items():
                cur_dict = dict(v.items())
                cur_dict["gid"] = k
                res_2_nodes.append(cur_dict)
            
            # print(res_2_nodes)  #现在为空

            # 定义范围2内结果的所有关系列表
            # res_2_relations = self.session.execute_read(query_graph_filtered_search_second_relations, gid_1)

            cypher_str7 = query_graph_filtered_search_second_relations_cypher_str(gid_1)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str7, code=pe.Status_codes.cypher_query
            )
            if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                final_res_dict = self.output()
                return final_res_dict, False

            res_data = res_dict["data"]
            try:
                # 后处理
                res_2_relations = [(x["start"], x["end"], x["type"]) for x in res_data]

            except:
                logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str7,
                                                                                                       res_data))
                final_res_dict = self.output()
                return final_res_dict, False

            # 范围2内结果的后处理
            new_res_2_relations = []

            # LLH: 下面一段已修改
            # ======================================================================================

            for i in range(len(res_2_relations)):
                if res_2_relations[i][2] in self.graph_const.get_graph_chinese_types().keys():
                    new_res_2_relations.append({
                        "start": res_2_relations[i][0],
                        "end": res_2_relations[i][1],
                        "name": res_2_relations[i][2],
                        "Chinese": self.graph_const.get_graph_chinese_types()[res_2_relations[i][2]]
                    })
                else:
                    new_res_2_relations.append({
                        "start": res_2_relations[i][0],
                        "end": res_2_relations[i][1],
                        "name": res_2_relations[i][2],
                        "Chinese": ""
                    })

            # ======================================================================================

            # 合并范围2内结果的所有节点和关系列表为一个字典
            single_second_res = {
                "nodes": res_2_nodes,
                "relations": new_res_2_relations
            }

            first_res.append(single_first_res)
            second_res.append(single_second_res)

        self.first_res = first_res
        self.second_res = second_res

        final_res_dict=self.output()
        logger.info("查询成果 成功完成")
        return final_res_dict,True

    # 输出查询结果
    def output(self):

        return {
            # 查询id
            "id": self.graph_const.get_updated_id(),
            # 节点gid
            "gid": self.gid,
            # 标签
            "label": self.label,
            # 属性名
            "property": self.property,
            # 关键词
            "text": self.text,
            # 第一级节点
            "first_res": self.first_res,
            # 第二级节点
            "second_res": self.second_res
        }
