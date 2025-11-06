import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Music lab")
fenetre.geometry("500x500")
fenetre.config(bg= "#0094FE")

tk.Label(fenetre, text= "Les differentes commandes sont:\n\n-refresh: actualise les valeur\nmesurée pour une meilleure préscision\n\n-stop: Déconnecte le module de cette\napplication\n\n-etteint: Eteint le module.", bg= "#FD0000", fg= "#26FF00").pack()

list_commandes = tk.Listbox(fenetre, justify= "center", )

fenetre.mainloop()