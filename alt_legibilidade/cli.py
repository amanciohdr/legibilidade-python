# alt_legibilidade/cli.py

"""
Script principal do pacote alt_legibilidade.
Executa a análise de legibilidade em todos os arquivos .txt, .pdf e .docx da pasta 'textos'.
Gera arquivos de saída em: resultados/resultados_origin.txt, resultados.csv e resultados.json.
"""

import os
import csv
import json
from alt_legibilidade.letras import contar_letras
from alt_legibilidade.palavras import contar_palavras
from alt_legibilidade.silabas import contar_silabas
from alt_legibilidade.frases import contar_frases
from alt_legibilidade.palavrasComplexas import carregar_banco_palavras, contar_palavras_complexas
from alt_legibilidade.extrair_texto import extrair_texto_arquivo

def main():
    banco = carregar_banco_palavras()
    PASTA_TEXTOS = "textos"

    if not os.path.exists(PASTA_TEXTOS):
        print(f"❌ A pasta '{PASTA_TEXTOS}' não foi encontrada. Crie essa pasta e adicione os arquivos .txt, .pdf ou .docx que deseja analisar.")
        return

    print(f"{'arquivo':30} {'Letras':>7} {'Sílabas':>8} {'Palavras':>9} {'Sentencas':>10} {'Complexas':>11}"
          f"{'Flesch':>7} {'Flesch-Kincaid':>14} {'Gunning Fog':>12} {'ARI':>4} {'CLI':>4} {'Gulpease':>9} {'Resultado':>10}")

    resultados = []

    for nome_arquivo in os.listdir(PASTA_TEXTOS):
        if nome_arquivo.startswith("~$") or nome_arquivo.startswith("."):
            continue

        caminho = os.path.join(PASTA_TEXTOS, nome_arquivo)
        try:
            texto = extrair_texto_arquivo(caminho)
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")
            continue

        letras = contar_letras(texto)
        silabas = contar_silabas(texto)
        palavras = contar_palavras(texto)
        complexas = contar_palavras_complexas(texto, banco)
        sentencas = contar_frases(texto)

        flesch = 226 - 1.04 * palavras / sentencas - 72 * silabas / palavras
        fleschKincaid = 0.36 * palavras / sentencas + 10.4 * silabas / palavras - 18
        gunningFog = 0.49 * palavras / sentencas + 19 * complexas / palavras
        ari = 4.6 * letras / palavras + 0.44 * palavras / sentencas - 20
        cli = 5.4 * letras / palavras - 21 * sentencas / palavras - 14
        gulpease = 89 + (300 * sentencas - 10 * letras) / palavras

        resultado = (fleschKincaid + gunningFog + ari + cli) / 4

        linha = {
            "arquivo": nome_arquivo,
            "letras": letras,
            "silabas": silabas,
            "palavras": palavras,
            "sentencas": sentencas,
            "complexas": complexas,
            "flesch": round(flesch, 1),
            "fleschKincaid": round(fleschKincaid, 1),
            "gunningFog": round(gunningFog, 1),
            "ari": round(ari, 1),
            "cli": round(cli, 1),
            "gulpease": round(gulpease, 1),
            "media": round((fleschKincaid + gunningFog + ari + cli) / 4, 1),
        }
        resultados.append(linha)

        print(f"{nome_arquivo:30} {letras:7} {silabas:8} {palavras:9} {sentencas:10} {complexas:11}"
              f" {flesch:6.1f} {fleschKincaid:14.1f} {gunningFog:12.1f} {ari:4.1f} {cli:4.1f} {gulpease:9.1f} {resultado:10.0f}")

    if not resultados:
        print("⚠️ Nenhum arquivo de texto válido foi encontrado na pasta 'textos/'.")
        return

    os.makedirs("resultados", exist_ok=True)

    with open("resultados/resultados_origin.txt", "w", encoding="utf-8") as f:
        f.write("\t".join(resultados[0].keys()) + "\n")
        for linha in resultados:
            f.write("\t".join(str(v) for v in linha.values()) + "\n")

    with open("resultados/resultados.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    with open("resultados/resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    verde = '\033[92m'
    azul = '\033[94m'
    reset = '\033[0m'

    print(f"\n{azul}{'=' * 50}")
    print("  Dados de legibilidade salvos com sucesso!")
    print(f"{'=' * 50}{reset}")

    print(f"{verde}📁 Pasta: resultados/{reset}")
    print(f" - resultados_origin.txt  → para uso no OriginLab")
    print(f" - resultados.csv         → para Excel, LibreOffice etc.")
    print(f" - resultados.json        → para uso em scripts e APIs\n")
