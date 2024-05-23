"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 主函数和所有的flask接口

"""
import logging
from flask import Flask
from flask import jsonify
from flask import request
from config import flask_config
from service.connector import back_end_connector as bnc
from config import process_errors as pe
from config import logging_config
from cypher_util import update_data_util
from service.connector.back_end_connector import back_end_get_data_from_end_end
from service.to_graph.new.k_default.k_transform import KTransform
import sys
import json
import re

from service.to_graph.new.k_default.k_default import KDefault
from service.to_graph.new.k_search.k_search import KSearch
from service.to_graph.update_const import UpdateConst
from static.graph_const import GraphConst

from service.to_graph.select_graph import TGraph, KGraph, Tip
from service.SearchEngineDetails.DetailsProcessing import SearchEngineDetailsProcessing
from service.to_graph import graph_init

# 该导入为测试函数，请勿删除！
import requests

log = logging.getLogger('werkzeug')
# log.disabled = True    #禁止werkzeug///requeys的日志记录
log.setLevel("WARNING")

sys.path.append(r"../")  # 返回上级目录

app = Flask(__name__)

app.config.from_object(flask_config.ProductionConfig)  # flask的配置文件
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 设置请求大小限制为16MB

logger = logging_config.logging_self_define().log(level='INFO', name="app.py")


# app.logger.addHandler(flask_config.ProductionConfig.LOGGER.hasHandlers())
# app.logger.setLevel(flask_config.ProductionConfig.LOGGER.level)


# logging.debug(pe.ProcessInfos.POST_SUCCEED)
# (知识图谱查询 + 搜索引擎详情页面数据查询)接口
@app.post("/kjxmzstp/knowledgeGraph/kquery")
def kquery():
    # 实例化图的类
    graph = KGraph()
    headers = request.headers
    logger.info("kquery接口访问  headers: --{}".format(headers))

    try:
        raw_input_byte = request.get_data()
        raw_input = json.loads(raw_input_byte)
        logger.info("获取的到的参数get_data()是: --{}".format(raw_input))
    except Exception as E:
        logger.error("获取参数请求失败 get_data() --{}".format(str(E)))
        try:
            raw_input = request.get_json(silent=True)
            # request.get_data()
            logger.info("获取的到的参数get_json()是: --{}".format(raw_input))
        except Exception as e:
            logger.error("获取参数请求失败 get_json() --{}".format(str(e)))
            try:
                raw_input = request.args.to_dict()
                logger.info("获取得到的参数args.to_dict()是:  __{}".format(raw_input))
            except Exception as ee:
                logger.error("获取参数请求失败 get_json() --{}".format(str(ee)))
                res_failed = {}
                res_failed["code"] = pe.ProcessInfos.GET_FAILED.status_code
                res_failed["msg"] = pe.ProcessInfos.GET_FAILED.message
                res_failed["data"] = {}
                del graph
                return res_failed

    # 传入输入的值
    graph.input(raw_input)

    # data:dict=None
    # ifSuccess:bool=None
    if graph.is_default():
        # 知识图谱默认搜索
        # 0523:调康哥的接口
        data, ifSuccess = graph.query_graph_init()
    else:
        # 知识图谱搜索
        data, ifSuccess = graph.expand_query_graph_filtered_search()

    # 获取输出值
    # outputs = graph.output()
    res = {}

    # processed_data=rfekg.second_phase_search_engine_deatil.data_process(data)

    if ifSuccess:
        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        k_transform = KTransform(data)
        finalData, ifFinalSuccess = k_transform.process()
        if not ifFinalSuccess:
            res["code"] = pe.ProcessInfos.GET_FAILED.status_code
            res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = finalData
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = data

    del graph
    # 返回输出结果
    return jsonify(res)


@app.post("/kjxmzstp/searchEngine/tqueryDetails")
def tqueryDetail():
    # 实例化图的类
    graph = KSearch()
    headers = request.headers
    logger.info("kquery接口访问  headers: --{}".format(headers))

    try:
        raw_input_byte = request.get_data()
        raw_input = json.loads(raw_input_byte)
        logger.info("获取的到的参数get_data()是: --{}".format(raw_input))
    except Exception as E:
        logger.error("获取参数请求失败 get_data() --{}".format(str(E)))
        try:
            raw_input = request.get_json(silent=True)
            # request.get_data()
            logger.info("获取的到的参数get_json()是: --{}".format(raw_input))
        except Exception as e:
            logger.error("获取参数请求失败 get_json() --{}".format(str(e)))
            try:
                raw_input = request.args.to_dict()
                logger.info("获取得到的参数args.to_dict()是:  __{}".format(raw_input))
            except Exception as ee:
                logger.error("获取参数请求失败 get_json() --{}".format(str(ee)))
                res_failed = {}
                res_failed["code"] = pe.ProcessInfos.GET_FAILED.status_code
                res_failed["msg"] = pe.ProcessInfos.GET_FAILED.message
                res_failed["data"] = {}
                del graph
                return res_failed

    # 传入输入的值
    graph.input(raw_input)

    # data:dict=None
    # ifSuccess:bool=None
    if graph.is_default():
        # 知识图谱默认搜索
        data, ifSuccess = graph.query_graph_init()
    else:
        # 知识图谱搜索
        data, ifSuccess = graph.expand_query_graph_filtered_search()

    res = {}

    # processed_data=rfekg.second_phase_search_engine_deatil.data_process(data)
    processed_data = data

    if ifSuccess:
        if len(processed_data['first_res']) == 0:
            res["code"] = pe.ProcessInfos.GET_FAILED.status_code
            res["msg"] = pe.ProcessInfos.GET_FAILED.message
            res["data"] = processed_data
            return jsonify(res)
        processed_data_example = SearchEngineDetailsProcessing(**processed_data)
        processed_data = processed_data_example.DetailsProcessing()  # 返回详情页面数据

        # 0403:
        # 额外处理

        # 绿色需要跳转页面的属性
        target_key_list = [
            "完成单位",
            "起草单位",
            "主要完成人",
            "其他完成人",
            "所属团队",
            "所属实验室",
            "发明/设计人",
            "作者姓名",
            "主要作者",
            "著作权人",
            "起草人"
        ]

        if 'achieveBaseInformation' in processed_data.keys():
            for i, x in enumerate(processed_data['achieveBaseInformation']):
                if x['chinese'] in target_key_list:
                    new_value_str = ""
                    new_value_index = None

                    for j, y in enumerate(x['value']):
                        if isinstance(y, str):
                            new_value_str = y
                            new_value_index = j

                        # 主要完成人的特殊情况 无str
                        elif isinstance(y, dict) and y['gid'] == "":
                            new_value_str = y['name']
                            new_value_index = j

                    for j, y in enumerate(x['value']):
                        if isinstance(y, dict) and y['gid'] != "":
                            new_value_str = new_value_str.replace(y['name'], "")
                            domain_str = y['domain']

                    if new_value_index != None:
                        new_value_list = new_value_str.strip(",").split(",")
                        new_value_str = ",".join(new_value_list)

                        new_value_obj = {'domain': domain_str, 'gid': "", 'name': new_value_str}
                        processed_data['achieveBaseInformation'][i]['value'][new_value_index] = new_value_obj

        if 'intellectualBasicInformation' in processed_data.keys():
            for i, x in enumerate(processed_data['intellectualBasicInformation']):
                if x['chinese'] in target_key_list:
                    new_value_str = ""
                    new_value_index = None

                    for j, y in enumerate(x['value']):
                        if isinstance(y, str):
                            new_value_str = y
                            new_value_index = j

                        # 主要完成人的特殊情况 无str
                        elif isinstance(y, dict) and y['gid'] == "":
                            new_value_str = y['name']
                            new_value_index = j

                    domain_str = ""
                    for j, y in enumerate(x['value']):
                        if isinstance(y, dict) and y['gid'] != "":
                            new_value_str = new_value_str.replace(y['name'], "")
                            domain_str = y['domain']

                    if new_value_index != None:
                        new_value_list = new_value_str.strip(",").split(",")
                        new_value_str = ",".join(new_value_list)

                    if domain_str:
                        new_value_obj = {'domain': domain_str, 'gid': "", 'name': new_value_str}
                        processed_data['intellectualBasicInformation'][i]['value'][new_value_index] = new_value_obj

        # 0509:

        if 'achieveBaseInformation' in processed_data.keys():
            if processed_data['achieveBaseInformation'][0]['value'] == []:
                for i, obj in enumerate(processed_data['achieveBaseInformation']):
                    if obj['chinese'] == 'value':
                        processed_data['achieveBaseInformation'][i]['value'] = [data['label']]
                        break

        if 'achieveBaseInformation' in processed_data.keys():
            if data['first_res'][0]['domain'] == 'entity_achievement_sbj':
                for i, obj in enumerate(processed_data['achieveBaseInformation']):
                    if obj['chinese'] == '其他完成人':
                        processed_data['achieveBaseInformation'].pop(i)
                        break

        if 'intellectualAnnex' in processed_data.keys() and processed_data['intellectualAnnex'] == "" and len(data['first_res']) > 0 and 'entity_technical_standard_annex' in data['first_res'][0].keys():
            processed_data['intellectualAnnex'] = data['first_res'][0]['entity_technical_standard_annex']
        elif 'intellectualAnnex' in processed_data.keys() and processed_data['intellectualAnnex'] == "" and len(data['first_res']) > 0 and 'zscqzl_achievement_annex' in data['first_res'][0].keys():
            processed_data['intellectualAnnex'] = data['first_res'][0]['zscqzl_achievement_annex']
        elif 'intellectualAnnex' in processed_data.keys() and processed_data['intellectualAnnex'] == "" and len(data['first_res']) > 0 and 'zscqlw_achievement_annex' in data['first_res'][0].keys():
            processed_data['intellectualAnnex'] = data['first_res'][0]['zscqlw_achievement_annex']
        elif 'intellectualAnnex' in processed_data.keys() and processed_data['intellectualAnnex'] == "" and len(data['first_res']) > 0 and 'zscqzz_achievement_annex' in data['first_res'][0].keys():
            processed_data['intellectualAnnex'] = data['first_res'][0]['zscqzz_achievement_annex']

        elif 'intellectualAnnex' in processed_data.keys() and processed_data['intellectualAnnex'] == "" and len(data['first_res']) > 0 and 'entity_process_standard_annex' in data['first_res'][0].keys():
            processed_data['intellectualAnnex'] = data['first_res'][0]['entity_process_standard_annex']

        elif 'projectAnnex' in processed_data.keys() and processed_data['projectAnnex'] == "" and len(data['first_res']) > 0 and 'entity_project_scjj_annex' in data['first_res'][0].keys():
            processed_data['projectAnnex'] = data['first_res'][0]['entity_project_scjj_annex']



        # 0511:
        if 'intellectualBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['intellectualBasicInformation']):
                if obj['chinese'] == '授权号':
                    value_list = [m['name'] for m in processed_data['intellectualBasicInformation'][i]['value']]
                    if len(value_list) > 0:
                        processed_data['intellectualBasicInformation'][i]['value'] = value_list[0]
                        break

        if 'intellectualBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['intellectualBasicInformation']):
                if obj['chinese'] == '授权公告日':
                    value_list = [m['name'] for m in processed_data['intellectualBasicInformation'][i]['value']]
                    if len(value_list) > 0:
                        processed_data['intellectualBasicInformation'][i]['value'] = value_list[0]
                        break

        if 'intellectualBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['intellectualBasicInformation']):
                if obj['chinese'] == '专利权人':
                    value_list = [m for m in processed_data['intellectualBasicInformation'][i]['value']]
                    for l, iter_value in enumerate(value_list):
                        cur_value = iter_value['name'] if isinstance(iter_value, dict) else iter_value
                        for k in range(l+1, len(value_list)):
                            other_value = value_list[k]['name'] if isinstance(value_list[k], dict) else value_list[k]
                            if cur_value == other_value:
                                value_list.pop(l)
                                break
                    processed_data['intellectualBasicInformation'][i]['value'] = value_list
                    break

        if 'intellectualBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['intellectualBasicInformation']):
                if obj['chinese'] == '著作权人':
                    new_value_list = []
                    for m in obj['value']:
                        if isinstance(m, str):
                            new_value_list.extend(m.split(","))
                        elif isinstance(m, dict) and 'name' in m.keys():
                            new_value_list.append(m['name'])
                    processed_data['intellectualBasicInformation'][i]['value'] = new_value_list



        if 'intellectualBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['intellectualBasicInformation']):
                for j, unit in enumerate(processed_data['intellectualBasicInformation'][i]['value']):
                    if isinstance(unit, dict) and "," in unit['name']:
                        processed_data['intellectualBasicInformation'][i]['value'][j]['name'] = processed_data['intellectualBasicInformation'][i]['value'][j]['name'].replace(",", " ")
                    elif isinstance(unit, str) and "," in unit:
                        processed_data['intellectualBasicInformation'][i]['value'][j] = processed_data['intellectualBasicInformation'][i]['value'][j].replace(",", " ")

        if 'projectBasicInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['projectBasicInformation']):
                for j, unit in enumerate(processed_data['projectBasicInformation'][i]['value']):
                    if isinstance(unit, dict) and "," in unit['name']:
                        processed_data['projectBasicInformation'][i]['value'][j]['name'] = processed_data['projectBasicInformation'][i]['value'][j]['name'].replace(",", " ")
                    elif isinstance(unit, str) and "," in unit:
                        processed_data['projectBasicInformation'][i]['value'][j] = processed_data['projectBasicInformation'][i]['value'][j].replace(",", " ")

        if 'achieveBaseInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['achieveBaseInformation']):
                for j, unit in enumerate(processed_data['achieveBaseInformation'][i]['value']):
                    if isinstance(unit, dict) and "," in unit['name']:
                        processed_data['achieveBaseInformation'][i]['value'][j]['name'] = processed_data['achieveBaseInformation'][i]['value'][j]['name'].replace(",", " ")
                    elif isinstance(unit, str) and "," in unit:
                        processed_data['achieveBaseInformation'][i]['value'][j] = processed_data['achieveBaseInformation'][i]['value'][j].replace(",", " ")

        if 'achieveBaseInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['achieveBaseInformation']):
                if obj['chinese'] == '完成单位':
                    index = None
                    target_list = []
                    for p, m in enumerate(obj['value']):
                        if m['gid'] != "":
                            target_list.append(m)
                        else:
                            index = p
                    if index != None:
                        processed_data['achieveBaseInformation'][i]['value'] = target_list

        if 'achievementSynopsis' in processed_data.keys() and processed_data['achievementSynopsis'] == "" and len(data['first_res']) > 0 and 'zl_achievement_recommendations' in data['first_res'][0].keys():
            processed_data['achievementSynopsis'] = data['first_res'][0]['zl_achievement_recommendations']
        # elif 'achievementSynopsis' in processed_data.keys() and processed_data['achievementSynopsis'] == "" and len(data['first_res']) > 0 and 'zl_achievement_recommendations' in data['first_res'][0].keys():
        #     processed_data['achievementSynopsis'] = data['first_res'][0]['zl_achievement_recommendations']

        if 'achieveBaseInformation' in processed_data.keys():
            for i, obj in enumerate(processed_data['achieveBaseInformation']):
                if obj['chinese'] == '起草单位':
                    new_list = []
                    for j, u in enumerate(processed_data['achieveBaseInformation'][i]['value']):
                        if u['name'] != '国网浙江省电力有限公司':
                            new_list.append(u)
                    processed_data['achieveBaseInformation'][i]['value'] = new_list

        # 0517:
        if data['label'] == '技术标准' and len(data['first_res']) > 0 and 'entity_technical_standard_significance' in data['first_res'][0].keys():
            processed_data['technicalSynopsis'] = data['first_res'][0]['entity_technical_standard_significance']


        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = processed_data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = processed_data

    del graph
    # 返回输出结果
    return jsonify(res)


# 搜索引擎查询接口
@app.post("/kjxmzstp/searchEngine/tquery")
def tquery():
    # print("user_ip:", user_str) -->获得客户端ip地址
    # 实例化图的类

    headers = request.headers
    # json_modul=request.json_module

    logger.info("tquery接口访问 headers: --{}".format(headers))
    # logger.info("tquery接口访问 json_modul: --{}".format(json_modul))

    graph = TGraph()

    # logger.info("用户ip:%s--正在执行搜索引擎请求操作"%(user_ip))

    #
    # # 前端数据位置
    # input_dir = "data/front_end_data/tquery_4.json"
    # # 读取json数据
    # with open(input_dir, "r", encoding="utf-8") as f:
    #     raw_input = json.load(f)
    try:
        raw_input_byte = request.get_data()
        raw_input = json.loads(raw_input_byte)
        logger.info("获取的到的参数get_data()是: --{}".format(raw_input))
    except Exception as E:
        logger.error("获取参数请求失败 get_data() --{}".format(str(E)))
        try:
            raw_input = request.get_json(silent=True)
            # request.get_data()
            logger.info("获取的到的参数get_json()是: --{}".format(raw_input))
        except Exception as e:
            logger.error("获取参数请求失败 get_json() --{}".format(str(e)))
            try:
                raw_input = request.args.to_dict()
                logger.info("获取得到的参数args.to_dict()是:  __{}".format(raw_input))
            except Exception as ee:
                logger.error("获取参数请求失败 get_json() --{}".format(str(ee)))
                res_failed = {}
                res_failed["code"] = pe.ProcessInfos.GET_FAILED.status_code
                res_failed["msg"] = pe.ProcessInfos.GET_FAILED.message
                res_failed["data"] = {}
                del graph
                return res_failed

    # 前处理 正则化匹配
    graph.input(raw_input)
    # print(current_app._get_current_object())

    # 搜索引擎搜索
    data, ifSuccess = graph.expand_query_tradition_filtered_search()

    # 0509: 论文时间（刊期）修复
    for m, obj in enumerate(data['res']):
        if obj['domain'] == 'entity_intellectual_property_paper':
            new_time = back_end_get_data_from_end_end.new_query_paper_time_service(name=data['res'][m]['name'], node_type=data['res'][m]['domain'])
            new_time = [x for x in new_time]
            new_time = new_time[0] if len(new_time) > 0 else ""
            if new_time:
                data['res'][m]['time'] = str(new_time)

    # 0515:
    for j, item in enumerate(data['res']):
        if item['company'] == "":
            new_raw_input = {
                "id": "",
                "gid": "",
                "label": "{}".format(item['type']),
                "property": "name",
                "text": "{}".format(item['name']),
                "first_res": "",
                "second_res": ""
            }
            new_graph = KSearch()
            new_graph.input(new_raw_input)
            new_data, ifSuccess = new_graph.expand_query_graph_filtered_search()

            new_company_list = []
            if len(new_data['second_res']) > 0:
                for single_node in new_data['second_res'][0]['nodes']:
                    if single_node['domain'] == 'entity_unit':
                        new_company_list.append(single_node['name'])
            data['res'][j]['company'] = ",".join(new_company_list)

    # 0517:

    # try:
    #     for p, company in enumerate(data['companies']):
    #         new_match = re.match(r'^(.*?)\s*（(.*)）', company)
    #         if new_match:
    #             f_company = new_match.group(1)
    #             f_num = int(new_match.group(2))
    #
    #             for q, other_company in enumerate(data['companies']):
    #                 new_match = re.match(r'^(.*?)\s*（(.*)）', other_company)
    #                 if new_match:
    #                     other_f_company = new_match.group(1)
    #                     other_f_num = int(new_match.group(2))
    #
    #                     if p != q and f_company in other_f_company:
    #                         f_num += other_f_num
    #
    #             data['companies'][p] = f_company + "（" + str(f_num) + "）"
    #
    # except Exception:
    #     pass


    res = {}
    if ifSuccess:
        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = data

    del graph

    logger.info("输出: {}".format(data))

    return jsonify(res)

    # [TEST]
    # test_func(graph.text, graph.times, graph.types, graph.themes, graph.companies, graph.graph_const.get_times_properties(), graph.graph_const.get_types_map(), graph.graph_const.get_themes_properties(), graph.graph_const.get_companies_properties(), graph.graph_const.get_experts_properties())
    # test_func(graph.text, [], graph.types, [], [], graph.graph_const.get_times_properties(), graph.graph_const.get_types_map(), graph.graph_const.get_themes_properties(), graph.graph_const.get_companies_properties(), graph.graph_const.get_experts_properties())

    # 获取输出值
    # outputs = graph.output()


# 搜索引擎主页热词获取接口
@app.get("/kjxmzstp/searchEngine/buzzwords")
def buzzwords():
    # print(graph_const.GraphConst.types_map["项目"])
    # 实例化提示的类
    headers = request.headers
    logger.info("buzzwords接口访问  --{}".format(headers))

    class_tip = Tip("", "", [])

    # 获取搜索引擎主页的热词
    data, ifSuccess = class_tip.acquire_buzzwords()
    res = {}
    if ifSuccess:
        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = data

    del class_tip
    return jsonify(res)


# 搜索引擎搜索框的提示获取接口
@app.post("/kjxmzstp/searchEngine/tips")
def tips():
    '''
    {
         "id": "",
          "tip": "电力",
          "res": []
    }
    :return: json
    '''

    # headers = request.headers
    # logger.info("tips接口访问 headers: --{}".format(headers))

    try:
        raw_input_byte = request.get_data()
        # print(raw_input_byte)
        raw_input = json.loads(raw_input_byte)
        logger.info("获取的到的参数get_data()是: --{}".format(raw_input))
    except Exception as E:
        logger.error("获取参数请求失败 get_data() --{}".format(str(E)))
        try:
            raw_input = request.get_json(silent=True)
            # request.get_data()
            logger.info("获取的到的参数get_json()是: --{}".format(raw_input))
        except Exception as e:
            logger.error("获取参数请求失败 get_json() --{}".format(str(e)))
            try:
                raw_input = request.args.to_dict()
                logger.info("获取得到的参数args.to_dict()是:  __{}".format(raw_input))
            except Exception as ee:
                logger.error("获取参数请求失败 get_json() --{}".format(str(ee)))
                res_failed = {}
                res_failed["code"] = pe.ProcessInfos.GET_FAILED.status_code
                res_failed["msg"] = pe.ProcessInfos.GET_FAILED.message
                res_failed["data"] = {}

                return res_failed

    front_end_json = raw_input

    # 获取json 传值 如果没有传入相关字段 那么就传入
    front_end_json_tip = front_end_json.get("tip", "")
    front_end_json_id = front_end_json.get("id", "")
    front_end_json_res = front_end_json.get("res", [])
    # 实例化提示的类
    class_tip = Tip(id=front_end_json_id, tip=front_end_json_tip, res=front_end_json_res)

    # 前端数据位置
    # input_dir = "data/front_end_data/tips_0.json"
    # 读取json数据
    # with open(input_dir, "r", encoding="utf-8") as f:
    #     raw_input = json.load(f)

    # 获取搜索的提示词
    data, ifSuccess = class_tip.acquire_tips()
    res = {}
    if ifSuccess:
        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = {}

    # del: 释放示例的内存
    del class_tip
    return jsonify(res)


@app.get("/kjxmzstp/searchEngine/downwardCount")
def count():
    # 实例化提示的类
    class_tip = Tip("", "", "")

    # 获取搜索引擎主页的热词
    # class_tip.acquire_count()

    # 获取输出值
    # outputs = class_tip.output()
    ifSuccess, data = class_tip.acquire_count()

    res = {}
    if ifSuccess:
        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = data

    del class_tip

    return jsonify(res)


@app.get("/kjxmzstp/const/getConst")
def get_const():
    res = {}
    data = GraphConst().show()
    res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
    res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
    res["data"] = data
    return jsonify(res)


# LLH: 新增接口
# 知识图谱默认显示
@app.get("/kjxmzstp/knowledgeGraph/kDefault")
def k_default():
    # LLH: input修改为json输入的参数

    # try:
    #     # relationData_json=requests.get(KDefault.url)
    #     relationData_json=requests.get("http://127.0.0.1:28081/kjxmzstp/yyyyy")
    #     logger.info("成功接收到康哥的数据 relationData_json {}".format(str(relationData_json)))
    # except Exception as e:
    #     logger.error("报错信息 --{}".format(str(e)))
    #     logger.error("请求康哥的接口失败  接口名:http://172.30.86.10:11623/kjxmprocess/kexportknowledgemapping/getAllRelationValue")
    #     res["code"] = pe.ProcessInfos.GET_FAILED.status_code
    #     res["msg"] = pe.ProcessInfos.GET_FAILED.message
    #     res["data"] = []
    #     return res

    # json_data = relationData_json.content.decode('utf-8')
    # relationData = json.loads(json_data)
    #
    # try:
    #     json_data = relationData_json.content.decode('utf-8')  #编译为json 转换成dict
    #     logger.info("json content :{}".format(json_data))
    #     logger.info("编译为str对象成功")
    #     # print(relationData_json.content.decode())
    #     # logger.info(relationData_json.content.decode())
    #     logger.info("编译结果返回 decode:{}".format(json_data))
    #     relationData = eval(json_data)  #转换成字典
    #     # relationData = json_data  # 转换成字典
    #     logger.info("str转换成字典成功")
    #     logger.info("最终的字典数据 dict:{}".format(relationData))
    # except json.JSONDecodeError as ee :
    #     logger.error("报错信息 --{}".format(str(ee)))
    #     logger.error(
    #         "接口数据处理失败  json_data:{}".format(json_data))
    #     res["code"] = pe.ProcessInfos.GET_FAILED.status_code
    #     res["msg"] = pe.ProcessInfos.GET_FAILED.message
    #     res["data"] = []
    #     return res

    res = {}
    k_default = KDefault()

    checkIfSuccess, input = k_default.query()

    if not checkIfSuccess:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = []

    k_default.get_input(input)

    data, ifSuccess = k_default.process()

    if ifSuccess:

        res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
        res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
        res["data"] = data
    else:
        res["code"] = pe.ProcessInfos.GET_FAILED.status_code
        res["msg"] = pe.ProcessInfos.GET_FAILED.message
        res["data"] = data

    del k_default
    return jsonify(res)


# LLH: 需增加postman页面数据，数据类似input
@app.post("/kjxmzstp/const/setConst")
def set_const():
    # LLH: input修改为json输入的参数
    input = {
        "key": "times_properties",
        "value": {
            "entity_project_kj": "time",
            "entity_technical_standard": "declare_year"
        }
    }

    graph_const = GraphConst()

    graph_const[input["key"]] = input["value"]

    res = {}
    res["code"] = pe.ProcessInfos.GET_SUCCEED.status_code
    res["msg"] = pe.ProcessInfos.GET_SUCCEED.message
    # res["data"] = data
    return res


# 图重构接口(更新热词节点的参数)
@app.get("/kjxmzstp/graphDatabaseNeo4j/reconstruct")
def reconstruct():
    # print("图数据库重构")
    # 实例化图的类
    headers = request.headers
    # logger.info("reconstruct 接口访问 headers: --{}".format(headers))

    graph = TGraph()

    # 更新热词节点
    ifSuccess = graph.update_entity_buzzwords_to_graph()
    if ifSuccess:
        logger.info("更新热词节点成功")
    else:
        logger.error("更新热词结点失败")

    finalIfSuccess = True
    try:
        # 创建常量类的调整类
        update_const = UpdateConst()
        # 更新常量类的搜索用的字段名
        update_const.update()

        try:
            graph = TGraph()
            ifCompleteSuccess = graph.complete()
            if not ifCompleteSuccess:
                logger.error("graph.complete() 内部执行错误 ")
                res = {"code": pe.ProcessInfos.UPDATE_FAILED.status_code, "msg": pe.ProcessInfos.UPDATE_FAILED.message,
                       "data": []}
                return res

        except Exception as ee:
            logger.error("complete 执行失败 --error:{}".format(ee))
            finalIfSuccess = False

    except Exception as e:
        logger.error("常量类的搜索用的字段名失败 --error:{}".format(e))
        finalIfSuccess = False
    if finalIfSuccess:
        logger.info("complete 和 常量类搜索的字段名成功")

    if ifSuccess and finalIfSuccess:
        res = {"code": pe.ProcessInfos.UPDATE_SUCCEED.status_code,
               "msg": pe.ProcessInfos.UPDATE_SUCCEED.message, "data": []}
    else:
        res = {"code": pe.ProcessInfos.UPDATE_FAILED.status_code, "msg": pe.ProcessInfos.UPDATE_FAILED.message,
               "data": []}

    del graph
    return jsonify(res)


# 初始化接口(关键词自生成、初始化搜索次数、创建热词节点、统一时间字段值的类型为字符串)
@app.get("/kjxmzstp/graphDatabaseNeo4j/init")
def init():
    # logger.info("数据库连接的旧的driver实例地址 --{}".format(id(bnc.back_end_get_data_from_end_end.driver)))
    # 断开数据库重新连接 目的是获取最新数据

    bnc.back_end_get_data_from_end_end.driver.close()
    del bnc.back_end_get_data_from_end_end.driver
    # del bnc.back_end_get_data_from_end_end.session

    bnc.back_end_get_data_from_end_end.driver = graph_init.ConnectToDatabase.init()
    # bnc.back_end_get_data_from_end_end.session=bnc.back_end_get_data_from_end_end.driver.session()

    logger.info("数据库连接的新的driver实例地址 --{}".format(id(bnc.back_end_get_data_from_end_end.driver)))

    logger.info("重新连接数据库成功")
    # 实例化图的类
    graph = TGraph()

    # graph.init_create_nodes()

    headers = request.headers
    logger.info("init接口访问 headers: --{}".format(headers))

    failed_dict_return = {
        "code": pe.ProcessInfos.UPDATE_FAILED.status_code,
        "msg": pe.ProcessInfos.UPDATE_FAILED.message,
        "data": []}
    failed_Json_return = jsonify(failed_dict_return)

    # 为所需的图节点添加主题相关的字段及对应的值
    ifSuccess = graph.add_theme_to_graph()
    str1 = "图节点添加主题相关的字段及对应的值:{}"
    if not ifSuccess:
        # print(str1.format("失败"))
        logger.info(str1.format("失败"))
        return failed_Json_return

    # print(str1.format("成功"))
    logger.info(str1.format("成功"))

    # 为所需的图节点添加搜索次数字段
    ifSuccess = graph.add_search_number_to_graph()
    str2 = "图节点添加搜索次数字段:{}"
    if not ifSuccess:
        # print(str2.format("失败"))
        logger.info(str2.format("失败"))
        return failed_Json_return

    # print(str2.format("成功"))
    logger.info(str2.format("成功"))

    # 创建热词节点
    ifSuccess = graph.create_entity_buzzwords_to_graph()
    str3 = "创建热词结点:{}"
    if not ifSuccess:
        # print(str3.format("失败"))
        logger.info(str3.format("失败"))
        return failed_Json_return

    # print(str3.format("成功"))
    logger.info(str3.format("成功"))

    # 强制统一节点的时间字段值得类型为字符串
    ifSuccess = graph.set_time_properties_to_string()
    str4 = "强制统一结点的时间字段值类型为字符串:{}"
    if not ifSuccess:
        # print(str4.format("失败"))
        logger.info(str4.format("失败"))
        return failed_Json_return

    # print(str4.format("成功"))
    logger.info(str4.format("成功"))

    localhost_ip = flask_config.Config.HOST_IP
    url = "http://%s:%d/kjxmzstp/graphDatabaseNeo4j/reconstruct" % (localhost_ip, flask_config.Config.PORT)
    # print(url)
    res = requests.get(url=url).json()

    return res


@app.post("/kjxmzstp/graphDatabaseNeo4j/cypher_back_end")
def cypher_back_end():
    # print("it is cypher back end")

    res: dict = request.get_json()

    # logger.info("访问后端接口传入cypher语句  --{}".format(res))
    # print(res)
    back_end_processing = bnc.back_end_get_data_from_end_end(**res)  # 字典解包
    back_end_data = back_end_processing.back_end_data_return()
    return jsonify(back_end_data)

    # return_cypher_result = {"code": 200, "data": [{"1": "hahah"}, {"2": "hahah"}], "msg": ""}
    # return jsonify(return_cypher_result)


@app.get("/kjxmzstp/checkHealth")
def check_health():
    # print("app running")
    logger.info("app running")
    return "app running"


@app.post("/kjxmzstp/dataUpdate")
def dataUpdate():
    res = request.get_json()
    # print(res)
    res_data = res["res"]

    backend_ip = res["backend_ip"]
    backend_port = res["backend_port"]

    for x in res_data:
        # print(x)
        # res_data = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
        #     update_search_number_cypher_str(x["gid"]),
        #     pe.Status_codes.cypher_update)
        cypher_str = update_data_util.update_search_number_cypher_str(x["gid"])
        code = pe.Status_codes.cypher_update
        backend_res_data = bnc.back_end_cypher_search_and_theme_return.cypher_search_Project_Description(
            cypher_str=cypher_str, code=code
        )

        # url = "http://%s:%d/kjxmzstp/graphDatabaseNeo4j/cypher_back_end" % (backend_ip,backend_port)
        # print(url)

        # back_end_processing = bnc.back_end_get_data_from_end_end(**temp_dict) # 字典解包
        # back_end_data = back_end_processing.back_end_data_return()

        # back_end_data:requests.models.Response = requests.post(url, json=temp_dict)

        # print(type(back_end_data))
        # back_end_data=back_end_data.json()
        # print(back_end_data)
        # print(type(back_end_data))
        # json_data = res_return.json()
        # backend_res_data = json.loads(back_end_data)
        # print(back_end_data)
        # back_end_processing=bnc.back_end_get_data_from_end_end(**res)  #字典解包
        # backend_res_data=back_end_processing.back_end_data_return()
        if backend_res_data["code"] != pe.ProcessInfos.UPDATE_SUCCEED.status_code:
            pass
            # TODO:记录日志 表示更新错误
            # print("记录日志")
            # print(backend_res_data["msg"])
            # logger.error("数据更新失败 tquery中 --cypher_str:"+temp_dict["cypher_str"])

    logger.info("tquery 异步更新数据成功 ")
    # print("异步更新数据结束")
    return "success"


# 主程序
if __name__ == "__main__":
    # print(app.config)
    # print(app.config['PORT'])
    # print(app.config["HOST"])
    # print(app.app_context())

    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config['DEBUG'])
    # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=True)
