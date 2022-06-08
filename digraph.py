from typing import Tuple, List
import pandas as pd
import matplotlib.pyplot as plt


class DirectedGraph:
    """class that represents a directed graph from a list of vertices and edges
    
    Attributes
    -----------
    vertices (list): vertices of the graph
    edges (List[tuple]): edges of the graph
    adj_list (dict): adjacency list of the graph
    vertex_out_degree (dict): number of edges coming out of each of the vertices

    Public Methods
    --------------
    info: Prints basic information of the graph, such as number of vertices and edges
    plot_bar: Export barplot of the vertex out-degree by vertex
    plot_histogram: Export histogram distribution of the vertex out-degree
    to_hdf: Export to HDF5 the adjacency matrix of the graph
    from_hdf:  Alternative constructor of the object by reading an adjacency matrix in HDF5 format
    """
    
    def __init__(self, vertices: list, edges: List[tuple]):
        """
            Constructor of the class. Creates an Directed graph object from a list of vertices and list of tuples
        Args:
            vertices (list): vertices of the graph
            edges (List[tuple]): edges of the graph


        Raises:
            Exception: if either the vertices or the edges are not list raise an error. Check first element of the 
            edges list to check if it is a tuple
        """
        # sourcery skip: raise-specific-error
        if not isinstance(vertices, list) or not isinstance(edges, list) or not isinstance(edges[0], tuple):
            raise Exception('vertices must be a list and edges must be a list of tuples')
        self.vertices = vertices
        self.edges = edges
        self.adj_list = self._create_adjacency_list()
        self.vertex_out_degree = self._create_vertex_out_degree()
    
    def info(self) -> None:
        """Prints basic information of the graph, such as number of vertices and edges
        """
        print(f'The directed graph has:\n  Vertices: {len(self.vertices)}\n  Edges: {len(self.edges)}')
    
    def plot_bar(self, file_name: str) -> None:
        """Export barplot of the vertex out-degree by vertex

        Args:
            file_name (str): file name for the export image. Can include a destination path
        """
        plt.bar(self.vertex_out_degree.keys(), self.vertex_out_degree.values())
        plt.title('Number of edges coming out of each of the vertices')
        plt.xlabel('Vertex')
        plt.ylabel('Out degree')
        plt.savefig(f'{file_name}.png')

    def plot_histogram(self, file_name: str) -> None:
        """ Export histogram distribution of the vertex out-degree

        Args:
            file_name (str): file name for the export image. Can include a destination path
        """
        plt.title('Out degree distribution')
        plt.xlabel('Out degree')
        plt.ylabel('Frequency')
        plt.hist(self.vertex_out_degree.values(), bins='auto')
        plt.savefig(f'{file_name}.png')

    def to_hdf(self, path: str, key: str) -> None:
        """Export to HDF5 the adjacency matrix of the graph

        Args:
            path (str): File path or HDFStore object.
            key (str): Identifier for the group in the store
        """
        adj_matrix = self._create_adjacency_matrix()
        adj_matrix.to_hdf(path, key=key, mode='w')

    @classmethod
    def from_hdf(cls, path: str, key: str) -> 'DirectedGraph':
        """ Alternative constructor of the object by reading an adjacency matrix in HDF5 format 

        Args:
            path (str): File path or HDFStore object.
            key (str): Identifier for the group in the store
        
        Raises:
            Exception: if either the path or key are not string raise an error

        Returns:
            DirectedGraph: Object that represents a Directed Graph
        """
        # sourcery skip: raise-specific-error
        if not isinstance(path, str) or not isinstance(key, str):
            raise Exception('path and key must be a string object')
        vertices, edges = cls._read_hdf(cls, path, key)
        return cls(vertices, edges)

    def _create_adjacency_list(self) -> dict:
        """ 
            Creates the adjacency list of the graph
        Returns:
            dict: adjacency list of the graph
        """
        adj_list = {node: [] for node in self.vertices}
        for i, j in self.edges:
            adj_list[i].append(j)
        return adj_list

    def _create_adjacency_matrix(self) -> pd.DataFrame:
        """
            Creates the adjacency matrix of the graph

        Returns:
            pd.DataFrame: adjacency matrix of the graph
        """
        adj_matrix = pd.DataFrame(0, columns=self.vertices, index=self.vertices)
        for edge in self.edges:
            adj_matrix.at[edge[0], edge[1]] = 1
        return adj_matrix
    
    def _create_vertex_out_degree(self) -> dict:
        """Creates from the adjacency list the directed graph's vertex out degree

        Returns:
            dict: directed graph's vertex out degree
        """
        return {item[0]: len(item[1]) for item in self.adj_list.items()}

    def _read_hdf(self, path: str, key: str) -> Tuple[list, List[tuple]]:
        """From a dataframe that represents the adjacency matrix of a directed graph, get the
        vertices and edges of the graph to create the object

        Args:
            path (str): File path or HDFStore object
            key (str):  Identifier for the group in the store

        Raises:
            Exception: If the matrix is not square raise an error

        Returns:
            Tuple[list, List[tuple]]: Vertices and Edges of the graph
        """
        # sourcery skip: raise-specific-error
        df_adj_matrix = pd.read_hdf(path, key)
        if df_adj_matrix.shape[0] != df_adj_matrix.shape[1]:
            raise Exception('The dataframe should be squared')
        vertices = df_adj_matrix.columns.to_list()
        edges = self._get_edges_from_adjacency_matrix(
            adj_matrix=self._get_adjacency_matrix_from_dataframe(df_adj_matrix),
            vertices=vertices)
        return vertices, edges
    
    @staticmethod
    def _get_edges_from_adjacency_matrix(adj_matrix: list, vertices: list) -> list:
        """From the adjacency matrix and vertices, get the edges of the graph

        Args:
            adj_matrix (list): adjacency matrix of the graph
            vertices (list): vertices of the graph

        Returns:
            list: edges of the graph
        """
        edges = []
        for i, vertix in enumerate(adj_matrix):
            edges.extend((vertices[i], vertices[j]) for j, weight in enumerate(vertix) if weight > 0)
        return edges

    @staticmethod
    def _get_adjacency_matrix_from_dataframe(df: pd.DataFrame) -> list:
        """Get the adjacency matrix as a list from a dataframe

        Args:
            df (pd.DataFrame): adjacency matrix as DataFrame

        Returns:
            list: adjacency matrix as List
        """
        return df.to_records(index=False).tolist()
