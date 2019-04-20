import pydotplus
from connectionDatabse import Connection
import pydotplus as ptp
from graphClass import Graph

class Habilitation:
# This instance use for instanciate an
# habilitation and load the graph

    def __init__(self, code):
        self.code = list(code)[0]

    def convert_requirements(self, requirements):

        # A, [B, C] -- A AND B OR C
        # [A, B], C

        new_req = []

        for req in requirements:

            if isinstance(req, list):

                if len(new_req) < 1:
                    new_req = req
                    continue

                first_element = req.pop(0)

                if isinstance(new_req[-1], list):
                    new_req[-1].append(first_element)
                else:
                    new_req[-1] = [new_req[-1], first_element]

                # add the rest
                for others_req in req:
                    new_req.append(others_req)

            else:

                if len(new_req) < 1:
                    new_req.append([req])

                elif isinstance(new_req[-1], list):
                    new_req[-1].append(req)
                else:
                    new_req[-1] = [new_req[-1], req]

        return new_req

    def get_and_name(self, code, index):
        return code + "_" + str(index)

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

            current_dis = collectionDiscipline.find_one({'code': str(discipline)})

            if current_dis is None:
                nodes.append((str(discipline), str(discipline)))
                continue

            requirements = self.convert_requirements(current_dis['requirements'])
            code = str(discipline)
            label = current_dis['name']

            nodes.append((code, label))
            discipline_relation[code] = []

            for index, requirement in enumerate(requirements):

                if isinstance(requirement, list):

                    and_node_name = self.get_and_name(code, index)
                    nodes.append((and_node_name, 'E'))
                    edges.append((and_node_name, code   ))

                    for req in requirement:
                        edges.append((str(req), and_node_name))
                        discipline_relation[code].append(str(req))

                else:
                    edges.append((str(requirement), code))
                    discipline_relation[code].append(str(requirement))
        
        print(discipline_relation)
        
        # Graph(discipline_relation).dfs_recursao()
        Graph(discipline_relation).topologicalSort()

        # create a direct graph horizontal
        graph = ptp.Dot(graph_type='digraph', rankdir='LR')
            
        # Adding all edges and nodes in instace of graph
        for e in edges:
            graph.add_edge(ptp.Edge(e[0], e[1]))
        for n in nodes:
            node = ptp.Node(name=n[0], label=n[1], style="filled")
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
