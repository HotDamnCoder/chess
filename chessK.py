"""
Töö autor:
    Karl Müllerbeck

Ülesandeks oli luua Command Line's male mängu loomine, kus kasutaja saab liigutada oma nuppe käsklustega.
Command Line's näidatakse kasutajale male lauda ASCII art'ina, mis jääb alati samasse asukohta ning selle all on koht,
kus kasutajad saavad sisse kirjutada valge või musta käigu nagu enne mainitud.
See mängu osa on selle nö. frontend

Et mängu jooksutada, on vaja käivitada see skript püütoni shelli kaudu, thonny konsoolis "cls" ei tööta nagu see töötab CMD pythoni shellis

"""

import os
from chessM import *

def render(k_kord):
    os.system("cls")
    
    print("\n    A   B   C   D   E   F   G   H\n  ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗\n1 ║", end = "") #ASCII arti teha pole kõige toredam
    
    for y in "12345678":
        for x in "ABCDEFGH":
            if mäng.laud[x][y] == None:   #kui ruut on tühi siis tekitab tühimikud, kui ei ole, siis paneb sinna nupu
                for letter in "ACEG":   #tekitab tühimikud ja ruudud ruudud ACEG veergudesse
                    if x == letter and int(y)%2 == 0:   #paaris arvude puhul ruut 
                        if not x == "H":   #H tähe puhul ta ei pane viimast post, see oleks üleliigne ja ei näeks hea välja
                            print(" ■ │", end="")
                            break
                        else:
                            print(" ■ ", end="")
                            break
                    elif x == letter and not int(y)%2 == 0:   #paaritute arvude puhul tühik
                        if not x == "H":
                            print("   │", end="")
                            break
                        else:
                            print("   ", end="")
                            break
                for letter in "BDFH":   #tekitab tühimikud ja ruudud ruudud BDFH veergudesse
                    if x == letter and not int(y)%2 == 0:
                        if not x == "H":
                            print(" ■ │", end="")
                            break
                        else:
                            print(" ■ ", end="")
                            break
                    elif x == letter and int(y)%2 == 0:
                        if not x == "H":
                            print("   │", end="")
                            break
                        else:
                            print("   ", end="")
                            break
            elif x == "H":   #H tähe puhul poste pole, täidab laua nuppudega
                if mäng.laud[x][y].värv == "B":
                    print(" " + mäng.laud[x][y].tähis + " ", end="")
                else:
                    print(" " + mäng.laud[x][y].tähis.lower() + " ", end="")
            else:   #täidab laua nuppudega
                if mäng.laud[x][y].värv == "B":
                    print(" " + mäng.laud[x][y].tähis + " │", end="")
                else:
                    print(" " + mäng.laud[x][y].tähis.lower() + " │", end="")
                
                    
        if not y == "8": #vahe postid
            print(f"║ {y}  \n  ╟───┼───┼───┼───┼───┼───┼───┼───╢\n{int(y)+1} ║", end = "")
        else:
            print("║", end = "")          
    print(" 8\n  ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝\n    A   B   C   D   E   F   G   H\n q - Välju\n Väikeste tähtedega nupud on valged\n")
    if k_kord == "B":
        print(" Musta käik\n")
    else:
        print(" Valge käik\n")
        

vk = lambda x: exit() if x.lower() == "q" else False   #kontrollib kas string on q ja selle alusel väljub või ei tee midagi

def valik():
    valik = input("Kas alustada uuesti, y/n\n")
    if valik.lower() == "y":
        mäng.restart() #mängu taasalustamine
        return
    elif valik.lower() == "n":
        exit()
    else:
        print(" See polnud üks valikutest")
        valik()
        

def liikumine(kkord, error = None, tkäike = 0):
    render(kkord)
    if mäng.lõpp() == (True, False) or mäng.lõpp() == (False, True):   #kui on šahhmatt siis küsib kas alustada uuesti või mitte "valik()" funktsiooni abil
        if mäng.lõpp() == (True, False):
            print(f" Šahhmatt, must võitis, mängus tehti {tkäike} käiku")
            valik()
            return
        else:
            print(" Šahhmatt, valge võitis, mängus tehti {tkäike} käiku")
            valik()
            return
    
    if not error == None: #kui rekursioon toimus errorita siis renderdab male laua nii sama, kui erroriga, siis renderdab ja prindib errori
        render(kkord)
        print(error)
    else:
        render(kkord)
    
    alg_koord = input(" Nupu koordinaat: ").upper()
    
    vk(alg_koord)
    
    if not len(alg_koord) == 2 or not alg_koord[0] in "ABCDEFGH" or not alg_koord[1] in "12345678":   #kontrollib, kas selline koordinaat on malelaual
        liikumine(kkord, " Sellist koordinaati pole male laual")
        return
    
    if mäng.laud[alg_koord[0]][alg_koord[1]] == None:  #kontrollib kas valitud ruut on tühi
        liikumine(kkord, " Sellel ruudul pole nuppu")
        return
        
    if not mäng.laud[alg_koord[0]][alg_koord[1]].värv == kkord:   #kontrollib, kas käidakse õige poole nupuga
        if kkord == "B":
            liikumine(kkord, " Praegu on musta kord aga valiti valge nupp")
            return
        else:
            liikumine(kkord, " Praegu on valge kord aga valiti must nupp")
            return
            
    render(kkord)

    lõpp_koord = input(f" {mäng.laud[alg_koord[0]][alg_koord[1]].__class__.__name__} koordinaadil {alg_koord} liigutatakse koordinaadile: ").upper()
    vk(lõpp_koord)
    
    if not lõpp_koord[0] in "ABCDEFGH" or not lõpp_koord[1] in "12345678":   #kontrollib, kas selline koordinaat on malelaual
        print(" Sellist koordinaati pole male laual")
        liikumine(kkord)
        return
    else:
        val = mäng.laud[alg_koord[0]][alg_koord[1]].liigu(lõpp_koord)
        if not val == True: #   kontrollib, kas valitud nupp on kunigas, kui on ja lõppruut on ruut, kuhu saab vangerdada vastava poole kuningaga, siis vangerdab.
            if mäng.laud[alg_koord[0]][alg_koord[1]].tähis == "K" and \
               (mäng.laud[alg_koord[0]][alg_koord[1]].värv == "W" and lõpp_koord == "C1" or lõpp_koord == "G1") or \
               (mäng.laud[alg_koord[0]][alg_koord[1]].värv == "B" and lõpp_koord == "C8" or lõpp_koord == "G8"):
                mäng.laud[alg_koord[0]][alg_koord[1]].vangerdus(lõpp_koord)
                return
            else:
                liikumine(kkord, val)# kui nupp ei ole kunigas üritab liikuda tavaliselt
                return
                
        
    
        
        
def main():
    mäng.restart()#mängu taasalustamine, st. paneb kõik nupud laual oma kohtadele
    käike = 0
    kord = ""
    while 1:
        if not mäng.lõpp() == (False, False):# kui tekib šahhmatt vahepole kummal poolel, siis muudab käikude lugeja tagasi nulliks
            käike = 0
            
        if käike % 2 == 0:#määrab kelle kord on paaris arvudel on valge kord, paaritutel musta kord
            kord = "W"
        else:
            kord = "B"
            
        liikumine(kord, tkäike = käike)
        
        käike += 1
        
main()

