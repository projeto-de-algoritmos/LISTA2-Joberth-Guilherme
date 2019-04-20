import pydotplus
from connectionDatabse import Connection
import pydotplus as ptp
from graphClass import Graph

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
        discipline_relation = {}

        # Load the disciplines of the habilitaion 
        # from all peorids and
        # join all in a unique list
        for discipline in self.code['disciplines']:
                list_disciplines += discipline.values()[0]
        
        # print(len(list_disciplines))
        # Run in all list disicplines code and search for it in database
        # Add it in node  list with name and code
        # And all the requirement belong it is add in edges from graph connect
        for discipline in list_disciplines:
            current_dis = collectionDiscipline.find_one({'code': discipline})
            # print(current_dis)
            if current_dis != None:

                type_str =False

                if len(current_dis['requirements']) > 1:
                    type_str = True
                else:
                    nodes.append((int(discipline), current_dis['name']))

                cont = 1
                for requirement in current_dis['requirements']:
                    # print(requirement)

                    if type_str:
                        nodes.append((str(discipline) + str(cont), 'E'))
                        edges.append((str(discipline) + str(cont), int(discipline)))
                    
                    if isinstance(requirement, list):
                        if cont == 1:
                            discipline_relation[current_dis['code']] = requirement

                        for single_requirement in requirement:
                            if type_str:
                                edges.append((int(single_requirement), str(discipline) + str(cont) ))
                            else:
                                edges.append((int(single_requirement), int(discipline) ))
                    else:
                        if cont == 1:
                            discipline_relation[current_dis['code']] = list(requirement)

                        edges.append((int(requirement), int(discipline)))
                    cont+= 1
            else:
                nodes.append((int(discipline), str(discipline)))
        
        print(discipline_relation)
        
        # Graph(discipline_relation).dfs_recursao()
        Graph(discipline_relation).topologicalSort()

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
          
''''
def generate_graph():

    graph = ptp.Dot(graph_type='graph')
    edges = [(1,2), (1,3), (2,4), (2,5), (3,5)]
    nodes = [(1, "A", "r"), (2, "B", "g"), (3, "C", "g"), (4, "D", "r"), (5, "E", "g")]
    for e in edges:
        graph.add_edge(ptp.Edge(e[0], e[1]))
    for n in nodes:
        node = ptp.Node(name=n[0], label= n[1], fillcolor=n[2], style="filled" )
        graph.add_node(node)
    graph.write_png("file.png")'''
