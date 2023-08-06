from sekg.graph.accessor import GraphAccessor


class MetadataGraphAccessor(GraphAccessor):
    """
    query the graph metadata
    """
    # todo: complete this accessor and pass test
    def get_max_id_for_node(self):
        """
            get the max id of Node in the whole graph
            :return: the max id
            """

        query = 'MATCH (n) return max(ID(n))'
        result = self.graph.evaluate(query)
        return result


    def get_max_id_for_relation(self):
        """
        get the max id of relation in the whole graph
        :return: the max id
        """
        query = 'MATCH ()-[n]-() return max(ID(n))'
        result = self.graph.evaluate(query)
        return result

    def get_node_num(self,label):
        pass
        # todo:
    def get_relation_num(self):
        pass
        # todo:
    def get_label_set(self):
        pass
        # todo:
    def get_relation_set(self):
        pass
        # todo: