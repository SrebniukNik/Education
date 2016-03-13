import random as rand
import string
import math

class AdoptionCenter:
    """
    The AdoptionCenter class stores the important information that a
    client would need to know about, such as the different numbers of
    species stored, the location, and the name. It also has a method to adopt a pet.
    """
    def __init__(self, name, species_types, location):
        self.name = name
        self.species_types = species_types
        self.location = (float(location[0]),float(location[1]))
    def get_number_of_species(self, animal):
        return self.species_types[animal]
    def get_location(self):
        return self.location
    def get_species_count(self):
        temp_dict = {}
        for key in self.species_types:
            if self.species_types[key] != 0:
                temp_dict[key] = self.species_types[key]
        return temp_dict
    def get_name(self):
        return self.name
    def adopt_pet(self, species):
        self.species_types[species] -= 1


class Adopter:
    """
    Adopters represent people interested in adopting a species.
    They have a desired species type that they want, and their score is
    simply the number of species that the shelter has of that species.
    """
    def __init__(self, name, desired_species):
        self.name = name
        self.desired_species = desired_species
    def get_name(self):
        return self.adopter_name
    def get_desired_species(self):
        return self.desired_species
    def get_score(self, adoption_center):
        return float(1 * adoption_center.species_types.get(self.desired_species, 0))



class FlexibleAdopter(Adopter):
    """
    A FlexibleAdopter still has one type of species that they desire,
    but they are also alright with considering other types of species.
    considered_species is a list containing the other species the adopter will consider
    Their score should be 1x their desired species + .3x all of their desired species
    """
    # Your Code Here, should contain an __init__ and a get_score method.
    def __init__(self, name, desired_species, considered_species):
        self.name = name
        self.desired_species = desired_species
        self.considered_species = considered_species
    def get_score(self, adoption_center):
        score = float(Adopter.get_score(self, adoption_center) + \
               0.3 * sum([ adoption_center.species_types.get(considered, 0) for considered in  self.considered_species]))
        #Return score
        return score if score > 0 else float(0.0)



class FearfulAdopter(Adopter):
    """
    A FearfulAdopter is afraid of a particular species of animal.
    If the adoption center has one or more of those animals in it, they will
    be a bit more reluctant to go there due to the presence of the feared species.
    Their score should be 1x number of desired species - .3x the number of feared species
    """
    # Your Code Here, should contain an __init__ and a get_score method.
    def __init__(self, name, desired_species, feared_species):
        self.name = name
        self.desired_species = desired_species
        self.feared_species = feared_species
    def get_score(self, adoption_center):
        score = float(Adopter.get_score(self, adoption_center) - \
               0.3 * adoption_center.species_types.get(self.feared_species, 0))
        #Return score
        return score if score > 0 else float(0.0)



class AllergicAdopter(Adopter):
    """
    An AllergicAdopter is extremely allergic to a one or more species and cannot
    even be around it a little bit! If the adoption center contains one or more of
    these animals, they will not go there.
    Score should be 0 if the center contains any of the animals, or 1x number of desired animals if not
    """
    # Your Code Here, should contain an __init__ and a get_score method.
    def __init__(self, name, desired_species, allergic_species):
        self.name = name
        self.desired_species = desired_species
        self.allergic_species = allergic_species
    def get_score(self, adoption_center):
        score = sum([ adoption_center.species_types.get(considered, 0) for considered in  self.allergic_species])
        #Return score
        return float(0.0) if score > 1 else float(Adopter.get_score(self, adoption_center))

class MedicatedAllergicAdopter(AllergicAdopter):
    """
    A MedicatedAllergicAdopter is extremely allergic to a particular species
    However! They have a medicine of varying effectiveness, which will be given in a dictionary
    To calculate the score for a specific adoption center, we want to find what is the most allergy-inducing species that the adoption center has for the particular MedicatedAllergicAdopter.
    To do this, first examine what species the AdoptionCenter has that the MedicatedAllergicAdopter is allergic to, then compare them to the medicine_effectiveness dictionary.
    Take the lowest medicine_effectiveness found for these species, and multiply that value by the Adopter's calculate score method.
    """
    # Your Code Here, should contain an __init__ and a get_score method.
    def __init__(self, name, desired_species, allergic_species, medicine_effectiveness):
        self.name = name
        self.desired_species = desired_species
        self.allergic_species = allergic_species
        self.medicine_effectiveness = medicine_effectiveness
    def get_score(self, adoption_center):
        allergic_species_presence = set.intersection(set(self.allergic_species),set(adoption_center.species_types.keys()))
        medicines = [ self.medicine_effectiveness.get(species, 0) for species in list(allergic_species_presence)]
        #score = min_medicine_effectiveness * Adopter.get_score(self, adoption_center)
        score = Adopter.get_score(self, adoption_center)
        return min(medicines) * score if len(medicines) > 0 else score


class SluggishAdopter(Adopter):
    """
    A SluggishAdopter really dislikes travelleng. The further away the
    AdoptionCenter is linearly, the less likely they will want to visit it.
    Since we are not sure the specific mood the SluggishAdopter will be in on a
    given day, we will asign their score with a random modifier depending on
    distance as a guess.
    Score should be
    If distance < 1 return 1 x number of desired species
    elif distance < 3 return random between (.7, .9) times number of desired species
    elif distance < 5. return random between (.5, .7 times number of desired species
    else return random between (.1, .5) times number of desired species
    """
    def __init__(self, name, desired_species, location):
        self.name = name
        self.desired_species = desired_species
        self.location = location

    def get_linear_distance(self, to_location):
        c1, c2 = to_location
        return math.sqrt( (c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)

    def get_score(self, adoption_center):
        self.distance = self.get_linear_distance((self.location, adoption_center.location))
        if self.distance < 1:
            return 1 * Adopter.get_score(self, adoption_center)
        elif 1 <= self.distance < 3:
            return rand.uniform(0.7,0.9) * Adopter.get_score(self, adoption_center)
        elif 3 <= self.distance < 5:
            return rand.uniform(0.5,0.7) * Adopter.get_score(self, adoption_center)
        elif self.distance >= 5:
            return rand.uniform(0.1,0.5) * Adopter.get_score(self, adoption_center)


def get_ordered_adoption_center_list(adopter, list_of_adoption_centers):
    """
    The method returns a list of an organized adoption_center such that the scores for each AdoptionCenter to the Adopter will be ordered from highest score to lowest score.
    """
    score_list = []
    for center in list_of_adoption_centers:
        score_list.append((adopter.get_score(center), center))

    score_list.sort(key=lambda x: x[0], reverse=True)

    return [ names[1] for names in score_list]

def get_adopters_for_advertisement(adoption_center, list_of_adopters, n):
    """
    The function returns a list of the top n scoring Adopters from list_of_adopters (in numerical order of score)
    """
    # score_list = []
    # new_list = []
    # for adopter in list_of_adopters:
    #     score_list.append((adopter.get_score(adoption_center), adopter))
    #     new_list.append((adopter.get_score(adoption_center), adopter.name))
    # score_list.sort(key=lambda x: (x[0],x[1].name[0]), reverse=True)
    # print new_list
    # names = [ names[1] for names in score_list]
    # new = ''
    # for name in names:
    #     new += name.name + ','
    # print new
    # return names if n > len(names) else names[:n]
    sorted_list = sorted(list_of_adopters, \
                  key=lambda x: (x.get_score(adoption_center), -string.ascii_uppercase.index(x.name[0]),-string.ascii_lowercase.index(x.name[1])), reverse=True )
    return sorted_list if n > len(sorted_list) else sorted_list[:n]


adopter = MedicatedAllergicAdopter("One", "Cat", ['Dog', 'Horse'], {"Dog": .5, "Horse": 0.2})
adopter2 = Adopter("Two", "Cat")
adopter3 = FlexibleAdopter("Three", "Horse", ["Lizard", "Cat"])
adopter4 = FearfulAdopter("Four","Cat","Dog")
adopter5 = SluggishAdopter("Five","Cat", (1,2))
adopter6 = AllergicAdopter("Six", "Cat", "Dog")

ac = AdoptionCenter("Place1", {"Mouse": 12, "Dog": 2}, (1,1))
ac2 = AdoptionCenter("Place2", {"Cat": 12, "Lizard": 2}, (3,5))
ac3 = AdoptionCenter("Place3", {"Horse": 25, "Dog": 9}, (-2,10))

# how to test get_adopters_for_advertisement
for names in get_adopters_for_advertisement(ac, [adopter, adopter2, adopter3, adopter4, adopter5, adopter6], 10):
    print names.name
# you can print the name and score of each item in the list returned





# adopter4 = FearfulAdopter("Four","Cat","Dog")
# adopter5 = SluggishAdopter("Five","Cat", (1,2))
# adopter6 = AllergicAdopter("Six", "Lizard", "Cat")
#
# ac = AdoptionCenter("Place1", {"Cat": 12, "Dog": 2}, (1,1))
# ac2 = AdoptionCenter("Place2", {"Cat": 12, "Lizard": 2}, (3,5))
# ac3 = AdoptionCenter("Place3", {"Cat": 40, "Dog": 4}, (-2,10))
# ac4 = AdoptionCenter("Place4", {"Cat": 33, "Horse": 5}, (-3,0))
# ac5 = AdoptionCenter("Place5", {"Cat": 45, "Lizard": 2}, (8,-2))
# ac6 = AdoptionCenter("Place6", {"Cat": 23, "Dog": 7, "Horse": 5}, (-10,10))
#
#
# # how to test get_ordered_adoption_center_list
# for name in get_ordered_adoption_center_list(adopter4, [ac,ac2,ac3,ac4,ac5,ac6]):
#     print name.name
