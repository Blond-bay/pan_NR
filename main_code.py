import tkinter as tk
from PIL import ImageTk,Image,ImageDraw
from functools import partial


app = tk.Tk()
app.title("Pan New Rock")

#Frame pour liste et suppr
frame = tk.Frame()
frame.pack(side='left')

#Canva dans frame pour liste bloc
canvas_boutton = tk.Canvas(frame)
canvas_boutton.pack()

#Canva dans frame pour suppr bloc
canvas_supp = tk.Canvas(frame)
canvas_supp.pack(side='bottom')

#Frame pour crée le bloc
frame1 = tk.Frame()
frame1.pack(side='top')


#                   #
#   Update a frame  #
#                   #
def update(thing,func):
    for widget in thing.winfo_children():
        widget.destroy()
    
    func()

#                   #
#   QQ Variables    #
#                   #

photo_mur = "mur.jpg"

f = 0.2 #Reduction de taille de l'image

l = 3024 #Taille image
L = 4032

#Nouvelle taille de l'image
l_new = int(l*f)
L_new = int(L*f)

#clear l'image et affiche la nouvelle
def clear_and_print_canvas(mur):
    global canvas
    canvas.destroy()
    global l_new, L_new
    resized = mur.resize((l_new,L_new),Image.ANTIALIAS)
    mur_resized = ImageTk.PhotoImage(resized)
    canvas = tk.Canvas(app, width = l_new, height = L_new)
    canvas.create_image(0,0,image=mur_resized, anchor="nw") 
    canvas.pack(side='right')
    canvas.mainloop()



#                   #
#   CREATION BLOC   #
#                   #


n_prises = tk.IntVar()
n=0
n_prises.set(n)
live = tk.StringVar()

#Check les coords
def coordonnees(event):
    xe, ye = int(event.x/f), int(event.y/f)
    bloc.append(xe)
    bloc.append(ye)
    global n
    n+=1
    n_prises.set(n)

#fonction bouton start
def start_log():
    live.set('Enregistrement...')
    global bloc
    bloc = list()
    canvas.bind('<Button-1>',coordonnees)


#fonction bouton stop
def stop_log():
    #Enleve le "Enregistrement..."
    live.set('')
    #Reset le nombre de prises
    global n
    n=0
    n_prises.set(n)

    #Copie le bloc dans le fichier text
    with open('blocs.txt', 'a') as file:
        for item in bloc:
            file.write("%s " % item)
        file.write('\n')
    
    #arrete la f() log
    canvas.unbind('<Button-1>')

    #MAJ les boutons d'affichage
    update(canvas_boutton,affiche_boutons)

#Bouttons et toussa

start = tk.Button(frame1,text = ('Enregistrer'), command=start_log)
stop = tk.Button(frame1,text = ('Stop'),command=stop_log)
start.grid(row=0,column=0)
stop.grid(row=0,column=1)

prises1 = tk.Label(frame1, text='Nombre de prises :')
prises1.grid(row=2,column=0)
prises2 = tk.Label(frame1, textvariable=n_prises)
prises2.grid(row=2,column=1)

en_cours = tk.Label(frame1, textvariable=live)
en_cours.grid(row=3,column=0)

#                   #
#   AFFICHE PHOTO   #
#                   #

mur = Image.open(photo_mur)

#Resize et affiche pour la 1er fois

resized = mur.resize((l_new,L_new),Image.ANTIALIAS)
mur_resized = ImageTk.PhotoImage(resized)
canvas = tk.Canvas(app, width = l_new, height = L_new)
canvas.create_image(0,0,image=mur_resized, anchor="nw") 
canvas.pack(side='right')

#                   #
#   AfFICHAGE BLOC  #
#                   #



#Fonction qui pour un bloc listé par prises, sort les coordonées pour le tracage des cerlces
def conversion(x):
    t = 20
    out = []
    for i in x:
        a = (i[0]-t,i[1]-t,i[0]+t,i[1]+t)
        out.append(a)
    return out


#Trace les points sur les prises 
def bloc(x):
	#On ouvre l'image pour la suite
	mur = Image.open(photo_mur)
	#Conversion des coordonées des prises du bloc avec les bonnes coordonées,pour tracer les cercles
	bloc = conversion(x)
        #Tracage des cerlces en eux même
	cercle = ImageDraw.Draw(mur)
	for i in bloc:
		cercle.arc(i,0,360, fill=228, width=20)
	#Nouveau canvas et image
	clear_and_print_canvas(mur)

def affiche_boutons():
    #Cree une liste avec tous les blocs

    #Dabord longue liste 
    with open('blocs.txt') as f:
        list_blocs_full = []
        for line in f:
            line = line.split()
            if line:            
                line = [int(i) for i in line]
                list_blocs_full.append(line)

    #Puis on ordone avec les coord groupées
    liste_blocs = []
    for i in range(len(list_blocs_full)):
        list_blocs_soon = []
        j=0
        while j<=len(list_blocs_full[i])-1:
            coord = []
            coord.append(list_blocs_full[i][j])
            coord.append(list_blocs_full[i][j+1])
            list_blocs_soon.append(coord)
            j+=2
        liste_blocs.append(list_blocs_soon)
    
    
    #Nombre de blocs
    n_blocs = len(liste_blocs)
    
    #fonction pré-finale
    def photo_bloc(n):
        call = liste_blocs[n]
        print(call)
        bloc(call)
        
    #Cree et affiche les boutons
    liste_bouttons = []
    for i in range(n_blocs):
        liste_bouttons.append(tk.Button(canvas_boutton,text=("Bloc",i+1), command=partial(photo_bloc, i)))
        liste_bouttons[i].pack()

#Affiche pour la 1er fois
affiche_boutons()

#                           #
#   SUPPRESSION DE BLOCS    # 
#                           #


#Fonction qui supprime dans le .txt
def efface_ligne():
    n = int(entree.get())
    print('supression ligne',n)
    file = open("blocs.txt", "r")
    lines = file.readlines()
    file.close()

    del lines[n-1]

    new_file = open("blocs.txt", "w+")
    for line in lines:
        new_file.write(line)

    new_file.close()
    
    #Updtae canvas_bouton
    update(canvas_boutton,affiche_boutons)
    

#Boutons suppr

label = tk.Label(canvas_supp, text='Bloc à supprimer:')
label.pack()

entree = tk.Entry(canvas_supp, bd =2, width=3)
entree.pack()

bouton_del = tk.Button(canvas_supp, text='Supprimer',command=efface_ligne)
bouton_del.pack()


app.mainloop()
