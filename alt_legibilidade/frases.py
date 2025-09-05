def contar_frases(
    texto: str,
    considerar_ponto_e_virgula: bool = True,
    considerar_dois_pontos: bool = True
) -> int:
    sentencas = 0
    forma_sentencas = "padrao"  # pode ser 'padrao', ';', ':', ':&&;'

    for k in range(len(texto)):
        caractere = texto[k]
        anterior1 = texto[k - 1] if k > 0 else ""

        # Condição base (nenhuma checkbox marcada)
        if not considerar_ponto_e_virgula and not considerar_dois_pontos:
            if caractere in [".", "!", "?"] or k == len(texto) - 1:
                sentencas += 1
                forma_sentencas = "padrao"

        # Somente ponto e vírgula
        elif considerar_ponto_e_virgula and not considerar_dois_pontos:
            if caractere in [".", "!", "?", ";"] or k == len(texto) - 1 or \
               (caractere == "\n" and anterior1 == ";"):
                sentencas += 1
                forma_sentencas = ";"

        # Somente dois pontos
        elif not considerar_ponto_e_virgula and considerar_dois_pontos:
            if caractere in [".", "!", "?", ":"] or k == len(texto) - 1 or \
               (caractere == "\n" and anterior1 == ":"):
                sentencas += 1
                forma_sentencas = ":"

        # Ambos marcados
        elif considerar_ponto_e_virgula and considerar_dois_pontos:
            if caractere in [".", "!", "?", ":", ";"] or k == len(texto) - 1 or \
               (caractere == "\n" and anterior1 in [":", ";"]):
                sentencas += 1
                forma_sentencas = ":&&;"

        # Corrigir contagem em caso de "..."
        if caractere == "." and anterior1 == ".":
            sentencas -= 1

    return max(sentencas, 1)  # garantir pelo menos 1 sentença, como fallback
