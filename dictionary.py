from enum import Enum


class Color(Enum):
    WHITE       = (255, 255, 255)
    BACKGROUND  = (255, 240, 220)
    ORANGE      = (255,  80,   0)
    PINK        = (247, 143, 167)
    RED         = (200,   0,   0)
    BROWN       = (150,  75,   1)
    GREY        = (130, 130, 130)
    VIOLET      = (112,  25, 194)
    GREEN       = (  0, 200,   0)
    BLUE        = (  0,   0, 200)
    BLACK       = (  1,   1,   1)


class Good(Enum):
    EMPTY = "Empty"

    BeefHeart   = "Beef hearts"
    BBeefHeart  = "Boiled beef hearts"
    CBeefHeart = "Chopped beef hearts"
    
    Pickles = "Pickles"
    CPickles = "Chopped Pickles"

    Eggs = "Eggs"
    BEggs = "Boiled Eggs"
    CEggs = "Chopped Eggs"

    O = "Onion"
    PO = "Peeled Onion"
    CO = "Chopped Onion"

    Potato = "Potato"
    PPotato = "Peeled Potato"
    BPotato = "Boiled Potato"
    CPotatp = "Chopped Potato" #Boiled

    Carrot = "Carrot"
    PCarrot = "Peeled Carrot"
    CCarrot = "Chopped Carrot"
    BCarrot = "Boiled Carrot"
    CBCarrot = "Chopped Boiled Carrot"

    Pease = "Pease"
    Seasonings = "Seasonings"
    Mayo = "Mayounnaise"