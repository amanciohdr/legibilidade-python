import fitz  # pymupdf

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    try:
        doc = fitz.open(caminho_pdf)
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
    except Exception as e:
        print(f"Erro ao processar {caminho_pdf}: {e}")
    return texto.strip()
