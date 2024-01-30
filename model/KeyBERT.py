"""

    @Author: 李凌浩
    @Updater_1:
    @LatestUpdateTime: 2023/10/4
    @Introduction: 深度学习大语言模型KeyBERT

"""


from keybert import KeyBERT
import jieba
import numpy as np
from sentence_transformers import SentenceTransformer

from static.graph_const import GraphConst
from config import logging_config
logger=logging_config.logging_self_define().log(level="INFO",name="keyBert")


# KeyBERT大语言模型的类
class KeyBERTModel:
    # 初始化模型
    def __init__(self):
        self.graph_const = GraphConst()
        self.doc = ""
        self.model = KeyBERT(model=SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2"))
    def __del__(self):
        logger.info("keyBert模型清除")

    # 定义输入函数
    def input(self, doc):
        self.doc = doc

    # 定义输出函数（推理）
    def output(self):
        try:
    
            # 定义候选词
            candidates = self.graph_const.get_predetermined_themes_list()
    
    
            # 对中文输入进行分词
            cutted_doc = " ".join(jieba.cut(self.doc))
            # logger.info("----------ber cutted_doc:{}".format(cutted_doc))
    
            # 加载大语言模型KeyBERT（KeyBERT）
            # kw_model = KeyBERT("paraphrase-multilingual-MiniLM-L12-v2")
            # 加载大语言模型KeyBERT（SentenceTransformer）
    
            # 保存模型权重文件到本地
            # sentence_model.save("paraphrase-multilingual-MiniLM-L12-v2")
            # 继承子类模型方法
            kw_model = self.model
            # logger.info("----------bert kw_model:{}".format(kw_model))
    
            # 计算文段和候选词各自的嵌入向量
            embedding = kw_model.extract_embeddings(cutted_doc, candidates=candidates)
            # logger.info("----------bert embedding:{}".format(embedding))
            # 获取文段的嵌入向量
            doc_embedding = np.array(embedding[0][0])
            # logger.info("----------bert doc_embedding:{}".format(doc_embedding))
            # 获取候选词的嵌入向量
            words_embedding = np.array(embedding[1])
            # logger.info("----------bert words_embedding:{}".format(words_embedding))
    
            # 定义余弦相似度列表
            cos_similarity_list = []
    
            # 计算各个候选词与文段的余弦相似度
            for word_embedding in words_embedding:
                cos_similarity_list.append(doc_embedding.dot(word_embedding) /
                                           (np.linalg.norm(doc_embedding) * np.linalg.norm(word_embedding)))
    
            # logger.info("----------bert cos_similarity_list:{}".format(cos_similarity_list))
    
            # 定义关键词嵌入向量列表
            keywords_embedding = []
    
            # 获取关键词各自的相似度
            for i in range(len(cos_similarity_list)):
                keywords_embedding.append((candidates[i], cos_similarity_list[i]))
    
            # 关键词的相似度降序排序
            keywords_embedding.sort(key=lambda s: s[1], reverse=True)
    
            # 获取相似度最高的关键词
            keywords = keywords_embedding[0][0]
        except Exception as e:
            logger.error("出错 --exception:{}".format(str(e)))
        # logger.info("----------bert keywords:{}".format(keywords))

        # 输出关键词
        return keywords

