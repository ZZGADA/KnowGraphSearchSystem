from service.SearchEngineDetails.DetailsProject import DetailProject
from  static.graph_const import GraphConst
from config import logging_config
logger = logging_config.logging_self_define().log(level='INFO',name="DetailsProject.py")
class AchievementsDetails:
    #     项目的二级 有哪些 需要我们写死
    # 需要注意 现在业务描述的二级包括一级属性  如二级中的研究内容
    propertiesName = ["name", "project_content", "keywords"]  # 在一级中的first_res中查找 first_res就是一级
    # 表述详情中各个板块 基本信息不需要我们
    
    # 键是中文名 对应包含的字段
    # "研究内容":["projectContent"],
    # 针对实体部分
    detailsClassification = {
        "知识产权": [
            "entity_technical_standard",
            "entity_intellectual_property_patent",
            "entity_intellectual_property_software_works",
            "entity_intellectual_property_monograph",
            "entity_intellectual_property_paper"]  # 这里稍微复杂一点 包含了 所有知识产权的分类
        #   从上往下 技术标准 专利 软著 专著 论文 一共五个
    }
    graph_types_map_reverse: dict = GraphConst().get_graph_types_map_reverse()  # 获取实体类型编码 和实体类型名称的一一对应的字典  单例对象
    
    def __init__(self, name: str, project_content: str, keywords: list):
        self.projectName = name
        # 研究内容
        self.projectContent = project_content  # TODO:这里面的内容 好像需要处理 暂时先不做处理
        self.keywords = keywords
    
    def processingClassification(self, nodes) -> dict:
        #         返回一个dict
        #         对详情页面的分类进行处理
        #         传入second_res的"node"对应的二级结点列表
        eachNode: dict
        
        res = {
            "zscq": [],
            "projectContent": self.projectContent,  # 详情页面中研究内容的返回结果
            "projectName": self.projectName,
            "projectKeywords": self.keywords
        }  # 最终的所有返回结果
        resZSCQ = res["zscq"]  # 详情页面中知识产权的返回结果
        # 遍历每一个二级结点
        count = 0
        for eachNode in nodes:
            domain = eachNode.get("domain", "")
            resZSCQ.append(count)
            count += 1
            if domain in DetailProject.detailsClassification["知识产权"]:
                #                 看domain的数据是否在知识产权中 如果在就纳入详情页面的返回数据
                domainChineseName = DetailProject.graph_types_map_reverse[domain]
                eachNodeName = eachNode.get("name", "")
                tempRes = {domainChineseName: eachNodeName}
                resZSCQ.append(tempRes)
        return res