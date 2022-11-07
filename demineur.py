from random import *
from tkinter import *  
import time
MINE = 'X'
NBR_MINE = 10
DRAPEAU = 0
M = 17 #nbres lignes
N = 10 #nbres col

BORDURE =  2 #bordure des rectangles
LARGEUR_CASE = 25 #largeur des rectangles
HAUTEUR_CASE = 25 #hauteur des rectangles

def entrerX(): #Entrer le nbres de ligne du plateau
    x = input("Entrer le nombre de ligne: ")
    try:
        x = int(x)
        if(x <=0):
            return entrerX()
    except:
        print("Entrer une valeur correcte")
        return entrerX()
    return x

def entrerY(): #Entrer le nbres de colonne du plateau
    y = input("Entrer le nombre de Colonne: ")
    try:
        y= int(y)
        if(y <=0):
            return entrerY()
    except:
        print("Entrer une valeur correcte")
        return entrerY()
    return y

def Saisir_Taille_jeu():
    x =  entrerX()
    y = entrerY()
    return x,y

def Placer_mines(grille,n_mines,m,n): # fonction qui place n mines aleatoires dans la grille   
    for i in range(n_mines):
        # Choisi des valeurs aleatoires
        lig = randrange(m) 
        col = randrange(n)

        while grille[lig][col] == MINE: #Choisi d'autres valeurs si la valeur choisie est une mine
            lig = randrange(m)
            col = randrange(n)
        
        grille[lig][col] = MINE #place la mine

        #Met le nombre de mine qu'il y a aux alentoures
        if  lig-1>=0 and col-1>=0 and grille[lig-1][col-1] != 'X' :
            grille[lig-1][col-1] += 1
                
        if  col-1>=0 and grille[lig][col-1] != 'X':
            grille[lig][col-1] += 1

        if ( (col-1>=0) and (lig+1<m) and grille[lig+1][col-1] != 'X'):
            grille[lig+1][col-1] += 1

        if lig+1<m and grille[lig+1][col] != 'X':
            grille[lig+1][col] += 1

        if ( (lig+1<m) and (col+1<n) and grille[lig+1][col+1] != 'X'):
            grille[lig+1][col+1] += 1
                
        if  col+1<n and grille[lig][col+1] != 'X':
            grille[lig][col+1] += 1

        if  (lig-1>=0) and (col+1<n) and (grille[lig-1][col+1] != 'X'):
            grille[lig-1][col+1] += 1

        if lig-1>=0 and grille[lig-1][col] != 'X':
            grille[lig-1][col] += 1


def  init_grille(m,n,n_mines):
    #initialise le plateau de jeu
    grille = []
    for i in range(m):
        L_2 = []
        for j in range(n):
            L_2.append(0)
        grille.append(L_2)
    Placer_mines(grille,n_mines,m,n) # place les mines dans le plateau
    return grille

def init_grille_joueur(m,n): #Creer une grille pour le joueur
    grille = []
    for i in range(m):
        L_2 = []
        for j in range(n):
            L_2.append(0)
        grille.append(L_2)
    return grille

def afficheGrille(grille,m,n): #Affiche une grille dans le console
    for i in range(m):
        for j in range(n):
            print(grille[i][j], end=" ")
        print()


def fenetre_principale(m,n):  # Création de la fenêtre principale
    bord1 = 40
    bord2 = bord1 + 30
    root = Tk() 
    root.title("Démineur")          
    root.geometry( str( LARGEUR_CASE * n + bord1)+'x'+str( HAUTEUR_CASE*m + bord2))
    return root

def  init_canvas(root,m,n):
    # Creation du canva
    bord = 2
    canvas = Canvas(root,height=m*HAUTEUR_CASE +100 ,width=n*LARGEUR_CASE+bord,bg='white')
    canvas.pack()

    for i in range(M):
        for j in range(N):
            #creation des Cases
            x1 = j*LARGEUR_CASE + bord
            y1 =  i *HAUTEUR_CASE + bord
            x2 = j*LARGEUR_CASE+LARGEUR_CASE +bord
            y2 =  bord + i*HAUTEUR_CASE+HAUTEUR_CASE
            canvas.create_rectangle(x1, y1 ,x2, y2 ,width=BORDURE,fill='gray',outline="lightgray")    
    
    btn = Button(root, text='Rejouer', width=5, height=1, bd='5', command=rejouer)
    btn.place(x=HAUTEUR_CASE*5, y=470)
    return canvas

def get_case(event): #retourne le numéro de ligne et de colonne de la case du Canvas ou se trouve le point de la fenêtre de coordonnées(x, y)
    canvas = event.widget
    shapes = sorted(canvas.find_overlapping(event.x, event.y, event.x, event.y))
    
    if len(shapes) == 0:
        return -1, -1
    x = (shapes[0]-1)//N
    y = (shapes[0]-1)%N
    return x, y

def indice(x,y): #retourne l'indice du rectangle ou se trouve le point x,y
    if x<0 or y <0 or x>=M or y>=N: #-1 si le point n'est pas dans le plateau de jeu
        return -1 
    i = (x*N) + (y+1)
    return i

def creuser(x,y,canvas): 
    # 0 pas creuser, -1 creuser, 1 drapeau?

    #recupere les coordonnes de la case
    c_y = 5+y*LARGEUR_CASE+LARGEUR_CASE/2
    c_x = 5+x*HAUTEUR_CASE+HAUTEUR_CASE/2

    if grille_joueur[x][y] == -1 or grille_joueur[x][y] == 1: #ne peut pas etre creuser, 
        return
    
    grille_joueur[x][y] = -1 # creuse
    canvas.itemconfig(indice(x,y),fill = 'white')
    
    if grille[x][y] == MINE:  
        print("Perdu")
        canvas.create_text(c_y,c_x, text=chr(77), font=("Wingdings", 20, 'bold'), fill='purple') #affiche l'image d'une mine
        #Affiche toutes les mines restantes, car le jeu est termine
        for i in range (M):
            for j in range(N):
                if  (grille[i][j] == MINE):
                    c_y = 5+j*LARGEUR_CASE+LARGEUR_CASE/2
                    c_x = 5+i*HAUTEUR_CASE+HAUTEUR_CASE/2
                    canvas.create_text(c_y,c_x, text=chr(77), font=("Wingdings", 20, 'bold'), fill='purple')
        stop_and_print(False) #arrete la partie

    elif grille[x][y] > 0:#affiche le nombre de mines qu'il y a aux alentours
        if grille[x][y] == 1:
            color = 'blue'
        elif grille[x][y] == 2:
            color = 'green'
        else:
            color = 'red'

        nb = grille[x][y]
        canvas.create_text(c_y,c_x, text=str(nb)+' ', font=("", 20, 'bold'), fill=color) 
        test_gagne()

    else: #Creuse les Cases vides
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i>= 0 and i <M and j>=0 and j<N:
                    creuser(i,j,canvas)


def drapeau(x,y,canvas): #place les drapeaux
    #recupere les coordonnes de la case
    global DRAPEAU
    c_y = 5+y*LARGEUR_CASE+LARGEUR_CASE/2
    c_x = 5+x*HAUTEUR_CASE+HAUTEUR_CASE/2
    

    if grille_joueur[x][y] == 0: #place un drapeau
        grille_joueur[x][y] = 1
        DRAPEAU +=1
        canvas.create_text(c_y,c_x, text=chr(80), font=("Wingdings", 19, 'bold'), fill='purple',tag =str(c_x)+str(c_y))

    
    else: # retire un drapeau
        bord = 2
        grille_joueur[x][y] = 0
        DRAPEAU -=1
        canvas.delete(str(c_x)+str(c_y))

    return canvas

def clic_gauche(event): #creuser avec le clic gauche de la souris
    canvas = event.widget
    x,y = get_case(event)
    if(x !=-1 and y !=-1):
        creuser(x,y,canvas)

def clic_droit(event): #place un drapeau en reaction avec le clic droit
    canvas = event.widget
    x,y = get_case(event)
    if(x !=-1 and y !=-1):
        drapeau(x,y,canvas)


def entete(root): # L'affichage du nbres de mines, message, et le temps ecoule 
    
    #creation d'un frame
    frame = Frame(root)
    frame.config(bg="white")
    frame.pack(fill=BOTH, expand=True)

    #Ajoute une marge
    lbl = Label(frame, text="", bg='white')
    lbl.pack(side=LEFT, ipadx=8, ipady=5)

    #affiche le nbres de mines qu'il y a
    mines_label = Label(frame, text=str(NBR_MINE), bg="white", font=("Courier", 20, 'bold'), fg='red') 
    mines_label.pack(side=LEFT, ipadx=00, ipady=5)
    lbl = Label(frame, text=chr(77), font=("Wingdings", 20, 'bold'), bg='white') #l'image de la mine
    lbl.pack(side=LEFT, ipadx=0, ipady=4)

    #Affiche rien au centre / va afficher gagner ou perdre
    center_label = Label(frame, text="", bg="white")
    center_label.pack(fill="x", expand=True, side=LEFT)

    #Affiche le nbre de secondes 
    time_label = Label(frame, text="00:00", bg="white", font=("Courier", 20, 'bold'), fg='red')
    time_label.pack(side=LEFT, ipadx=0, ipady=5)

    #Ajoute une marge
    lbl = Label(frame, text="", bg='white') 
    lbl.pack(side=LEFT, ipadx=8, ipady=5)

    return mines_label, center_label, time_label


def maj_labels(): #permet de mettre a jour notre jeu
    mines_label.config(text=str(NBR_MINE - DRAPEAU) ) #Met a jour le nombre de mines restantes
    time_now = int(time.time() - START)

    #met a jour l'heure
    if (time_now//60) <10:
        minutes =  '0{}'.format(str( int (time_now//60)))
    elif (time_now//60) >=10:
        minutes = '{}'.format(str( int (time_now//60)))
    
    if (time_now%60) < 10:
        secondes =  '0{}'.format(str( int (time_now%60)))
    elif (time_now%60) >=10:
        secondes = '{}'.format(str( int (time_now%60)))

    msg = '{}:{}'.format(minutes,secondes)
    time_label.config(text= msg)

    if partie: #permet de mettre a jour tant que la partie joue
        root.after(100, maj_labels)

def test_gagne(): #verifie si on a gagne
    if NBR_MINE != DRAPEAU:
        return True
    for i in range (M):
        for j in range (N):
            if grille_joueur[i][j] == 0:
                return False
    stop_and_print(True)
    return True
    

def stop_and_print(gagne): #permet d'arreter la partie
    col = 'blue'
    if gagne:
        msg = 'Gagné !'       
    else:
        msg = 'Perdu !'
        col = "red"
    
    global partie
    global test
    global DRAPEAU
    DRAPEAU = 0
    test = False
    partie = False #arrete la partie
    center_label.config(text = msg, font=("Courier", 17, 'bold'),fg = col )
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    
def rejouer():
    print("ok past")
    root.destroy()
    global test
    test = True
    

# def pied(root):
#     frame = Frame(root)
#     frame.config(bg="white")
#     frame.pack(fill=BOTH, expand=True)

#     #Ajoute une marge
#     pied = Label(frame, text=" okkk", bg='white')
#     pied.pack(side=LEFT, ipadx=8, ipady=5)
#     # btn = Button(root, text='Rejouer', width=5, height=1, bd='5', command=rejouer)
#     # btn.place(x=700, y=640)
#     return pied      
##############programme principal###########################3

print("Bienvenu!!")
# M,N = Saisir_Taille_jeu()

test = True
while(test):
    grille = init_grille(M,N,NBR_MINE)
    grille_joueur = init_grille_joueur(M,N)

    root = fenetre_principale(M,N)
    mines_label, center_label, time_label = entete(root)
    canvas = init_canvas(root,M,N)
    partie = True

    canvas.bind('<Button-1>', clic_gauche, add='')
    canvas.bind('<Button-3>', clic_droit, add='')

    START = time.time()
    root.after(500, maj_labels)
    test = False
    root.mainloop()
