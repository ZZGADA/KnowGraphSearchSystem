from  static.graph_const import GraphConst
from config import logging_config
from service.SearchEngineDetails import DetailsProcessing as dp
logger = logging_config.logging_self_define().log(level='INFO',name="DetailsProject.py")
from static.graph_const import GraphConst

class DetailProject:
    # 注意现在项目一共有五个 每个项目的全部给我分开写死 屮
    
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    graph_const_example=GraphConst()
    graph_types_map=graph_const_example.get_graph_types_map()
    graph_types_map_reverse=graph_const_example.get_graph_types_map_reverse()
    
    #多个返回结果的分类
    commonUseClassificationChines=["标题","基本信息","研究内容","预期目标","知识产权","附件材料"]
    #详情页面较多的关系
    '''
    关联实验室 关联参与人员 关联评审专家  关联知识产权（论文*4+技术标准*2） 关联创新团队  项目负责人 项目牵头单位'''
    commonUseRelationMore=["relation_laboratory",
                           "relation_participation",
                            "relation_review_experts",
                           "relation_intellectual_property",
                            "relation_team",
                           "relation_technical_standard",
                           "relation_project_leader",
                           "relation_leading_unit"]
    #详情页面较少的关系
    '''
    关联 知识产权 （论文*4+技术标准*2） 项目牵头人 项目牵头单位'''
    commonUseRelationLess=["relation_intellectual_property",
                           "relation_technical_standard",
                            "relation_project_leader",
                           "relation_leading_unit"]
    
    
    # 在一级中的first_res中查找 first_res就是一级  实体属性 其他是在一级中查询的详情都需要注意 不要放在属性中
    # propertiesName中只有基本信息里的内容
    '''
    项目类型 项目编码 项目负责人 项目牵头单位 项目开始时间 项目结束时间 项目预期目标
    项目参与人员 项目评审专家 因为是个数组就直接添加了 单独的 注意一下就好 '''
    propertiesName={
        "entity_project_kjgw":["entity_project_kjgw_category","entity_project_kjgw_number",
                               "entity_project_kjgw_leader","entity_project_kjgw_leading_unit",
                               "entity_project_kjgw_time_on","entity_project_kjgw_enddate",
                               "entity_project_kjgw_participants","entity_project_kjgw_review_experts",
                               "entity_project_kjgw_team","entity_project_kjgw_laboratory"
                               ],
        
        "entity_project_kjsgs":["entity_project_kjsgs_category","entity_project_kjsgs_number",
                               "entity_project_kjsgs_leader","entity_project_kjsgs_leading_unit",
                               "entity_project_kjsgs_time_on","entity_project_kjsgs_enddate",
                                "entity_project_kjsgs_team","entity_project_kjsgs_participants",
                                "entity_project_kjsgs_review_experts","entity_project_kjsgs_laboratory"
                                ],
        
        
        "entity_project_qc":["entity_project_qc_category","entity_project_qc_number",
                               "entity_project_qc_leader","entity_project_qc_leading_unit",
                               "entity_project_qc_time_on","entity_project_qc_enddate"],
        
        "entity_project_sczj":["entity_project_sczj_category","entity_project_sczj_number",
                               "entity_project_sczj_leader","entity_project_sczj_leading_unit",
                               "entity_project_sczj_time_on","entity_project_sczj_enddate"],
        
        
        "entity_project_scjj":["entity_project_scjj_category","entity_project_scjj_number",
                               "entity_project_scjj_leader","entity_project_scjj_leading_unit",
                               "entity_project_scjj_time_on","entity_project_scjj_enddate"]
    }
 
    #对BaseInformation 的后处理 lstrip掉domain的名字 然后写出中文
    propertiesNameChinese={
        "category":"项目类型",
        "number":"项目编码",
        "leader":"项目负责人",
        "leading_unit":"牵头单位",
        "time_on":"项目开始时间",
        "enddate":"项目结束时间",
        "laboratory":"实验室",
        "participants":"参与人员",
        "review_experts":"评审专家",
        "team":"创新团队"
        
    }
    
    #这个可能不要了 如果需要的话再说 是用做存储项目详情页面的大分类的
    resultList={
        "entity_project_kjgw":["标题","基本信息","研究内容","知识产权","附件材料"],
        "entity_project_kjsgs":commonUseClassificationChines,
        "entity_project_qc":commonUseClassificationChines,
        "entity_project_sczj":commonUseClassificationChines,
        "entity_project_scjj":commonUseClassificationChines,
    }
    


    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    
    # 存放关联关系
    detailsClassification={
        "entity_project_kjgw":commonUseRelationMore,
        
        "entity_project_kjsgs":commonUseRelationMore,
        "entity_project_qc":commonUseRelationLess,
        "entity_project_sczj":commonUseRelationLess,
        "entity_project_scjj":commonUseRelationLess,
        
    }
    # graph_types_map_reverse:dict=GraphConst().get_graph_types_map_reverse()  #获取实体类型编码 和实体类型名称的一一对应的字典  单例对象

    def __init__(self,properties:dict,content:str,name:str,keywords:list,annex,domain,exceptions):
        # TODO:project_content这里面的内容 好像需要处理 暂时先不做处理
        self.properties=properties
        self.content=content
        self.name=name
        self.keywords=keywords
        self.annex=annex
        self.domain=domain
        self.exceptions=exceptions
        
        
    def BaseInformationProcessing(self,domain:str,BaseInformation:dict):
        #BaseInformation 是项目的基本信息  以字典的形式存储者每一个属性以及关联关系得到的新属性
        # 接下来是遍历 然后添加中文
        #返回结果 列表嵌套字典
        res=[]
        target=domain+"_"
        for k,v in BaseInformation.items():
            tempRes={}
            # lstrip的运行机制：如果你传给他一个字符串, 那么它会从左到右挨个检查变量的字符, 如果在你给的参数内, 则删除这个字符, 直到出现不符合条件的字符才停止
            newKey=k.replace(target,"",1)
            # print(newKey,k,target)
            chinese=self.propertiesNameChinese[newKey]
            tempRes["chinese"]=chinese
            tempRes["value"]=v
            tempRes["propertyCode"]=k
            res.append(tempRes)
        return res
        
        
    
    def processingClassification(self,nodes:list,relations:list)->dict:
#         返回一个dict
#         对详情页面的分类进行处理
#         传入second_res的"node"对应的二级结点列表
        eachNode:dict
        nodesMap=dp.SearchEngineDetailsProcessing.MapNodeRelations(nodes)
        BaseInforamtion=self.properties
        projectIntellectual=[] # 详情页面中知识产权的返回结果


        # 遍历每一个二级结点
      
        for relationNode in relations:
            targetGid = relationNode["end"]  # 根据属性获取二级目标gid
            eachNode = nodesMap[targetGid]  # 获取目标结点
            
            eachNodeDomain=eachNode.get("domain","")  #当前结点的实体类型
            eachNodeGid=eachNode.get("gid","") #TODO:gid不存在的话直接返回
            eachNodeName=eachNode.get("name","")  #结点名称
            eachNodeNameAppend=";"+eachNodeName
            relationEn=relationNode.get("name","") #关系英文名
            relationCn=relationNode.get("Chinese","") #关系中文名
            eachNodeDomainChinese = self.graph_types_map_reverse[eachNodeDomain]
            
            #如果我需要的关系在当前结点需要的关系中 那么进入
            if relationEn in DetailProject.detailsClassification[self.domain] :
                logger.info(
                    "项目--{}--{} --gid:{} --domain --name".format(relationCn,
                                                                   eachNodeDomainChinese,
                                                                   eachNodeGid,
                                                                   eachNodeDomain,
                                                                   eachNodeName))
                if eachNodeDomain in self.graph_types_map["知识产权"]:
                    # 如果当前结点的关联关系在该节点需要的关联关系内 而且结点名称（实体类型）属于知识产权的话 那么就放入知识产权的详细列表中
                    domainChineseName=self.graph_types_map_reverse[eachNodeDomain]
                    tempRes={
                        "type":domainChineseName,
                        "name":eachNodeName,
                        "domain":eachNodeDomain,
                        "gid":eachNodeGid
                    }
                    projectIntellectual.append(tempRes)   #加入知识产权的列表 列表嵌套字典
                    
                # 上面是知识产权类的详情分类
                if eachNodeDomain in self.graph_types_map["实验室"]:
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey=self.domain+"_laboratory"
                    if type(BaseInforamtion[tempKey][0]) == str:
                        BaseInforamtion[tempKey].pop(0)
                        
                    tempNode={
                        "gid":eachNodeGid,
                        "name":eachNodeName
                    }
        #             如果在实验室中
                    BaseInforamtion[self.domain+"_laboratory"].append(tempNode)

                #参与人员
                if eachNodeDomain in self.graph_types_map["专家"] and relationEn=="relation_participation":
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey=self.domain+"_participants"
                    # if type(BaseInforamtion[tempKey][0]) == str:
                    #     BaseInforamtion[tempKey].pop(0)
                        
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }

                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempKey],tempNode)

                    # #如果是参与人员
                    # BaseInforamtion[tempKey].append(tempNode)

                 #评审专家
                if eachNodeDomain in self.graph_types_map["专家"] and relationEn=="relation_review_experts":
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey=self.domain + "_review_experts"
                    # if type(BaseInforamtion[tempKey][0]) == str:
                    #     BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    #如果是评审人员
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempKey], tempNode)
                    # BaseInforamtion[tempKey].append(tempNode)

                #项目负责人
                if eachNodeDomain in self.graph_types_map["专家"] and relationEn=="relation_project_leader":
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey = self.domain + "_leader"
                    # if type(BaseInforamtion[tempKey][0]) == str:
                    #     BaseInforamtion[tempKey].pop(0)
                        
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    #如果是项目负责人
                    dp.SearchEngineDetailsProcessing.ExpertListProcessing(BaseInforamtion[tempKey], tempNode)
                    # BaseInforamtion[tempKey].append(tempNode)
                    
                if eachNodeDomain in self.graph_types_map["团队"]:
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey = self.domain + "_team"
                    if type(BaseInforamtion[tempKey][0]) == str:
                        BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    #如果是团队
                    BaseInforamtion[tempKey].append(tempNode)
                
                if eachNodeDomain in self.graph_types_map["单位"]:
                    
                    # 如果是根据关系类型获取数据的话 如果列表index 0 为字符串（有属性不为空的情况 所以需要通过类型判断）
                    # 那么就移除掉
                    tempKey = self.domain + "_leading_unit"
                    if type(BaseInforamtion[tempKey][0]) == str:
                        BaseInforamtion[tempKey].pop(0)
                    
                    tempNode = {
                        "gid": eachNodeGid,
                        "name": eachNodeName
                    }
                    
                    #如果是 牵头单位
                    BaseInforamtion[tempKey].append(tempNode)
            

        #格式化
        BaseInforamtionProcessed=dp.SearchEngineDetailsProcessing.BaseInformationProcessing(domain=self.domain,
                                                                                            BaseInformation=BaseInforamtion,
                                                                                            propertiesNameChinese=self.propertiesNameChinese)

        res = {
            "projectIntellectual": projectIntellectual,
            "projectAnnex": self.annex,
            "projectContent": self.content,  # 详情页面中研究内容的返回结果
            "projectTitle": {
                "projectName":self.name,
                "projectKeywords": self.keywords
            },
            "projectBasicInformation": BaseInforamtionProcessed,
            "projectException":self.exceptions
        }  # 最终的所有返回结果
        return res
        
        
