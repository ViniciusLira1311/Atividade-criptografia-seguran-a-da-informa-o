def _cesar(texto, chave):
    resultado = []
    for char in texto:
        if char.isupper():
            novo = chr((ord(char) - ord('A') + chave)%26 + ord('A'))
            resultado.append(novo)
        elif char.islower():
            novo = chr((ord(char) - ord('a') + chave)%26 + ord('a'))
            resultado.append(novo)
        else:
            resultado.append(char)
    return ''.join(resultado)

def criptografar(texto, chave):
    try:
        desloc = int(chave)
    except ValueError:
        raise ValueError("A chave para a cifra de cesar precisa ser um número inteiro.")
    return _cesar(texto, desloc)

def descriptografar(texto, chave):
    try:
        desloc = int(chave)
    except ValueError:
        raise ValueError("A chave para a cifra de cesar precisa ser um número inteiro.")
    return _cesar(texto, -desloc)