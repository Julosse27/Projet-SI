import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Music lab")
fenetre.geometry("500x500")
fenetre.config(bg= "#0094FE")
fenetre.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
fenetre.columnconfigure(0, weight=1)

tk.Label(fenetre, text= "Voici les differentes commandes:\n\n-Refresh: actualise les valeur\nmesurée pour une meilleure préscision\n\n-Stop: Déconnecte le module de cette\napplication\n\n-Etteint: Eteint le module.", bg= "#FD0000", fg= "#26FF00", font= ("arial", 13, "bold")).grid(row= 1, column= 0, pady= (0, 5))
commandes = tk.Variable(value= ["Refresh", "Stop", "Etteint"])

list_commandes = tk.Listbox(fenetre, justify= "center", activestyle= "dotbox", listvariable= commandes, height= 4, width= 10)
list_commandes.grid(column= 0, row= 2, pady= 5)

def lancer_commande():
    list_commandes.curselection()
    

fenetre.mainloop()