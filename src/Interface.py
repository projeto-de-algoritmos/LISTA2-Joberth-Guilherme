import Tkinter as tk
from IPython.display import SVG, display
from PIL import ImageTk, Image
from connectionDatabse import Connection
from habilitationClass import Habilitation
import random
from graphClass import Graph


class Application:
# This class is use for generate the
# widgets interface in screen

    def __init__(self, master=None):

        # Define the height and width from the master frame
        self.heightScreen = master.winfo_screenheight(),
        self.widthScreen = master.winfo_screenwidth(),

        # Container for user input
        self.containerEntry = tk.Frame(master)
        self.containerEntry.pack()

        # Label and input for habilitation code
        self.labelCodeCourse = tk.Label(self.containerEntry,
                                        text="Codigo da habilitacao: ")
        self.labelCodeCourse.pack(side=tk.LEFT)
        self.codeCourse = tk.Entry(self.containerEntry)
        self.codeCourse["width"] = 30
        self.codeCourse.pack(side=tk.LEFT, padx=10, pady=10)

        # button for bind the search
        self.buttonCodeCourse = tk.Button(self.containerEntry)
        self.buttonCodeCourse["text"] = "Procurar"
        self.buttonCodeCourse["command"] = self.generateGraph
        self.buttonCodeCourse.pack(side=tk.LEFT)

        self.topologicalButton = tk.Button(self.containerEntry)
        self.topologicalButton["text"] = "Ordem Topologica"
        self.topologicalButton["command"] = self.changeLabelTopologicalTrue
        self.topologicalButton.pack_forget()

        # Container where the graph is
        self.containerGraph = tk.Frame(master, bg="white")
        self.containerGraph.pack(pady=20, expand=tk.YES, fill=tk.NONE)

        self.topological = False

    def destroyContainerGraphWidget(self):

        for widget in self.containerGraph.winfo_children():
            widget.destroy()


    def changeLabelTopologicalTrue(self):
        self.topological = True
        self.topologicalButton["text"] = "Ver grafo"
        self.topologicalButton["command"] = self.changeLabelTopologicalFalse

        self.destroyContainerGraphWidget()

        self.showGraph()
    
    def changeLabelTopologicalFalse(self):
        self.topological = False
        self.topologicalButton["text"] = "Ordem Topologica"
        self.topologicalButton["command"] = self.changeLabelTopologicalTrue

        self.destroyContainerGraphWidget()
        self.showGraph()

    def showGraph(self):
        
        # set button topological visible
        self.topologicalButton.pack(side=tk.RIGHT, padx=500)

        # Load the image width and height
        if self.topological == True:
            imageLoad = Image.open("topological.png")
        else:
            imageLoad = Image.open("graph.png")

        widthImg, heightImg = imageLoad.size

        # Another container but is special for images
        canvas = tk.Canvas(self.containerGraph,
                           width=self.widthScreen,
                           height=self.heightScreen[0] - 200,
                           bg="white",
                           scrollregion=(0,0,widthImg, heightImg))
        
        # Setting configurations of scroll

        hbar=tk.Scrollbar(self.containerGraph,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=canvas.xview)
        vbar=tk.Scrollbar(self.containerGraph,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=2000,height=2000)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

        # resize the graph image
        '''    
        imageResized = imageLoad.resize((self.containerGraph.winfo_screenwidth() - 100,
                                        self.containerGraph.winfo_screenheight() - 200),
                                        Image.ANTIALIAS)

        imageResized.save('imageResized.png')
        '''
        if self.topological == True:
            img = tk.PhotoImage(file="topological.png")
        else:
            img = tk.PhotoImage(file="graph.png")
        
    
        # Determine the pre set configurations for image
        canvas.create_image(0,
                            0,
                            anchor=tk.NW,
                            image=img)
        # Adding image to container
        canvas.image = img


        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Able the container to show in master contatiner
        canvas.pack()

    def generateGraph(self):
        # Get habilitation code input
        habilitationCode = self.codeCourse.get()

        # verify if the code is empty and set 0
        if habilitationCode == '':
            habilitationCode = 0

        # Clean all the widget if there is some in screen
        self.destroyContainerGraphWidget()

        # Connection to database and set the colletion used 
        database = Connection.connectionDatabase()
        collectionHabilitation = database['habilitations']

        habilitationCode = collectionHabilitation.find(
                            {'code': int(habilitationCode)})

        # Save the count number documents in query 
        feedbackCount = habilitationCode.count()
        
        # Verify if the result return 0 and show a 
        # warning mesage
        if feedbackCount == 0:
            self.Warning = tk.Label(self.containerGraph,
                                    text="Nao existe esse codigo para essa habilitacao")
            self.Warning.pack()
        else:
            # If there is the habilitation code we generate the graph
            Habilitation(habilitationCode).load_graph()

            # Call the function to show the graph in screen
            self.showGraph()

        
if __name__ == "__main__":
    
    root = tk.Tk()  # Allow the widget be on the table

    # Title and size of screen
    root.title('Trabalho 2 Grafo')
    root.attributes('-zoomed', True)

    Application(root)  # Pass the root with config to Application class
    root.mainloop()  # loop for aba
    
