# -*- encoding:utf-8 -*-
"""

    @Author: 张赞
    @Updater_1: 李凌浩
    @LatestUpdateTime: 2023/10/4
    @Introduction: 模块测试文件

"""



import logging
import os
import sys
# from service.connector import  return_front_end_knowledge_graph as rfekg
import pandas

from config import process_errors as ProcessError
from config import flask_config
from config import logging_config

from flask import Flask
from flask import jsonify
from flask import request
from config import flask_config
from config import process_errors
import requests
import sys
import json
from service.to_graph import  select_graph as sg

from service.to_graph.select_graph import TGraph
from config import logging_config
import threading
import os

sys.path.append(r"../")  # 返回上级目录


def statues_code_checking():
    status_code_class = ProcessError.Status_codes  # 直接调用类 而不是创建对象
    status_message_class = ProcessError.Status_messages
    print(status_code_class.SAVE_OK)
    save_statue = ProcessError.ProcessInfo(status_code=status_code_class.SAVE_OK, message=status_message_class.SAVE_OK)
    print(save_statue.message)

    print(ProcessError.ProcessInfos.POST_SUCCEED)


def config_checking():
    flask_Config = flask_config.Config
    print(flask_Config.APP_ID)
    print(os.environ.keys())
    print(os.environ.get("path"))


def logging_self_define():
    logging_define = logging_config.logging_self_define()
    # logging_define.make_log_dir()
    # filename_path=logging_define.get_log_filename()
    logger = logging_define.log(level="WARNING" ,name="module_testing")
    logger.debug("1111111111111111111111")  # 使用日志器生成日志
    logger.info("222222222222222222222222")
    logger.error("000000000000000000000000")
    logger.warning("3333333333333333333333333333")
    logger.critical("44444444444444444444444444")


# 测试搜索引擎函数
def query_tradition_filtered_search(
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
                            if "2021年以前" in time:
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
    a = 1

    # 输出查询结果
    return [x for x in res]


# if __name__ == "__main__":
#     print("--调用模块测试文件--")
#     # statues_code_checking()
#     # config_checking()
#     # logging_self_define()
#
#     # 实例化图的类
#     graph = Graph()
#
#     # TODO [本地json测试]
#     # 前端数据位置
#     input_dir = "../data/front_end_data/query_data_0.json"
#     # 读取json数据
#     with open(input_dir, "r", encoding="utf-8") as f:
#         raw_input = json.load(f)
#
#     # 传入输入的值
#     graph.input(raw_input)
#
#     query_tradition_filtered_search(
#         graph.text,
#         graph.times,
#         graph.types,
#         graph.themes,
#         graph.companies,
#         graph.graph_const.get_times_properties(),
#         graph.graph_const.get_types_map(),
#         graph.graph_const.get_themes_properties(),
#         graph.graph_const.get_companies_properties(),
#         graph.graph_const.get_experts_properties()
#     )
# -*- coding: UTF-8 -*-
import time


async def get_data_from_db_async(counter):
    data = []
    print("参数counter：", counter)
    for i in range(counter):
        time.sleep(1)
        data.append(i)
    return data
'''async关键字创建的异步函数，就是协程。异步函数的返回值并不是该函数的执行结果，而是一个协程对象，协程对象调用send方法才会触发异步函数的执行。'''
from multiprocessing import Process
def get_data_from_db_threading(): #多线程测试
    data = []
    counter=5
    print("参数counter：", counter)
    for i in range(counter):
        time.sleep(0.5)
        data.append(i)
    print(data)

def father_func_asyns():
    coroutine_obj = get_data_from_db_async(5)
    print("异步函数返回值：", coroutine_obj)

    try:
        coroutine_obj.send(None)  #触发异步函数
    except Exception as e:
        print(e)
    print("jump   coroutine_obj ")  #异步的使用不能 先执行此句 还是等待异步函数执行完毕
    return "father func stop"

def father_func_threading():
    threadTest=threading.Thread(target=get_data_from_db_threading, name="新线程")  # threading.Thread（）创建了一个线程实例
    threadTest.start()
    print("jump threadTest ")  #异步的使用不能 先执行此句 还是等待异步函数执行完毕

    return "father func stop"



#
# def father_func_process(): #多进程测试
#     # threadTest=Process(target=get_data_from_db_threading(5), args=("主进程参数"))  # threading.Thread（）创建了一个线程实例
#     # threadTest.start()
#     process = Process(target=new_process, args=("主进程参数",1,2,3))
#     process.start()  # 启动进程
#
#     print("jump threadTest ")  #异步的使用不能 先执行此句 还是等待异步函数执行完毕
#     return "father func stop"

def new_process(para,a,b,c):
    time.sleep(1)
    print(para,a,b,c,type(para))
    print("子进程ID：{0}".format(os.getpid()))
    print("主进程传递来的参数：{0}".format(para))
from pandas import DataFrame
from pandas import Series
from pandas import read_excel as re

def kquery_return_process():
    # 1 是 2 不是
    # contrast_dict={"属性编码":"propertyCode","属性名称":"propertyName","属性类别":"propertyType","是否做为关键属性":"keyProperty","是否图谱展示":"showOrNot"}

    return_dir = "../data/back_end_data/kquery_res_json.json"
    target_dict={
                        "domain": "entity_achievement_sgs_kxkj",
                        "gid": 613,
                        "id": "63",
                        "keywords": [
                            "其他"
                        ],
                        "kjjb_achievement_Authorized": "2",
                        "kjjb_achievement_IPR": "3",
                        "kjjb_achievement_classificationcode": "5306-高电压带电作业技术720000-电工材料及其制品5201-输电综合",
                        "kjjb_achievement_endtime": "2019-09-30",
                        "kjjb_achievement_grouping": "电网二组",
                        "kjjb_achievement_name_english": "KeytechnologyandequipmentdevelopmentofintelligentprotectionforliveworkingonEHV/UHVtransmissionlines",
                        "kjjb_achievement_planname": "国网浙江省电力公司科技项目",
                        "kjjb_achievement_plannumber": "5211JH16000D",
                        "kjjb_achievement_projectnameableornot": "可",
                        "kjjb_achievement_recommendations": "我单位认真审阅了该项目推荐书及附件材料，确认全部材料真实有效，相关栏目均符合2021年度公司科学技术奖励推荐工作手册的填写要求。我单位和项目完成单位都已对该项目的拟推荐情况进行了确认，目前无异议。该项目基于带电作业环境下人员穿着屏蔽服后热舒适性差、有效沟通手段匮乏、人员安全监护手段不足等问题，通过自主创新，建立了超/特高压带电作业过程的人体传热学模型，提出了人员热舒适性评估体系，研制了带电作业用降温服装，提升了高温天气下作业人员的舒适度。研制了基于化学镀覆、外场诱导工艺的电磁屏蔽复合材料，实现了宽频域电磁场防护，提高了电子设备在强电磁场下的抗干扰能力。研发了强电磁环境下无线通讯装置和人体关键体征监测装置，提升了带电作业智能防护水平。项目成果已在省内外多家单位开展应用，研制的装置已实现规模化生产，经济效益和社会效益显著。该成果申报中的单位、人员排序和前述技术内容属实，对照《国网浙江省电力公司科学技术奖励办法实施细则》，推荐该项目申报2021年度国网浙江省电力有限公司科学技术进步奖一等奖。",
                        "kjjb_achievement_reference": "国网浙江省电力有限公司金华供电公司",
                        "kjjb_achievement_referencelevel": "一等奖",
                        "kjjb_achievement_rewardcategory": "科技进步奖",
                        "kjjb_achievement_rewardlevel": "二等奖",
                        "kjjb_achievement_source": "D．浙江公司科技项目计划",
                        "kjjb_achievement_specialityplatform": "运检",
                        "kjjb_achievement_starttime": "2012-01-01",
                        "kjjb_achievement_subjectterm": "带电作业；热舒适性；电磁屏蔽；无线通讯；体征监测；安全监护",
                        "kjjb_achievement_synopsis": "本项目属于电气工程、材料工程、通信工程交叉学科，涉及输电带电作业、温控材料、无线传输通讯等领域，是关键技术开发和实际工程应用相结合的综合性研究课题。浙江省经济发达，大量电能依赖外部输送，超/特高压线路是电力传输的骨干网络，其安全稳定运行要求高，停电消缺机会少，且损失大。因此，超/特高压线路一般采用带电方式开展检修消缺。然而，目前国内外对超/特高压线路带电作业防护技术尚缺乏系统研究，存在着人员穿着屏蔽服后热舒适性差、作业人员间沟通手段匮乏、等电位人员安全监护有效手段缺失等问题，导致带电作业过程存在较大的安全风险隐患。为此，国网浙江省电力有限公司金华供电公司联合全球能源互联网研究院有限公司等单位历时七年，产学研用协同攻关，形成了从理论方法、新型屏蔽材料到智能防护装备的系列研究成果，并开展了实际应用，取得以下创新：（1）攻克了带电作业人员人体舒适性评估及提升关键技术。项目建立了超/特高压线路带电作业过程的人体传热学模型，提出了带电作业人员热舒适性评估体系，研制了基于聚乙二醇固-固相变材料的带电作业用降温服装，实现了蓄冷、吸湿、风冷的高效协同，服内温度较服外降低19%以上，持续时间在2小时以上，提升了高温天气下作业人员的舒适度。（2）开发了带电作业用微纳米壳-核结构复合屏蔽材料。项目基于Schelkunoff理论，通过化学镀覆、外场诱导取向工艺，研制了壳-核结构微纳米填料电磁屏蔽复合橡胶材料，实现了屏蔽填料的低比例添加，屏蔽效能大于65dB，提高了电子设备在强电磁场下的抗干扰能力，成本较进口材料降低30%以上。（3）首创强电磁环境下无线通讯装置和人体关键体征监测装置。项目研发了强电磁环境下的音视频无线通讯装置和人体关键体征监测装置，实现了带电作业中作业工况可视化监控和人员语音实时交流及人体状态（血压、心率、体温、血氧、空间三维位置）的监测和智能报警，装置连续工作时长不低于6小时，信号传输距离大于100m，提升了带电作业智能防护水平。项目已获授权发明专利2项、实用新型专利3项，受理发明专利3项，发表学术论文8篇（其中SCI收录2篇，核心期刊4篇），编写电力行业标准1项（送审稿）。成果被浙江省电力学会鉴定为国际领先水平。项目成果于2017年7月起开始实施，已累计在金华超/特高压输电线路带电作业中应用41次，并推广至全省范围。实现了带电作业全年时间段的全覆盖，提高了超/特高压输电线路带电作业人员安全水平，有效保障了电网安全稳定运行。项目成果近三年在产品生产销售、减少线路停电时间、提高清洁能源输送等方面累计创造利润2748.93万元；研发的智能防护装备拥有自主知识产权，并已实现规模化生产和销售，有力促进了浙江制造企业快速发展。",
                        "name": "省公司科学技术进步奖0901001",
                        "search_number": 1
                    }
    with open(return_dir, "r", encoding="utf-8") as f:
        return_data = dict(json.load(f))["data"]["second_res"][0]["nodes"]
    exclude_list=["domain","gid","id","keywords","search_number"]
    node_details={}
    for i in return_data:
        print(i)
        target_dict=i
        entity_type_code = target_dict.get("domain", "")
        each_entity_list=[]

        entity_type_name_chinese=rfekg.second_phase_search_engine_deatil.get_entity_type_chinese_from_dataFrame(entity_type_code)
        gid = target_dict.get("gid", "")
        node_details_key=entity_type_name_chinese.split("-")[0]

        for k,v in target_dict.items():

            id=target_dict.get('id',"")
            property_code=k
            value=v
            example=rfekg.second_phase_search_engine_deatil(gid=gid,
                                                    id=id,
                                                    entity_type_code=entity_type_code,
                                                    property_code=property_code,value=value,entity_type_name_chinese=entity_type_name_chinese)
            dict_temp=example.return_package()
            #返回的是一个dict
            each_entity_list.append(dict_temp)


        if node_details.get(node_details_key,"").__class__==str:#表示为空
            temp_list=[{gid:each_entity_list}]
            node_details[node_details_key]=temp_list
        else:
            node_details[node_details_key].append({gid:each_entity_list})


    print(node_details)

    for k,v in node_details.items():
        print(k)
        print(v)
        for g in v:
            print(g)


def get_downwardCount():
    print("it is a function for getting downwardCount")
    class_tip=sg.Tip("","","")

    # 获取搜索引擎主页的热词
    ifSuccess,res=class_tip.acquire_count()  # TODO:新增


    # 获取输出值
    # outputs = class_tip.output()  ##TODO:改了

    print(res)
    return jsonify(data=res)



    


import re
if __name__=='__main__':
    # kquery_return_process()
    # print([].__class__==list)
    # print(father_func_threading())
    # print(father_func_process())
    # print("父进程ID是：{0}".format(os.getpid()))
    # process = Process(target=new_process, args=("主进程参数",))
    # process.start()# 启动进程
    # # process.join()# 等待子进程执行完毕，再执行主进程
    # print("主进程执行完毕！")

    # rfekg.second_phase_search_engine_deatil.set_all_message_dict()
    # print(rfekg.second_phase_search_engine_deatil.all_message_dict)
    # get_downwardCount()
    print("hello world")
    a=re.split(",","ioosoos")
    print(a)
