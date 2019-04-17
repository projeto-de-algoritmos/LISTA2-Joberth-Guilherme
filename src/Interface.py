import Tkinter as tk
from IPython.display import SVG, display
from PIL import ImageTk, Image
from connectionDatabase import Connection
from graph import Habilitation
import random


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
        self.codeCourse.pack(side=tk.LEFT, padx=10)

        # button for bind the search
        self.buttonCodeCourse = tk.Button(self.containerEntry)
        self.buttonCodeCourse["text"] = "Procurar"
        self.buttonCodeCourse["command"] = self.generateGraph
        self.buttonCodeCourse.pack(side=tk.LEFT)

        # Container where the graph is
        self.containerGraph = tk.Frame(master, bg="white")
        self.containerGraph.pack(pady=20, expand=tk.YES, fill=tk.NONE)

    def showGraph(self):
        # Another container but is special for images
        canvas = tk.Canvas(self.containerGraph,
                           width=self.widthScreen,
                           height=self.heightScreen[0] - 200,
                           bg="white")
        # Load the photo in variable
        img = tk.PhotoImage(file="graph.png")
        # Determine the pre set configurations for image
        canvas.create_image(20,
                            (self.heightScreen[0]) // 6,
                            anchor=tk.NW,
                            image=img)
        # Adding image to container
        canvas.image = img
        # Able the container to show in master contatiner
        canvas.pack()

    def generateGraph(self):
        # Get habilitation code input
        habilitationCode = self.codeCourse.get()

        # verify if the code is empty and set 0
        if habilitationCode == '':
            habilitationCode = 0

        # Clean all the widget if there is some in screen
        for widget in self.containerGraph.winfo_children():
            widget.destroy()

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
    root.geometry('700x700')

    Application(root)  # Pass the root with config to Application class
    root.mainloop()  # loop for aba
