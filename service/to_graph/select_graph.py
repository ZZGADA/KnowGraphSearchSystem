"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/8/19
    @Introduction: 图数据库的数据查询

"""
import copy
from flask import jsonify
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
from config import process_errors as pe
import re
import json

from config import logging_config

logger = logging_config.logging_self_define().log(level='INFO', name="select_graph.py")


# 图的基类
class Graph:
    pass


# 搜索引擎图的类
class TGraph:
    # 图数据库初始化
    # driver = graph_init.ConnectToDatabase.init()
    graph_const_example = GraphConst()

    def __init__(self):

        # 实例化图的常量类
        self.graph_const = GraphConst()
        # 获取初始时间选项列表
        self.times = []
        # 获取初始类型选项列表
        self.types = []
        # 定义初始主题选项列表
        self.themes = []
        # 定义初始公司选项列表
        self.companies = []
        # 定义查询id
        self.id = ""
        # 定义初始查询的关键词
        self.text = ""
        # 定义初始所有结果字典列表
        self.res = []
        # 定义初始分页结果字典列表
        self.real_res = []
        # 定义当前页数
        self.page = 0
        # 定义总页数
        self.total_pages = 0
        # 定义每页页数
        self.page_limit = self.graph_const.get_per_page_limit()

        # 设定初始值 如果出问题就返回初始值
        self.original = ''

    def __del__(self):
        logger.info("tGraph缓存清理")

    def init_create_nodes(self):
        for k, v in self.graph_const.get_graph_types_map_reverse().items():
            # self.session.execute_write(init_create_node_cypher_str, k)
            cypher_str_init_create_node = init_create_node_cypher_str(k)
            res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                code=pe.Status_codes.cypher_add, cypher_str=cypher_str_init_create_node)

            if res["code"] != pe.Status_codes.UPDATE_OK:
                logger.error("请注意 init_create_node 没有成功 ")
            else:
                logger.info("init_create_node 成功 k:{} v:{}".format(k, v))

    # LLH NEW:
    # 补全缺失的数据
    def complete(self) -> bool:
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

        for check in check_list:
            for k, v in check.items():
                if isinstance(v, list):
                    for x in v:
                        complete_null_str1 = complete_null_data_cypher_str(k, x)
                        res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                            code=pe.Status_codes.cypher_update,
                            cypher_str=complete_null_str1
                        )
                        if res_dict["code"] != pe.Status_codes.UPDATE_OK:
                            logger.error("complete_null_data_cypher_str1 语句执行错误 --cypher_str:{}".
                                         format(complete_null_str1))
                            return False
                        logger.info("complete_null_data_cypher_str1 语句执行成功  --k:{}  x:{}".
                                    format(k, x))

                else:
                    complete_null_str2 = complete_null_data_cypher_str(k, v)
                    res_dict2 = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                        code=pe.Status_codes.cypher_update,
                        cypher_str=complete_null_str2
                    )
                    # 报错检查
                    if res_dict2["code"] != pe.Status_codes.UPDATE_OK:
                        logger.error("complete_null_data_cypher_str2 语句执行错误 --cypher_str:{}".
                                     format(complete_null_str2))
                        return False
                    logger.info("complete_null_data_cypher_str2 语句执行成功  --k:{}  v:{}".
                                format(k, v))

        return True

    # 输入查询数据
    def input(self, dict):
        # 传入输入的值
        # 循环遍历字典
        dictDeep = copy.deepcopy(dict)
        self.original = self.set_original_front_end_data(dictDeep["text"], dictDeep["times"], dictDeep["types"],
                                                         dictDeep["themes"],
                                                         dictDeep["companies"],
                                                         dictDeep["res"], dictDeep["total_pages"], dictDeep["page"])

        for k, v in dict.items():
            # 如果键值对的值为列表
            if isinstance(v, list) and v != []:
                # 循环遍历列表
                for i, x in enumerate(v):
                    # 正则化匹配"（...）"
                    regularization = re.findall("（\d*）", x)
                    # 去除每个选项字符串的数量
                    v[i] = x.replace("".join(regularization), "")

            # 存储数据
            if k == "times":
                self.times = v
            elif k == "types":
                # 若没有类型限制，则全选类型
                if not v:
                    self.types = self.graph_const.get_types()
                else:
                    self.types = v
            elif k == "themes":
                self.themes = v
            elif k == "companies":
                self.companies = v
            elif k == "text":
                self.text = v
            elif k == "page":
                self.page = v
            elif k == "page_limit":
                self.page_limit = v

        # original_test=copy.deepcopy(dict)

        # self.original_front_end_data_dict={
        #
        # "id": self.graph_const.get_updated_id(),
        # # 关键词
        # "text": self.text,
        # # 时间选项
        # "times": self.times,
        # # 类型选项
        # "types": self.types,
        # # 主题选项
        # "themes": self.themes,
        # # 公司选项
        # "companies": self.companies,
        # # 结果字典列表
        # "res": self.real_res,
        # # 总页数
        # "total_pages": self.total_pages,
        # # 当前页数
        # "page": self.page,
        # "page_limit": self.page_limit
        # }

    # 判断是否为默认值(空值)
    def is_default(self):

        if (self.text == "" and
                self.times == [] and
                self.types == [] and
                self.themes == [] and
                self.companies == []):
            return True
        else:
            return False

    # 更新时间选项各分支个数
    def update_times_num(self) -> bool:
        try:
            # 获取标准时间选项列表
            standard_times = self.graph_const.get_times()
            # 定义计数器列表
            count_list = []

            # 循坏遍历所有时间选项
            for i, time in enumerate(standard_times[:-1]):
                # 重置计数器
                count = 0
                # 循环遍历所有的时间属性
                for x in self.res:
                    # 计数叠加查询的数量结果
                    if str(x["time"]) == time[:4]:
                        count += 1

                # 更新时间选项字符串
                standard_times[i] += "（" + str(count) + "）"
                # 添加当前计数器到计数器列表
                count_list.append(count)

            """其他时间的合并计数"""
            # # 重置计数器
            # count = 0
            # # 循环遍历所有的时间属性
            # for x in self.res:
            #     # 计数叠加查询的数量结果，时间实参为默认值
            #     if "20" in str(x["time"]):
            #         count += 1
            # 更新时间选项字符串
            standard_times[len(standard_times) - 1] += "（" + str(len(self.res) - sum(count_list)) + "）"

            # 更新时间选项列表
            self.times = standard_times
        except Exception as e:
            logger.error("更新tquery_output时间出错: {}".format(str(e)))
            return False

        return True

    # 更新类型选项各分支个数
    def update_types_num(self):
        # 获取标准类型选项列表
        standard_types = self.graph_const.get_types()

        # 循坏遍历所有类型选项
        for i, type in enumerate(standard_types):
            # 重置计数器
            count = 0
            # 循环遍历所有的类型属性
            for x in self.res:
                # 计数叠加查询的数量结果
                if x["type"] == type:
                    count += 1
            # 更新类型选项字符串
            standard_types[i] += "（" + str(count) + "）"

        # 更新类型选项列表
        self.types = standard_types
        # print(self.types)

        # 默认按数量排序
        self.types.sort(key=re_get_num, reverse=True)
        return True

    # 更新主题选项各分支个数
    def update_themes_num(self) -> bool:
        # 获取主题选项的最大数量
        themes_limit = self.graph_const.get_themes_limit()
        # 含冗余的主题列表
        raw_themes_list = []

        if self.themes:

            # 获取查询结果
            # outputs = self.session.execute_read(
            #     query_tradition_filtered_search,
            #     self.text,
            #     [],
            #     self.types,
            #     [],
            #     [],
            #     self.graph_const.get_times_properties(),
            #     self.graph_const.get_types_map(),
            #     self.graph_const.get_themes_properties(),
            #     self.graph_const.get_companies_properties(),
            #     self.graph_const.get_experts_properties(),
            # )
            #
            # # 初始化输出结果
            # cur_res = []
            #
            # # 更改输出的格式为内嵌字典的列表
            # for x in outputs:
            #     cur_res.append(dict(x.items()))
            cypher_str1 = query_tradition_filtered_search_cypher_str(
                self.text,
                [],
                self.types,
                [],
                [],
                self.graph_const.get_times_properties(),
                self.graph_const.get_types_map(),
                self.graph_const.get_themes_properties(),
                self.graph_const.get_companies_properties(),
                self.graph_const.get_experts_properties())
            query_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str1,
                pe.Status_codes.cypher_query
            )

            if query_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                # 如果查询失败直接返回原前端值
                logger.error(
                    "更新主题选项各分支个数 --图数据库查询失败,cypher语句可能存在问题  {0} --msg:{1}  --cypher: {2}".format(
                        query_res["code"], query_res["msg"], cypher_str1))
                return False
            cur_res = query_res["data"]
            # if len(res) == 0:  # 查询结果为空直接返回
            #     return self.original_front_end_data(), False

            # 计算text在name和summary中各自出现的次数
            try:
                for x in cur_res:
                    # logger.info(res)
                    if "name" in x.keys() and x["name"]:
                        x["text_name_count"] = x["name"].count(self.text)
                    else:
                        x["text_name_count"] = 0

                    if "summary" in x.keys() and x["summary"]:
                        x["text_summary_count"] = x["summary"].count(self.text)
                    else:
                        x["text_summary_count"] = 0

            except Exception as e:
                logger.error(
                    "更新主题选项各分支个数 --图数据库查询结果不包含相应字段,cypher语句可能存在问题  --cypher: {0} ".format(
                        cypher_str1))
                logger.error("报错信息如下 ---error:{}".format(str(e)))
                return False

            # 降序排序，name为第一关键词，summary为第二关键词
            cur_res.sort(key=lambda s: (s["text_name_count"], s["text_summary_count"]), reverse=True)

            # 含冗余的主题列表
            raw_themes_list = []

            try:
                # 获取所有主题
                if cur_res:
                    for x in cur_res:
                        for y in x["theme"]:
                            if y:
                                raw_themes_list.append(y)

                    # 定义主题对应的数量字典
                    themes_dict = dict(Counter(raw_themes_list))
                else:
                    themes_dict = {k: v for k, v in zip(self.themes, ["0"] * len(self.themes))}
            except Exception as e:
                print("获取主题词出错")
                logger.error("获取主题词出错 没有获取到theme字段 ---{} ".format(str(e)))
                return False

            new_cur_themes = []

            # 循环遍历主题对应的数量字典
            for k, v in themes_dict.items():
                # 拼接主题选项的字符串
                string = k + "（" + str(v) + "）"
                # 将当前主题选项的字符串添加到主题选项列表
                new_cur_themes.append(string)

            # 默认按数量排序
            new_cur_themes.sort(key=re_get_num, reverse=True)
            # 限制主题选项显示数量
            new_cur_themes = new_cur_themes[:themes_limit]

            # 循环遍历列表
            for i, x in enumerate(new_cur_themes):
                # 正则化匹配"（...）"
                regularization = re.findall("（\d*）", x)
                # 去除每个选项字符串的数量
                new_cur_themes[i] = x.replace("".join(regularization), "")

            raw_themes_list = []

            # 获取所有主题
            if self.res:
                for x in self.res:
                    for y in x["theme"]:
                        if y:
                            raw_themes_list.append(y)

                # 定义主题对应的数量字典
                themes_dict = dict(Counter(raw_themes_list))
            else:
                themes_dict = {k: v for k, v in zip(self.themes, ["0"] * len(self.themes))}

            # 获取与关键词查询的搜索引擎查询中的相关关键词字典
            themes_dict = {k: v for k, v in themes_dict.items() if k in new_cur_themes}

            cur_themes = []

            # 获取新需求的关键词列表
            for x in new_cur_themes:
                if x in themes_dict.keys():
                    string = x + "（" + str(themes_dict[x]) + "）"
                else:
                    string = x + "（0）"

                cur_themes.append(string)

            self.themes = cur_themes

            # 默认按数量排序
            self.themes.sort(key=re_get_num, reverse=True)
            # 限制主题选项显示数量
            self.themes = self.themes[:themes_limit]



        else:
            if self.res:
                # 获取所有主题
                for x in self.res:
                    for y in x["theme"]:
                        if y:
                            raw_themes_list.append(y)

                # 定义主题对应的数量字典
                themes_dict = dict(Counter(raw_themes_list))
            else:
                themes_dict = {k: v for k, v in zip(self.themes, ["0"] * len(self.themes))}

            cur_themes = []

            # 循环遍历主题对应的数量字典
            for k, v in themes_dict.items():
                # 拼接主题选项的字符串
                string = k + "（" + str(v) + "）"
                # 将当前主题选项的字符串添加到主题选项列表
                cur_themes.append(string)

            self.themes = cur_themes

            # 默认按数量排序
            self.themes.sort(key=re_get_num, reverse=True)
            # 限制主题选项显示数量
            self.themes = self.themes[:themes_limit]
        return True

    # 更新公司选项各分支个数
    def update_company_num(self):
        # 获取公司选项的最大数量
        companies_limit = self.graph_const.get_companies_limit()
        # 含冗余的公司列表
        raw_companies_list = []

        if self.companies:

            # 获取查询结果
            # outputs = self.session.execute_read(
            #     query_tradition_filtered_search,
            #     self.text,
            #     "",
            #     self.types,
            #     "",
            #     "",
            #     self.graph_const.get_times_properties(),
            #     self.graph_const.get_types_map(),
            #     self.graph_const.get_themes_properties(),
            #     self.graph_const.get_companies_properties(),
            #     self.graph_const.get_experts_properties(),
            # )
            cypher_str1 = query_tradition_filtered_search_cypher_str(

                self.text,
                "",
                self.types,
                "",
                "",
                self.graph_const.get_times_properties(),
                self.graph_const.get_types_map(),
                self.graph_const.get_themes_properties(),
                self.graph_const.get_companies_properties(),
                self.graph_const.get_experts_properties()
            )
            query_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str1,
                                                                                                      pe.Status_codes.cypher_query)

            if query_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                # 如果查询失败直接返回原前端值
                logger.error("更新公司选项各分支个数  --图数据库查询失败  {0} --msg:{1}".format(query_res["code"],
                                                                                                query_res["msg"]))
                return False
            res = query_res["data"]
            # if len(res) == 0:  # 查询结果为空直接返回
            #     logging.warning(
            #         "图数据库查询失败,cypher语句可能错误  {0} --msg:{1} --cypher:{2}".format(query_res["code"],
            #                                                                                  query_res["msg"],
            #                                                                                  cypher_str1))
            #     # return self.original_front_end_data(), False
            # logging.info("图数据库查询成功  {0} --msg:{1}".format(query_res["code"], query_res["msg"]))

            # 初始化输出结果
            cur_res = res
            # print(cur_res)

            # 更改输出的格式为内嵌字典的列表
            # for x in outputs:
            #     cur_res.append(dict(x.items()))

            # 计算text在name和summary中各自出现的次数
            try:
                for x in cur_res:
                    # logger.info(res)
                    if "name" in x.keys() and x["name"]:
                        x["text_name_count"] = x["name"].count(self.text)
                    else:
                        x["text_name_count"] = 0

                    if "summary" in x.keys() and x["summary"]:
                        x["text_summary_count"] = x["summary"].count(self.text)
                    else:
                        x["text_summary_count"] = 0
            except Exception as e:
                logger.error(
                    "更新公司选项各分支个数 --图数据库查询结果不包含相应字段,cypher语句可能存在问题  --cypher: {0}  --return_data: {1}  --报错: {2}".format(
                        cypher_str1, cur_res, str(e)))
                return False

            # 降序排序，name为第一关键词，summary为第二关键词
            cur_res.sort(key=lambda s: (s["text_name_count"], s["text_summary_count"]), reverse=True)

            # 获取所有公司
            if cur_res:
                for x in cur_res:

                    # cur_company = self.session.execute_read(query_second_rank_company_name, x["company"])
                    # TODO:如果查询失败怎么办

                    # 1127 切分字符串为列表
                    # *1127
                    if x["company"] and "," in x["company"]:
                        new_companies = [z for z in x["company"].split(",")]
                    elif x["company"]:
                        new_companies = [x["company"]]
                    else:
                        new_companies = []
                    # 1127 增加循环
                    for single_company in new_companies:
                        # cypher_str_2 = query_second_rank_company_name_cypher_str(single_company)
                        # query_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                        #     cypher_str_2, pe.Status_codes.cypher_query)
                        #
                        # if query_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                        #     # 如果查询失败直接返回原前端值
                        #     logger.error(
                        #         "更新公司选项各分支个数 --图数据库查询失败,cypher语句可能存在问题  {0} --msg:{1}  --cypher: {2}".format(
                        #             query_res["code"], query_res["msg"], cypher_str_2))
                        #
                        #     return False
                        #
                        # query_data = query_res["data"]
                        #
                        # try:
                        #     cur_company = [x["name"] for x in query_data]
                        # except Exception as e:
                        #     logger.error(
                        #         "更新公司选项各分支个数 --图数据库查询结果不包含相应字段,cypher语句可能存在问题  --cypher: {0}  --return_data: {1}  --报错: {2}".format(
                        #             cypher_str_2, query_data, str(e)))
                        #     return False

                        # 1127
                        # if len(cur_company) >= 2:
                        #     cur_company.remove(single_company)

                        # if cur_company:
                        #     raw_companies_list.append(cur_company[0])

                        raw_companies_list.append(single_company)

                # 定义公司对应的数量字典
                companies_dict = dict(Counter(raw_companies_list))
            else:
                companies_dict = {k: v for k, v in zip(self.companies, ["0"] * len(self.companies))}

            new_cur_companies = []

            # 循环遍历公司对应的数量字典
            for k, v in companies_dict.items():
                # 拼接公司选项的字符串
                string = k + "（" + str(v) + "）"
                # 将当前公司选项的字符串添加到公司选项列表
                new_cur_companies.append(string)

            # 默认按数量排序
            new_cur_companies.sort(key=re_get_num, reverse=True)
            # 限制公司选项显示数量
            new_cur_companies = new_cur_companies[:companies_limit]

            # 循环遍历列表
            for i, x in enumerate(new_cur_companies):
                # 正则化匹配"（...）"
                regularization = re.findall("（\d*）", x)
                # 去除每个选项字符串的数量
                new_cur_companies[i] = x.replace("".join(regularization), "")

            raw_companies_list = []

            if self.res:
                # 获取所有公司
                for x in self.res:
                    # cur_company = self.session.execute_read(query_second_rank_company_name, x["company"])
                    # flag = 0
                    # for seg in [",", ".", "/", "，", "。", ";", "；", "、"]:
                    #     if seg in x["company"]:
                    #         companies_to_search = [z for z in x["company"].split(seg)]
                    #         flag = 1
                    #         break
                    # if flag == 0:
                    #     companies_to_search = [x["company"]]
                    # companies_to_search = re.split(',./，。；;\\、', x["company"])
                    # *1127
                    if x["company"] and "," in x["company"]:
                        companies_to_search = [z for z in x["company"].split(",")]
                    elif x["company"]:
                        companies_to_search = [x["company"]]
                    else:
                        companies_to_search = []
                    for company_to_search in companies_to_search:
                        # cypher_str_3 = query_second_rank_company_name_cypher_str(company_to_search)
                        # query_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                        #     cypher_str_3, pe.Status_codes.cypher_query)
                        #
                        # if query_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                        #     # 如果查询失败直接返回原前端值
                        #     logger.error(
                        #         "更新公司选项各分支个数 --图数据库查询失败,cypher语句可能存在问题  {0} --msg:{1}  --cypher: {2}".format(
                        #             query_res["code"], query_res["msg"], cypher_str_3))
                        #     return False
                        #
                        # cur_company = query_res["data"]
                        #
                        # try:
                        #     cur_company = [x["name"] for x in cur_company]
                        # except Exception as e:
                        #     logger.error(
                        #         "更新公司选项各分支个数 --图数据库查询结果不包含相应字段,cypher语句可能存在问题  --cypher: {0}  --return_data: {1}  --报错: {2}".format(
                        #             cypher_str_3, query_res["data"], str(e)))
                        #     return False
                        #
                        # # 1127
                        # # if len(cur_company) >= 2:
                        # #     cur_company.remove(company_to_search)
                        #
                        # if cur_company:
                        #     raw_companies_list.append(cur_company[0])

                        raw_companies_list.append(company_to_search)

                # 定义公司对应的数量字典
                companies_dict = dict(Counter(raw_companies_list))
            else:
                companies_dict = {k: v for k, v in zip(self.companies, ["0"] * len(self.companies))}

            # 获取与公司查询的搜索引擎查询中的相关公司字典
            companies_dict = {k: v for k, v in companies_dict.items() if k in new_cur_companies}

            cur_companies = []

            # 获取新需求的公司列表
            for x in new_cur_companies:
                if x in companies_dict.keys():
                    string = x + "（" + str(companies_dict[x]) + "）"
                else:
                    string = x + "（0）"

                cur_companies.append(string)

            self.companies = cur_companies

            # 默认按数量排序
            self.companies.sort(key=re_get_num, reverse=True)
            # 限制主题选项显示数量
            self.companies = self.companies[:companies_limit]
        else:

            if self.res:
                # 获取所有公司
                for x in self.res:
                    # cur_company = self.session.execute_read(query_second_rank_company_name, x["company"])
                    # flag = 0
                    # for seg in [",", ".", "/", "，", "。", ";", "；", "、"]:
                    #     if seg in x["company"]:
                    #         companies_to_search = [z for z in x["company"].split(seg)]
                    #         flag = 1
                    #         break
                    # if flag == 0:
                    #     companies_to_search = [x["company"]]
                    # companies_to_search = re.split(',./，。；;\\、', x["company"])
                    # *1127
                    if x["company"] and "," in x["company"]:
                        companies_to_search = [z for z in x["company"].split(",")]
                    elif x["company"]:
                        companies_to_search = [x["company"]]
                    else:
                        companies_to_search = []
                    for company_to_search in companies_to_search:
                        raw_companies_list.append(company_to_search)
                # 定义公司对应的数量字典
                # companies_dict = dict(Counter(raw_companies_list))

                # 0403:
                raw_companies_list_copy = []
                for obj in raw_companies_list:
                    raw_companies_list_copy.append(obj.strip(" "))

                companies_dict = Counter(raw_companies_list_copy)
            else:
                companies_dict = {k: v for k, v in zip(self.companies, ["0"] * len(self.companies))}

            cur_companies = []

            # 循环遍历公司对应的数量字典
            for k, v in companies_dict.items():
                # 拼接公司选项的字符串
                string = k + "（" + str(v) + "）"
                # 将当前公司选项的字符串添加到公司选项列表
                cur_companies.append(string)

            self.companies = cur_companies

            # 默认按数量排序
            self.companies.sort(key=re_get_num, reverse=True)
            # 限制公司选项显示数量
            self.companies = self.companies[:companies_limit]
        return True

    # [含处理]<搜索引擎>: 搜索范围[0:0], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string), 限制条件: ({condition})
    def expand_query_tradition_filtered_search(self) -> (dict, bool):

        cypher_str1 = query_tradition_filtered_search_cypher_str(self.text,
                                                                 self.times,
                                                                 self.types,
                                                                 self.themes,
                                                                 self.companies,
                                                                 self.graph_const.get_times_properties(),
                                                                 self.graph_const.get_types_map(),
                                                                 self.graph_const.get_themes_properties(),
                                                                 self.graph_const.get_companies_properties(),
                                                                 self.graph_const.get_experts_properties())

        query_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str1, pe.Status_codes.cypher_query)

        if query_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
            # 如果查询失败直接返回原前端值
            logger.error("图数据库查询失败  {0} --msg:{1}".format(query_res["code"], query_res["msg"]))
            return self.original, False
        res = query_res["data"]

        # 0517:
        gid_list = []
        new_res = []
        for obj in res:
            if obj['gid'] not in gid_list:
                gid_list.append(obj['gid'])
                new_res.append(obj)
        res = new_res

        # print(res)
        if res == 0:  # 查询结果为空直接返回
            logger.warning(
                "图数据库返回结果为空,cypher语句可能错误  {0} --msg:{1} --cypher:{2}".format(query_res["code"], query_res["msg"], cypher_str1))

        # 过滤时间和公司为空的检索结果 + 二次过滤时间相关
        raw_total_times = self.graph_const.get_times()
        total_times = []
        for ctime in raw_total_times:
            if "其他" not in ctime:
                total_times.append(ctime[:4])

        if not self.times:
            times_to_scan = self.graph_const.get_times()
        else:
            times_to_scan = self.times

        filtered_res = []

        for time_to_scan in times_to_scan:
            for x in res:
                cur_time = str(x["time"])[:4]
                if cur_time in time_to_scan and "其他" not in time_to_scan and x["time"]:
                    y = x
                    y["time"] = cur_time
                    filtered_res.append(y)
                elif "其他" in time_to_scan and cur_time not in total_times:
                    y = x
                    y["time"] = cur_time
                    filtered_res.append(y)

        res = filtered_res

        # 计算text在name和summary中各自出现的次数
        for x in res:
            # logger.info(res)
            if "name" in x.keys() and x["name"]:
                x["text_name_count"] = x["name"].count(self.text)
            else:
                x["text_name_count"] = 0

            if "summary" in x.keys() and x["summary"]:
                x["text_summary_count"] = x["summary"].count(self.text)
            else:
                x["text_summary_count"] = 0

        # 降序排序，name为第一关键词，summary为第二关键词
        res.sort(key=lambda s: (s["text_name_count"], s["text_summary_count"]), reverse=True)

        self.res = res

        if self.page_limit:
            page_limit = self.page_limit
        else:
            page_limit = self.graph_const.get_per_page_limit()

        # 获取总页数
        int_total_pages = int(len(res) / page_limit)

        extra_total_pages = len(res) % page_limit
        if extra_total_pages != 0:
            extra_total_pages = 1

        self.total_pages = int_total_pages + extra_total_pages

        # 分页限制输出的范围
        real_res = res[(self.page - 1) * page_limit:
                       (self.page - 1) * page_limit + page_limit]

        self.real_res = real_res

        # 如果更新返回结果出错也是返回原始值
        final_res_data, ifSuccess = self.output()

        # print(current_app.app_context())
        localhost_ip = flask_config.Config.HOST_IP
        # print(localhost_ip)
        update_dict = {
            "res": res,
            "backend_ip": flask_config.Config.BACK_END_URL,
            "backend_port": flask_config.Config.BACK_END_PORT
        }
        result = requests.post("http://%s:%d/kjxmzstp/dataUpdate" % (localhost_ip, flask_config.Config.PORT),
                               json=update_dict)
        # threading.Thread(target=update_search_times, args=(current_app, res,
        #                                                    localhost_ip,flask_config.Config.PORT)).start()  # 执行线程

        # print("跳过更新 异步执行")
        """更新搜索次数字段值"""
        # 异步 先返回再更新
        # for x in self.res:
        #     res_data=bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
        #         update_search_number_cypher_str(x["gid"]),
        #         pe.Status_codes.cypher_update)
        #     if res_data["code"]!=pe.ProcessInfos.UPDATE_SUCCEED.status_code:
        #         #记录日志表示更新错误
        #         print("记录日志")
        #         print(res_data["msg"])
        # self.session.execute_write(update_search_number, x["gid"])
        return final_res_data, ifSuccess

    # 添加图数据库的相关节点属性{keywords}
    def add_theme_to_graph(self) -> bool:
        # 实例化KeyBERT模型的类
        key_bert_model = KeyBERTModel()

        # 获取主题相关节点的文本
        # contents = self.session.execute_read(
        #     query_theme_name_with_summary,
        #     self.graph_const.get_themes_properties(),
        #     self.graph_const.get_themes_type()
        # )

        contents_cypher = query_theme_name_with_summary_cypher_str(self.graph_const.get_themes_properties(),
                                                                   self.graph_const.get_themes_type())
        # logger.info("contents_cypher 语句是--:{}".format(contents_cypher))
        res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
            cypher_str=contents_cypher, code=pe.Status_codes.cypher_query
        )
        if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
            logger.error("图数据库查询失败,cypher语句可能错误  --cypher:{0}".format(contents_cypher))
            return False

        res_data = res_dict["data"]
        logger.info("图数据库返回状态码" + str(res_dict["code"]))
        logger.info("图数据库查询数据为  --data:{}".format(res_data))
        # logger.info("图数据库查询结果数据  --{}".format(res_data))
        try:
            contents = [x for x in res_data]
        except:
            logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(contents_cypher,
                                                                                                   res_data))
            return False

        # [x for x in res]
        new_contents = []

        # 对查询结果进行后处理
        for content in contents:
            a = dict(content.items())
            new_contents.append(a)
            # logger.info("单个图数据查询结果  --  {}".format(a))

        median_contents = []

        # print(f"节点关键词生成中...")
        logger.info(f"节点关键词生成中...")

        # 获取总个数
        contents_len = len(new_contents)
        # 遍历获取各个节点的名字主题和概要主题
        for i, content in enumerate(new_contents):
            id = content["id"]

            key_bert_model.input(content["name"])
            try:
                name_keywords = key_bert_model.output()
            except Exception as e:
                logger.error("加载大语言模型失败 :{}".format(str(e)))
                return False

            if content["summary"]:
                key_bert_model.input(content["summary"])
                try:
                    summary_keywords = key_bert_model.output()
                except Exception as e:
                    logger.error("加载大语言模型失败 :{}".format(str(e)))
                    return False

            else:
                summary_keywords = ""

            # 如果生成的概要主题和名字主题相同，则舍弃概要主题
            if summary_keywords == name_keywords:
                summary_keywords = ""

            if summary_keywords:
                cur_list = [name_keywords, summary_keywords]
            else:
                cur_list = [name_keywords]

            median_contents.append({
                "id": id,
                "keywords": cur_list
            })

            # print(f"完成关键词的提取: {i + 1} / {contents_len}")
            logger.info(f"完成关键词的提取: {i + 1} / {contents_len}")

        # print(f"节点关键词生成结束...")
        logger.info(f"节点关键词生成结束...")

        # 添加名字主题和概要主题到图数据库中
        for content in median_contents:
            # self.session.execute_write(set_themes, content)
            cypher_str2 = set_themes_cypher_str(content)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str2, code=pe.Status_codes.cypher_update
            )
            if res_dict["code"] != pe.ProcessInfos.UPDATE_SUCCEED.status_code:
                logger.error("图数据库更新失败,cypher语句可能错误  --cypher:{0}".format(contents_cypher))
                return False
        del key_bert_model
        return True

    # 添加图数据库的相关节点属性{search_number}
    def add_search_number_to_graph(self) -> bool:
        for k in self.graph_const.get_themes_properties().keys():
            # self.session.execute_write(set_search_number, k)
            cypher_str1 = set_search_number_cypher_str(k)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str1,
                                                                                                     pe.Status_codes.cypher_add)
            if res_dict["code"] != pe.ProcessInfos.ADD_SUCCEED.status_code:
                logger.error("图数据库添加节点失败,cypher语句可能错误  --cypher:{0}".format(cypher_str1))
                return False
        return True

    # 创建热词节点
    def create_entity_buzzwords_to_graph(self) -> bool:
        # self.session.execute_write(create_entity_buzzwords)
        #  [x["n"] for x in re

        cypher_str_check = check_entity_buzzwords_cypher_str()
        res_dict_check = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str_check,
                                                                                                       pe.Status_codes.cypher_query)
        if res_dict_check["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
            logger.error("图数据库添加节点失败,cypher语句可能错误  --cypher:{0}".format(cypher_str_check))
            return False

        res_dict_check_data = res_dict_check["data"]

        try:
            check_data = [x["n"] for x in res_dict_check_data]
        except:
            logger.error("图数据库添加节点失败,cypher语句可能错误  --cypher:{0}".format(cypher_str_check))
            return False

        if len(check_data) == 0:
            cypher_str1 = create_entity_buzzwords_cypher_str()
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str1,
                                                                                                     pe.Status_codes.cypher_add)
            if res_dict["code"] != pe.ProcessInfos.ADD_SUCCEED.status_code:
                logger.error("图数据库添加节点失败,cypher语句可能错误  --cypher:{0}".format(cypher_str1))
                return False
            return True
        else:
            return True

    # 更新热词节点
    def update_entity_buzzwords_to_graph(self):
        # 获取存储节点对应的相关主题属性
        themes_properties = self.graph_const.get_themes_properties()
        # 含冗余的热词列表
        raw_buzzwords_list = []

        # 获取所有热词
        for k in themes_properties.keys():

            # cur_list = self.session.execute_read(query_all_buzzwords, k)
            # [(x["keywords"], x["search_number"]) for x in res]
            # print(cur_list)
            cypher_str1 = query_all_buzzwords_cypher_str(k)
            res: dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str1, code=pe.Status_codes.cypher_query)
            if res["code"] != 200:
                logger.error(
                    "图数据库查询失败,cypher语句可能错误  --cypher:{0} ".format(cypher_str1))
                # TODO:如果查询失败就直接返回
                return False

            res_data = res["data"]

            try:
                cur_list = [(x["keywords"], x["search_number"]) for x in res_data]

            except:
                logger.error("图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str1,
                                                                                                       res_data))
                return False
            try:
                for x in cur_list:
                    raw_buzzwords_list += list(x[0]) * x[1]
            except:
                logger.error("图数据库热词结点有误,请查看热词结点  --res_data:{}".format(cur_list))
                return False

        if raw_buzzwords_list:
            # 定义热词对应的数量字典
            buzzwords_dict = dict(Counter(raw_buzzwords_list))

            # 定义热词排序列表
            order_list = []

            # 循环遍历热词对应的数量字典
            for k, v in buzzwords_dict.items():
                order_list.append((k, v))

            # 默认按数量排序
            order_list.sort(key=lambda d: d[1], reverse=True)

            # 更新热词节点
            # self.session.execute_write(update_entity_buzzwords, order_list)
            cypher_str2 = update_entity_buzzwords_cypher_str(order_list)
            update_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str2, code=pe.Status_codes.cypher_update)
            if update_res["code"] != 200:
                logger.error(
                    "图数据库更新失败,cypher语句可能错误  --cypher:{0} ".format(cypher_str2))
                return False

            return True

    # LLH: 该函数修改
    # 统一节点的时间字段值得类型为字符串
    def set_time_properties_to_string(self) -> bool:
        times_properties = self.graph_const.get_times_properties()

        for k, v in times_properties.items():
            for l in v:
                # self.session.execute_write(set_time_properties, k, l)

                cypher_str1 = set_time_properties_cypher_str(k, l)
                res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(cypher_str1,
                                                                                                         pe.Status_codes.cypher_update)
                if res_dict["code"] != pe.ProcessInfos.ADD_SUCCEED.status_code:
                    logger.info("图数据库更新失败,cypher语句可能错误  --cypher:{0}".format(cypher_str1))
                    return False
        return True

    # 输出查询结果
    def output(self) -> (dict, bool):
        # 更新失败全部返回原始值
        # 更新时间选项
        ifSuccess = self.update_times_num()
        if not ifSuccess:
            logger.error("时间更新失败 返回原值 ")
            return self.original, False

        # 更新主题选项
        ifSuccess = self.update_themes_num()
        if not ifSuccess:
            logger.error("主题词更新失败 返回原值 ")

            return self.original, False

        # 更新公司选项
        ifSuccess = self.update_company_num()
        if not ifSuccess:
            logger.error("公司更新失败 返回原值 ")
            return self.original, False

        # 更新类型选项
        ifSuccess = self.update_types_num()
        if not ifSuccess:
            logger.error("类型更新失败 返回原值 ")
            return self.original, False

        res_dict = {
            # 查询id
            "id": self.graph_const.get_updated_id(),
            # 关键词
            "text": self.text,
            # 时间选项
            "times": self.times,
            # 类型选项
            "types": self.types,
            # 主题选项
            "themes": self.themes,
            # 公司选项
            "companies": self.companies,
            # 结果字典列表
            "res": self.real_res,
            # 总页数
            "total_pages": self.total_pages,
            # 当前页数
            "page": self.page,
            # 每页页数
            "page_limit": self.page_limit,
            # 总结果数量
            "total_num": len(self.res)
        }

        return res_dict, True

    def set_original_front_end_data(self, text, times, types, themes, companies, real_res, total_pages, page):
        res = {
            # 查询id
            "id": self.graph_const.get_updated_id(),
            # 关键词
            "text": text,
            # 时间选项
            "times": times,
            # 类型选项
            "types": types,
            # 主题选项
            "themes": themes,
            # 公司选项
            "companies": companies,
            # 结果字典列表
            "res": real_res,
            # 总页数
            "total_pages": total_pages,
            # 当前页数
            "page": page,
            "total_num": 0
        }

        return res

        # TODO:因为返回的数据与原始前端数据不同 所以不能直接返回self.的实例属性 这些属性是一直的在更新的 和llh商量一下
        # return self.original_front_end_data_dict


# 知识图谱图的类
class KGraph:
    # 图数据库初始化
    # driver = graph_init.init()

    def __init__(self):
        # 创建连接
        # self.session = self.driver.session()
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
        if (not self.text) and (not self.gid):
            return True
        else:
            return False

    # 知识图谱默认搜索
    def query_graph_init(self) -> (dict, bool):

        final_res_dict = None
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
            cypher_str1 = query_graph_init_cypher_str(label, nodes_init_limit)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str1, code=pe.Status_codes.cypher_query
            )
            if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                logger.error(
                    "图数据库查询失败,cypher语句可能错误  --cypher:{0} ".format(cypher_str1))
                final_res_dict = self.output()
                return final_res_dict, False

            res_data = res_dict["data"]
            try:
                raw_res_1 = {x["gid"]: x["n"] for x in res_data}
            #     知识图谱默认搜索不会发生异常  因为text为空
            except:
                logger.error(
                    "图数据库返回结果错误,cypher语句可能错误  --cypher:{0} --data:{1}".format(cypher_str1, res_data))
                final_res_dict = self.output()
                return final_res_dict, False

            # 范围1内结果的后处理
            for k, v in raw_res_1.items():
                cur_dict = dict(v.items())
                cur_dict["gid"] = k
                first_res.append(cur_dict)

        self.first_res = first_res
        final_res_dict = self.output()

        return final_res_dict, True

    # [含处理]<知识图谱>: 搜索范围[0:1], 搜索结点标签: (label), 搜索结点属性: (property), 搜索内容: (string)
    def expand_query_graph_filtered_search(self):
        # 定义范围1内的结果
        first_res = []
        # 定义范围2内的结果
        second_res = []

        final_res_dict = {}

        # 如果没有点击特定节点并获取了对应的gid
        if not self.gid:
            # LLH: 以下一段，增加if判断
            # ===============================================================================
            if self.label in self.graph_const.get_graph_types_map_reverse().keys():
                labels = []
                labels.append(self.label)
            else:
                # 获取知识图谱的type中文名和对应节点名的映射关系
                labels = self.graph_const.get_graph_types_map()[self.label]
            # ===============================================================================

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
                    logger.warning(
                        "返回结果为空 当前阶段的label不可用 没有遍历到目标label  --label:{}  --text:{}".format(label,
                                                                                                               self.text))
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
                    logger.warning(
                        "kquery非默认搜索中res_1为空 表示当前label和text是不匹配的 跳过  --label:{}  --text:{}".format(
                            label, self.text))
                    #   跳过
                    continue
                # 范围1内结果的后处理
                try:
                    gid_1 = [x for x in res_1.keys()][0]
                except Exception as e:
                    logger.error("获取gid_1的结果为空  -- 报错:{}  --cypher:{}".format(e, cypher_str2))
                    return final_res_dict, False

                single_first_res = dict(res_1[gid_1].items())
                single_first_res["gid"] = gid_1

                # 定义范围2内结果的所有节点列表
                res_2_nodes = []

                # 获取原生的范围2内结果的所有节点列表
                # raw_res_2_nodes = self.session.execute_read(query_graph_filtered_search_second_nodes, gid_1)
                cypher_str3 = query_graph_filtered_search_second_nodes_cypher_str(gid_1)
                res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                    cypher_str=cypher_str3, code=pe.Status_codes.cypher_query
                )
                if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                    final_res_dict = self.output()
                    return final_res_dict, False

                res_data = res_dict["data"]
                try:
                    # 后处理
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
                cypher_str4 = query_graph_filtered_search_second_relations_cypher_str(gid_1)
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
                res_1 = {x["gid"]: x["n"] for x in res_data}

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
                logger.error("获取gid_1的结果为空  -- {}".format(e))
                return final_res_dict, False

            single_first_res = dict(res_1[gid_1].items())
            single_first_res["gid"] = gid_1

            # 定义范围2内结果的所有节点列表
            res_2_nodes = []

            # 获取原生的范围2内结果的所有节点列表
            # raw_res_2_nodes = self.session.execute_read(query_graph_filtered_search_second_nodes, gid_1)

            cypher_str6 = query_graph_filtered_search_second_nodes_cypher_str(gid_1)
            res_dict = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                cypher_str=cypher_str6, code=pe.Status_codes.cypher_query
            )
            if res_dict["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                final_res_dict = self.output()
                return final_res_dict, False

            res_data = res_dict["data"]
            try:
                # 后处理
                raw_res_2_nodes = {x["gid"]: x["n2"] for x in res_data}

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

        final_res_dict = self.output()
        return final_res_dict, True

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


# 提示的类
class Tip:
    # 图数据库初始化
    # driver = graph_init.init()

    def __init__(self, id, tip, res):
        # 创建连接
        # self.session = self.driver.session()
        self.id = id
        self.tip = tip
        self.res = res
        # 实例化图的常量类
        self.graph_const = GraphConst()

    def input(self, dict):
        # 传入输入的值
        # 循环遍历字典
        for k, v in dict.items():
            # 存储数据
            if k == "tip":
                self.tip = v

    def __del__(self):
        logger.info("tips 清理缓存")

    # 获取搜索的提示词
    def acquire_tips(self) -> (dict, bool):
        tips_res = []
        res_data = {
            "id": self.graph_const.get_updated_id(),
            "tip": self.tip
        }
        # 获取提示词选项的最大数量
        tips_limit = self.graph_const.get_tips_limit()

        # 获取热词节点的属性
        # raw_buzzwords_properties = self.session.execute_read(query_entity_buzzwords)
        query_entity_buzzwords_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
            cypher_str=query_entity_buzzwords_cypher_str(), code=pe.Status_codes.cypher_query)

        if query_entity_buzzwords_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
            res_data["res"] = []
            return res_data, False
        query_entity_buzzwords_res_data = query_entity_buzzwords_res["data"]
        try:
            query_entity_buzzwords_res_data = [x.get("n") for x in query_entity_buzzwords_res_data][0]
        except Exception as e:
            logger.error("查询失败  --res_data:{}  --Exception:{}".format(query_entity_buzzwords_res_data, e))
            res_data["res"] = []
            return res_data, False
        # 热词节点的后处理
        # if len(query_entity_buzzwords_res_data)==0:  #如果没有查询到也是返回空值
        #     res_data["res"] = []
        #     return res_data, False  #返回空值 以及标记错误

        raw_buzzwords_dict = dict(query_entity_buzzwords_res_data.items())

        raw_buzzwords_list = raw_buzzwords_dict.values()

        order_list = []

        for x in raw_buzzwords_list:
            cur_tuple = tuple(x.split(","))
            order_list.append(cur_tuple)

        filtered_order_list = []

        # 过滤与提示词不相关的热词
        for x in order_list:
            if self.tip in x[0]:
                filtered_order_list.append(x)

        # 对处理后的热词列表进行排序
        filtered_order_list.sort(key=lambda d: d[1], reverse=True)

        # 去除多余的不显示的热词
        filtered_order_list = filtered_order_list[:tips_limit]

        for x in filtered_order_list:
            tips_res.append(x[0])

        self.res = tips_res
        res_data["res"] = tips_res
        return res_data, True

    # 获取搜索引擎主页的热词
    def acquire_buzzwords(self) -> (dict, bool):
        # 获取热词选项的最大数量
        buzzwords_limit = self.graph_const.get_buzzwords_limit()
        res_data = {
            "id": self.graph_const.get_updated_id(),
            "tip": self.tip
        }

        # 获取热词节点的属性
        # raw_buzzwords_properties = self.session.execute_read(query_entity_buzzwords)
        query_entity_buzzwords_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
            cypher_str=query_entity_buzzwords_cypher_str(), code=pe.Status_codes.cypher_query)

        if query_entity_buzzwords_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:  # 如果查询错误 就直接返回
            res_data["res"] = []
            return res_data, False

        raw_buzzwords_properties = query_entity_buzzwords_res["data"]
        # if len(raw_buzzwords_properties)==0:  #如果data查询没有结果 也是直接返回
        #     res_data["res"] = []
        #     return res_data, False
        try:
            raw_buzzwords_properties = [x.get("n") for x in raw_buzzwords_properties][0]
        except:
            logger.error("沒有指定的字段值")
            res_data["res"] = []
            return res_data, False
        # 热词节点的后处理
        if len(raw_buzzwords_properties) == 0:  # 查询指定字段结果为空 也直接返回
            res_data["res"] = []
            return res_data, False

        raw_buzzwords_dict = dict(raw_buzzwords_properties.items())

        raw_buzzwords_list = raw_buzzwords_dict.values()

        order_list = []

        for x in raw_buzzwords_list:
            cur_tuple = tuple(x.split(","))
            order_list.append(cur_tuple)

        # 对处理后的热词列表进行排序
        order_list.sort(key=lambda d: d[1], reverse=True)

        # 去除多余的不显示的热词
        order_list = order_list[:buzzwords_limit]

        buzzwords_res = []

        for x in order_list:
            buzzwords_res.append(x[0])

        self.res = buzzwords_res
        res_data["res"] = buzzwords_res
        return res_data, True

    # 获取首页的统计数据
    def acquire_count(self) -> (bool, dict):  # TODO:新增
        types_count = self.graph_const.get_types_count()

        res = {}

        for k, v in types_count.items():
            res[k] = 0
            for x in v:

                # cur_num = self.session.execute_read(query_types_count, x)
                cypher_str_types = query_types_count_cypher_str(x)
                query_number_types_count_res = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
                    cypher_str=cypher_str_types, code=pe.Status_codes.cypher_query)
                # 获取查询到的返回结果

                if query_number_types_count_res["code"] != pe.ProcessInfos.GET_SUCCEED.status_code:
                    logger.error("获取智能检索下方的type_count错误 --code:{} --msg:{} --cypher_str{}".format(
                        query_number_types_count_res["code"],
                        query_number_types_count_res["msg"],
                        cypher_str_types
                    ))
                    return False, {}

                query_data = query_number_types_count_res["data"]
                if query_data:
                    try:
                        # print(query_data)
                        res[k] += query_data[0]["count(n)"]  # 总结最终的type-count 返回结果
                    except Exception as e:
                        logger.error("发生报错 --{}".format(str(e)))
                        return False, {}
                    # res[k] += cur_num[0]
        downwardCountMap = self.graph_const.get_downwardCountChineseToEnglish()
        resProcessed = {}
        for k, v in res.items():
            resProcessed[downwardCountMap.get(k, "")] = v

        return True, resProcessed

    def output(self):

        # 输出结果
        return {
            "id": self.graph_const.get_updated_id(),
            "tip": self.tip,
            "res": self.res,
        }


'''

def update_search_times(app:flask.Flask,res,localhost_ip,port):
    #TODO：异步执行中间含有http请求 所以有点问题
    print("线程执行")
    # with app.app_context():

    for x in res:
        # print(x)
        # res_data = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
        #     update_search_number_cypher_str(x["gid"]),
        #     pe.Status_codes.cypher_update)
        temp_dict={
            "cypher_str":update_search_number_cypher_str(x["gid"]),
            "code":pe.Status_codes.cypher_update
        }
        print("hsisiisi")

        print("异步更新数据结束，开辟线程")
        url = "http://%s:%d/graphDatabaseNeo4j/cypher_back_end" % (localhost_ip, port)

        # back_end_processing = bnc.back_end_get_data_from_end_end(**temp_dict) # 字典解包
        # back_end_data = back_end_processing.back_end_data_return()

        back_end_data = requests.post(url, json=temp_dict)
        print("异步更新数据结束，开辟线程")
        # json_data = res_return.json()
        res_data = json.loads(back_end_data)
        # print(res_data)
        if res_data["code"] != pe.ProcessInfos.UPDATE_SUCCEED.status_code:
            # TODO:记录日志 表示更新错误
            print("记录日志")
            print(res_data["msg"])
            logger.error("数据更新失败(线程中) --cypher_str:"+temp_dict["cypher_str"])
            # print("执行更新")
'''
