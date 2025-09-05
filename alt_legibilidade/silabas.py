def contar_silabas(texto: str) -> int:
    """
    Conta o número total de sílabas em um texto em português.
    
    Args:
        texto (str): Texto para análise
        
    Returns:
        int: Número total de sílabas no texto
    """
    if not texto or not texto.strip():
        return 0
    
    # Definir conjuntos para lookup O(1) - mais eficiente que listas
    vogais = {
        'a', 'ã', 'â', 'á', 'à', 
        'e', 'é', 'ê', 'è',
        'i', 'í', 'ì', 'î',
        'o', 'õ', 'ô', 'ó', 'ò',
        'u', 'ú', 'ù', 'û', 'ü'
    }
    
    ditongos = {
        'ai', 'au', 'ei', 'eu', 'éu', 'iu', 'oi', 'ói', 'ou', 'ui',
        'ia', 'ie', 'io', 'ua', 'ue', 'uo', 'ũi',
        'ãe', 'ão', 'õe'
    }
    
    tritongos = {
        'uai', 'uei', 'uão', 'uõe', 'uiu', 'uou'
    }
    
    # Hiatos comuns - vogais que devem ser pronunciadas separadamente
    hiatos = {
        'aí', 'aú', 'eí', 'eú', 'oí', 'uí',  # í/ú tônicos
        'aa', 'ee', 'ii', 'oo', 'uu'         # vogais repetidas
    }
    
    silabas_total = 0
    texto_lower = texto.lower()
    i = 0
    
    while i < len(texto_lower):
        char = texto_lower[i]
        
        # Se encontrou uma vogal
        if char in vogais:
            silabas_grupo = 1  # Por padrão, 1 vogal = 1 sílaba
            
            # Verificar tritongos (3 vogais)
            if i + 2 < len(texto_lower):
                tritongo = texto_lower[i:i+3]
                if tritongo in tritongos:
                    silabas_grupo = 1
                    i += 3
                    silabas_total += silabas_grupo
                    continue
            
            # Verificar ditongos e hiatos (2 vogais)
            if i + 1 < len(texto_lower):
                ditongo = texto_lower[i:i+2]
                
                # Se é hiato conhecido, contar como 2 sílabas
                if ditongo in hiatos:
                    silabas_grupo = 2
                    i += 2
                # Se é ditongo, contar como 1 sílaba
                elif ditongo in ditongos:
                    silabas_grupo = 1
                    i += 2
                # Se são duas vogais mas não é ditongo nem hiato catalogado
                elif texto_lower[i+1] in vogais:
                    # Aplicar regra: í/ú tônicos formam hiato
                    if ditongo[1] in ['í', 'ú'] or ditongo[0] in ['í', 'ú']:
                        silabas_grupo = 2  # Hiato
                        i += 2
                    else:
                        # Assumir ditongo se não detectado como hiato
                        silabas_grupo = 1
                        i += 2
                else:
                    # Vogal isolada
                    silabas_grupo = 1
                    i += 1
            else:
                # Vogal isolada no final
                silabas_grupo = 1
                i += 1
            
            silabas_total += silabas_grupo
        else:
            # Não é vogal, continuar
            i += 1
    
    # Garantir pelo menos 1 sílaba se houver texto válido
    return max(silabas_total, 1) if silabas_total > 0 or any(c.isalpha() for c in texto) else 0


# ============== VERSÃO ALTERNATIVA MAIS PRÓXIMA DA ORIGINAL ==============

def contar_silabas_original_melhorada(texto: str) -> int:
    """
    Versão melhorada mantendo a lógica similar à original:
    1. Contar vogais
    2. Corrigir ditongos  
    3. Corrigir tritongos
    4. Tratar hiatos
    """
    if not texto or not texto.strip():
        return 0
    
    silabas = 0
    texto_lower = texto.lower()
    
    # Usar sets para performance
    vogais = {'a', 'ã', 'â', 'á', 'à', 'e', 'é', 'ê', 'è', 'i', 'í', 'ì', 'î', 'o', 'õ', 'ô', 'ó', 'ò', 'u', 'ú', 'ù', 'û', 'ü'}
    ditongos = {'ai', 'au', 'ei', 'eu', 'éu', 'iu', 'oi', 'ói', 'ou', 'ui', 'ia', 'ie', 'io', 'ua', 'ue', 'uo', 'ãe', 'ão', 'õe'}
    tritongos = {'uai', 'uei', 'uão', 'uõe', 'uiu', 'uou'}
    hiatos = {'aí', 'aú', 'eí', 'eú', 'oí', 'uí', 'aa', 'ee', 'ii', 'oo', 'uu'}
    
    # Passo 1: Contar todas as vogais
    for char in texto_lower:
        if char in vogais:
            silabas += 1
    
    # Passo 2: Corrigir ditongos (duas vogais = uma sílaba)
    i = 0
    while i < len(texto_lower) - 1:
        par = texto_lower[i:i+2]
        if par in ditongos and par not in hiatos:
            silabas -= 1  # Remove uma sílaba (duas vogais viram uma)
        i += 1
    
    # Passo 3: Corrigir tritongos (três vogais = uma sílaba total)
    i = 0
    while i < len(texto_lower) - 2:
        trio = texto_lower[i:i+3]
        if trio in tritongos:
            silabas -= 1  # Remove mais uma sílaba (já foi corrigido como ditongo)
        i += 1
    
    # Passo 4: Adicionar sílabas para hiatos conhecidos
    i = 0
    while i < len(texto_lower) - 1:
        par = texto_lower[i:i+2]
        if par in hiatos:
            silabas += 1  # Hiato = duas sílabas em vez de uma
        i += 1
    
    # Garantir mínimo de 1 sílaba se houver letras
    return max(silabas, 1) if any(c.isalpha() for c in texto) else 0


# ============== VERSÃO MAIS SIMPLES E ROBUSTA ==============

def contar_silabas_simples(texto: str) -> int:
    """
    Versão simplificada focada em precisão para português brasileiro.
    Mantém interface original mas com melhor tratamento de casos especiais.
    """
    if not texto or not texto.strip():
        return 0
    
    import re
    
    # Extrair apenas palavras (ignorar números, pontuação)
    palavras = re.findall(r'[a-záàâãéêíóôõúçü]+', texto, re.IGNORECASE)
    
    if not palavras:
        return 0
    
    silabas_total = 0
    
    # Definições otimizadas
    vogais = set('aáàâãeéèêiíìîoóòôõuúùûü')
    ditongos = {
        'ai', 'au', 'ei', 'eu', 'éu', 'iu', 'oi', 'ói', 'ou', 'ui',
        'ia', 'ie', 'io', 'ua', 'ue', 'uo', 'ãe', 'ão', 'õe'
    }
    tritongos = {'uai', 'uei', 'uão', 'uõe', 'uiu', 'uou'}
    
    for palavra in palavras:
        palavra = palavra.lower()
        silabas_palavra = 0
        
        # Contar vogais
        for char in palavra:
            if char in vogais:
                silabas_palavra += 1
        
        # Corrigir ditongos
        for i in range(len(palavra) - 1):
            if palavra[i:i+2] in ditongos:
                # Verificar se não é hiato (í/ú tônicos)
                if not (palavra[i+1] in 'íú' or palavra[i] in 'íú'):
                    silabas_palavra -= 1
        
        # Corrigir tritongos
        for i in range(len(palavra) - 2):
            if palavra[i:i+3] in tritongos:
                silabas_palavra -= 1
        
        silabas_total += max(silabas_palavra, 1)
    
    return silabas_total