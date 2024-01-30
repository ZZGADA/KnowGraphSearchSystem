from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsIntellectual.py")
from static.graph_const import GraphConst


class DetailIntellectual:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse = graph_const_example.get_graph_types_map_reverse()
    
    # 多个返回结果的分类
    commonUseClassificationChines = ["标题", "基本信息", "研究内容", "预期目标", "知识产权", "附件材料"]

    '''
    专利：专利权人、发明/设计人、所属团队、所属实验室、关联项目、成果；
    论文：作者姓名、所属团队、所属实验室、关联项目、成果；
    软著：著作权人、关联项目、所属团队、所属实验室、成果；
    专著：主要作者、关联项目、所属团队、所属实验室、成果；
    省公司标准：起草单位、关联项目、所属团队、所属实验室、成果；
    过程标准：编制单位、关联项目、所属团队、所属实验室、成果；
    
    '''
    
    # 需要的关联管关系:
    #专利 专利权人、发明/设计人、所属团队、所属实验室、关联项目、成果；
    relationPatent=[
        "relation_patentee",
        "relation_invention_designer",
        "relation_team",
        "relation_laboratory",
        "relation_project",
        "relation_achievement"
    ]
    #论文 作者姓名、所属团队、所属实验室、关联项目、成果；
    relationParper=[
        "relation_author_name",
        "relation_team",
        "relation_laboratory",
        "relation_achievement"
    ]
    #软著 著作权人、关联项目、所属团队、所属实验室、成果；
    relationSoftwareWorks=[
        "relation_author_rights_holder",
        "relation_project",
        "relation_team",
        "relation_laboratory",
        "relation_achievement"
    ]
    #专著 主要作者、关联项目、所属团队、所属实验室、成果；
    relationMonograph=[
        "relation_lead_author",
        "relation_project",
        "relation_team",
        "relation_laboratory",
        "relation_achievement"
    ]
    # 省公司标准：起草人、起草单位、关联项目、所属团队、所属实验室、成果；
    relationTechnicalStandard=[
        "relation_drafter",
        "relation_drafting_unit",
        "relation_project",
        "relation_team",
        "relation_laboratory",
        "relation_achievement"
    ]
    # 过程标准：编制单位、关联项目、所属团队、所属实验室、成果；
    relationProcessStandard=[
        "relation_prepared_by",
        "relation_project",
        "relation_team",
        "relation_laboratory",
        "relation_achievement"
    ]
    propertiesName = {
        "entity_intellectual_property_patent": ["zscqzl_achievement_patenttype",
                                                "zscqzl_achievement_authorizationnumber",
                                                "zscqzl_achievement_patentee",
                                                "zscqzl_achievement_designer",
                                                "zscqzl_achievement_authorizationdate",
                                                "zscqzl_achievement_technosphere",
                                                "zscqzl_achievement_team",
                                                "zscqzl_achievement_laboratory",
                                                "zscqzl_achievement_participate_project"],
        
        "entity_intellectual_property_paper": ["zscqlw_achievement_author",
                                               "zscqlw_achievement_periodicalname",
                                               "zscqlw_achievement_issn",
                                               "zscqlw_achievement_reportingyear",
                                               "zscqlw_achievement_technosphere",
                                               "zscqlw_achievement_periodicallevel",
                                               "zscqlw_achievement_team",
                                               "zscqlw_achievement_laboratory",
                                               "zscqlw_achievement_participate_project"],
        
        "entity_intellectual_property_software_works": ["zscqrjzz_achievement_copyrightowner",
                                                        "zscqrjzz_achievement_certificatenumber",
                                                        "zscqrjzz_achievement_dateoffirstpublication",
                                                        "zscqrjzz_achievement_technosphere",
                                                        "zscqrjzz_achievement_participate_project",
                                                        "zscqrjzz_achievement_team",
                                                        "zscqrjzz_achievement_laboratory"],
        
        "entity_intellectual_property_monograph": ["zscqzz_achievement_mainauthor",
                                                   "zscqzz_achievement_zx",
                                                   "zscqzz_achievement_isbn",
                                                   "zscqzz_achievement_pubdate",
                                                   "zscqzz_achievement_technosphere",
                                                   "zscqzz_achievement_participate_project",
                                                   "zscqzz_achievement_team",
                                                   "zscqzz_achievement_laboratory"],
        
        "entity_technical_standard": [
                                        "entity_technical_standard_type",
                                        "entity_technical_standard_draft_by",
                                      "entity_technical_standard_draft_by_unit",
                                      "entity_technical_standard_time",
                                      "entity_technical_standard_standard_num",
                                      "entity_technical_standard_project",
                                      "entity_technical_standard_laboratory",
                                      "entity_technical_standard_team"],
        
        "entity_process_standard": ["entity_process_standard_type",
                                    "entity_process_standard_unit",
                                      "entity_process_standard_time",
                                    "entity_process_standard_standard_num",
                                      "entity_process_standard_project",
                                    "entity_process_standard_laboratory",
                                      "entity_process_standard_team"]
    }
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
        "patenttype":"专利类型",
        "authorizationnumber":"授权号",
        "patentee":"专利权人",
        "designer":"发明/设计人",
        "authorizationdate":"授权公告日",
        "technosphere":"技术领域",
        "team":"所属团队",
        "laboratory":"所属实验室",
        "participate_project":"关联项目",
        "project":"关联项目",
        "author":"作者姓名",
        "periodicalname":"刊物名称",
        "issn":"刊号",
        'reportingyear':"上报年份",
        "peportingyear":"上报年份",
        "periodicallevel":"刊物级别",
        "copyrightowner":"著作权人",
        "certificatenumber":"证书编号",
        "dateoffirstpublication":"首次发表日期",
        "mainauthor":"主要作者",
        "zx":"出版社",
        "isbn":"书号",
        "pubdate":"出版日期",
        "draft_by":"起草人",
        "type":"标准类型",
        "draft_by_unit":"起草单位",
        "time":"发布时间",
        "standard_num":"标准号",
        "unit":"编制单位",
    }
    

    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification = {
        "entity_intellectual_property_patent":relationPatent,
        "entity_intellectual_property_paper":relationParper,
        "entity_intellectual_property_software_works": relationSoftwareWorks,
        "entity_intellectual_property_monograph":relationMonograph,
        "entity_technical_standard":relationTechnicalStandard,
        "entity_process_standard":relationProcessStandard,
        
    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, properties: dict, name: str, keywords: list, annex, domain,propertyCodeDomain):
        # TODO:project_content这里面的内容 好像需要处理 暂时先不做处理
        self.properties = properties
        self.name = name
        self.keywords = keywords
        self.annex = annex
        self.domain = domain
        self.propertyCodeDomain = propertyCodeDomain
        #正常来说 是以实体名为默认开头的键 但是现在不对
    #     对于知识产权和成果来说不对 他们的属性名词的前缀与实体名不同

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
        intellectualAchievement=[]

        
        # 遍历每一个二级结点
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName =str( eachNode.get("name", "") ) # 结点名称
            eachNodeNameAppend=";"+eachNodeName
            relationEn = relationNode.get("name", "")  # 关系英文名
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailIntellectual.detailsClassification[self.domain]:
                logger.info(
                    "{}--{}--{} --gid:{} --domain{} --name{}".format(self.domain,relationCn, eachNodeDomainChinese, eachNodeGid,
                                                                   eachNodeDomain, eachNodeName))
                #成果
                if eachNodeDomain in self.graph_types_map["成果"]:
                    # 如果是成果
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    domainChineseNameKey = domainChineseName.replace("成果库-", "", 1)
                    
                    tempRes = {
                        "type": domainChineseNameKey,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    intellectualAchievement.append(tempRes)  # 加入成果的列表 列表嵌套字典
                
                # 所属实验室`
                if eachNodeDomain in self.graph_types_map["实验室"]:
                   
                    tempPropertyCode = self.propertyCodeDomain + "_laboratory"
                    
                    basicTemp=self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                           BaseInformation=BaseInforamtion,
                                                           eachNodeGid=eachNodeGid,
                                                           eachNodeName=eachNodeName,
                                                           eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                
                #所属团队
                if eachNodeDomain in self.graph_types_map["团队"] and relationEn == "relation_team":
                    
                    tempPropertyCode = self.propertyCodeDomain + "_team"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                    
                #关联项目   在技术标准里面的
                if eachNodeDomain in self.graph_types_map["项目"] and self.domain in self.graph_types_map["技术标准"]:
                    
                    tempPropertyCode = self.propertyCodeDomain + "_project"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                
                #关联项目 非技术标准里面的
                if eachNodeDomain in self.graph_types_map["项目"] and self.domain not in self.graph_types_map["技术标准"]:
                    
                    tempPropertyCode = self.propertyCodeDomain + "_participate_project"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)

                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)

                
                # 专利：专利权人
                if relationEn == "relation_patentee":
                    
                    tempPropertyCode = self.propertyCodeDomain + "_patentee"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                    
                # 专利：发明/设计人
                if relationEn == "relation_invention_designer":
                    
                    tempPropertyCode = self.propertyCodeDomain + "_designer"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)

                # 论文：作者姓名
                if relationEn == "relation_author_name":
                    tempPropertyCode = self.propertyCodeDomain + "_author"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                
                # 软著 ：著作权人
                if relationEn == "relation_author_rights_holder":
                    tempPropertyCode = self.propertyCodeDomain + "_copyrightowner"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                
                #专著 ：主要作者
                if relationEn == "relation_lead_author":
                    
                    tempPropertyCode = self.propertyCodeDomain + "_mainauthor"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)

                #省公司标准 起草人
                if relationEn == "relation_drafter":
                    tempPropertyCode = self.propertyCodeDomain + "_draft_by"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    # BaseInforamtion[tempPropertyCode].append(basicTemp)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempPropertyCode], basicTemp)
                
                #省公司标准 起草单位
                if relationEn == "relation_drafting_unit":
                    tempPropertyCode = self.propertyCodeDomain + "_draft_by_unit"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                    
                # 过程标准：编制单位
                if relationEn == "relation_prepared_by":
                    tempPropertyCode = self.propertyCodeDomain + "_unit"
                    
                    basicTemp = self.BaseInformationRelationProcessing(propertyCode=tempPropertyCode,
                                                                       BaseInformation=BaseInforamtion,
                                                                       eachNodeGid=eachNodeGid,
                                                                       eachNodeName=eachNodeName,
                                                                       eachNodeDomain=eachNodeDomain)
                    
                    BaseInforamtion[tempPropertyCode].append(basicTemp)
                    
           
        
        BaseInforamtionProcessed = dp.SearchEngineDetailsProcessing.BaseInformationProcessing(domain=self.propertyCodeDomain, BaseInformation=BaseInforamtion,
                                                                                              propertiesNameChinese=self.propertiesNameChinese)
        
        
        '''
        附件材料、标题、基本信息、参与成果、
        '''
        
        res = {
            "intellectualAnnex": self.annex,
            "intellectualTitle": {
                "intellectualName": self.name,
                "intellectualKeywords": self.keywords
            },
            "intellectualBasicInformation":BaseInforamtionProcessed,
            "intellectualEngageAchievement": intellectualAchievement,
            
        }  # 最终的所有返回结果
        return res


