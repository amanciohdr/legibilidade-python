def contar_palavras(texto):
    palavras = 0
    for k in range(len(texto)):
        caractere = texto[k]
        anterior1 = texto[k - 1] if k > 0 else ''
        
        if (
            (caractere == " " or caractere == "\n" or k == len(texto) - 1)
            and anterior1 not in [" ", "\n", "-"]
        ):
            palavras += 1
    return palavras
