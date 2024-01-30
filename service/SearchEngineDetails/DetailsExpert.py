from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsExpert.py")



class DetailExpert:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse=graph_const_example.get_graph_types_map_reverse()
    
    # 多个返回结果的分类
    commonUseClassificationChines = ["标题", "参与项目", "评审项目", "参与知识产权", "参与成果"]
    # 详情页面较多的关系
    '''
     专家参与项目、专家评审项目、专家参与知识产权、专家参与成果、专家所属实验室、专家所属团队、专家所属单位'''
    
    commonUseRelationMore = [ "relation_participate_in",
                              "relation_review_items",
                              "relation_intellectual_property",
                              "relation_technical_standard",
                              "relation_achievement",
                              "relation_laboratory",
                              "relation_team",
                              "relation_unit"]

    
    # 在一级中的first_res中查找 first_res就是一级  实体属性 其他是在一级中查询的详情都需要注意 不要放在属性中
    # propertiesName中只有基本信息里的内容
    '''
    专家没有基本信息 所以不显示 '''
    propertiesName = {
        "entity_expert": []
    }
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
        "workunit": "工作单位",
        "team":"所属团队",
        "laboratory":"实验室",
        
    }
    
    
    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification = {
        "entity_expert": commonUseRelationMore,
        "":commonUseClassificationChines
    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, properties: dict,  name: str, workUnit, domain):
        
        self.properties = properties
        self.name = name
        self.workUnit = workUnit
        self.domain = domain

    
    def processingClassification(self, nodes: list, relations: list) -> dict:
        #         返回一个dict
        #         对详情页面的分类进行处理
        #         传入second_res的"node"对应的二级结点列表
        eachNode: dict
        nodesMap = dp.SearchEngineDetailsProcessing.MapNodeRelations(nodes)
        BaseInforamtion = self.properties
        expertIntellectual = []  # 详情页面中知识产权的返回结果
        expertTeam=""
        expertLab=""
        expertAchievement=[] #详情页面成功的返回结果
        expertEngageProject=[] #详情页面的参与项目返回结果
        expertReviewProject=[] #参与项目
        expertLab = []   #所属实验室
        expertTeam = []  # 所属团队
        expertUnit = []  #所属工作单位
        
        
        # 遍历每一个二级关系
        for relationNode in relations:
            targetGid=relationNode["end"] #根据属性获取二级目标gid
            eachNode=nodesMap[targetGid] #获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName = eachNode.get("name", "")  # 结点名称
            planYear= eachNode.get("plan_year","")  #计划年度
            eachNodeNameAppend=";"+eachNodeName
            relationEn = relationNode.get("name", "")  # 关系英文名
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            eachNodeDomainChinese=self.graph_types_map_reverse[eachNodeDomain]
            
            
 
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailExpert.detailsClassification[self.domain]:
                #如果结点与二级结点的关系是我们需要的 在DetailProject.detailsClassification[self.domain] 里面
                # print("-------"+relationEn)
                logger.info(
                    "专家--{}({})--{} --gid:{} --domain:{} --name:{}".format(relationCn,eachNodeDomainChinese,relationEn,
                                                                             eachNodeGid, eachNodeDomain, eachNodeName))
                if eachNodeDomain in self.graph_types_map["知识产权"]:
                    
                    # 知识产权详情页面
                    # 如果当前结点的关联关系在该节点需要的关联关系内 而且结点名称（实体类型）属于知识产权的话 那么就放入知识产权的详细列表中
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    tempRes = {
                        "type":domainChineseName,
                        "name": eachNodeName,
                        "domain": eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    expertIntellectual.append(tempRes)  # 加入知识产权的列表 列表嵌套字典
                
                
                if eachNodeDomain in self.graph_types_map["项目"] and relationEn == "relation_participate_in":
                    # 如果是参与项目
                 
                    projectCategoryNameCode=eachNodeDomain   #获取category的属性编码
                    
                    projectCategoryName=self.graph_types_map_reverse[projectCategoryNameCode]#获取编码对应的项目类型
                    projectCategoryNameKey=projectCategoryName.replace("项目-","",1)
                    
                    eachEngageProject={
                        "type":projectCategoryNameKey,
                        "name":eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid,
                        "year":planYear
                    }  #结点名称 存储为字典
                    
                    expertEngageProject.append(eachEngageProject) #加入数组
                
                if eachNodeDomain in self.graph_types_map["项目"] and relationEn == "relation_review_items" :
                    # 如果是评审项目
                    projectCategoryNameCode = eachNodeDomain
                    projectCategoryName = self.graph_types_map_reverse[projectCategoryNameCode]
                    projectCategoryNameKey = projectCategoryName.replace("项目-", "", 1)
                    eachEngageProject = {
                        "key":projectCategoryNameKey,
                        "name":eachNodeName,
                        "domain": eachNodeDomain,
                        "gid":eachNodeGid,
                        "year":planYear
                    }
                    expertReviewProject.append(eachEngageProject)
                    
                if  eachNodeDomain in self.graph_types_map["成果"] and relationEn == "relation_achievement":
                    # 如果是成果
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    domainChineseNameKey=domainChineseName.replace("成果库-","",1)
                    
                    tempRes = {
                        "type":domainChineseNameKey,
                        "name": eachNodeName,
                        "domain": eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    expertAchievement.append(tempRes)  # 加入成果的列表 列表嵌套字典
                    
                if eachNodeDomain in self.graph_types_map["实验室"] and relationEn == "relation_laboratory":
                    tempLab={
                        "type":"所属实验室",
                        "name":eachNodeName,
                        "propertyCode":"entity_laboratory",
                        "gid":eachNodeGid
                    }
                    # expertLab=tempLab  #得到实验室
                    expertLab.append(tempLab)
                    
                
                if eachNodeDomain in self.graph_types_map["团队"] and relationEn == "relation_team":
                    tempTeam = {
                        "type": "所属团队",
                        "name": eachNodeName,
                        "propertyCode": "entity_team",
                        "gid":eachNodeGid
                    }
                    # expertLab = tempTeam  # 得到实验室
                    expertTeam.append(tempTeam)
                    
                if relationEn == "relation_unit":
                    tempUnit = {
                        "type": "所属单位",
                        "name": eachNodeName,
                        "propertyCode": "entity_unit",
                        "gid": eachNodeGid
                    }
                    expertUnit.append(tempUnit)
                    
                
                    
        # BaseInforamtionProcessed = self.BaseInformationProcessing(domain=self.domain, BaseInformation=BaseInforamtion)
        
        
        '''
        参与知识产权 参与成果 参与项目 参与评审项目 title(name,workUnit team Lab)'''
        
        res = {
            
            "expertIntellectual": expertIntellectual,
            "expertAchievement": expertAchievement,
            "expertEngageProject": expertEngageProject,
            "expertTitle": {
                "expertName": self.name,
                "expertWorkUnit": expertUnit,
                "expertTeam":expertTeam,
                "expertLaboratory":expertLab
            },
            "expertReviewProject": expertReviewProject,

        }  # 最终的所有返回结果
        return res





