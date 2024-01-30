from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsAchievement.py")
from static.graph_const import GraphConst



class DetailAchievement:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse = graph_const_example.get_graph_types_map_reverse()
    
    
    '''
        省公司 科学技术进步奖 :完成单位、 主要完成人、其他完成人、所属团队、所属实验室、包含知识产权
        省公司 标准类 ：主要起草人、其他起草人、起草单位、所属团队、所属实验室、包含知识产权
        省公司成果 专利类：发明设计人、专利权人、所属团队、所属实验室、包含知识产权
        省公司成果 技术发明类 ：完成单位、主要完成人、其他完成人、所属团队、所属实验室、包含知识产权
        省部级以上、其他成果（科学技术进步、技术发明） ：主要完成人、其他完成人、完成单位、所属团队、所属实验室、知识产权
        省部级以上、其他成果（标准）：主要起草人、其他起草人、所属团队、所属实验室、起草单位、包含知识产权
        省部级以上、其他成果（专利）：发明设计人、专利权人、所属团队、所属实验室、包含知识产权
    '''
    #省公司 科学技术进步奖 :完成单位、 主要完成人、其他完成人、所属团队、所属实验室、包含知识产权
    relation_sgs_kxkj=[
        "relation_completion_unit",
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省公司 标准类 ：主要起草人、其他起草人、起草单位、所属团队、所属实验室、包含知识产权
    relation_sgs_bz=[
        "relation_main_drafter",
        "relation_other_drafters",
        "relation_drafting_unit",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省公司成果 专利类：发明设计人、专利权人、所属团队、所属实验室、包含知识产权
    relation_sgs_zl=[
        "relation_invention_designer",
        "relation_patentee",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    #省公司成果 技术发明类 ：完成单位、主要完成人、其他完成人、所属团队、所属实验室、包含知识产权
    relation_sgs_jsfm=[
        "relation_completion_unit",
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    #省部级以上、其他成果（科学技术进步、技术发明） ：主要完成人、其他完成人、完成单位、所属团队、所属实验室、知识产权
    
    relation_sbj_kxkj = [
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_completion_unit",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（标准）：主要起草人、所属团队、所属实验室、起草单位、包含知识产权
    
    relation_sbj_bz = [
        "relation_main_drafter",
        "relation_team",
        "relation_laboratory",
        "relation_drafting_unit",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（专利）：发明设计人、专利权人、所属团队、所属实验室、包含知识产权
    relation_sbj_zl = [
        "relation_invention_designer",
        "relation_patentee",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（科学技术进步、技术发明） ：主要完成人、其他完成人、完成单位、所属团队、所属实验室、知识产权
    relation_sbj_jsfm = [
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_completion_unit",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（科学技术进步、技术发明） ：主要完成人、其他完成人、完成单位、所属团队、所属实验室、知识产权
    relation_qt_kxkj = [
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_completion_unit",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（标准）：主要起草人、其他起草人、所属团队、所属实验室、起草单位、包含知识产权
    relation_qt_bz = [
        "relation_main_drafter",
        "relation_team",
        "relation_laboratory",
        "relation_drafting_unit",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（专利）：发明设计人、专利权人、所属团队、所属实验室、包含知识产权
    relation_qt_zl = [
        "relation_invention_designer",
        "relation_patentee",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    # 省部级以上、其他成果（科学技术进步、技术发明） ：主要完成人、其他完成人、完成单位、所属团队、所属实验室、知识产权
    relation_qt_jsfm = [
        "relation_main_completion_personnel",
        "relation_other_complainants",
        "relation_completion_unit",
        "relation_team",
        "relation_laboratory",
        "relation_intellectual_property",
        "relation_technical_standard"
    ]
    
    
    #一共12个详情页面的属性
    propertiesName = {
        "entity_achievement_sgs_kxkj": ["kjjb_achievement_rewardcategory",
                                        "kjjb_achievement_rewardlevel",
                                        "kjjb_achievement_subjectterm",
                                        "kjjb_achievement_completeunit",
                                        "kjjb_achievement_principal",
                                        "kjjb_achievement_accomplices",
                                        "kjjb_achievement_team",
                                        "kjjb_achievement_laboratory",
                                       ],
        
        "entity_achievement_sgs_bz": ["cxgx_achievement_reward_category",
                                       "cxgx_achievement_rapporteur",
                                       "cxgx_achievement_drafters",
                                       "cxgx_achievement_draftingunit",
                                       "cxgx_achievement_field",
                                       "cxgx_achievement_internationalaq",
                                       "cxgx_achievement_stars",
                                       "cxgx_achievement_team",
                                       "cxgx_achievement_laboratory"],
        
        "entity_achievement_sgs_zl": ["zl_achievement_reward_category",
                                    "zl_achievement_designer",
                                    "zl_achievement_patentee",
                                    "zl_achievement_zl",
                                    "zl_achievement_authorizationdate",
                                    "zl_achievement_type",
                                    "zl_achievement_reward_level",
                                    "zl_achievement_team",
                                    "zl_achievement_laboratory"],
        
        "entity_achievement_sgs_jsfm": ["jsfm_achievement_reward_category",
                                        "jsfm_achievement_reward_level",
                                        "jsfm_achievement_subjectterm",
                                        "jsfm_achievement_completeunit",
                                        "jsfm_achievement_principal",
                                        "jsfm_achievement_accomplices",
                                        "jsfm_achievement_team",
                                        "jsfm_achievement_laboratory"],
        
        "entity_achievement_sbj_kxkj": [
                                    "sbj_achievement_rewardcategory",
                                    "sbj_achievement_rewardlevel",
                                    "sbj_achievement_subjectterm",
                                    "sbj_achievement_principal",
                                    "sbj_achievement_accomplices",
                                    "sbj_achievement_completeunit",
                                    "sbj_achievement_notificationtime",
                                    "sbj_achievement_team",
                                    "sbj_achievement_laboratory"],
        
        "entity_achievement_sbj_jsfm": [
                                "sbj_achievement_rewardcategory",
                                "sbj_achievement_rewardlevel",
                                "sbj_achievement_subjectterm",
                                "sbj_achievement_principal",
                                "sbj_achievement_accomplices",
                                "sbj_achievement_completeunit",
                                "sbj_achievement_notificationtime",
                                "sbj_achievement_team",
                                "sbj_achievement_laboratory"],
        
        "entity_achievement_qt_kxkj": [
                                "qt_achievement_rewardcategory",
                                    "qt_achievement_rewardlevel",
                                    "qt_achievement_subjectterm",
                                    "qt_achievement_principal",
                                    "qt_achievement_accomplices",
                                    "qt_achievement_completeunit",
                                    "qt_achievement_notificationtime",
                                    "qt_achievement_team",
                                    "qt_achievement_laboratory"],
        
        "entity_achievement_qt_jsfm": [
                                "qt_achievement_rewardcategory",
                                "qt_achievement_rewardlevel",
                                "qt_achievement_subjectterm",
                                "qt_achievement_principal",
                                "qt_achievement_accomplices",
                                "qt_achievement_completeunit",
                                "qt_achievement_notificationtime",
                                "qt_achievement_team",
                                "qt_achievement_laboratory"],
        
        "entity_achievement_sbj_zl": [
            "sbj_achievement_rewardcategory",
            "sbj_achievement_designer",
            "sbj_achievement_patentee",
            "sbj_achievement_rewardlevel",
            "sbj_achievement_notificationtime",
            "sbj_achievement_subjectterm",
            "sbj_achievement_team",
            "sbj_achievement_laboratory"],
        
        "entity_achievement_qt_zl": [
            "qt_achievement_rewardcategory",
            "qt_achievement_designer",
            "qt_achievement_patentee",
            "qt_achievement_rewardlevel",
            "qt_achievement_notificationtime",
            "qt_achievement_subjectterm",
            "qt_achievement_team",
            "qt_achievement_laboratory"],
        
        "entity_achievement_sbj_bz": [
            "sbj_achievement_rewardcategory",
            "sbj_achievement_rapporteur",
            "sbj_achievement_rewardlevel",
            "sbj_achievement_notificationtime",
            "sbj_achievement_subjectterm",
            "sbj_achievement_team",
            "sbj_achievement_laboratory",
            "sbj_achievement_draftingunit"
            ],
        
        "entity_achievement_qt_bz": [
            "qt_achievement_rewardcategory",
            "qt_achievement_rapporteur",
            "qt_achievement_rewardlevel",
            "qt_achievement_notificationtime",
            "qt_achievement_subjectterm",
            "qt_achievement_team",
            "qt_achievement_laboratory",
            "qt_achievement_draftingunit"
        ]
        
        
    }
    
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
       "rewardcategory":"奖励类别",
        "rewardlevel":"奖励等级",
        "subjectterm":"主题词",
        "completeunit":"完成单位",
        "principal":"主要完成人",
        "accomplices":"其他完成人",
        "team":"所属团队",
        "laboratory":"所属实验室",
        "rapporteur":"主要起草人",
        "drafters":"其他起草人",
        "draftingunit":"起草单位",
        "field":"标准领域",
        "internationalaq":"标准备案号",
        "stars":"奖励等级",
        "reward_category":"奖励类别",
        "designer":"发明/设计人",
        "patentee":"专利权人",
        "zl":"专利号",
        "authorizationdate":"专利授权日",
        "type":"专利类型",
        "reward_level":"奖励等级",
        "notificationtime":"奖励通告时间"
        
    }
    

    
    # 存放关联关系
    detailsClassification = {
        "entity_achievement_sgs_kxkj": relation_sgs_kxkj,
        "entity_achievement_sgs_bz": relation_sgs_bz,
        "entity_achievement_sgs_zl": relation_sgs_zl,
        "entity_achievement_sgs_jsfm": relation_sgs_jsfm,
        
        "entity_achievement_sbj_kxkj":relation_sbj_kxkj,
        "entity_achievement_sbj_bz": relation_sbj_bz,
        "entity_achievement_sbj_zl": relation_sbj_zl,
        "entity_achievement_sbj_jsfm": relation_sbj_jsfm,
        
        "entity_achievement_qt_kxkj": relation_qt_kxkj,
        "entity_achievement_qt_bz": relation_qt_bz,
        "entity_achievement_qt_zl": relation_qt_zl,
        "entity_achievement_qt_jsfm": relation_qt_jsfm,
        
    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self,
                 properties: dict,
                 name: str,
                 keywords: list,
                 annex:str,
                 synopsis:str,
                 propertyCodeDomain:str,
                 domain:str):
        
        self.properties = properties
        self.name = name
        self.keywords = keywords
        self.annex = annex
        self.domain = domain
        self.synopsis=synopsis
        self.propertyCodeDomain = propertyCodeDomain
        

    def BaseInformationRelationProcessing(self,propertyCode:str,BaseInformation:dict,eachNodeGid:str,eachNodeName:str,eachNodeDomain:str):
        # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
        # 那么就移除掉
        tempKey = propertyCode
        # if type(BaseInformation[tempKey][0]) == str:
        #     BaseInformation[tempKey].pop(0)
        basicTemp = {
            "gid": eachNodeGid,
            "name": eachNodeName,
            "domain": eachNodeDomain
        }
        return basicTemp

    def BaseInformationRelationProcessing2(self, propertyCode: str, BaseInformation: dict, eachNodeGid: str,
                                          eachNodeName: str, eachNodeDomain: str):
        # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
        # 那么就移除掉
        tempKey = propertyCode
        if type(BaseInformation[tempKey][0]) == str:
            BaseInformation[tempKey].pop(0)
        basicTemp = {
            "gid": eachNodeGid,
            "name": eachNodeName,
            "domain": eachNodeDomain
        }
        return basicTemp

    def processingClassification(self, nodes: list, relations: list) -> dict:
        #         返回一个dict
        #         对详情页面的分类进行处理
        #         传入second_res的"node"对应的二级结点列表
        eachNode: dict
        nodesMap = dp.SearchEngineDetailsProcessing.MapNodeRelations(nodes)
        BaseInforamtion = self.properties
        achievementIntellectual = []
        
        # 遍历每一个二级结点
        
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName = str(eachNode.get("name", "") ) # 结点名称
            eachNodeNameAppend=";"+eachNodeName  #前端统一数据类型 由list 转换成str的操作
            relationEn = relationNode.get("name", "")  # 关系英文名
            
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailAchievement.detailsClassification[self.domain]:
                logger.info(
                    "{}--{}--{} --gid:{} --domain{} --name{}".format(self.domain,relationCn, eachNodeDomainChinese, eachNodeGid,
                                                                   eachNodeDomain, eachNodeName))
                # 知识产权详情页面
                if eachNodeDomain in self.graph_types_map["知识产权"]:
                    
                    # 如果当前结点的关联关系在该节点需要的关联关系内 而且结点名称（实体类型）属于知识产权的话 那么就放入知识产权的详细列表中
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    tempRes = {
                        "type": domainChineseName,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    achievementIntellectual.append(tempRes)  # 加入知识产权的列表 列表嵌套字典
                
                # 所属实验室`
                if eachNodeDomain in self.graph_types_map["实验室"]:
                    tempPropertyCode = self.propertyCodeDomain + "_laboratory"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                
                #所属团队
                if relationEn == "relation_team":
                    tempPropertyCode = self.propertyCodeDomain + "_team"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                    
                #完成单位
                if relationEn == "relation_completion_unit":
                    tempPropertyCode = self.propertyCodeDomain + "_completeunit"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                
                #主要完成人
                if relationEn == "relation_main_completion_personnel":
                    tempPropertyCode = self.propertyCodeDomain + "_principal"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)

                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    
                # 其他完成人
                if relationEn == "relation_other_complainants":
                    tempPropertyCode = self.propertyCodeDomain + "_accomplices"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)

                # 主要起草人
                if relationEn == "relation_main_drafter":
                    tempPropertyCode = self.propertyCodeDomain + "_rapporteur"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                    
                # 其他起草人
                if relationEn == "relation_other_drafters":
                    tempPropertyCode = self.propertyCodeDomain + "_drafters"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                
                #起草单位
                if relationEn == "relation_drafting_unit":
                    tempPropertyCode = self.propertyCodeDomain + "_draftingunit"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)

                #发明设计人
                if relationEn == "relation_invention_designer":
                    tempPropertyCode = self.propertyCodeDomain + "_designer"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                    
                #专利权人
                if relationEn == "relation_patentee":
                    tempPropertyCode = self.propertyCodeDomain + "_patentee"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                    
                
                
        
        BaseInforamtionProcessed = dp.SearchEngineDetailsProcessing.BaseInformationProcessing(domain=self.propertyCodeDomain,
                                                                  BaseInformation=BaseInforamtion,
                                                                                              propertiesNameChinese=self.propertiesNameChinese)
        
        res = {
            
            "achievementAnnex": self.annex,
            "achievementTitle": {
                "achievementName": self.name,
                "achievementKeywords": self.keywords
            },
            "achievementSynopsis":self.synopsis,
            "achievementIntellectual":achievementIntellectual,
            "achieveBaseInformation":BaseInforamtionProcessed
            
        }  # 最终的所有返回结果
        return res


