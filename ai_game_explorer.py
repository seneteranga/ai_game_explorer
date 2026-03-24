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
    with open('ai_datas.json', 'w', encoding='utf-8') as file:
        json.dump(datas, file, ensure_ascii=False, indent=4)


def creer_barragess():
    nbr = r.randint(2, 4)
    barrages=[]
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
          x,y = r.randint(0,9), r.randint(0,9)
          if(not (x,y) in barrages and not (x,y) in refuges and (x,y)!=player):               
                coffre=(x,y)
                break
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
    for y in range(10):
        row = ""    
        for x in range(10):
            el=""
            if ((x,y) in barrages):
                el= " ⛔"
            elif ((x,y) in refuges):
                el= " 🏡"
            elif((x,y)==player):
                el= " 🧑"
                dx = abs(chien[0]-player[0])
                dy = abs(chien[1]-player[1]) 
                if(((dy==0 and dx==1) or (dy==1 and dx==0) or chien==player) and player not in refuges):
                    el= "  ☠"
            elif((x,y)==chien):
                el= " 🐯"
            elif((x,y)==coffre):
                el= " 💰"
            else:             
                el= "  ."        
            row+=el
        print(row)
def auto_move(barrages, refuges, player, chien, level):
        x1, y1 = chien
        x2, y2 = player
        dt= abs((y1-1)-y2) + abs(x1-x2)
        db= abs((y1+1)-y2) + abs(x1-x2)
        dl= abs((x1-1)-x2) + abs(y1-y2)
        dr= abs((x1+1)-x2) + abs(y1-y2)
        directions= {'t':(x1, y1-1), 'b':(x1, y1+1), 'r':(x1+1, y1), 'l':(x1-1, y1)}
        distances={'t':dt,'b':db, 'l':dl,'r':dr}
        distances_valids={}
        valids=[]
        for k, v in directions.items():
            x,y= v
            if(v in barrages or v in refuges or y>9 or x>9 or y<0 or x<0):
                pass
            else:
                distances_valids[k]=distances.get(k) 
                   
        distances_valids = dict(sorted(distances_valids.items(), key= lambda item: item[1]))
        valids= list(distances_valids.keys())

        puissanceparniveau= [4,6,7,9]
        niveau = level-1
        puissance= puissanceparniveau[niveau]
        if(len(valids)==0):
            return chien
        else:
            for i in range(puissance):
                valids.append(valids[0])
        key = r.choice(valids)
        return directions.get(key)




def auto_play(player, coffre, barrages, chien):
        x1, y1 = player
        x2, y2 = coffre
        dt= abs((y1-1)-y2) + abs(x1-x2)
        db= abs((y1+1)-y2) + abs(x1-x2)
        dl= abs((x1-1)-x2) + abs(y1-y2)
        dr= abs((x1+1)-x2) + abs(y1-y2)
        directions= {'t':(x1, y1-1), 'b':(x1, y1+1), 'r':(x1+1, y1), 'l':(x1-1, y1)}
        distances={'t':dt,'b':db, 'l':dl,'r':dr}
        distances_valids={}
        for k, v in directions.items():
            x,y= v
            if(v in barrages or y>9 or x>9 or y<0 or x<0):
                pass
            else:
                distances_valids[k]=distances.get(k)    
        distances_valids = dict(sorted(distances_valids.items(), key= lambda item: item[1]))
        try:
            return list(distances_valids.keys())[0]
        except:
            return 'p'
        
 

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
    run = True
    while run:
        dx = abs(chien[0]-player[0])
        dy = abs(chien[1]-player[1])       
        direction=""

        os.system("cls" if os.name == "nt" else "clear")
        afficher(barrages, refuges, player , coffre, chien, score)
        if(((dy==0 and dx==1) or (dy==1 and dx==0) or chien==player) and player not in refuges):        
            print("Vous avez perdu !")
            run = False 
            break

        if(mode=="auto"):
            time.sleep(1)
            direction = auto_play(player, coffre, barrages, chien) 
        else:
            direction= input("t/haut, b/bas, r/droit, l/gauche")
        neyt_y, neyt_x = 0, 0
        position= [(player[0], player[1]),
                         (coffre[0], coffre[1]),
                         (chien[0], chien[1])
                         ]
        match direction:
            case "l":
                if(player==chien):
                    player=player
                elif(player[0]>0 ):
                    if(not (player[0]-1,player[1]) in barrages):
                        player= (player[0]-1, player[1])
                        neyt_x, neyt_y = 0, -1

            case "r":
                if(player==chien):
                    player=player
                elif(player[0]<9):
                    if(not (player[0]+1,player[1]) in barrages):
                        player= (player[0]+1,player[1])
                        neyt_x, neyt_y = 0, 1
            case "t":
                if(player==chien):
                    player=player
                elif(player[1]>0 ):
                    if(not (player[0],player[1]-1) in barrages):
                        player= (player[0],player[1]-1)
                        neyt_x, neyt_y = -1, 0
            case "b":
                if(player==chien):
                    player=player
                elif(player[1]<9 ):
                    if(not (player[0],player[1]+1) in barrages):
                        player= (player[0],player[1]+1)
                        neyt_x, neyt_y = 1, 0
            case "p":
                pass
            case _:
                break
        position.append((neyt_x, neyt_y))
        parcours.append(position)   
        if(player==coffre):
            score +=1
            datas_ia.append(parcours)
            parcours=[]
            #save_datas(datas_ia)
            coffre = creer_coffre(barrages, refuges, player)
        os.system("cls" if os.name == "nt" else "clear")
        afficher(barrages, refuges, player , coffre, chien, score)
        if(((dy==0 and dx==1) or (dy==1 and dx==0) or chien==player) and player not in refuges):        
            print("Vous avez perdu !")
            run = False
            break  
        else:                
            chien = auto_move(barrages, refuges, player, chien, level)
        if(mode=="auto"):
            time.sleep(1)

mode= input("quel mode utilisez vous (man/auto): ")
level= int(input("quel niveau utilisez vous (1 à 4): "))
nbr= int(input("Combien de tentative souhaitez vous: "))


for i in range(nbr): 
    os.system("cls" if os.name == "nt" else "clear")
    action(level, mode)