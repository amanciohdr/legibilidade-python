def is_letter(c):
    return c.lower() != c.upper()

def contar_letras(texto):
    letras = 0
    for caractere in texto:
        if is_letter(caractere):
            letras += 1
    return letras

# Exemplo de uso
texto = "Olá, mundo!"
total_letras = contar_letras(texto)
