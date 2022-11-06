import imp
from random import *
from tkinter import * 
import tkinter as tk  
import time
MINE = 'X'
NBR_MINE = 10
DRAPEAU = 0
M = 17 #nbres lignes
N = 10 #nbres col

BORDURE =  2 #bordure des rectangles
LARGEUR_CASE = 25 #largeur des rectangles
HAUTEUR_CASE = 25 #hauteur des rectangles




def Placer_mines(grille,n_mines,m,n): # fonction qui place n mines aleatoires dans la grille   
    for i in range(n_mines):
        lig = randrange(m)
        col = randrange(n)

        while grille[lig][col] == MINE:
            lig = randrange(m)
            col = randrange(n)
        
        grille[lig][col] = MINE
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


def palcerNbrsMine(grille,m,n): #fonction qui met a jour les valeurs de la grille en fonction du nbres de mines aux alentours
    
    for i in range(m): #mbr de ligne
        for j in range(n): #nbre de colonne
            if grille[i][j] == MINE: # verifie si la grille est une mine
                if  i-1>=0 and j-1>=0 and grille[i-1][j-1] != 'X' :
                    grille[i-1][j-1] += 1
                
                if  j-1>=0 and grille[i][j-1] != 'X':
                    grille[i][j-1] += 1

                if ( (j-1>=0) and (i+1<m) and grille[i+1][j-1] != 'X'):
                    grille[i+1][j-1] += 1

                if i+1<m and grille[i+1][j] != 'X':
                    grille[i+1][j] += 1

                if ( (i+1<m) and (j+1<n) and grille[i+1][j+1] != 'X'):
                    grille[i+1][j+1] += 1
                
                if  j+1<n and grille[i][j+1] != 'X':
                    grille[i][j+1] += 1

                if  (i-1>=0) and (j+1<n) and (grille[i-1][j+1] != 'X'):
                    grille[i-1][j+1] += 1

                if i-1>=0 and grille[i-1][j] != 'X':
                    grille[i-1][j] += 1

def  init_grille(m,n,n_mines):
    grille = []
    for i in range(m):
        L_2 = []
        for j in range(n):
            L_2.append(0)
        grille.append(L_2)

    Placer_mines(grille,n_mines,m,n)
    return grille


def fenetre_principale(m,n):
    bord1 = 40
    bord2 = bord1 + 30

    root = Tk() 
    root.title("Démineur")    
      # Création de la fenêtre principale
    
    root.geometry( str( LARGEUR_CASE * n + bord1)+'x'+str( HAUTEUR_CASE*m + bord2))
    return root

def  init_canvas(root,m,n):
    bord = 2
    canvas = Canvas(root,height=m*HAUTEUR_CASE +bord ,width=n*LARGEUR_CASE+bord,bg='white')
    canvas.pack()

    grilleCanva = []
    for i in range(M):
        L_2 = []
        for j in range(N):
            id = canvas.create_rectangle(j*LARGEUR_CASE + bord,  i *HAUTEUR_CASE + bord ,j*LARGEUR_CASE+LARGEUR_CASE +bord,  bord + i*HAUTEUR_CASE+HAUTEUR_CASE  ,width=BORDURE,fill='gray',outline="lightgray")
            L_2.append(id)
        grilleCanva.append(L_2)
    
    return canvas,grilleCanva

def get_case(event):
    canvas = event.widget
    shapes = sorted(canvas.find_overlapping(event.x, event.y, event.x, event.y))
    
    if len(shapes) == 0:
        return -1, -1
    x = (shapes[0]-1)//N
    y = (shapes[0]-1)%N
    return x, y

def indice(x,y):
    if x<0 or y <0 or x>=M or y>=N:
        return -1
    i = (x*10) + (y+1)
    return i

def creuser(x,y,canvas):
    # 0 pas creuser -1 creuser 1 drapeau?
    
    c_y = 5+y*LARGEUR_CASE+LARGEUR_CASE/2
    c_x = 5+x*HAUTEUR_CASE+HAUTEUR_CASE/2

    if grille_joueur[x][y] == -1 or grille_joueur[x][y] == 1:
        return
    
    grille_joueur[x][y] = -1 
    t =  indice(x,y)
    canvas.itemconfig(t,fill = 'white')
    
    if grille[x][y] == MINE:  
        print("Perdu")
        canvas.create_text(c_y,c_x, text=chr(77), font=("Wingdings", 20, 'bold'), fill='purple')
        for i in range (M):
            for j in range(N):
                if  (grille[i][j] == MINE):
                    c_y = 5+j*LARGEUR_CASE+LARGEUR_CASE/2
                    c_x = 5+i*HAUTEUR_CASE+HAUTEUR_CASE/2
                    canvas.create_text(c_y,c_x, text=chr(77), font=("Wingdings", 20, 'bold'), fill='purple')
        stop_and_print(False)

    elif grille[x][y] > 0:
        color=''
        if grille[x][y] == 1:
            color = 'blue'
        if grille[x][y] == 2:
            color = 'green'
        if grille[x][y] >2:
            color = 'red'
        nb = grille[x][y]
        canvas.create_text(c_y,c_x, text=str(nb)+' ', font=("", 20, 'bold'), fill=color)
        test_gagne()

        

    elif  grille[x][y] == 0:
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i>= 0 and i <M and j>=0 and j<N:
                    creuser(i,j,canvas)



def clic_gauche(event):
    canvas = event.widget
    x,y = get_case(event)
    if(x !=-1 and y !=-1):
        creuser(x,y,canvas)

def drapeau(x,y,canvas):
    i =  indice(x,y)
    c_y = 5+y*LARGEUR_CASE+LARGEUR_CASE/2
    c_x = 5+x*HAUTEUR_CASE+HAUTEUR_CASE/2
    global DRAPEAU

    if grille_joueur[x][y] == 0:
        grille_joueur[x][y] = 1
        DRAPEAU +=1
        canvas.create_text(c_y,c_x, text=chr(80), font=("Wingdings", 19, 'bold'), fill='purple')

    
    else:
        bord = 2
        grille_joueur[x][y] = 0
        DRAPEAU -=1
        canvas.create_rectangle(y*LARGEUR_CASE + bord,  x *HAUTEUR_CASE + bord ,y*LARGEUR_CASE+LARGEUR_CASE +bord,  bord + x*HAUTEUR_CASE+HAUTEUR_CASE  ,width=BORDURE,fill='gray',outline="lightgray")
        
    return canvas

def clic_droit(event):
    canvas = event.widget
    x,y = get_case(event)
    # if(x !=-1 and y !=-1):
    drapeau(x,y,canvas)

def init_grille_joueur(m,n):
    grille = []
    for i in range(m):
        L_2 = []
        for j in range(n):
            L_2.append(0)
        grille.append(L_2)
    return grille

def afficheGrille(grille,m,n):
    for i in range(m):
        for j in range(n):
            print(grille[i][j], end=" ")
        print()

def entete(root):
    
    frame = Frame(root)
    frame.config(bg="white")
    frame.pack(fill=BOTH, expand=True)

    lbl = Label(frame, text="", bg='white')
    lbl.pack(side=LEFT, ipadx=8, ipady=5)

    mines_label = Label(frame, text=str(NBR_MINE), bg="white", font=("Courier", 20, 'bold'), fg='red')
    mines_label.pack(side=LEFT, ipadx=00, ipady=5)

    lbl = Label(frame, text=chr(77), font=("Wingdings", 20, 'bold'), bg='white')
    lbl.pack(side=LEFT, ipadx=0, ipady=4)

    center_label = Label(frame, text="", bg="white")
    center_label.pack(fill="x", expand=True, side=LEFT)

    time_label = Label(frame, text="00:00", bg="white", font=("Courier", 20, 'bold'), fg='red')
    time_label.pack(side=LEFT, ipadx=0, ipady=5)

    lbl = Label(frame, text="", bg='white')
    lbl.pack(side=LEFT, ipadx=8, ipady=5)

    return mines_label, center_label, time_label


def maj_labels():
    mines_label.config(text=str(NBR_MINE - DRAPEAU) )

    time_now = int(time.time() - START)

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

    if partie == True:
        root.after(500, maj_labels)

def test_gagne():

    if NBR_MINE != DRAPEAU:
        return True
    for i in range (M):
        for j in range (N):
            if grille_joueur[i][j] == 0:
                return False
    stop_and_print(True)
    

def stop_and_print(gagne):
    if gagne:
        msg = 'Gagne'
        
    else:
        msg = 'Perdu'
    
    global partie
    partie = False
    center_label.config(text = msg, font=("Courier", 20, 'bold') )
    canvas.unbind('<Button-3>')
    canvas.unbind('<Button-1>')
    
        
##############programme principal###########################3

print("Bienvenu!!")

grille = init_grille(M,N,NBR_MINE)
grille_joueur = init_grille_joueur(M,N)
root = fenetre_principale(M,N)
mines_label, center_label, time_label = entete(root)
canvas,grilleCanvas = init_canvas(root,M,N)

partie = True

canvas.bind('<Button-1>', clic_gauche, add='')
canvas.bind('<Button-3>', clic_droit, add='')

START = time.time()
root.after(500, maj_labels)
root.mainloop()