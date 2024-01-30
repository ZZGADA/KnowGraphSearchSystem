from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsTeam.py")
from static.graph_const import GraphConst


class DetailTeam:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse = graph_const_example.get_graph_types_map_reverse()
    
    # 多个返回结果的分类
    commonUseClassificationChines = ["标题", "基本信息", "基本情况", "研究方向", "人员信息", "参与项目", "参与成果",
                                     "附件材料"]
    # 详情页面较多的关系
    '''
    带头人、依托单位、人员信息、参与项目、参与知识产权、参与成果、'''
    commonUseRelationMore = [
                             "relation_supporting_unit",
                             "relation_team_leader",
                             "relation_backbone_members",
                             "relation_members",
                             "relation_technical_advisor",
                             "relation_project",
                            "relation_intellectual_property",
                            "relation_technical_standard",
                            "relation_achievement"
]
    
    # 在一级中的first_res中查找 first_res就是一级  实体属性 其他是在一级中查询的详情都需要注意 不要放在属性中
    # propertiesName中只有基本信息里的内容

    propertiesName = {
        "entity_team": ["entity_team_declare_type",
                        "entity_team_leader",
                        "entity_team_unit",
                        "entity_team_date",
                        "entity_team_declare_direction"]
    }
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
        "declare_type": "类别",
        "leader": "团队带头人",
        "unit": "依托单位",
        "date": "成立时间",
        "declare_direction": "研究方向",
        
    }
    
    # 这个可能不要了 如果需要的话再说 是用做存储项目详情页面的大分类的
    resultList = {
        
        "entity_team": commonUseClassificationChines,
        
    }
    
    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification = {
        "entity_team": commonUseRelationMore,
        
    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, properties: dict, name: str, domain,
                 keywords,attack,construction,
                 annex):
        # TODO:project_content这里面的内容 好像需要处理 暂时先不做处理
        self.properties = properties
        self.name = name
        self.domain = domain
        self.keywords = keywords
        self.attack = attack
        self.annex = annex
        self.construction = construction
    
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
        teamIntellectual = []  # 详情页面中知识产权的返回结果
        teamMembership = [] #成员
        teamProjectEngage = []  #详情页页面参与项目
        teamAchievement = []  #详情页面成果
        
        # 遍历每一个二级结点
        
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName = eachNode.get("name", "")  # 结点名称
            relationEn = relationNode.get("name", "")  # 关系英文名
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailTeam.detailsClassification[self.domain]:
                print(eachNodeName, relationEn)
                logger.info(
                    "团队详情--{}--{} --gid:{} --domain --name".format(relationCn, eachNodeDomainChinese, eachNodeGid,
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
                    teamIntellectual.append(tempRes)  # 加入知识产权的列表 列表嵌套字典
                
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
                    teamAchievement.append(tempRes)  # 加入成果的列表 列表嵌套字典
                
                if eachNodeDomain in self.graph_types_map["项目"]:
                    # 如果是项目
                    projectCategoryNameCode = eachNodeDomain
                    projectCategoryName = self.graph_types_map_reverse[projectCategoryNameCode]
                    projectCategoryNameKey = projectCategoryName.replace("项目-", "", 1)
                    eachEngageProject = {
                        "key": projectCategoryNameKey,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    teamProjectEngage.append(eachEngageProject)
                
                if eachNodeDomain in self.graph_types_map["专家"]:
                    print(eachNodeName,relationEn)
                    # 如果是评审人员
                    # post=self.graph_const_example.get_graph_chinese_types()[relationEn]
                    # post=post.replace("团队","",1)
                    tempExpertRes = {
                        "type": relationCn,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    teamMembership.append(tempExpertRes)
                    
                    if relationEn =="relation_team_leader":
                        # 如果是团队牵头人的话 需要添加到基本信息里面
                        tempKey = self.domain + "_leader"
                        # if type(BaseInforamtion[tempKey][0]) == str:
                        #     BaseInforamtion[tempKey].pop(0)
                        
                        tempNode = {
                            "gid": eachNodeGid,
                            "name": eachNodeName
                        }
                        # 如果是团队牵头人
                        dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempKey], tempNode)
                
                
                if eachNodeDomain in self.graph_types_map["单位"] and relationEn == "relation_supporting_unit":
                    # print(eachNodeName,relationEn)
                    #如果拿到了 依托单位
                    tempKey = self.domain + "_unit"
                    if type(BaseInforamtion[tempKey][0]) == str:
                        BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    # 如果是参与人员
                    BaseInforamtion[tempKey].append(tempNode)
                    
        
        BaseInforamtionProcessed = dp.SearchEngineDetailsProcessing.BaseInformationProcessing(
            domain=self.domain, BaseInformation=BaseInforamtion,propertiesNameChinese=self.propertiesNameChinese)
        
        res = {
            "teamIntellectual": teamIntellectual,
            "teamAnnex": self.annex,
            "teamTitle": {
                "teamName": self.name,
                "teamKeywords": self.keywords
            },
            "teamBasicInformation": BaseInforamtionProcessed,
            "teamAttack": self.attack,
            "teamConstruction": self.construction,
            "teamMembership": teamMembership,
            "teamProjectEngage": teamProjectEngage,
            "teamAchievement": teamAchievement
            
        }  # 最终的所有返回结果
        return res


