"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/8/18
    @Introduction: 图数据库的驱动初始化

"""

from neo4j import GraphDatabase


# 初始化函数

class ConnectToDatabase:
    @classmethod
    def init(cls):
        # 创建驱动的实例
        
        # driver = GraphDatabase.driver(
        #     "bolt://172.30.86.10:5724",
        #     auth=("neo4j", "neo4j.kjxm..")
        # )
        driver = GraphDatabase.driver(
                "bolt://127.0.0.1:7687",
                auth=("neo4j", "12345678")
            )
    
        # 验证是否成功连接数据库
        driver.verify_connectivity()
        return driver
        
        
        
