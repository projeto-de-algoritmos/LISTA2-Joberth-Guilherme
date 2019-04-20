from collections import defaultdict, OrderedDict
import pydotplus as ptp

class Graph:
    def __init__(self, graph):
        self.graph = graph
    
    def visited_recursive_dsf(self, vertex, visited, order):
        
        visited.append(vertex)

        try:
            self.graph[vertex]
        except KeyError:
            order.append(vertex)
            return  
          
        for vertex_aux in self.graph[vertex]:
            if vertex_aux not in visited:
                    self.visited_recursive_dsf(vertex_aux, visited, order)
        order.insert(0, vertex)

        '''
            for current_vertex in vertex_aux:
                if current_vertex not in visited:
                    self.visited_recursive_dsf(current_vertex, visited, order)
        order.insert(0, vertex)'''
        

    def topologicalSort(self):
        visited = []
        order = []

        for vertex in self.graph:
            if vertex not in visited:
                self.visited_recursive_dsf(vertex, visited, order)
        print('order')
        order.reverse()

        edges = []

        for edge in range(len(order) - 1):
            edges.append((order[edge], order[edge + 1]))

        # create a direct graph horizontal
        graph = ptp.Dot(graph_type='digraph', rankdir='LR')

        print('aqui')
            
        # Adding all edges and nodes in instace of graph
        for e in edges:
            graph.add_edge(ptp.Edge(str(e[0]), str(e[1]),color='green'))
                
                    
        for n in order:
            node = ptp.Node(name=str(n), label= str(n), style="filled" )
            graph.add_node(node)
            
            try:
                req_current = self.graph[n]
            except KeyError:
                continue
            
            for node in req_current:
                edges.append((n, node))
                graph.add_edge(ptp.Edge(str(n), str(node)))
        

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
        