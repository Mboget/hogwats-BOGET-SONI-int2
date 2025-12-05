################################# Choice and management of the house #################################

class House:
    def __init__(self,nom = 'Gryffindor'):
        assert nom in ["Gryffindor","Slytherin","Hufflepuff","Ravenclaw"]
        self.nom = nom
        self.nombre_point = 0
    
    def ajout_point(self,nombre_point_ajouter):
        self.nombre_point += nombre_point_ajouter
    
    def afficher_point(self):
        return (f"Maison {self.nom}: {self.nombre_point} points")
    
test = [House("Gryffindor"),House("Slytherin"),House("Hufflepuff"),House("Ravenclaw")]    

def display_winning_houses(houses):
    max_nombre_point = houses[0].nombre_point
    nom_max_nombre_point = []
    for house in houses:
        if house.nombre_point >= max_nombre_point:
            nom_max_nombre_point.append( house.nom)
            max_nombre_point = house.nombre_point
    return str(nom_max_nombre_point)[1:-1].replace("'","")
    
#print(display_winning_houses(test))
