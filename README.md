# ALT – Análise de Legibilidade Textual

**alt-legibilidade** é um pacote Python gratuito e de código aberto que permite analisar a legibilidade de textos em **língua portuguesa**. Ele conta letras, palavras, sílabas e frases, e calcula índices como Flesch, Flesch-Kincaid, Gunning Fog, ARI, CLI e Gulpease.

📌 Página oficial do projeto: [https://legibilidade.com](https://legibilidade.com)

📄 Artigo de referência:  
Gleice Carvalho de Lima Moreno, Marco P. M. de Souza, Nelson Hein, Adriana Kroenke Hein,  
**ALT: um software para análise de legibilidade de textos em Língua Portuguesa**  
arXiv:2203.12135 [cs.CL] — [https://doi.org/10.48550/arXiv.2203.12135](https://doi.org/10.48550/arXiv.2203.12135)

---

## 💻 Requisitos: Instalando o Python (somente se ainda não tiver)

1. Acesse o site oficial:  
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Clique em **Download Python 3.x.x** (a versão mais recente aparecerá em destaque).

3. **Durante a instalação**, marque a opção ✅ **"Add Python to PATH"** antes de clicar em "Install Now".

4. Para testar se deu certo, abra o terminal (Prompt de Comando no Windows) e digite:

```bash
python --version
```

Você deverá ver algo como: `Python 3.12.3`

---

## 🚀 Instalando o alt-legibilidade

Com o Python instalado, abra o terminal e digite:

```bash
pip install alt-legibilidade
```

Esse comando instala o analisador de legibilidade na sua máquina.

---

## 📁 Como usar

```bash
# 1. Crie uma pasta chamada "textos" no mesmo local onde você está no terminal:
mkdir textos

# 2. Coloque dentro dela os arquivos que deseja analisar:
#    - Arquivos de texto (.txt)
#    - Arquivos do Word (.docx)
#    - Arquivos PDF (.pdf)

# 3. Rode o analisador com:
alt-legibilidade

# O programa exibirá uma tabela com os resultados diretamente no terminal.
# Ele também criará uma pasta "resultados" com três arquivos:

# 📄 resultados_origin.txt  → ideal para uso no OriginLab
# 📊 resultados.csv         → compatível com Excel, LibreOffice etc.
# 🔧 resultados.json        → útil para desenvolvedores e APIs
```

---

## 📈 Índices calculados

- Número total de **letras**, **sílabas**, **palavras**, **frases**
- Número de **palavras complexas** (pouco frequentes)
- Índices de legibilidade:
  - Flesch
  - Flesch-Kincaid
  - Gunning Fog
  - ARI (Automated Readability Index)
  - CLI (Coleman-Liau Index)
  - Gulpease
  - Resultado = (Flesch-Kincaid + Gunning Fog + ARI + CLI)/4

---

## 🛠 Suporte a arquivos

✅ `.txt`  
✅ `.pdf`  
✅ `.docx`  

Todos devem estar na pasta `textos/`.

---

## 🧑‍💻 Desenvolvedores

Este projeto é open-source e aceita contribuições. Acesse o repositório oficial:

👉 [https://github.com/marcopolomoreno/alt-python](https://github.com/marcopolomoreno/alt-python)

---

## 📜 Licença

Distribuído sob a licença MIT.