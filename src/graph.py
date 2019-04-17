import pydotplus
from connectionDatabase import Connection
import pydotplus as ptp

class Habilitation:
# This instance use for instanciate an
# habilitation and load the graph

    def __init__(self, code):
        self.code = list(code)[0]
    
    def load_graph(self):
        # Initiate the disciplines collection
        database = Connection.connectionDatabase()
        collectionDiscipline = database['disciplines'] 
        
        # load the list of disciplines, node and edges for graph
        list_disciplines = []
        nodes = []
        edges = []

        # Load the disciplines of the habilitaion 
        # from all peorids and
        # join all in a unique list
        for discipline in self.code['disciplines']:
                list_disciplines += discipline.values()[0]

        # Run in all list disicplines code and search for it in database
        # Add it in node  list with name and code
        # And all the requirement belong it is add in edges from graph connect
        for discipline in list_disciplines:
            current_dis = collectionDiscipline.find_one({'code': str(discipline)})
            nodes.append((int(discipline), current_dis['name']))
            for requirement in current_dis['requirements']:
                edges.append((int(requirement), int(discipline) ))

        print(nodes)
        print(edges)
                
        # create a direct graph horizontal
        graph = ptp.Dot(graph_type='digraph', rankdir='LR')
            
        # Adding all edges and nodes in instace of graph
        for e in edges:
            graph.add_edge(ptp.Edge(e[0], e[1]))
        for n in nodes:
            node = ptp.Node(name=n[0], label= n[1], style="filled" )
            graph.add_node(node)

        # create an png image from the result
        graph.write_png('graph.png')


