#(état actuel, action prise, nouvel état, résultat)

#1 Mamadou sokone aprés (à zall)
#2 bou aliou (reçu)
#3 ibrahima sy (à zall)
#4 Assane Dieme (à zall)
#5 Abdoulaye DIA aprés korité(reçu)
#6 sanoussi moundir sene aprés korité(à zall)
#7 
import random as r
import random
import os
import json
import time
def get_datas():
    datas=[]
    with open('ai_datas.json', 'r', encoding='utf-8') as files:
        try:
            datas=json.load(files)            
        except json.JSONDecodeError:
            datas=[]
    if(datas==None):
        datas=[]
    return datas
def save_datas(datas):
    datas_clean=[]
    for data in datas:
        for row in datas:
            for other in datas:
                pass


    with open('ai_datas.json', 'w', encoding='utf-8') as file:
        json.dump(datas, file, ensure_ascii=False, indent=4)


def creer_barragess():
    nbr = r.randint(2, 5)
    barrages=[]
    print(f" Nombre de barrages: {nbr}")
    for c in range(nbr):
        while True:
                x, y = r.randint(0,9), r.randint(0,9)
                if((x,y) in barrages):
                    pass
                else:
                    barrages.append((x,y))
                    break 
    return barrages
def creer_refuges(barrages):
    refuges=[]
    nbr = r.randint(1,3)
    print(f" Nombre de refuges: {nbr}")
    for c in range(nbr):
        while True:
                x, y = r.randint(0,9), r.randint(0,9)
                if((x,y) in barrages or (x,y) in refuges):
                    pass
                else:
                    refuges.append((x,y))
                    break 
    return refuges
def positionne(barrages, refuge):
    while True:
          x, y = r.randint(0,9), r.randint(0,9)
          if(not (x,y) in barrages and not (x,y) in refuge):
               player= (x,y)
               break
    return player
def creer_coffre(barrages, refuges, player):
    while True:
          x, y = r.randint(0,9), r.randint(0,9)
          if(not (x,y) in barrages and not (x,y) in refuges and (x,y)!=player):               
                coffre=(x,y)
                break
    print(f" coffre : $")
    return coffre
def creer_chien(barrages, refuges, player, coffre):
    while True:
          x, y = r.randint(0,9), r.randint(0,9)
          if(not (x,y) in barrages and not (x,y) in refuges and (x,y)!=player and (x,y)!=coffre):               
                chien= (x,y)
                break
    return chien

def afficher(barrages, refuges, player, coffre, chien, score):
    print(f" Score: {score}")
    for l in range(10):
        row = ""    
        for c in range(10):
            el=""
            if ((l,c) in barrages):
                el= " ⛔"
            elif ((l,c) in refuges):
                el= " 🏡"
            elif((l,c)==player):
                el= " 🧑"
                dx = chien[0]-player[0] if(chien[0]>player[0]) else player[0]-chien[0]
                dy = chien[1]-player[1] if(chien[1]>player[1]) else player[1]-chien[1]
                if(((dx==0 and dy==1) or (dx==1 and dy==0)) and player not in refuges):
                    el= "  ☠"
            elif((l,c)==chien):
                el= " 🐯"
            elif((l,c)==coffre):
                el= " 💰"
            else:             
                el= "  ."
        
            row+=el
        print(row)
def auto_move(barrages, refuges, player, chien, level):
    dx = chien[0]-player[0] if(chien[0]>player[0]) else player[0]-chien[0]
    dy = chien[1]-player[1] if(chien[1]>player[1]) else player[1]-chien[1]
    if(((dx==0 and dy==1) or (dx==1 and dy==0)) and player not in refuges):
        return chien
    best=(0,0)
    x1, y1 = chien[0], chien[1]
    x2, y2 = player[0], player[1]
    dx = x1-x2 if(x1>x2) else x2-x1
    dy = y1-y2 if(y1>y2) else y2-y1

    if(dx<dy):
        if(x1==x2):
            if(y1<y2):
                best= (x1,y1+1)
            elif(y1>y2):
                best= (x1,y1-1)
        else:
            if(x1<x2):
                best= (x1+1,y1)
            elif(x1>x2):
                best= (x1-1,y1)
    elif(dx>dy):
        if(y1==y2):
            if(x1<x2):                
                best= (x1+1,y1)
            elif(x1>x2):
                best= (x1-1,y1)
        else:
            if(y1<y2):        
                best= (x1,y1+1)
            elif(y1>y2):
                best= (x1,y1-1)
    else:
        if(x1>x2):
            best= (x1-1,y1)
        elif(x1<x2):
            best= (x1+1,y1)
    
    x= chien[0]
    y= chien[1]

    


    puissanceparniveau= [4,6,7,9]
    niveau = level-1
    puissance= puissanceparniveau[niveau]
    valids=[]
    for i in range(puissance):
        valids.append(best)
    
    valids.append((x,y-1) if(y-1>1) else chien)
    valids.append((x,y+1) if(y+1<10) else chien)
    valids.append((x-1,y) if(x-1>1) else chien)
    valids.append((x+1,y) if(x+1<10) else chien)

    if(chien in valids):
        valids.remove(chien)
    while True:        
        chien_next = r.choice(valids)    
        if(chien_next not in  barrages and chien_next not in  refuges):
            break
    if(chien_next[0]<0 or chien_next[1]<0 or chien_next[0]>9 or chien_next[1]>9):
        return chien
    return chien_next
def auto_play(player, coffre, barrages, chien):
        y1, x1 = player
        y2, x2 = coffre
        print(f"x1:{x1}y1:{y1}     x2:{x2}y2:{y2}")
        directions= {'t':(x1, y1-1), 'b':(x1, y1+1), 'r':(x1+1, y1), 'l':(x1-1, y1)}
        distances={'t':y1-y2,'b':y2-y1, 'l':x1-x2,'r':x2-x1}
        directions_valids=directions.copy()
        distances_valids=distances.copy()
        for k, v in directions.items():
            y,x= v
            if(v in barrages):
                directions_valids.pop(k)
                distances_valids.pop(k)
            elif(x>9 or y>9 or x<0 or y<0):
                directions_valids.pop(k)
                distances_valids.pop(k)
        
        if(len(list(directions_valids.items()))==0):
            print(f"aucun chemin :{directions_valids.items()}")
            return 'p'
        else:    
            distances_valids = dict(sorted(distances_valids.items(), key=lambda item: item[1]))
            fast_path = list(distances_valids.keys())[0]
            for k, v in distances_valids.items():
                if(v==0 and (k=='t' or k=='b')):
                        if('l' in list(distances_valids.keys())):
                            if('r' in list(distances_valids.keys())):
                                
                                pass
                        elif('r' in list(distances_valids.keys())):
                            return 'r'
                        else:
                            return 'p'

                pass

            print(distances_valids)
            print(fast_path)
            return fast_path



def action (level=0, mode="auto"):
    level = int(input(" Donner le niveau que vous jouez entre 1 et 4:")) if(level==0) else level
    barrages = creer_barragess()
    refuges = creer_refuges(barrages)
    player = positionne(barrages, refuges)
    coffre = creer_coffre(barrages, refuges, player)
    chien= creer_chien(barrages, refuges, player, coffre)
    score=0
    datas_ia = get_datas()
    parcours = []
    while True:
        dx = chien[0]-player[0] if(chien[0]>player[0]) else player[0]-chien[0]
        dy = chien[1]-player[1] if(chien[1]>player[1]) else player[1]-chien[1]
        if(((dx==0 and dy==1) or (dx==1 and dy==0)) and player not in refuges):        
            afficher(barrages, refuges, player , coffre, chien, score)
            print("Vous avez perdu !")
            break
        afficher(barrages, refuges, player , coffre, chien, score)
        

        
        direction=""
        if(mode=="auto"):
            direction = auto_play(player, coffre, barrages, chien) 

            x1, y1 =  player[0], player[1]
            x2, y2 =chien[0], chien[1]
        else:
            direction= input("t/haut, b/bas, r/droit, l/gauche")

        next_x, next_y = 0, 0
        position= [(player[0], player[1]),
                         (coffre[0], coffre[1]),
                         (chien[0], chien[1])
                         ]
        if(mode=="auto"):
            time.sleep(15)
        os.system("cls" if os.name == "nt" else "clear")
        match direction:
            case "t":
                if(player==chien):
                    player=player
                elif(player[0]>0 ):
                    if(not (player[0]-1,player[1]) in barrages):
                        player= (player[0]-1, player[1])
                        next_x, next_y = 0, -1

            case "b":
                if(player==chien):
                    player=player
                elif(player[0]<9):
                    if(not (player[0]+1,player[1]) in barrages):
                        player= (player[0]+1,player[1])
                        next_x, next_y = 0, 1
            case "l":
                if(player==chien):
                    player=player
                elif(player[1]>0 ):
                    if(not (player[0],player[1]-1) in barrages):
                        player= (player[0],player[1]-1)
                        next_x, next_y = -1, 0
            case "r":
                if(player==chien):
                    player=player
                elif(player[1]<9 ):
                    if(not (player[0],player[1]+1) in barrages):
                        player= (player[0],player[1]+1)
                        next_x, next_y = 1, 0
            case "p":
                pass
            case _:
                break
        position.append((next_x, next_y))
        parcours.append(position)   
        if(player==coffre):
            score +=1
            datas_ia.append(parcours)
            parcours=[]
            #save_datas(datas_ia)
            coffre = creer_coffre(barrages, refuges, player)
        chien = auto_move(barrages, refuges, player, chien, level)

mode= input("quel mode utilisez vous (man/auto): ")
level= int(input("quel niveau utilisez vous (1 à 4): "))
nbr= int(input("Combien de tentative souhaitez vous: "))

for i in range(nbr): 
    os.system("cls" if os.name == "nt" else "clear")
    action(level, mode)