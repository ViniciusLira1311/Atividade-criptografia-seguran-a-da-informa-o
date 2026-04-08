import random
import string
def gerar():
    alfabeto = list(string.ascii_uppercase)
    random.shuffle(alfabeto)
    return ''.join(alfabeto)
def _monoalfabetica(texto):
    pass
