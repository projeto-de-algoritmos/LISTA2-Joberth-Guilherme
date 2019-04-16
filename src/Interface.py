import Tkinter as tk
import pydotplus as ptp
from IPython.display import SVG, display
from PIL import ImageTk, Image
from connectionDatabse import Connection
import random


class Application:

    def __init__(self, master=None):

        self.heightScreen = master.winfo_screenheight(),
        self.widthScreen = master.winfo_screenwidth(),

        self.containerEntry = tk.Frame(master)
        self.containerEntry.pack()

        Connection.connectionDatabase()

        self.labelCodeCourse = tk.Label(self.containerEntry,
                                        text="Codigo da habilitacao: ")
        self.labelCodeCourse.pack(side=tk.LEFT)
        self.codeCourse = tk.Entry(self.containerEntry)
        self.codeCourse["width"] = 30
        self.codeCourse.pack(side=tk.LEFT, padx=10)

        self.buttonCodeCourse = tk.Button(self.containerEntry)
        self.buttonCodeCourse["text"] = "Procurar"
        self.buttonCodeCourse["command"] = self.generateGraph
        self.buttonCodeCourse.pack(side=tk.LEFT)

        self.containerGraph = tk.Frame(master, bg="white")
        self.containerGraph.pack(pady=20, expand=tk.YES, fill=tk.NONE)

    def showGraph(self):
        canvas = tk.Canvas(self.containerGraph,
                           width=self.widthScreen,
                           height=self.heightScreen[0] - 200,
                           bg="white")
        img = tk.PhotoImage(file="file.png")
        canvas.create_image(20,
                            (self.heightScreen[0]) // 6,
                            anchor=tk.NW,
                            image=img)
        canvas.image = img
        canvas.pack()

    def generateGraph(self):

        habilitationCode = self.codeCourse.get()

        if habilitationCode == '':
            habilitationCode = 0

        for widget in self.containerGraph.winfo_children():
            widget.destroy()

        database = Connection.connectionDatabase()
        collectionDiscipline = database.disciplines
        collectionHabilitation = database['habilitations']

        feedbackCount = collectionHabilitation.find(
            {'code': int(habilitationCode)}).count()
        

        if feedbackCount == 0:
            self.Warning = tk.Label(self.containerGraph,
                                    text="Nao existe esse codigo para essa habilitacao")
            self.Warning.pack()
        else:

            edges = []
            nodes = []

            disciplines = collectionHabilitation.find_one({'code': int(habilitationCode)})

            list_discipline = []

            for discipline in disciplines['disciplines']:
                list_discipline += discipline.values()[0]

            for discipline in list_discipline:
                current_dis = collectionDiscipline.find_one({'code': str(discipline)})
                nodes.append((int(discipline), current_dis['name']))
                for requirement in current_dis['requirements']:

                    edges.append((int(requirement), int(discipline) ))

            print(nodes)
            print(edges)
                    
                
            graph = ptp.Dot(graph_type='digraph', rankdir='LR')
               
            for e in edges:
                graph.add_edge(ptp.Edge(e[0], e[1]))
            for n in nodes:
                node = ptp.Node(name=n[0], label= n[1], style="filled" )
                graph.add_node(node)
            graph.write_png('file.png')
            
            

            self.showGraph()

        


if __name__ == "__main__":

    root = tk.Tk()  # Allow the widget be on the table

    root.title('Trabalho 2 Grafo')
    root.geometry('700x700')

    Application(root)  # Pass the root with config to Application class
    root.mainloop()  # loop for aba
