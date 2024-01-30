from static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp

logger = logging_config.logging_self_define().log(level='INFO', name="DetailsUnit.py")


class DetailUnit:
    #TODO: 找浩 还要需要再写一个cypher语句用来查找和项目相关的合作单位的
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example = GraphConst()
    graph_types_map = graph_const_example.get_graph_types_map()
    graph_types_map_reverse = graph_const_example.get_graph_types_map_reverse()
    
    # 多个返回结果的分类
    commonUseClassificationChines = ["标题", "牵头项目列表", "参与知识产权", "参与成果", "参与成果"]
    # 详情页面较多的关系
    '''
     关联参与人员 关联评审专家 关联创新团队  关联知识产权（论文*4+技术标准*2） 成果
     所属实验室 所属团队'''
    commonUseRelationMore = [
                             "relation_leading_unit",
                             "relation_intellectual_property",
                             "relation_technical_standard",
                             "relation_achievement",
                             ]
    
    # 在一级中的first_res中查找 first_res就是一级  实体属性 其他是在一级中查询的详情都需要注意 不要放在属性中
    # propertiesName中只有基本信息里的内容
    '''
    专家没有基本信息 所以不显示 '''
    propertiesName = {
        "entity_unit": []
    }
    
    # 对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese = {
        "workunit": "工作单位",
        "team": "所属团队",
        "laboratory": "实验室",
        
    }
    
    # 这个可能不要了 如果需要的话再说 是用做存储项目详情页面的大分类的
    resultList = {
        "entity_unit": commonUseClassificationChines
    }
    
    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification = {
        "entity_unit": commonUseRelationMore
    }
    
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, properties: dict, name: str, domain:str):
        
        self.properties = properties
        self.name = name
        self.domain = domain
    
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
    def getCorporateUnit(self,domain:str,name:str,Node:dict)->str:
    #     domain 是实体类型编码 那么是项目名称
    # 需要查合作单位 只有科技项目-国网项目才有承担项目
        res=""
        if domain=="entity_project_kjgw":
            res=Node.get("entity_project_kjgw_undertaking_unit")
        return res
    
    
    
    def processingClassification(self, nodes: list, relations: list) -> dict:
        #         返回一个dict
        #         对详情页面的分类进行处理
        #         传入second_res的"node"对应的二级结点列表
        eachNode: dict
        nodesMap = dp.SearchEngineDetailsProcessing.MapNodeRelations(nodes)
        BaseInforamtion = self.properties
        unitIntellectual = []  # 详情页面中知识产权的返回结果
        unitAchievement = []  # 详情页面成功的返回结果
        unitLeadingProject = []  # 详情页面的牵头项目返回结果

        
        # 遍历每一个二级关系
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain = eachNode.get("domain", "")  # 当前结点的实体类型
            eachNodeGid = eachNode.get("gid", "")  # TODO:gid不存在的话直接返回
            eachNodeName = eachNode.get("name", "")  # 结点名称
            relationEn = relationNode.get("name", "")  # 关系英文名
            relationCn = relationNode.get("Chinese", "")  # 关系中文名
            planYear=   eachNode.get("plan_year","")   #计划年度
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            # 如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailUnit.detailsClassification[self.domain]:
                # 如果结点与二级结点的关系是我们需要的 在DetailProject.detailsClassification[self.domain] 里面

                logger.info(
                    "单位--{}({})--{} --gid:{} --domain:{} --name:{}".format(relationCn, eachNodeDomainChinese,
                                                                             relationEn,
                                                                             eachNodeGid, eachNodeDomain, eachNodeName))
                if eachNodeDomain in self.graph_types_map["知识产权"]:
                    # 知识产权详情页面
                    # 如果当前结点的关联关系在该节点需要的关联关系内 而且结点名称（实体类型）属于知识产权的话 那么就放入知识产权的详细列表中
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    tempRes = {
                        "type":domainChineseName,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    unitIntellectual.append(tempRes)  # 加入知识产权的列表 列表嵌套字典
                
                if eachNodeDomain in self.graph_types_map["项目"] :
                    # 如果是牵头项目
                    
                    unitCategoryNameCode = eachNodeDomain  # 获取category的属性编码
                    
                    unitCategoryName = self.graph_types_map_reverse[unitCategoryNameCode]  # 获取编码对应的项目类型
                    unitCategoryNameKey = unitCategoryName.replace("项目-", "", 1)
                    
                    eachLeddingProject = {
                        "type": unitCategoryNameKey,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid,
                        "workUnit":self.getCorporateUnit(self.domain,self.name,eachNode),  #获得合作单位
                        "year": planYear
                    }  # 结点名称 存储为字典
                    unitLeadingProject.append(eachLeddingProject)  # 加入数组
                
                
                if eachNodeDomain in self.graph_types_map["成果"]:
                    # 如果是成果
                    domainChineseName = self.graph_types_map_reverse[eachNodeDomain]
                    domainChineseNameKey=domainChineseName.replace("成果库-",'',1)
                    tempRes = {
                        "type": domainChineseNameKey,
                        "name": eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    unitAchievement.append(tempRes)  # 加入成果的列表 列表嵌套字典
                

        
        # BaseInforamtionProcessed = self.BaseInformationProcessing(domain=self.domain, BaseInformation=BaseInforamtion)
        
        '''
        参与知识产权 参与成果 参与项目 参与评审项目 title(name,workUnit team Lab)'''
        res = {
        
            "unitIntellectual": unitIntellectual,
            "unitAchievement": unitAchievement,
            "unitLeadingProject": unitLeadingProject,
            "unitTitle": {
                "unitName": self.name,
            }
            
        }  # 最终的所有返回结果
        return res





