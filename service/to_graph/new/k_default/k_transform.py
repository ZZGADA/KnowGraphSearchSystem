from service.to_graph.select_graph import KGraph


# LLH: 新增的类
# 知识图谱检索后处理的类
class KTransform:
    def __init__(self, input):
        self.input = input

    def process(self):
        try:
            cur_input = self.input
            node_list = []
            relationship_list = []

            for x in cur_input["first_res"]:
                target_end = []
                children = []
                for y in cur_input["second_res"]:
                    for relation in y["relations"]:
                        if relation["start"] == x["gid"]:
                            target_end.append(relation["end"])

                for y in cur_input["second_res"]:
                    for node in y["nodes"]:
                        if node["gid"] in target_end:
                            children.append(node)

                x["children"] = children
                node_list.append(x)

            for m in cur_input["second_res"]:
                for n in m["relations"]:
                    relationship_list.append(n)

            res = {"node": node_list, "relationship": relationship_list}
            return res, True
        except Exception as e:
            return [],False

       
