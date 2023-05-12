from time import sleep
import tkinter as tk
from game import game
from MiniMaxAlgo import minimax


class window():
    def __init__(self):
        # Create the window
        self.window = tk.Tk()
        self.window.title("Project")
        self.window.geometry("700x500")
        self.window.configure(bg = "#D9D9D9")

        self.Frame1 = tk.Frame(self.window,bg="#A97171",pady=10)
        self.Frame1.columnconfigure(0,weight=1)
        self.Frame1.columnconfigure(1,weight=1)
        self.Frame1.columnconfigure(2,weight=1)
        #######################################
        label = tk.Label(self.Frame1,text="Type:",font =('Arial',10),bg ="#A97171",foreground="white")
        label.grid(row=0,column=0,sticky="w",padx=10)
        
        label = tk.Label(self.Frame1,text="Difficulty:",font =('Arial',10),bg ="#A97171",foreground="white")
        label.grid(row=1,column=0,sticky="w",padx=10)
        #######################################
        def on_select(value):
            print("Selected:", value)
            
        options = ["MiniMax", "MiniMax with pruning"]
        algorithm = tk.StringVar(self.Frame1)
        algorithm.set(options[0])
        #print(selected.get())
        dropdown = tk.OptionMenu(self.Frame1, algorithm, *options, command=on_select)
        dropdown.grid(row=0 , column= 1 , padx= 10)
        
        options = [2,3,4]
        difficulty = tk.StringVar(self.Frame1)
        difficulty.set(options[0])
        #print(selected.get())
        dropdown = tk.OptionMenu(self.Frame1, difficulty, *options, command=on_select)
        dropdown.grid(row=1 , column= 1 , padx= 10 )
        #######################################
        buttonUninformed = tk.Button(self.Frame1,text="Reset",border=0,bg="#7B6585",foreground="white",width=15,command=lambda :self.game.reset_obj())
        buttonUninformed.grid(row = 0, column=3,padx=10)
        turn_indicator = tk.Button(self.Frame1,text="Next Move",border=0,bg="#7B6585",foreground="white",width=15,command=lambda :self.game.play())
        turn_indicator.grid(row = 1, column=3,padx=10)

        self.Frame1.pack(fill="both",side="top")

        self.Frame2 = tk.Frame(self.window,bg="#D9D9D9")
        self.Frame2.pack(expand=True)
      
        self.game = game(self.Frame2,turn_indicator,algorithm,difficulty)

        self.window.mainloop()    


if __name__=="__main__":
    obj = window()