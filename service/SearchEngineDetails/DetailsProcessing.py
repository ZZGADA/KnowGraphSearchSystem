import logging
import re

from service.SearchEngineDetails import DetailsProject as dp
from service.SearchEngineDetails import DetailsExpert as de
from service.SearchEngineDetails import DetailsUnity as du
from service.SearchEngineDetails import DetailsLab as dl
from service.SearchEngineDetails import DetailsTeam as dt
from service.SearchEngineDetails import DetailsIntellectual as di
from service.SearchEngineDetails import DetailsAchievement as da
from static.graph_const import GraphConst
import re
from datetime import datetime

from config import logging_config
logger = logging_config.logging_self_define().log(level='INFO',name="DetailsProcessing.py")
class SearchEngineDetailsProcessing:
    # 详情页面后处理的总处理类
    
    IntellectualList=["专利","论文","软著","专著","技术标准"]
    graphConstExample=GraphConst()

    def __init__(self,label:str,text:str,first_res:list,second_res:list,**kwargs):
        # 我们只需要first_res的第一个
        self.label=label
        self.text=text
        self.first_res:dict=first_res[0]
        self.second_res=second_res

    @staticmethod
    def ExpertListProcessing(OriginalExpertList:list,tempNode:dict):
        originalNode:dict
        count = 0

        for originalNode in OriginalExpertList:
            if originalNode.get("name") == tempNode["name"]:
                OriginalExpertList.pop(count)
            count+=1
        OriginalExpertList.append(tempNode)
        # return  OriginalExpertList
        
    @staticmethod
    def BaseInformationProcessing(domain: str, BaseInformation: dict,propertiesNameChinese):
        # BaseInformation 是项目的基本信息  以字典的形式存储者每一个属性以及关联关系得到的新属性
        # 接下来是遍历 然后添加中文
        # 返回结果 列表嵌套字典
        res = []
        target = domain + "_"
        v:list
        for k, v in BaseInformation.items():
            tempRes = {}
            # lstrip的运行机制：如果你传给他一个字符串, 那么它会从左到右挨个检查变量的字符, 如果在你给的参数内, 则删除这个字符, 直到出现不符合条件的字符才停止
            newKey = k.replace(target, "", 1)
            chinese = propertiesNameChinese[newKey]
            
            # 如果数组长度为1 且数组内容是空字符串 表示没有实体属性 为空 直接pop掉
            # 所有的value的数据类型都是列表 所以只有当列表长度为1 而且
            if len(v) == 1 and v[0]=="":
                v.pop(0)
            
            tempRes["chinese"] = chinese
            tempRes["value"] = v  # 因为现在要统一数据格式 为列表嵌套字典
            tempRes["propertyCode"] = k
            
            logger.info("实体基本信息查询 --chinese:{}  --value{}".format(chinese,v))
            
            res.append(tempRes)
        return res
    
    @staticmethod
    def MapNodeRelations( nodes: list):
        # 对node做处理 获取唯一的end==="gid" 值为node所有属性

        nodeMap = {}
        # 获取每个二级结点唯一的gid  为键 绑定
        
        for node in nodes:
            gid=node["gid"]
            nodeMap[gid]=node
        
        return nodeMap
    def PropertyProcessingDateTime(self,baseInf):
        logger.info("实体属性基本信息 --{}".format(baseInf))
        
        try:
            baseInf = datetime.strptime(baseInf, "%Y-%m-%d%H:%M:%S").date().__str__()
        except:
            baseInf = baseInf
            logger.warn("实体属性基本信息不符合标准时间 --{}\n".format(baseInf))
        finally:
            logger.info("finally  执行")
            
            
        return baseInf

    #详情页面开始方法
    def DetailsProcessing(self)->dict:
        res:dict
        domain = self.first_res.get("domain", "")
        
        try:
            nodes=self.second_res[0].get("nodes",[])
            relations=self.second_res[0].get("relations",[])
        except:
            relations=[]
            logger.warning("second_res关联结点为空 没有二级的返回数据")
        
        logger.info(self.label)
        
        if self.label=="项目" or self.label=="项目名称":
            logger.info("进入项目详情页面")
            projectProperties=dp.DetailProject.propertiesName[domain]  #获取项目详细的基础信息 与属性相关的 从first_res中获取
            
            projectContent=self.first_res.get(domain+"_content","")  #获取项目的研究内容
            projectContent=self.first_res.get(domain+"_contents","") if projectContent =="" else projectContent
            projectName=self.first_res.get("name","") #项目名称
            projectKeywords=self.first_res.get("keywords",[]) #主题词
            projectAnnex=self.first_res.get(domain+"_annex","") #附件材料
            projectExceptions=self.first_res.get(domain+"_expectations","")  #预期目标
            
            # 获取实体属性编码 没有获取到就传入 空值
            initParam={}
            for key in projectProperties:
                baseInf=self.PropertyProcessingDateTime( self.first_res.get(key, ""))  #日期字符处理
                if ("participants" in key or "review_experts" in key or "leader" in key):
                    reBaseiInf=re.split(",.-\/_，。、‘；;'",baseInf)   #将拼接字符串转换成列表
                    finalBaseInf=[]
                    #对列表进行循环 然后添加gid 注意gid全部都是"" 走后面的根据关联关系匹配的过程中，如果有重复人名那么就剔除掉gid为空的这个
                    for j in reBaseiInf:
                        finalBaseInf.append({
                            "gid": "",
                            "name": j
                        })
                    initParam[key] = finalBaseInf  #分割属性
                else:
                    initParam[key] = [baseInf]  # 属性获得为空  直接返回 然后后处理统一处理

            #DetailProject() 核心处理逻辑
            detailProjectExample=dp.DetailProject(initParam,projectContent,projectName,projectKeywords,projectAnnex,domain,projectExceptions)  #生成项目属性的实例对象
            detailProjectRes=detailProjectExample.processingClassification(nodes,relations)
            res=detailProjectRes
            
            
        elif self.label=="专家" or self.label=="专家名称":
            logger.info("进入专家详情页面")
            
            projectNames = de.DetailExpert.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
            
            expertName=self.first_res.get("name","")
            expertWorkUnit=self.first_res.get("professor_workunit","")
            
            initParam = {}
            for key in projectNames:
                baseInf=self.PropertyProcessingDateTime( self.first_res.get(key, ""))  #日期字符处理
                initParam[key] = [baseInf]
            
                
            detailExpertExample = de.DetailExpert(initParam,
                                                  expertName,
                                                  expertWorkUnit,
                                                  domain)  # 生成项目属性的实例对象
            detailExpertRes = detailExpertExample.processingClassification(nodes, relations)
            
            
            res = detailExpertRes
            
        elif self.label == "单位" or self.label == "单位名称":
            logger.info("进入单位详情页面")
            unitNames = du.DetailUnit.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
            
            unitName = self.first_res.get("name", "")
            
            initParam = {}
            for key in unitNames:
                baseInf = self.PropertyProcessingDateTime(self.first_res.get(key, ""))  # 日期字符处理
                initParam[key] = [baseInf]
                    
                # initParam[key] = str(self.first_res.get(key, []) ) # 如果没有默认为空
            
            detailUnitExample = du.DetailUnit(initParam, unitName, domain)  # 生成项目属性的实例对象
            detailUnitRes = detailUnitExample.processingClassification(nodes, relations)
            # print(detailProjectRes)
            res = detailUnitRes
        
        elif self.label == "实验室" or self.label == "实验室名称":
            logger.info("进入实验室详情页面")
            LabNames = dl.DetailLab.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
            
            labName = self.first_res.get("name", "")
            labKeywords=self.first_res.get("keywords",[])
            labMember=self.first_res.get("entity_laboratory_member","")
            labAnnex=self.first_res.get("entity_laboratory_annex","")
            labDirection=self.first_res.get("entity_laboratory_research_direction","")
            labBasicInformation=self.first_res.get("entity_laboratory_basic_information","")

            # 获取实体属性编码 没有获取到就传入 空值
            initParam = {}
            for key in LabNames:
                baseInf = self.PropertyProcessingDateTime(self.first_res.get(key, ""))  # 日期字符处理
                if ("director" in key ):
                    reBaseiInf = re.split(",.-\/_，。、‘；;'", baseInf)  # 将拼接字符串转换成列表
                    finalBaseInf = []
                    # 对列表进行循环 然后添加gid 注意gid全部都是"" 走后面的根据关联关系匹配的过程中，如果有重复人名那么就剔除掉gid为空的这个
                    for j in reBaseiInf:
                        finalBaseInf.append({
                            "gid": "",
                            "name": j
                        })
                    initParam[key] = finalBaseInf  # 分割属性
                else:
                    initParam[key] = [baseInf]  # 属性获得为空  直接返回 然后后处理统一处理
            
            detailLabExample = dl.DetailLab(initParam,
                                            labName,
                                            domain,
                                            labKeywords,
                                            labMember,
                                            labAnnex,
                                            labDirection,
                                            labBasicInformation)  # 生成项目属性的实例对象
            
            detailLabRes = detailLabExample.processingClassification(nodes, relations)
            # print(detailProjectRes)
            res = detailLabRes
        
        elif self.label == "团队" or self.label == "团队名称":
            logger.info("进入团队详情页面")
            #TODO:团队详情的所有字段都还没有改 记得跟康哥确认
            teamNames = dt.DetailTeam.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
            
            teamName = self.first_res.get("name", "")
            teamKeywords = self.first_res.get("keywords", [])
            teamAttack = self.first_res.get("entity_team_tackling_direction", "") #攻关方向
            teamConstruction = self.first_res.get("construction_plan", "") #建设计划
            teamAnnex = self.first_res.get("formal_file", "")  #附件材料

            initParam = {}
            for key in teamNames:
                baseInf = self.PropertyProcessingDateTime(self.first_res.get(key, ""))  # 日期字符处理
                print(baseInf)
                if ("leader" in key):
                    reBaseiInf = re.split(",.-\/_，。、‘；;'", baseInf)  # 将拼接字符串转换成列表
                    finalBaseInf = []
                    # 对列表进行循环 然后添加gid 注意gid全部都是"" 走后面的根据关联关系匹配的过程中，如果有重复人名那么就剔除掉gid为空的这个
                    for j in reBaseiInf:
                        finalBaseInf.append({
                            "gid": "",
                            "name": j
                        })
                    initParam[key] = finalBaseInf  # 分割属性
                else:
                    initParam[key] = [baseInf]  # 属性获得为空  直接返回 然后后处理统一处理


                    
                # initParam[key] = str(self.first_res.get(key, []) ) # 如果没有默认为空
            
            detailTeamExample = dt.DetailTeam(initParam,
                                              teamName,
                                              domain,
                                              teamKeywords,
                                              teamAttack,
                                              teamConstruction,
                                              teamAnnex)  # 生成项目属性的实例对象
            detailTeamRes = detailTeamExample.processingClassification(nodes, relations)
            # print(detailProjectRes)
            res = detailTeamRes
            
            
        elif self.label in self.IntellectualList :
            logger.info("进入知识产权详情页面")

            intellectualNames = di.DetailIntellectual.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
            propertyCodeDomain = self.graphConstExample.get_intellectualKeyMap().get(domain,"")
            
            intellectualName = self.first_res.get("name", "")
            intellectualKeywords = self.first_res.get("keywords", [])
            intellectualAnnex = self.first_res.get("formal_file", "")  # 附件材料

            initParam = {}
            for key in intellectualNames:
                baseInf = self.PropertyProcessingDateTime(self.first_res.get(key, ""))  # 日期字符处理
                if ("designer" in key or "author" in key or "mainauthor" in key or "draft_by" in key):
                    reBaseiInf = re.split(",.-\/_，。、‘；;'", baseInf)  # 将拼接字符串转换成列表
                    finalBaseInf = []
                    # 对列表进行循环 然后添加gid 注意gid全部都是"" 走后面的根据关联关系匹配的过程中，如果有重复人名那么就剔除掉gid为空的这个
                    for j in reBaseiInf:
                        finalBaseInf.append({
                            "gid": "",
                            "name": j
                        })
                    initParam[key] = finalBaseInf  # 分割属性
                else:
                    initParam[key] = [baseInf]  # 属性获得为空  直接返回 然后后处理统一处理

                
            
            detailIntellectualExample = di.DetailIntellectual(initParam,
                                                              intellectualName,
                                                              intellectualKeywords,
                                                              intellectualAnnex,
                                                              domain,
                                                              propertyCodeDomain)  # 生成项目属性的实例对象
            detailIntellectualRes = detailIntellectualExample.processingClassification(nodes, relations)
            
            
            res = detailIntellectualRes
            
            
        elif self.label =="成果":
            logger.info("进入省公司成果详情页面")
            # TODO:团队详情的所有字段都还没有改 记得跟康哥确认
        
            propertyCodeDomain = self.graphConstExample.get_achievementKeyMap().get(domain, "") #获取属性编码前缀
            
            #因为关系的问题 需要对省部级以上和其他两个实例对象分类
            if domain in ["entity_achievement_sbj","entity_achievement_qt"]:
                achievementTypeJudge=self.first_res.get(propertyCodeDomain+"_judgetype","") #中文
                achievementTypeJudgeEn=self.graphConstExample.get_achievementChineseMap()[achievementTypeJudge]
                domainClassify=domain+"_"+achievementTypeJudgeEn  #成果的12个分类结果
                achievementNames=da.DetailAchievement.propertiesName[domainClassify]
                achievementSynopsis = self.first_res.get(propertyCodeDomain + "_introduction", "")  # 成果简介 如果是sbj和qt的 都是这些
            else:
                domainClassify=domain   #成果的12个分类结果
                achievementNames = da.DetailAchievement.propertiesName[domain]  # 获取项目详细的基础信息 与属性相关的 从first_res中获取
                achievementSynopsis = self.first_res.get(propertyCodeDomain + "_synopsis", "")  # 项目简介
            
            
            
            achievementName = self.first_res.get("name", "")
            achievementKeywords = self.first_res.get("keywords", [])
            achievementAnnex = self.first_res.get(propertyCodeDomain+"_annex", "")  # 附件材料

            initParam = {}
            for key in achievementNames:
                baseInf = self.PropertyProcessingDateTime(self.first_res.get(key, ""))  # 日期字符处理
                if ("principal" in key or
                        "accomplices" in key or
                        "rapporteur" in key or
                        "drafters" in key or
                        "designer" in key or
                        "patentee" in key or
                         "patentee" in key):
                    reBaseiInf = re.split(",.-\/_，。、‘；;'", baseInf)  # 将拼接字符串转换成列表
                    finalBaseInf = []
                    # 对列表进行循环 然后添加gid 注意gid全部都是"" 走后面的根据关联关系匹配的过程中，如果有重复人名那么就剔除掉gid为空的这个
                    for j in reBaseiInf:
                        finalBaseInf.append({
                            "gid": "",
                            "name": j
                        })
                    initParam[key] = finalBaseInf  # 分割属性
                else:
                    initParam[key] = [baseInf]  # 属性获得为空  直接返回 然后后处理统一处理

            detailAchievementExample = da.DetailAchievement(initParam,
                                                                achievementName,
                                                                achievementKeywords,
                                                                achievementAnnex,
                                                                achievementSynopsis,
                                                                propertyCodeDomain,
                                                                domainClassify)  # 生成项目属性的实例对象
            detailAchievementRes = detailAchievementExample.processingClassification(nodes, relations)
            # print(detailProjectRes)
            res = detailAchievementRes

        return res
