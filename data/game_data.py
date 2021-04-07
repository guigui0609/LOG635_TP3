from enum import Enum

class CharacterTypes(Enum):
    COLONEL_MUSTARD = "Colonel Mustard"
    MRS_WHITE = "Mrs White"
    MISS_SCARLET = "Miss Scarlet"
    MR_GREEN = "Mr Green"
    MRS_PEACOCK = "Mrs Peacock"
    PROFESSOR_PLUM = "Professor Plum"
    MISS_PEACH = "Miss Peach"
    MONSIEUR_BRUNETTE = "Monsieur Brunette"
    MADAME_ROSE = "Madame Rose"
    SERGENT_GRAY = "Sergent Gray"

class RoomTypes(Enum):
    HALL = "Hall"
    SALON = "Salon"
    CUISINE = "Cuisine"
    SALLE_A_MANGER = "Salle a manger"
    VERANDA = "Veranda"
    COURS = "Cours"
    SALLE_DE_JEU = "Salle de jeu"
    SALLE_DE_BAIN = "Salle de bain"
    CHAMBRE = "Chambre"
    GARAGE = "Garage"

class WeaponTypes(Enum):
    COUTEAU = "Couteau"
    MARTEAU = "Marteau"
    FUSIL = "Fusil"
    CORDE = "Corde"
    TRONCONNEUSE = "Tronçonneuse"
    CHANDELIER = "Chandelier"
