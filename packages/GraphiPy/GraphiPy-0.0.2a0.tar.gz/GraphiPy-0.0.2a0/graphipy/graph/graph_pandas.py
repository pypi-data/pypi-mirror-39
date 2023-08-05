import pandas as pd
import os

from graphipy.graph.graph_base import BaseGraph

# Graph object implemented by pandas


class PandasGraph(BaseGraph):
    def __init__(self):
        BaseGraph.__init__(self)
        self._type = "pandas"
        # a dict of node data frames and edge data frames
        # key=label, value=dataframe
        self.nodes_df = {}
        self.edges_df = {}

        # buffer for optimization
        self.node_count = 0
        self.edge_count = 0
        self.buffer = 5000

        self.nodes_dict = {}
        self.edges_dict = {}

        self.path = os.getcwd() + "\\csv"
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def graph_type(self):
        return self._type

    def convert_to_df(self, _type):

        if _type == "node" or _type == "both":
            for key in self.nodes_df:
                nodes_list = []
                for _id in self.nodes_dict[key]:
                    nodes_list.append(vars(self.nodes_dict[key][_id]))
                df = pd.DataFrame(nodes_list)
                self.nodes_df[key] = self.nodes_df[key].append(
                    df, sort=False, ignore_index=True)
                self.nodes_dict[key] = {}
            self.node_count = 0

        if _type == "edge" or _type == "both":
            for key in self.edges_df:
                edges_list = []
                for _id in self.edges_dict[key]:
                    edges_list.append(vars(self.edges_dict[key][_id]))
                df = pd.DataFrame(edges_list)
                self.edges_df[key] = self.edges_df[key].append(
                    df, sort=False, ignore_index=True)
                self.edges_dict[key] = {}
            self.edge_count = 0

    def export_all_csv(self, prefix):
        """ exports all dataframes as csv """

        # Create folders to export to
        export_path = self.path + "\\" + prefix + "\\"
        export_path_node = export_path + "nodes\\"
        export_path_edge = export_path + "edges\\"

        if not os.path.exists(export_path):
            os.mkdir(export_path)

        if not os.path.exists(export_path_node):
            os.mkdir(export_path_node)

        if not os.path.exists(export_path_edge):
            os.mkdir(export_path_edge)

        # append remaining nodes/edges to dataframe
        self.convert_to_df("both")

        # get node data frames
        n_df = self.get_nodes()
        for key in n_df.keys():
            # convert data frame to csv
            n_df[key].to_csv(export_path_node + key + ".csv",
                             encoding="utf-8", index=False)
        # get edge data frames
        e_df = self.get_edges()
        for key in e_df.keys():
            # convert data frame to csv
            e_df[key].to_csv(export_path_edge + key + ".csv",
                             encoding="utf-8", index=False)

        return export_path

    # export data frame to csv specified by node label and edge label
    def export_csv(self, prefix, node_option=set(), edge_option=set()):
        """ exports a specified dataframe as csv """

        # Create folders to export to
        export_path = self.path + "\\" + prefix + "\\"
        export_path_node = export_path + "nodes\\"
        export_path_edge = export_path + "edges\\"

        if not os.path.exists(export_path):
            os.mkdir(export_path)

        if not os.path.exists(export_path_node):
            os.mkdir(export_path_node)

        if not os.path.exists(export_path_edge):
            os.mkdir(export_path_edge)

        # append remaining nodes/edges to dataframe
        self.convert_to_df("both")

        if len(node_option) > 0:
            # get node data frames
            n_df = self.get_nodes()
            for key in n_df.keys():
                # if matches node label that user wants
                if key in node_option:
                    n_df[key].to_csv(export_path_node + key +
                                     ".csv", encoding="utf-8", index=False)
        if len(edge_option) > 0:
            # get edge data frames
            e_df = self.get_edges()
            for key in e_df.keys():
                 # if matches edge label that user wants
                if key in edge_option:
                    e_df[key].to_csv(export_path_edge + key +
                                     ".csv", encoding="utf-8", index=False)

        return export_path

    def create_node(self, node):
        """ creates a node in the graph """

        label = node.get_label_attribute().lower()
        _id = node.get_id()

        # create a new dataframe if it is a new node type
        if label not in self.nodes_dict:
            self.nodes_dict[label] = {}
            self.nodes_df[label] = pd.DataFrame(
                columns=vars(node).keys())

        # append the node to the dictionary
        self.nodes_dict[label][_id] = node
        self.node_count += 1

        # if buffer is reached, move everything to the dataframe
        if (self.node_count == self.buffer):
            self.convert_to_df("node")

    def create_edge(self, edge):
        """ creates an edge in the graph """

        label = edge.get_label_attribute().lower()
        _id = edge.get_id()

        # create a new dataframe if it is a new edge type
        if label not in self.edges_df:
            self.edges_dict[label] = {}
            self.edges_df[label] = pd.DataFrame(
                columns=vars(edge).keys())

        # append the node to the dictionary
        self.edges_dict[label][_id] = edge
        self.edge_count += 1

        # if buffer is reached, move everything to the dataframe
        if self.edge_count >= self.buffer:
            self.convert_to_df("edge")

    def get_nodes(self):
        """ returns all node dataframes """

        # append remaining nodes/edges to dataframe
        self.convert_to_df("node")

        return self.nodes_df

    def get_edges(self):
        """ returns all edge dataframes """

        # append remaining nodes/edges to dataframe
        self.convert_to_df("edge")

        return self.edges_df

    def get_df_multiple(self, node_df=set(), edge_df=set()):
        """ returns specified dataframes in a dictionary"""

        # append remaining nodes/edges to dataframe
        self.convert_to_df("both")

        dataframes = {
            "node": {},
            "edge": {}
        }

        # check nodes
        for node in node_df:
            node = node.lower()
            if node in self.nodes_df:
                dataframes["node"][node] = self.nodes_df[node]

        # check edges
        for edge in edge_df:
            edge = edge.lower()
            if edge in self.edges_df:
                dataframes["edge"][edge] = self.edges_df[edge]

        return dataframes

    def get_df(self, name, _type="node"):
        """ returns a single specified dataframe """

        # append remaining nodes/edges to dataframe
        self.convert_to_df(_type.lower())
        name = name.lower()
        if _type == "node":
            if name in self.nodes_df:
                return self.nodes_df[name]
        else:
            if name in self.edges_df:
                return self.edges_df[name]
