# directedGraph

This repository contains a python class that represent a directed graph

## Instructions
---
### Environment set up
---
Type in your terminal the following commands to create and activate your Virtual Environment once you have clone the repo

```cd directedGraph```

```python3 -m venv venv```

```source venv/bin/activate``` (unix)

```.\venv\Scripts\activate``` (windows)

For more info about Virtual Environments https://docs.python.org/3/library/venv.html
Now to install the necessary packages, run the following command

```pip install -r requirements.txt```

### How to use
---
First of all you'll need to import the package
`from digraph import DirectedGraph`

1. You can initialize the object passing a list of vertices and a list of edges
`vertices = ['a', 'b', 'c', 'd']`
`edges = [('a', 'b'), ('a', 'd'), ('b', 'c'), ('c', 'd')]`
`dgraph = DirectedGraph(vertices, edges)`

2. Or you can do it from a hdf5 file that represents an adjacency matrix 
`hdf_dgraph = DirectedGraph.from_hdf('data.h5', 'df')`

Once the object is initialize. You can:
- check the number of vertices and edges by using the method info
`dgraph.info()`
- Visualize its out-degree distribution by using the method plot_histogram
`dgraph.plot_histogram('histogram')`
- Visualize its the out-degree by node using the method plot_bar
`dgraph.plot_bar('bar_plot')`
- Export to hdf5 file that represents the graph adjacency matrix by using the method to_hdf
`dgraph.to_hdf('data.h5', 'df')`


##  Note
---
If you are using testing this class in a Jupyter notebook please be aware that the export image might make trasparent the axis and title. 
https://stackoverflow.com/questions/19576317/matplotlib-savefig-does-not-save-axes