import json
from abc import ABCMeta, abstractmethod

import gensim
from sekg.graph.accessor import GraphAccessor
from sekg.graph.metadata_accessor import MetadataGraphAccessor

"""
this package is used to export a neo4j instance to Memory to build a copy of graph.
You can used it to train graph vector or to query graph 
"""


class NodeInfo(object):
    """
    a basic abstract class for NodeInfo
    """
    __metaclass__ = ABCMeta
    PRIVATE_PROPERTY = {
        "lastrevid",
        "_create_time",
        "_update_time",
        "_modify_version",
        "modified",
        "logo image"
    }

    def __init__(self, node_id, labels, properties):
        self.labels = labels
        self.properties = properties
        self.node_id = node_id

    @abstractmethod
    def get_main_name(self):
        pass

    @abstractmethod
    def get_all_names(self):
        return []

    def get_all_names_str(self):
        return " , ".join(self.get_all_names())

    @abstractmethod
    def get_all_valid_attributes(self):
        valid_attribute_pairs = []

        for property_name in self.properties.keys():
            if self.is_valid_property(property_name):
                value = self.properties[property_name]
                if not value:
                    continue
                valid_attribute_pairs.append((property_name, value))
        return valid_attribute_pairs

    def get_all_valid_attributes_str(self):
        result = []
        valid_attribute_pairs = self.get_all_valid_attributes()
        for (property_name, value) in valid_attribute_pairs:
            result.append(property_name + " : " + value)

        return " , ".join(result)

    @abstractmethod
    def is_valid_property(self, property_name):
        if property_name in NodeInfo.PRIVATE_PROPERTY:
            return False
        return True

    def __repr__(self):
        return "<NodeInfo id=%d labels=%r properties=%r>" % (self.node_id, self.labels, self.properties)


class NodeInfoFactory(object):
    """
    a basic abstract class for NodeInfo
    """
    __metaclass__ = ABCMeta
    """
    a factory to create NodeInfo, can be extend to create Multi type NodeInfo instance by condition
    """

    def __init__(self):
        pass

    @abstractmethod
    def create_node_info(self, node_info_dict):
        """need to implement"""
        return None


class RelationInfo:

    def __init__(self, start_node_info, relation_name, end_node_info):
        self.relation_name = relation_name
        self.end_node_info = end_node_info
        self.start_node_info = start_node_info

    def get_in_relation_str(self):
        return "{start} {r}".format(
            start=self.start_node_info.get_main_name(),
            r=self.relation_name
        )

    def get_out_relation_str(self):
        return "{r} {end}".format(
            r=self.relation_name,
            end=self.end_node_info.get_main_name()
        )

    def get_full_relation_str(self):
        return "{start} {r} {end}".format(start=self.start_node_info.get_main_name(),
                                          r=self.relation_name,
                                          end=self.end_node_info.get_main_name())


class GraphDataReader:
    """
    this class is a graph Data reader, can get the graph exporter not in the raw json,
    but in more clean format, wrap the result to a specific Object NodeInfo or RelationInfo.
    """

    def __init__(self, graph_data, node_info_factory):
        if isinstance(graph_data, GraphData):
            self.graph_data = graph_data
        else:
            self.graph_data = None

        if isinstance(node_info_factory, NodeInfoFactory):
            self.node_info_factory = node_info_factory
        else:
            self.node_info_factory = None

    def get_all_out_relation_infos(self, node_id):
        relation_list = self.graph_data.get_all_out_relation_dict_list(node_id=node_id)

        return self.create_relation_info_list(relation_list)

    def get_all_in_relation_infos(self, node_id):
        relation_list = self.graph_data.get_all_in_relation_dict_list(node_id=node_id)

        return self.create_relation_info_list(relation_list)

    @staticmethod
    def create_relation_info(start_node_info, relation_type, end_node_info):
        return RelationInfo(start_node_info=start_node_info,
                            relation_name=relation_type,
                            end_node_info=end_node_info)

    def create_from_relation_info_dict(self, relation_info_dict):
        graph_data = self.graph_data
        start_node_info_dict = graph_data.get_node_info_dict(relation_info_dict["startId"])
        start_node_info = self.node_info_factory.create_node_info(start_node_info_dict)

        end_node_info_dict = graph_data.get_node_info_dict(relation_info_dict["endId"])
        end_node_info = self.node_info_factory.create_node_info(end_node_info_dict)

        relation_type = relation_info_dict["relationType"]

        return self.create_relation_info(start_node_info=start_node_info, relation_type=relation_type,
                                         end_node_info=end_node_info,
                                         )

    def create_relation_info_list(self, relation_info_dict_list):
        info_list = []
        for r in relation_info_dict_list:
            info_list.append(self.create_from_relation_info_dict(r))
        return info_list

    def get_node_info(self, node_id):
        node_info_dict = self.graph_data.get_node_info_dict(node_id=node_id)
        return self.node_info_factory.create_node_info(node_info_dict)

    def get_all_node_infos(self):
        result = []
        for node_id in self.graph_data.get_node_ids():
            result.append(self.get_node_info(node_id))
        return result



class GraphData(gensim.utils.SaveLoad):
    """
    the store of a graph exporter for
    """

    def __init__(self):
        # two map for
        self.out_relation_map = {}
        self.in_relation_map = {}
        self.id_to_nodes_map = {}

        self.relation_num = 0
        self.node_num = 0

    def clear(self):
        self.out_relation_map = {}
        self.in_relation_map = {}
        self.id_to_nodes_map = {}

        self.relation_num = 0
        self.node_num = 0

    def set_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_node(self, node_json):
        node_id = node_json["id"]
        self.id_to_nodes_map[node_id] = node_json
        self.node_num = self.node_num + 1

    def set_relations(self, relations):
        for t in relations:
            self.add_relation(t)

    def add_relation(self, relation_json):
        startId = relation_json["startId"]
        endId = relation_json["endId"]
        if startId in self.out_relation_map:
            self.out_relation_map[startId].append(relation_json)
        else:
            self.out_relation_map[startId] = [relation_json]

        if endId in self.in_relation_map:
            self.in_relation_map[endId].append(relation_json)
        else:
            self.in_relation_map[endId] = [relation_json]
        self.relation_num = self.relation_num + 1

    def save_as_json(self, path):
        temp = {
            "out_relation_map": self.out_relation_map,
            "in_relation_map": self.in_relation_map,
            "id_to_nodes_map": self.id_to_nodes_map
        }
        json.dump(temp, path)

    def get_node_num(self):
        return self.node_num

    def get_relation_num(self):
        return self.relation_num

    def get_node_ids(self):
        return self.id_to_nodes_map.keys()

    def get_relation_pairs(self):
        # todo:cache the result?
        """
        get the relation list in [(startId,endId)] format
        :return:
        """
        pairs = []
        for r_list in self.out_relation_map.values():
            for r in r_list:
                pairs.append((r["startId"], r["endId"]))

        return pairs

    def get_all_out_relation_dict_list(self, node_id):
        if node_id not in self.out_relation_map:
            return []

        return self.out_relation_map[node_id]

    def get_all_in_relation_dict_list(self, node_id):
        if node_id not in self.in_relation_map:
            return []

        return self.in_relation_map[node_id]

    def get_node_info_dict(self, node_id):
        """
        get the node info dict,
        :param node_id: the node id
        :return:
        """
        if node_id not in self.id_to_nodes_map:
            return None
        return self.id_to_nodes_map[node_id]


class DataExporterAccessor(GraphAccessor):
    def get_all_nodes_not_batch(self, node_label):
        try:
            query = 'Match (n:`{node_label}`) return n'.format(node_label=node_label)

            cursor = self.graph.run(query)
            nodes = []
            for record in cursor:
                nodes.append(record["n"])
            return nodes
        except Exception:
            return []

    def get_all_nodes(self, node_label, step=100000):
        metadata_accessor = MetadataGraphAccessor(self)
        max_node_id = metadata_accessor.get_max_id_for_node()

        nodes = []

        for start_id in range(0, max_node_id, step):
            end_id = min(max_node_id, start_id + step)
            nodes.extend(self.get_all_nodes_in_scope(node_label, start_id=start_id, end_id=end_id))
            print("get nodes step %d-%d" % (start_id, end_id))

        return nodes

    def get_all_nodes_in_scope(self, node_label, start_id, end_id):
        try:
            query = 'Match (n:`{node_label}`) where ID(n)>{start_id} and ID(n)<={end_id} return n'.format(
                node_label=node_label, start_id=start_id, end_id=end_id)

            cursor = self.graph.run(query)
            nodes = []
            for record in cursor:
                nodes.append(record["n"])

            return nodes
        except Exception:
            return []

    def get_all_relation(self, node_label, step=200000):
        metadata_accessor = MetadataGraphAccessor(self)
        max_relation_id = metadata_accessor.get_max_id_for_relation()

        relations = []

        for start_id in range(0, max_relation_id, step):
            end_id = min(max_relation_id, start_id + step)
            relations.extend(self.get_all_relation_in_scope(node_label, start_id=start_id, end_id=end_id))
            print("get relation step %d-%d" % (start_id, end_id))
        return relations

    def get_all_relation_in_scope(self, node_label, start_id, end_id):
        try:
            query = 'Match (n:`{node_label}`)-[r]->(m:`{node_label}`) where ID(r)>{start_id} and ID(r)<={end_id} return ID(n) as startId,ID(m) as endId, type(r) as relationType'.format(
                node_label=node_label, start_id=start_id, end_id=end_id)

            cursor = self.graph.run(query)
            data = cursor.data()
            return data
        except Exception:
            return []

    def get_all_relation_not_batch(self, node_label):
        try:
            query = 'Match (n:`{node_label}`)-[r]->(m:`{node_label}`) return ID(n) as startId,ID(m) as endId, type(r) as relationType'.format(
                node_label=node_label)

            cursor = self.graph.run(query)
            data = cursor.data()
            return data
        except Exception:
            return []


class GraphDataExporter:
    """
    export specific data
    """

    def __init__(self):
        pass

    def export_all_graph_data(self, graph, node_label):
        accessor = DataExporterAccessor(graph=graph)
        nodes = accessor.get_all_nodes(node_label=node_label)
        graph_data = GraphData()

        for node in nodes:
            labels = [label for label in node.labels]
            team = {"id": node.identity, "properties": dict(node), "labels": labels}
            graph_data.add_node(team)

        print("load entity complete, num=%d" % len(nodes))
        relations = accessor.get_all_relation(node_label=node_label)
        print("load relation complete,num=%d" % len(relations))
        graph_data.set_relations(relations=relations)

        return graph_data
