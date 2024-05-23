"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 存储图数据库相关的全局常量

"""

import time


'''

class GraphConst:


    """搜索引擎搜索"""

    # 查询id号
    id = 0
    # 搜索引擎的主题选项关键词的最大数量
    themes_limit = 5

    # 搜索引擎的公司选项关键词的最大数量
    companies_limit = 5

    # 每页结果显示的个数
    per_page_limit = 5

    # 搜索引擎首页热词显示的个数
    buzzwords_limit = 5

    # 搜索引擎提示词显示的个数
    tips_limit = 10

    # 存储搜索引擎的时间选项关键词
    times = []

    # 存储节点对应的相关时间属性(对于有时间属性的类文件节点)
    times_properties = {
        "entity_project_kj": "time",
        "entity_technical_standard": "declare_year",
        "entity_intellectual_property_paper": "zscqlw_achievement_Reportingyear",
        "entity_intellectual_property_software_works": "zscqrjzz_achievement_Reportingyear",
        "entity_intellectual_property_patent": "zscqzl_achievement_reportingyear",
        "entity_intellectual_property_monograph": "zscqzz_achievement_reportingyear",
    }

    # 存储搜索引擎的类型选项关键词
    types = [
        "项目",
        "专利",
        "论文",
        "技术标准",
        "软著",
        "成果"
    ]

    # 存储搜索引擎的type中文名和对应节点名的映射关系
    types_map = {
        "项目": ["entity_project_kj"],
        "专利": ["entity_intellectual_property_patent"],
        "论文": ["entity_intellectual_property_paper"],
        "技术标准": ["entity_technical_standard"],
        "软著": ["entity_intellectual_property_software_works"],
        "专著": ["entity_intellectual_property_monograph"],
        "成果": ["entity_achievement_sbj", "entity_achievement_qt", "entity_achievement_sgs_bz",
                 "entity_achievement_sgs_kxkj", "entity_achievement_sgs_jsfm", "entity_achievement_sgs_zl"]
    }

    # 存储节点对应的相关主题属性(对于有主题属性的类文件节点)
    themes_properties = {
        "entity_project_kj": ["name", "project_content"],
        "entity_intellectual_property_paper": ["name"],
        "entity_intellectual_property_software_works": ["name"],
        "entity_intellectual_property_patent": ["name"],
        "entity_intellectual_property_monograph": ["name"],
        "entity_technical_standard": ["name"],
        "entity_achievement_sbj": ["name"],
        "entity_achievement_qt": ["name"],
        "entity_achievement_sgs_bz": ["name"],
        "entity_achievement_sgs_kxkj": ["name"],
        "entity_achievement_sgs_jsfm": ["name"],
        "entity_achievement_sgs_zl": ["name"]
    }

    # TODO
    # 存储主题属性的类型
    themes_type = {
        "entity_project_kj": "string",
        "entity_intellectual_property_paper": "string",
        "entity_intellectual_property_software_works": "string",
        "entity_intellectual_property_patent": "string",
        "entity_intellectual_property_monograph": "string",
        "entity_technical_standard": "string",
        "entity_achievement_sbj": "string",
        "entity_achievement_qt": "string",
        "entity_achievement_sgs_bz": "string",
        "entity_achievement_sgs_kxkj": "string",
        "entity_achievement_sgs_jsfm": "string",
        "entity_achievement_sgs_zl": "string"
    }

    # 预设主题关键词
    predetermined_themes_list = [
        "电网形态与规划",
        "电网分析与控保",
        "电力系统自动化",
        "输变电器件与装备",
        "输变电工程设计施工与环保",
        "输变电设备运维",
        "配电网与分布式电源",
        "用电能效与综合能源",
        "大规模新能源并网控制",
        "储能本体及并网控制",
        "电力通信",
        "电力信息与网络安全",
        "电工新材料",
        "传感与量测",
        "人工智能",
        "电力芯片",
        "决策支持",
        "能源发展与企业管理技术",
        "输变电设备运行与防灾技术",
        "电力系统自动化技术",
        "电网发展与规划技术",
        "信息通信及安全技术",
        "用电能效与电动汽车技术",
        "大规模新能源发电并网与运行控制技术",
        "储能技术",
        "电网安全控制与保护技术",
        "电网安全分析与仿真技术",
        "配电网及分布式电源并网技术",
        "输变电工程设计施工与环保技术",
        "输变电装备技术",
        "电测量技术",
        "超/特高压输变电技术",
        "新材料与器件技术",
        "技术标准",
        "战略性前瞻技术",
        "储能与能源转化",
        "大电网安全控制",
        "电力市场化机制",
        "能源互联网商业模式",
        "输变电装备",
        "主动配电网及用户互动",
        "知识产权",
        "群众性创新",
        "电力市场技术",
        "电网运行管理技术",
        "配电网技术",
        "输电线路在线监测技术",
        "综合能源",
        "3060双碳与综合能源",
        "电力信息技术",
        "新能源接入及分布式供电技术",
        "研究开发",
        "源网荷储协调",
        "其他",
        "实验室项目"
    ]

    # 存储节点对应的相关公司属性(对于有公司属性的类文件节点)
    companies_properties = {
        "entity_project_kj": "lead_unit",
        "entity_technical_standard": "first_unit_name",
        "entity_intellectual_property_patent": "zscqzl_achievement_patentee",  # 多个、
    }

    # 存储节点对应的相关专家属性(对于有公司属性的类文件节点)
    experts_properties = {
        "entity_intellectual_property_paper": "zscqlw_achievement_author",
        "entity_intellectual_property_patent": "zscqzl_achievement_designer",  # 多个;
        "entity_intellectual_property_monograph": "zscqzz_achievement_mainauthor",
    }

    """知识图谱搜索"""

    # 知识图谱搜索初始显示个数
    nodes_init_limit = 30

    # 存储知识图谱的type中文名和对应节点名的映射关系
    graph_types_map = {
        "项目": ["entity_project_kj"],
        "专利": ["entity_intellectual_property_patent"],
        "论文": ["entity_intellectual_property_paper"],
        "技术标准": ["entity_technical_standard"],
        "软著": ["entity_intellectual_property_software_works"],
        "专著": ["entity_intellectual_property_monograph"],
        "成果": ["entity_achievement_sbj", "entity_achievement_qt", "entity_achievement_sgs_bz",
                 "entity_achievement_sgs_kxkj", "entity_achievement_sgs_jsfm", "entity_achievement_sgs_zl"],
        "单位": ["entity_unit"],
        "专家": ["entity_expert"],
        "团队": ["entity_team"],
        "实验室": ["entity_laboratory"]
    }

    # 存储知识图谱的关系和对应的中文名的映射关系
    graph_chinese_types = {
        "relation_invent": "拥有",
        "relation_belong_to": "属于",
        "relation_participate_in": "参与",
        "relation_colleague": "同事",
        "relation_review": "评审",
        "relation_support": "支撑",
        "reletion_obtain": "获得",
        "reletion_generate": "产生",
        "reletion_draft": "起草",
        "reletion_lead": "牵头",
        "relation_design": "发明设计",
        "contain": "包含",
        "relation_rely_on": "依托"
    }






    """以下为获取相应常量的函数(进行过后处理)"""

    def get_updated_id(self):
        self.id = self.id + 1
        return self.id

    def get_times(self):
        new_times=[]

        cur_time = int(time.localtime().tm_year)

        for i in range(3):
            string = str(cur_time - i) + "年"
            new_times.append(string)

        string = str(cur_time - 2) + "年以前"
        new_times.append(string)

        return new_times

    def get_times_properties(self):
        return self.times_properties

    def get_types(self):
        new_types = [
        "项目",
        "专利",
        "论文",
        "技术标准",
        "软著",
        "成果"
    ]
        return new_types

    def get_types_map(self):
        return self.types_map

    def get_relationships(self):
        return self.relationships

    def get_themes_properties(self):
        return self.themes_properties

    def get_themes_type(self):
        return self.themes_type

    def get_themes_limit(self):
        return self.themes_limit

    def get_predetermined_themes_list(self):
        return self.predetermined_themes_list

    def get_companies_limit(self):
        return self.companies_limit

    def get_companies_properties(self):
        return self.companies_properties

    def get_experts_properties(self):
        return self.experts_properties

    def get_per_page_limit(self):
        return self.per_page_limit

    def get_buzzwords_limit(self):
        return self.buzzwords_limit

    def get_tips_limit(self):
        return self.tips_limit

    def get_graph_types_map(self):
        return self.graph_types_map

    def get_nodes_init_limit(self):
        return self.nodes_init_limit

    def get_graph_chinese_types(self):
        return self.graph_chinese_types

    def get_types_count(self):
        return self.info["types_count"]

'''

# LLH: 全部修改
class GraphConst:
    """搜索引擎搜索"""

    info = {
        # 查询id号
        "id": 0,

        # 搜索引擎的主题选项关键词的最大数量
        "themes_limit": 5,

        # 搜索引擎的公司选项关键词的最大数量
        "companies_limit": 5,

        # 每页结果显示的个数
        "per_page_limit": 5,

        # 搜索引擎首页热词显示的个数
        "buzzwords_limit": 5,

        # 搜索引擎提示词显示的个数
        "tips_limit": 10,

        # 存储搜索引擎的时间选项关键词
        "times": [],

        # 知识图谱搜索初始显示个数
        "nodes_init_limit": 30,

        # 存储搜索引擎的类型选项关键词
        "types": [
            "项目",
            "专利",
            "论文",
            "技术标准",
            "软著",
            "专著",
            "成果"
        ],

        # 存储搜索引擎的type中文名和对应节点名的映射关系
        # "省公司标准": ["entity_technical_standard"],
        "types_map": {
            "项目": ["entity_project_kjgw", "entity_project_kjsgs", "entity_project_qc", "entity_project_scjj", "entity_project_sczj"],
            "专利": ["entity_intellectual_property_patent"],
            "论文": ["entity_intellectual_property_paper"],
            "技术标准": ["entity_process_standard","entity_technical_standard"],
            "软著": ["entity_intellectual_property_software_works"],
            "专著": ["entity_intellectual_property_monograph"],
            "成果": ["entity_achievement_sbj", "entity_achievement_qt", "entity_achievement_sgs_bz",
                     "entity_achievement_sgs_kxkj", "entity_achievement_sgs_jsfm", "entity_achievement_sgs_zl"]
        },

        # 存储主题属性的类型
        "themes_type": {
            "entity_project_kjgw": "string",
            "entity_project_kjsgs": "string",
            "entity_project_qc": "string",
            "entity_project_scjj": "string",
            "entity_project_sczj": "string",
            "entity_intellectual_property_paper": "string",
            "entity_intellectual_property_software_works": "string",
            "entity_intellectual_property_patent": "string",
            "entity_intellectual_property_monograph": "string",
            "entity_technical_standard": "string",
            "entity_process_standard": "string",
            "entity_achievement_sbj": "string",
            "entity_achievement_qt": "string",
            "entity_achievement_sgs_bz": "string",
            "entity_achievement_sgs_kxkj": "string",
            "entity_achievement_sgs_jsfm": "string",
            "entity_achievement_sgs_zl": "string",
            "entity_team": "string",
            "entity_laboratory": "string"
        },

        # 预设主题关键词
        "predetermined_themes_list": [
            "电网形态与规划",
            "电网分析与控保",
            "电力系统自动化",
            "输变电器件与装备",
            "输变电工程设计施工与环保",
            "输变电设备运维",
            "配电网与分布式电源",
            "用电能效与综合能源",
            "大规模新能源并网控制",
            "储能本体及并网控制",
            "电力通信",
            "电力信息与网络安全",
            "电工新材料",
            "传感与量测",
            "人工智能",
            "电力芯片",
            "决策支持",
            "能源发展与企业管理技术",
            "输变电设备运行与防灾技术",
            "电力系统自动化技术",
            "电网发展与规划技术",
            "信息通信及安全技术",
            "用电能效与电动汽车技术",
            "大规模新能源发电并网与运行控制技术",
            "储能技术",
            "电网安全控制与保护技术",
            "电网安全分析与仿真技术",
            "配电网及分布式电源并网技术",
            "输变电工程设计施工与环保技术",
            "输变电装备技术",
            "电测量技术",
            "超/特高压输变电技术",
            "新材料与器件技术",
            "技术标准",
            "战略性前瞻技术",
            "储能与能源转化",
            "大电网安全控制",
            "电力市场化机制",
            "能源互联网商业模式",
            "输变电装备",
            "主动配电网及用户互动",
            "知识产权",
            "群众性创新",
            "电力市场技术",
            "电网运行管理技术",
            "配电网技术",
            "输电线路在线监测技术",
            "综合能源",
            "3060双碳与综合能源",
            "电力信息技术",
            "新能源接入及分布式供电技术",
            "研究开发",
            "源网荷储协调",
            "其他",
            "实验室项目"
        ],
        

        # 存储知识图谱的type中文名和对应节点名的映射关系
        "graph_types_map": {
            "专家名称": ["entity_expert"],
            "专家":["entity_expert"],
            "项目": ["entity_project_kjgw",
                     "entity_project_kjsgs",
                     "entity_project_qc",
                     "entity_project_scjj",
                     "entity_project_sczj"]
            ,
            "项目名称": ["entity_project_kjgw",
                         "entity_project_kjsgs",
                         "entity_project_qc",
                         "entity_project_scjj",
                         "entity_project_sczj"],
            "知识产权": [
                "entity_technical_standard","entity_process_standard",
                "entity_intellectual_property_patent",
                "entity_intellectual_property_software_works",
                "entity_intellectual_property_monograph",
                "entity_intellectual_property_paper"],
            
            
            "成果": ["entity_achievement_sbj",
                     "entity_achievement_qt",
                     "entity_achievement_sgs_bz",
                     "entity_achievement_sgs_kxkj",
                     "entity_achievement_sgs_jsfm",
                     "entity_achievement_sgs_zl"],
            "专利": ["entity_intellectual_property_patent"],
            "论文": ["entity_intellectual_property_paper"],
            "技术标准": ["entity_process_standard", "entity_technical_standard"],
            "软著": ["entity_intellectual_property_software_works"],
            "专著": ["entity_intellectual_property_monograph"],
            "单位": ["entity_unit"],
            "团队": ["entity_team"],
            "实验室": ["entity_laboratory"],
            "expert": ["entity_expert"],
            "company": ["entity_unit"],
       
        },

        # 每个结点对应的实体类型名称
        "graph_types_map_reverse":{
            "entity_project_qc":"项目-群创项目",
            "entity_project_sczj":"项目-双创资金类项目",
            "entity_project_scjj":"项目-双创基金类项目",
            "entity_project_kjgw":"项目-科技国网项目",
            "entity_project_kjsgs":"项目-科技省公司项目",
            "entity_intellectual_property_patent":"专利" ,
            "entity_intellectual_property_paper":"论文",
            "entity_technical_standard":"技术标准",
            "entity_process_standard": "技术标准",
            "entity_intellectual_property_software_works": "软著",
            "entity_intellectual_property_monograph":"专著",
            "entity_achievement_sbj":"成果库-省部级及以上成果",
            "entity_achievement_sgs_kxkj":"成果库-省公司成果-科学科技进步类",
            "entity_achievement_sgs_jsfm":"成果库-省公司成果-技术发明类",
            "entity_achievement_sgs_bz":"成果库-省公司成果-标准类",
            "entity_achievement_sgs_zl":"成果库-省公司成果-专利类",
            "entity_achievement_qt":"成果库-其他成果",
            "entity_unit":"单位",
            "entity_expert":"专家",
            "entity_team":"团队",
            "entity_laboratory":"实验室"
        },
        

        # 存储知识图谱的关系和对应的中文名的映射关系
        "graph_chinese_types": {
            "relation_project": "项目",
            "relation_lead_project": "牵头项目",
            "relation_review_items": "评审项目",
            "relation_unit": "单位",
            "relation_leading_unit": "牵头单位",
            "relation_intellectual_property": "知识产权",
            "relation_laboratory": "实验室",
            "relation_team": "团队",
            "relation_technical_standard": "技术标准",
            "relation_expert": "专家",
            "relation_achievement": "成果",
            "relation_project_leader": "项目负责人",
            "relation_participation": "参与人员",
            "relation_main_completion_personnel": "主要完成人",
            "relation_completion_unit": "完成单位",
            "relation_other_complainants": "其他完成人",
            "relation_main_drafter": "主要起草人",
            "relation_drafting_unit": "起草单位",
            "relation_other_drafters": "其他起草人",
            "relation_invention_designer": "发明设计人",
            "relation_patentee": "专利权人",
            "relation_author_name": "作者姓名",
            "relation_author_rights_holder": "著作权人",
            "relation_lead_author": "主要作者",
            "relation_drafter": "起草人",
            "relation_prepared_by": "编制单位",
            "relation_laboratory_director": "实验室主任",
            "relation_supporting unit": "依托单位",
            "relation_main_member": "主要成员",
            "relation_team_leader": "团队带头人",
            "relation_backbone_members": "骨干成员",
            "relation_members": "成员",
            "relation_technical_advisor": "技术顾问",
            "relation_invent": "拥有",
            "relation_belong_to": "属于",
            "relation_participate_in": "参与",
            "relation_colleague": "同事",
            "relation_review": "评审",
            "relation_support": "支撑",
            "reletion_obtain": "获得",
            "reletion_generate": "产生",
            "reletion_draft": "起草",
            "reletion_lead": "牵头",
            "relation_design": "发明设计",
            "contain": "包含",
            "relation_rely_on": "依托"
        },

        # 存储搜索引擎首页的统计数据
        "types_count": {
            "项目资源": ["entity_project_qc",
                         "entity_project_sczj",
                         "entity_project_scjj",
                         "entity_project_kjgw",
                         "entity_project_kjsgs"],
            "专家资源": ["entity_expert"],
            "知识产权资源": ["entity_intellectual_property_patent", "entity_intellectual_property_software_works",
                             "entity_intellectual_property_monograph", "entity_intellectual_property_paper",
                             "entity_technical_standard", "entity_process_standard"],
            "成果资源": ["entity_achievement_sbj", "entity_achievement_qt", "entity_achievement_sgs_bz",
                         "entity_achievement_sgs_kxkj", "entity_achievement_sgs_jsfm", "entity_achievement_sgs_zl"]
        },

        # 存储节点对应的相关主题属性(对于有主题属性的类文件节点)
        "themes_properties": {
            "entity_project_qc": ["name", "entity_project_qc_content"],
            "entity_project_sczj": ["name", "entity_project_sczj_contents"],
            "entity_project_scjj": ["name", "entity_project_scjj_contents"],
            "entity_project_kjgw": ["name", "entity_project_kjgw_content"],
            "entity_project_kjsgs": ["name", "entity_project_kjsgs_content"],
            "entity_intellectual_property_paper": ["name"],
            "entity_intellectual_property_software_works": ["name"],
            # 0509:
            "entity_intellectual_property_patent": ["name", "zscqzl_achievement_awards_info"],
            "entity_intellectual_property_monograph": ["name"],
            "entity_technical_standard": ["name", "entity_technical_standard_significance"],
            "entity_process_standard": ["name"],
            "entity_achievement_sbj": ["name", "sbj_achievement_introduction"],
            "entity_achievement_sgs_bz": ["name", "cxgx_achievement_synopsis"],
            "entity_achievement_sgs_jsfm": ["name", "jsfm_achievement_synopsis"],
            "entity_achievement_sgs_kxkj": ["name", "kjjb_achievement_synopsis"],
            "entity_achievement_qt": ["name", "qt_achievement_introduction"],
            "entity_achievement_sgs_zl": ["name", "zl_achievement_recommendations"],
            "entity_team": ["name", "entity_team_tackling_direction"],
            "entity_laboratory": ["name", "entity_laboratory_research_direction"]
        },
    
        # 存储节点对应的相关时间属性(对于有时间属性的类文件节点)
        "times_properties": {
            "entity_project_qc": "plan_year",
            "entity_project_sczj": "plan_year",
            "entity_project_scjj": "plan_year",
            "entity_project_kjgw": "plan_year",
            "entity_project_kjsgs": "plan_year",
            "entity_technical_standard": "entity_technical_standard_time",
            "entity_process_standard": "entity_process_standard_time",
            "entity_intellectual_property_paper": "zscqlw_achievement_frequencyofpublication",
            "entity_intellectual_property_software_works": "zscqrjzz_achievement_dateoffirstpublication",
            "entity_intellectual_property_patent": "zscqzl_achievement_authorizationdate",
            "entity_intellectual_property_monograph": "zscqzz_achievement_pubdate",
            "entity_achievement_sbj": "ach_year",
            "entity_achievement_sgs_bz": "ach_year",
            "entity_achievement_sgs_jsfm": "ach_year",
            "entity_achievement_sgs_kxkj": "ach_year",
            "entity_achievement_sgs_zl": "ach_year",
            "entity_achievement_qt": "ach_year",
        },

        # 存储节点对应的相关公司属性(对于有公司属性的类文件节点)
        "companies_properties": {
            "entity_project_qc": "entity_project_qc_leading_unit",
            "entity_project_sczj": "entity_project_sczj_leading_unit",
            "entity_project_scjj": "entity_project_scjj_leading_unit",
            "entity_project_kjgw": "entity_project_kjgw_leading_unit",
            "entity_project_kjsgs": "entity_project_kjsgs_leading_unit",
            "entity_technical_standard": "entity_technical_standard_draft_by_unit",
            "entity_process_standard": "entity_process_standard_unit",
            "entity_achievement_sbj": "sbj_achievement_mainunit",
            "entity_achievement_sgs_bz": "cxgx_achievement_draftingunit",
            "entity_achievement_sgs_jsfm": "jsfm_achievement_completeunit",
            "entity_achievement_sgs_kxkj": "kjjb_achievement_completeunit",
            "entity_achievement_sgs_zl": "zl_achievement_patentee",
            "entity_achievement_qt": "qt_achievement_mainunit",
            "entity_intellectual_property_software_works": "zscqrjzz_achievement_reportunit",
            "entity_intellectual_property_patent": "zscqzl_achievement_patentee",
            "entity_intellectual_property_monograph": "zscqzz_achievement_authorunit",
            "entity_intellectual_property_paper": "zscqlw_achievement_firstauthorunit"
        },

        # 存储节点对应的相关专家属性(对于有公司属性的类文件节点)
        "experts_properties": {
            "entity_project_qc": "entity_project_qc_leader",
            "entity_project_sczj": "entity_project_sczj_leader",
            "entity_project_scjj": "entity_project_scjj_leader",
            "entity_project_kjgw": "entity_project_kjgw_leader",
            "entity_project_kjsgs": "entity_project_kjsgs_leader",
            "entity_achievement_sbj": "sbj_achievement_principalpersonnel",
            "entity_achievement_sgs_bz": "cxgx_achievement_rapporteur",
            "entity_achievement_sgs_jsfm": "jsfm_achievement_principal",
            "entity_achievement_sgs_kxkj": "kjjb_achievement_principal",
            "entity_achievement_sgs_zl": "zl_achievement_designer",
            "entity_achievement_qt": "qt_achievement_principalpersonnel",
            "entity_intellectual_property_paper": "zscqlw_achievement_author",
            "entity_intellectual_property_software_works": "zscqrjzz_achievement_copyrightowner",
            "entity_intellectual_property_patent": "zscqzl_achievement_designer",
            "entity_intellectual_property_monograph": "zscqzz_achievement_mainauthor",
            "entity_technical_standard": "entity_technical_standard_draft_by",
            "entity_process_standard": "entity_process_standard_contacts"
        },
        
        "intellectualKeyMap":{
            "entity_intellectual_property_paper":"zscqlw_achievement",
            "entity_intellectual_property_software_works":"zscqrjzz_achievement",
            "entity_intellectual_property_patent":"zscqzl_achievement",
            "entity_intellectual_property_monograph":"zscqzz_achievement",
            "entity_technical_standard":"entity_technical_standard",
            "entity_process_standard":"entity_process_standard"
        
    },
        "achievementKeyMap":{
            "entity_achievement_sbj":"sbj_achievement",
            "entity_achievement_sgs_bz":"cxgx_achievement",
            "entity_achievement_sgs_jsfm":"jsfm_achievement",
            "entity_achievement_sgs_kxkj":"kjjb_achievement",
            "entity_achievement_sgs_zl":"zl_achievement",
            "entity_achievement_qt":"qt_achievement"
        },
        "achievementChineseMap":{
            "科学技术进步奖":"kxkj",
            "科学技术专利奖":"zl",
            "科学技术发明奖":"jsfm",
            "科学技术标准创新贡献奖":"bz",
        },
        "downwardCountChineseToEnglish":{
            "专家资源":"expertResources",
            "成果资源":"achievementResources",
            "知识产权资源":"intellectualResources",
            "项目资源":"projectResources",
        }
        



    }

    # 设置生成的对象为单例对象（全局只有一个实例）
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    """显示所有键值对信息"""

    def show(self):
        return [
            ["查询id号", "id", self.info["id"]],
            ["搜索引擎的主题选项关键词的最大数量", "themes_limit", self.info["themes_limit"]],
            ["搜索引擎的公司选项关键词的最大数量", "companies_limit", self.info["companies_limit"]],
            ["每页结果显示的个数", "per_page_limit", self.info["per_page_limit"]],
            ["搜索引擎首页热词显示的个数", "buzzwords_limit", self.info["buzzwords_limit"]],
            ["搜索引擎提示词显示的个数", "tips_limit", self.info["tips_limit"]],
            ["存储节点对应的相关时间属性(对于有时间属性的类文件节点)", "times_properties",
             self.info["times_properties"]],
            ["存储搜索引擎的类型选项关键词", "types", self.info["types"]],
            ["存储搜索引擎的type中文名和对应节点名的映射关系", "types_map", self.info["types_map"]],
            ["存储节点对应的相关主题属性(对于有主题属性的类文件节点)", "themes_properties",
             self.info["themes_properties"]],
            ["存储主题属性的类型", "themes_type", self.info["themes_type"]],
            ["预设主题关键词", "predetermined_themes_list", self.info["predetermined_themes_list"]],
            ["存储节点对应的相关公司属性(对于有公司属性的类文件节点)", "companies_properties",
             self.info["companies_properties"]],
            ["存储节点对应的相关专家属性(对于有公司属性的类文件节点)", "experts_properties",
             self.info["experts_properties"]],
            ["知识图谱搜索初始显示个数", "nodes_init_limit", self.info["nodes_init_limit"]],
            ["存储知识图谱的type中文名和对应节点名的映射关系", "graph_types_map", self.info["graph_types_map"]],
            ["存储知识图谱的关系和对应的中文名的映射关系", "graph_chinese_types", self.info["graph_chinese_types"]],
            ["存储搜索引擎首页的统计数据", "types_count", self.info["types_count"]],
            ["存储节点对应的相关专家属性(对于有公司属性的类文件节点)", "experts_properties", self.info["experts_properties"]],
            ["每个结点对应的实体类型名称", "graph_types_map_reverse", self.info["graph_types_map_reverse"]]
        ]

    def __getitem__(self, item):
        return self.info[item]

    def __setitem__(self, key, value):
        self.info[key] = value

    """以下为获取和更改相应常量的函数(进行过后处理)"""

    def get_updated_id(self):
        self.info["id"] = self.info["id"] + 1
        return self.info["id"]

    def get_times(self):
        # cur_time = int(time.localtime().tm_year)
        #
        # for i in range(3):
        #     string = str(cur_time - i) + "年"
        #     self.info["times"].append(string)
        #
        # string = str(cur_time - 2) + "年以前"
        # self.info["times"].append(string)
        #
        # return self.info["times"]

        new_times = []

        cur_time = int(time.localtime().tm_year)

        for i in range(3):
            string = str(cur_time - i) + "年"
            new_times.append(string)

        # string = str(cur_time - 2) + "年以前"
        string = "其他年份"
        new_times.append(string)

        return new_times

    def get_times_properties(self):
        return self.info["times_properties"]

    def get_types(self):
        new_types = [
            "项目",
            "专利",
            "论文",
            "技术标准",
            "软著",
            "专著",
            "成果"
        ]
        return new_types
        # return self.info["types"]

    def get_types_map(self):
        return self.info["types_map"]

    def get_themes_properties(self):
        return self.info["themes_properties"]

    def get_themes_type(self):
        return self.info["themes_type"]

    def get_themes_limit(self):
        return self.info["themes_limit"]

    def get_predetermined_themes_list(self):
        return self.info["predetermined_themes_list"]

    def get_companies_limit(self):
        return self.info["companies_limit"]

    def get_companies_properties(self):
        return self.info["companies_properties"]

    def get_experts_properties(self):
        return self.info["experts_properties"]

    def get_per_page_limit(self):
        return self.info["per_page_limit"]

    def get_buzzwords_limit(self):
        return self.info["buzzwords_limit"]

    def get_tips_limit(self):
        return self.info["tips_limit"]

    def get_graph_types_map(self):
        return self.info["graph_types_map"]

    def get_nodes_init_limit(self):
        return self.info["nodes_init_limit"]

    def get_graph_chinese_types(self):
        return self.info["graph_chinese_types"]

    def get_types_count(self):
        return self.info["types_count"]

    def get_graph_types_map_reverse(self):
        return self.info["graph_types_map_reverse"]
    def get_intellectualKeyMap(self):
        return self.info["intellectualKeyMap"]
    def get_achievementKeyMap(self):
        return self.info["achievementKeyMap"]
    def get_achievementChineseMap(self):
        return self.info["achievementChineseMap"]
    def get_downwardCountChineseToEnglish(self):
        return self.info["downwardCountChineseToEnglish"]