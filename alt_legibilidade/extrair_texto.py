import fitz  # PyMuPDF
from docx import Document

def extrair_texto_txt(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def extrair_texto_pdf(caminho):
    texto = ""
    try:
        doc = fitz.open(caminho)
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
    except Exception as e:
        print(f"Erro ao ler PDF {caminho}: {e}")
    return texto.strip()

def extrair_texto_docx(caminho):
    texto = ""
    try:
        doc = Document(caminho)
        for par in doc.paragraphs:
            texto += par.text + "\n"
    except Exception as e:
        print(f"Erro ao ler DOCX {caminho}: {e}")
    return texto.strip()

def extrair_texto_arquivo(caminho):
    if caminho.endswith(".txt"):
        return extrair_texto_txt(caminho)
    elif caminho.endswith(".pdf"):
        return extrair_texto_pdf(caminho)
    elif caminho.endswith(".docx"):
        return extrair_texto_docx(caminho)
    else:
        print(f"Tipo de arquivo não suportado: {caminho}")
        return ""
