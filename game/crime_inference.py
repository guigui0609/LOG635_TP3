# Permet d'inferer qui est le meurtrier, quand, comment, où il a tué.
from demos.reasonning_system.aima.logic import *
from demos.reasonning_system.aima.utils import expr
import nltk


class CrimeInference:

    def __init__(self, rooms, characters, weapons):
        self.weapons = weapons
        self.rooms = rooms
        self.persons = characters

        # Liste de clauses (faits) qui seront stockées dans la base de connaissance.
        self.clauses = []

        self.base_clauses()
        self.initialize_KB()
        self.inference_rules()

        # Base de connaissances (First-order logic - FOL)
        self.crime_kb = FolKB(self.clauses)

    # Déclaration dans la logique du premier ordre
    def base_clauses(self):
        # Le paramètre est une arme
        self.arme_clause = 'Arme({})'

        # Le paramètre est une pièce
        self.piece_clause = 'Piece({})'

        # Le paramètre est une persone
        self.personne_clause = 'Personne({})'

        # paramètre 1 : arme; paramètre 2 : pièce
        # p.ex.: Le couteau se trouve dans la cuisine
        self.weapon_room_clause = 'Arme_Piece({},{})'

        # paramètre 1 : personne; paramètre 2 : pièce; paramètre 3 : heure
        # p.ex.: Mustart était dans la cuisine à 11h00
        self.person_room_hour_clause = 'Personne_Piece_Heure({}, {}, {})'

        # paramètre 1 : personne; paramètre 2 : piece
        # p.ex.: Mustard se trouve dans la cuisine
        self.person_room_clause = 'Personne_Piece({}, {})'

        # paramète 1 : personne
        # p. ex.: Mustard est mort
        self.dead_clause = 'EstMort({})'

        # paramète 1 : personne
        # p. ex.: Mustard est vivant
        self.alive_clause = 'EstVivant({})'

        # paramètre 1 : personne
        # p. ex.: Mustard est la victime
        self.victim_clause = 'Victime({})'

        # paramètre 1 : personne
        # p. ex.: Mustard a des marques au cou
        self.body_mark_clause = 'MarqueCou({})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.room_different_clause = 'PieceDifferente({},{})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.weapon_different_clause = 'ArmeDifferente({},{})'

        # paramètre 1 : heure
        self.crime_hour_clause = 'HeureCrime({})'

        # paramètre 1 : heure
        self.drop_weapon_hour_clause = 'HeureArmeTombee({})'

    def initialize_KB(self):
        # Clause pour differencier les pièces
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms)):
                if i != j:
                    # Le bureau est different de la cuisine = PieceDifferente(Bureau, Cuisine)
                    self.clauses.append(expr(self.room_different_clause.format(self.rooms[i], self.rooms[j])))

        # Clause pour differencier les armes
        for i in range(len(self.weapons)):
            for j in range(len(self.weapons)):
                if i != j:
                    # Le couteau est different de la corde = ArmeDifferente(Couteau, Corde)
                    self.clauses.append(expr(self.weapon_different_clause.format(self.weapons[i], self.weapons[j])))

        # Initialiser KB sur Armes, Pieces, Personnes
        for weapon in self.weapons:
            # Le couteau est une arme = Arme(Couteau)
            self.clauses.append(expr(self.arme_clause.format(weapon)))

        for room in self.rooms:
            # La cuisine est une pièce = Piece(Cuisine)
            self.clauses.append(expr(self.piece_clause.format(room)))

        for person in self.persons:
            # Mustar est une personne = Personne(Mustard)
            self.clauses.append(expr(self.personne_clause.format(person)))

    # Expressions dans la logique du premier ordre permettant de déduire les caractéristiques du meurtre
    def inference_rules(self):
        # Determine la piece du crime
        self.clauses.append(expr('EstMort(x) & Personne_Piece_Heure(x, y, z) & HeureActuelle(z) ==> PieceCrime(y)'))

        # Determiner l'arme du crime
        self.clauses.append(expr('Arme_Marque(x,y) & Personne_Marque(z,y) ==> ArmeCrime(y)'))

        # Determiner la pièce où le meurtrier à laissé tomber l'arme du crime
        self.clauses.append(expr('ArmeCrime(y) & Piece_Arme(x,y) ==> PieceArmeTombee(x)'))

        # Si la personne est morte alors elle est la victime et ce n'est pas un suicide
        self.clauses.append(expr('EstMort(x) ==> Victime(x)'))

        # Si la personne est morte alors elle est innocente et ce n'est pas un suicide
        self.clauses.append(expr('EstMort(x) ==> Innocent(x)'))

        # Si un arme n'est pas l'arme du crime, l'arme n'est pas l'arme du crime
        self.clauses.append(expr('Arme(x) & ArmeCrime(y) ==> ArmePasCrime(x)'))

        # Si une pièce n'est pas la pièce où à eu lieu le crime, la pièce n'est pas la pièce où à eu lieu le crime
        self.clauses.append(expr('Piece(x) & PieceCrime(y)  ==> PiecePasCrime(x)'))

        # Si une pièce n'est pas la pièce où se trouve l'arme du crime, la pièce n'est pas la pièce où se trouve l'arme
        # du crime
        self.clauses.append(expr('Piece(x) & PieceArmeTombee(y)  ==> PiecePasArmeTombee(x)'))

        # Si la personne se trouve dans une pièce qui n'est pas la pièce du crime à l'heure du crime, alors elle est
        # innocente
        self.clauses.append(expr('Personne_Piece_Heure(x, y, z) & HeureCrime(z) & PiecePasCrime(y) ==> Innocent(x)'))

        # Si la personne se trouve dans une pièce qui n'est pas la pièce où le meurtrier à laissé tomber son arme à
        # l'heure où le meurtrier à laissé tomber son arme, alors elle est innocente
        self.clauses.append(expr('Personne_Piece_Heure(x, y, z) & HeureArmeTombee(z) & PiecePasArmeTombee(y) ==> Innocent(x)'))

    # Ajouter des clauses, c'est-à-dire des faits, à la base de connaissances
    def add_clause(self, clause_string):
        self.crime_kb.tell(expr(clause_string))

    # Demander à la base de connaissances qui est la victime
    def get_victim(self):
        result = self.crime_kb.ask(expr('Victime(x)'))
        if not result:
            return False
        else:
            return result[x]

    # Demander à la base de connaissances la pièce du meurtre
    def get_crime_room(self):
        result = self.crime_kb.ask(expr('PieceCrime(x)'))
        if not result:
            return False
        else:
            return result[x]

    # Demander à la base de connaissances l'arme du meurtrier
    def get_crime_weapon(self):
        result = self.crime_kb.ask(expr('ArmeCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    # Demander à la base de connaissances l'heure du meurtre
    def get_crime_hour(self):
        result = self.crime_kb.ask(expr('HeureCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_crime_hour_plus_one(self):
        result = self.crime_kb.ask(expr('UneHeureApresCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    # Demander à la base de connaissances le suspect
    def get_suspect(self):
        result = self.crime_kb.ask(expr('Suspect(x)'))
        if not result:
            return result
        else:
            return result[x]

    # Demander à la base de connaissances la liste d'innocents
    def get_innocent(self):
        result = list(fol_bc_ask(self.crime_kb, expr('Innocent(x)')))
        res = []

        for elt in result:
            if not res.__contains__(elt[x]):
                res.append(elt[x])
        return res

    @staticmethod
    def create_clause(logic_data, *args):

        formatted_args = []
        for arg in args:
            if isinstance(arg,str):
                formatted_args.append(arg.replace(" ", ""))
            else:
                formatted_args.append(arg)

        return logic_data.format(*formatted_args)
