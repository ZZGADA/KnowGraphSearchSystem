from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsLib.py")
from static.graph_const import GraphConst


class DetailLab:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse = graph_const_example.get_graph_types_map_reverse()
    
    # 多个返回结果的分类
    commonUseClassificationChines = ["标题", "基本信息", "基本情况", "研究方向", "人员信息", "参与项目","参与成果","附件材料"]
    # 详情页面较多的关系
    '''
    实验室主任、依托单位、人员信息(主要成员、实验室主任)、参与项目、参与知识产权、参与成果、'''
    commonUseRelationMore = ["relation_laboratory_director",
                            "relation_supporting_unit",
                            "relation_main_member",
                            "relation_laboratory_director",
                             "relation_project",
                             "relation_achievement",
                              "relation_intellectual_property",
                             "relation_technical_standard",
                             ]
    
    
    # 在一级中的first_res中查找 first_res就是一级  实体属性 其他是在一级中查询的详情都需要注意 不要放在属性中
    # propertiesName中只有基本信息里的内容
    '''
    项目类型 项目编码 项目负责人 项目牵头单位 项目开始时间 项目结束时间 项目预期目标
    项目参与人员 项目评审专家 因为是个数组就直接添加了 单独的 注意一下就好 '''
    propertiesName = {
        "entity_laboratory":["entity_laboratory_type",
                             "entity_laboratory_director",
                             "entity_laboratory_unit",
                             "entity_laboratory_research_field",
                             "entity_laboratory_establishment_time"]
    }
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
        "type":"类别",
        "director":"实验室主任",
        "unit":"依托单位",
        "establishment_time":"成立时间",
        "research_field":"研究领域",
        
    }
    
    # 这个可能不要了 如果需要的话再说 是用做存储项目详情页面的大分类的
    resultList = {
   
        "entity_laboratory": commonUseClassificationChines,

    }
    
    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification = {
        "entity_laboratory": commonUseRelationMore,

    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, properties: dict,name:str,domain,keywords:list,
                 member:str,annex,direction,
                 basicSituations):
        # TODO:project_content这里面的内容 好像需要处理 暂时先不做处理
        self.properties = properties
        self.name=name
        self.domain=domain
        self.keywords=keywords
        self.member=member
        self.annex=annex
        self.direction=direction
        self.basicSituations =basicSituations
       
    
    def BaseInformationProcessing(self, domain: str, BaseInformation: dict):
        # BaseInformation 是项目的基本信息  以字典的形式存储者每一个属性以及关联关系得到的新属性
        # 接下来是遍历 然后添加中文
        # 返回结果 列表嵌套字典
        res = []
        target = domain + "_"
        for k, v in BaseInformation.items():
            tempRes = {}
            # lstrip的运行机制：如果你传给他一个字符串, 那么它会从左到右挨个检查变量的字符, 如果在你给的参数内, 则删除这个字符, 直到出现不符合条件的字符才停止
            newKey = k.replace(target, "", 1)
            # print(newKey,k,target)
            chinese = self.propertiesNameChinese[newKey]
            tempRes["chinese"] = chinese
            tempRes["value"] = v
            tempRes["propertyCode"] = k
            res.append(tempRes)
        return res
    
    def processingClassification(self, nodes: list, relations: list) -> dict:
        #         返回一个dict
        #         对详情页面的分类进行处理
        #         传入second_res的"node"对应的二级结点列表
        eachNode: dict
        nodesMap = dp.SearchEngineDetailsProcessing.MapNodeRelations(nodes)
        BaseInforamtion = self.properties
        labIntellectual = []  # 详情页面中知识产权的返回结果
        labMembership=[]
        labProjectEngage=[]
        labAchievement=[]
        
        
        # 遍历每一个二级结点
        
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName = eachNode.get("name", "")  # 结点名称
            relationEn = relationNode.get("name", "")  # 关系英文名
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            planYear=   eachNode.get("plan_year","")  #计划年度
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailLab.detailsClassification[self.domain]:
                logger.info(
                    "实验室详情--{}--{} --gid:{} --domain --name".format(relationCn, eachNodeDomainChinese, eachNodeGid,
                                                                   eachNodeDomain, eachNodeName))
                if eachNodeDomain in self.graph_types_map["知识产权"]:
                    # 知识产权类的详情分类
                    # 如果当前结点的关联关系在该节点需要的关联关系内 而且结点名称（实体类型）属于知识产权的话 那么就放入知识产权的详细列表中
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    tempRes = {
                        "type": domainChineseName,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    labIntellectual.append(tempRes)  # 加入知识产权的列表 列表嵌套字典
            
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
                    labAchievement.append(tempRes)  # 加入成果的列表 列表嵌套字典
                    
                if eachNodeDomain in self.graph_types_map["项目"] and relationEn=="relation_project":
                    # 如果是参与项目
                    projectCategoryNameCode = eachNodeDomain
                    projectCategoryName = self.graph_types_map_reverse[projectCategoryNameCode]
                    projectCategoryNameKey = projectCategoryName.replace("项目-", "", 1)
                    eachEngageProject = {
                        "key": projectCategoryNameKey,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid,
                        "year":planYear
                    }
                    labProjectEngage.append(eachEngageProject)
                
                if eachNodeDomain in self.graph_types_map["专家"] and relationEn=="relation_laboratory_director":
                    #如果实验室主任 那么加入到人员信息和基本信息
                    tempExpertRes={
                        "type":relationCn,
                        "name":eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    
                    tempKey = self.domain + "_director"
                    # if type(BaseInforamtion[tempKey][0]) == str:
                    #     BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }

                    labMembership.append(tempExpertRes)
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempKey], tempNode)
                    
                if eachNodeDomain in self.graph_types_map["专家"] and relationEn=="relation_main_member":
                    tempExpertRes = {
                        "type": relationCn,
                        "name": eachNodeName,
                        "domain": eachNodeDomain,
                        "gid": eachNodeGid
                    }
                    labMembership.append(tempExpertRes)
                
                if eachNodeDomain in self.graph_types_map["单位"] and relationEn == "relation_supporting_unit":
                    tempKey = self.domain + "_unit"
                    if type(BaseInforamtion[tempKey][0]) == str:
                        BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    
                    BaseInforamtion[tempKey].append(tempNode)
                    
        BaseInforamtionProcessed = dp.SearchEngineDetailsProcessing.BaseInformationProcessing(
            domain=self.domain, BaseInformation=BaseInforamtion,propertiesNameChinese=self.propertiesNameChinese)
        
        res = {
            "labIntellectual": labIntellectual,
            "labAnnex": self.annex,
            "labTitle": {
                "labName": self.name,
                "labKeywords": self.keywords
            },
            "labBasicInformation": BaseInforamtionProcessed,
            "labBasicSituations ":self.basicSituations ,
            "labDirection":self.direction,
            "labMembership": labMembership,
            "labProjectEngage":labProjectEngage,
            "labAchievement":labAchievement
            
        }  # 最终的所有返回结果
        return res


