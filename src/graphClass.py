from collections import defaultdict, OrderedDict
import pydotplus as ptp

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.adjacentList = defaultdict(list)
    
    def dfs_recursivo_visita(self, vertice, visitado, ordem):

        visitado.append(vertice)

        try:
            self.graph[vertice]
        except KeyError:
            ordem.append(vertice)
            return  
          
        for vertice_aux in self.graph[vertice]:
            print('aux')
            print(vertice_aux)
            for current_vertice in vertice_aux:
                if current_vertice not in visitado:
                    self.dfs_recursivo_visita(current_vertice, visitado, ordem)
        ordem.insert(0, vertice)
        

    def dfs_recursao(self):
        print(self.graph)
        visitado = []
        ordem = []
        for vertice in self.graph:
            if vertice not in visitado:
                self.dfs_recursivo_visita(vertice, visitado, ordem)
        print('Ordem')
        ordem.reverse()

        edges = []

        for edge in range(len(ordem) - 1):
            edges.append((ordem[edge], ordem[edge + 1]))

        print(edges)

        print(ordem)

        # create a direct graph horizontal
        graph = ptp.Dot(graph_type='digraph', rankdir='LR')
            
        # Adding all edges and nodes in instace of graph
        for e in edges:
            graph.add_edge(ptp.Edge(str(e[0]), str(e[1])))
        for n in ordem:
            node = ptp.Node(name=str(n), label= str(n), style="filled" )
            graph.add_node(node)

        # create an png image from the result
        graph.write_png('topological.png')
    '''
    # A recursive function used by topologicalSort 
    def topologicalSortUtil(self,v,visited,stack): 
  
        # Mark the current node as visited. 
        visited[v] = True

        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
        
        # Recur for all the vertices adjacent to this vertex 
        
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack) 
  
        # Push current vertex to stack which stores result 
        stack.insert(0,v) 
        
  
    # The function to do Topological Sort. It uses recursive  
    # topologicalSortUtil() 
    def defineTopologicalOrder(self): 
        # Mark all the vertices as not visited 
        visited = {}

        print(self.graph.items())

        for key in self.graph:
            visited[key] = False 
        stack =[] 
  
        # Call the recursive helper function to store Topological 
        # Sort starting from all vertices one by one 
        for key in self.graph: 
            print(key)
            if visited[key] == False: 
                self.topologicalSortUtil(key,visited,stack) 
  
        # Print contents of stack 
        print stack 
        '''
        