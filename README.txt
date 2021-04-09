Aide pour les informations transmis à l'agent

Q : 'À quelle heure le meurtrier a laissé tomber son arme?'
R : 'Le meurtrier a laissé tomber son arme à {HeureDuCrime + 1} h'
ex : 'Le meurtrier a laissé tomber son arme à 0 h'

Q : 'Dans quel état se trouve le corps de {victime}?'
R : 'Le/La {PartieDuCorps} de {victime} est {Marque}'
ex : 'La poitrine de Mr Green est incisée'

-- Partie du corps et marque en fonction des différents types d'armes --

Arme : Couteau
PartieDuCorps : poitrine
Marque : incisée

Arme : Marteau
PartieDuCorps : crâne
Marque : fendu

Arme : Fusil
PartieDuCorps : poitrine
Marque : perforée

Arme : Corde
PartieDuCorps : cou
Marque : lacéré

Arme : Tronçonneuse
PartieDuCorps : corps
Marque : déchiqueté

Arme : Chandelier
PartieDuCorps : corps
Marque : calciné
