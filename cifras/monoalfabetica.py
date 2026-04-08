import random
import string

_mapeamento_cripto = None
_mapeamento_desc = None

def gerar_alfabeto_aleatorio():
    alfabeto = list(string.ascii_uppercase)
    cifrado = alfabeto[:]
    random.shuffle(cifrado)
    mapeamento = dict(zip(alfabeto, cifrado))
    inverso = {v: k for k, v in mapeamento.items()}
    return mapeamento, inverso

def inicializar_mapeamento():
    global _mapeamento_cripto, _mapeamento_desc
    _mapeamento_cripto, _mapeamento_desc = gerar_alfabeto_aleatorio()

def _substituir(texto, mapeamento):
    resultado = []
    for char in texto.upper():
        if char in mapeamento:
            resultado.append(mapeamento[char])
        else:
            resultado.append(char)  
    return ''.join(resultado)

def criptografar(texto, chave):
    global _mapeamento_cripto
    if _mapeamento_cripto is None:
        inicializar_mapeamento()
    return _substituir(texto, _mapeamento_cripto)

def descriptografar(texto, chave):
    global _mapeamento_desc
    if _mapeamento_desc is None:
        inicializar_mapeamento()
    return _substituir(texto, _mapeamento_desc)

def obter_alfabeto_atual():
    global _mapeamento_cripto
    if _mapeamento_cripto is None:
        inicializar_mapeamento()
    alfabeto_original = string.ascii_uppercase
    alfabeto_cifrado = ''.join(_mapeamento_cripto.get(c, '?') for c in alfabeto_original)
    return alfabeto_cifrado

def nova_chave_aleatoria():
    inicializar_mapeamento()