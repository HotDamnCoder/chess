class Mäng:
    def __init__(self):
        self.laud = {täht : {i : None for i in "12345678"} for täht in "ABCDEFGH"}
        self.nuppud = [Ettur("B", y + "7") for y in self.laud.keys()] + [Ettur("W", y + "2") for y in self.laud.keys()] + [ 
            Vanker("W", "A1"),
            Hobune("W", "B1"),
            Oda("W", "C1"),
            Lipp("W", "D1"),
            Kuningas("W", "E1"),
            Oda("W", "F1"),
            Hobune("W", "G1"),
            Vanker("W", "H1"),
            Vanker("B", "A8"),
            Hobune("B", "B8"),
            Oda("B", "C8"),
            Lipp("B", "D8"),
            Kuningas("B", "E8"),
            Oda("B", "F8"),
            Hobune("B", "G8"),
            Vanker("B", "H8")]
        
        for nupp in self.nuppud:
            if nupp.tähis == "K" and nupp.värv == "B":
                self.must_kuningas = nupp
            elif nupp.tähis == "K" and nupp.värv == "W":
                self.valge_kuningas = nupp
            self.laud[nupp.koht[0]][nupp.koht[1]] = nupp
   
    def tuli(self):
        for nupp in self.nuppud:
            if nupp.värv == "W" and nupp.saab_liikuda(self.must_kuningas.koht):
                return True, "W"
            elif nupp.värv == "B" and nupp.saab_liikuda(self.valge_kuningas.koht):
                return True, "B"    
        return False, ""
    
    def tuli_pool(self, pool):
        for nupp in self.nuppud:
            if nupp.värv != pool and nupp.saab_liikuda(self.must_kuningas.koht if pool == "B" else self.valge_kuningas.koht):
                return True
        return False
            
    def tuli_nupp(self, nupp, koht):
        
        nupp_2_koopia = self.laud[koht[0]][koht[1]]
        koht_koopia = nupp.koht
        self.laud[nupp.koht[0]][nupp.koht[1]] = None
        if self.laud[koht[0]][koht[1]] in self.nuppud:
            self.nuppud.remove(mäng.laud[koht[0]][koht[1]])
        self.laud[koht[0]][koht[1]] = nupp
        nupp.koht = koht
        tuli = self.tuli_pool(nupp.värv)
        nupp.koht = koht_koopia
        self.laud[koht[0]][koht[1]] = nupp_2_koopia
        if nupp_2_koopia is not None:
            self.nuppud.append(mäng.laud[koht[0]][koht[1]])
        self.laud[nupp.koht[0]][nupp.koht[1]] = nupp
        return tuli
    
    def lõpp(self):
        lõpp_valge = True
        lõpp_must = True
        for nupp in [nupp for nupp in self.nuppud if nupp.värv == "W"]:
            for x in "ABCDEFGH":
                for y in "12345678":
                     if nupp.saab_liikuda(x + y) and nupp.koht_vaba(x + y) and not mäng.tuli_nupp(nupp, x + y):
                        lõpp_valge = False
        for nupp in [nupp for nupp in self.nuppud if nupp.värv == "B"]:
            for x in "ABCDEFGH":
                for y in "12345678":
                     if nupp.saab_liikuda(x + y) and nupp.koht_vaba(x + y) and not mäng.tuli_nupp(nupp, x + y):
                        lõpp_must = False
        return lõpp_valge, lõpp_must
        
    def restart(self):
        self.__init__()
class Nupp:
    def __init__(self, värv, koht):
        self.värv = värv
        self.koht = koht
        self.algus_koht = koht
        
    def liigu(self, koht):
        if self.saab_liikuda(koht):
            if self.koht_vaba(koht):
                if not mäng.tuli_nupp(self, koht):
                    mäng.laud[self.koht[0]][self.koht[1]] = None
                    if mäng.laud[koht[0]][koht[1]] in mäng.nuppud:
                        mäng.nuppud.remove(mäng.laud[koht[0]][koht[1]])
                    mäng.laud[koht[0]][koht[1]] = self
                    self.koht = koht
                else:
                     return "Sellel kohal on tuli"
            else:
                return "See koht ei ole vaba"
        else:
            return "Nii ei saa selle nupuga liikuda"
            
    def set_vektorid(self, koht):
        pass
    
    def saab_liikuda(self, koht):
        self.set_vektorid(koht)

        return (ord(koht[0]) - ord(self.koht[0]), int(koht[1]) - int(self.koht[1])) in self.liikumise_vektorid
    
    def koht_vaba(self,koht):
        return mäng.laud[koht[0]][koht[1]] == None or (mäng.laud[koht[0]][koht[1]].värv != self.värv and mäng.laud[koht[0]][koht[1]].tähis != "K")

    def ees_vaba(self, koht):
        liikumine_x = ord(koht[0]) - ord(self.koht[0])
        liikumine_y = int(koht[1]) - int(self.koht[1])
        suund = lambda x : -1 if x < 0 else 1
        if liikumine_y== 0:
            ruudud = [mäng.laud[chr(ord(self.koht[0]) + x)][self.koht[1]] for x in range(suund(liikumine_x), liikumine_x, suund(liikumine_x)) if x != 0]
        else:
            ruudud = [mäng.laud[self.koht[0]][str(int(self.koht[1]) + y)] for y in range(suund(liikumine_y), liikumine_y, suund(liikumine_y)) if y != 0]
        for ruut in ruudud:
            if ruut != None:
                return False
        return True
    
    def diagonaal_vaba(self,koht):
        liikumine_y = ord(koht[0]) - ord(self.koht[0])
        liikumine_x = int(koht[1]) - int(self.koht[1])
        suund = lambda x : -1 if x < 0 else 1
        x_id = [x for x in range(suund(liikumine_x), liikumine_x, suund(liikumine_x)) if x != 0]
        y_id = [y for y in range(suund(liikumine_y), liikumine_y, suund(liikumine_y)) if y != 0]
        ruudud = [mäng.laud[chr(ord(self.koht[0]) + y)][str(int(self.koht[1]) + x)] for x, y in zip(x_id, y_id)]
        for ruut in ruudud:
            if ruut != None:
                return False
        return True
            
class Ettur(Nupp):
    tähis = "P"
    def set_vektorid(self, koht):
        koht_edasi = -1 if self.värv == "B" else 1
        if mäng.laud[koht[0]][koht[1]] == None:
            self.liikumise_vektorid = [(0, koht_edasi)]
        else:
            self.liikumise_vektorid = [(1, koht_edasi), (-1, koht_edasi)]
        if self.koht == self.algus_koht:
            self.liikumise_vektorid += [(0, koht_edasi * 2)]
      
               
class Vanker(Nupp):
    tähis = "R"
    def saab_liikuda(self,  koht):
        if koht[0] == self.koht[0] or koht[1] == self.koht[1]:
            return self.ees_vaba(koht)
        return False
class Hobune(Nupp):
    tähis = "N"
    liikumise_vektorid = [(1,2), (-1, 2), (1, -2), (-1, -2), (2,1), (-2, 1), (2, -1), (-2, -1)]
       
class Oda(Nupp):
    tähis = "B"
    def saab_liikuda(self, koht):
        if abs(ord(self.koht[0]) - ord(koht[0])) == abs(int(self.koht[1]) - int(koht[1])):
            return self.diagonaal_vaba(koht)
        return False
                
class Kuningas(Nupp):
    liikumise_vektorid = [(0,1), (0,-1), (1, -1), (1,1), (-1, -1), (-1, 1), (1,0), (-1, 0)]
    tähis = "K"
    def saab_vangerdada(self, koht):
        liikumine = ord(koht[0]) - ord(self.koht[0])
        if self.värv == "W":
            self.vangerdus_vanker = mäng.laud["H"]["1"] if liikumine > 0 else mäng.laud["A"]["1"] 
        else:
            self.vangerdus_vanker = mäng.laud["H"]["8"] if liikumine > 0 else mäng.laud["A"]["8"]
        self.vankri_vangerdus_koht = chr(ord(koht[0]) - 1) + koht[1] if liikumine > 0 else chr(ord(koht[0]) + 1) + koht[1]
        if Vanker.saab_liikuda(self, koht) and self.algus_koht == self.koht and self.vangerdus_vanker.koht == self.vangerdus_vanker.algus_koht:
            suund = lambda x : -1 if x < 0 else 1
            for x in range(suund(liikumine), liikumine, suund(liikumine)):
                if mäng.tuli_nupp(self, chr(ord(self.koht[0]) + x) + self.koht[1]):
                    return False
            return True
        return False
    
    def vangerdus(self, koht):
        if self.saab_vangerdada(koht):
            mäng.laud[self.koht[0]][self.koht[1]] = None
            mäng.laud[koht[0]][koht[1]] = self
            self.koht = koht
            mäng.laud[self.vangerdus_vanker.koht[0]][self.vangerdus_vanker.koht[1]] = None
            mäng.laud[self.vankri_vangerdus_koht[0]][self.vankri_vangerdus_koht[1]] = self.vangerdus_vanker
            self.vangerdus_vanker.koht = self.vankri_vangerdus_koht
        del self.vangerdus_vanker
        del self.vankri_vangerdus_koht
                 
class Lipp(Nupp):
    tähis = "Q"
    def saab_liikuda(self,koht):
        return Oda.saab_liikuda(self,koht) or Vanker.saab_liikuda(self, koht)
    
mäng = Mäng()
