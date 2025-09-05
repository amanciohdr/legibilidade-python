#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALT - Análise de Legibilidade Textual (Versão Web Expandida)
Interface web moderna usando Streamlit com análise de planilhas
"""

import streamlit as st
import pandas as pd
import io
import zipfile
from datetime import datetime
import tempfile
import os

# Importações do seu código original
try:
    from alt_legibilidade.letras import contar_letras
    from alt_legibilidade.palavras import contar_palavras
    from alt_legibilidade.silabas import contar_silabas
    from alt_legibilidade.frases import contar_frases
    from alt_legibilidade.palavrasComplexas import carregar_banco_palavras, contar_palavras_complexas
    from extrair_texto import extrair_texto_arquivo
    ALT_DISPONIVEL = True
except ImportError as e:
    ALT_DISPONIVEL = False
    ERRO_IMPORT = str(e)


def configurar_pagina():
    """Configura a página do Streamlit"""
    st.set_page_config(
        page_title="ALT - Análise de Legibilidade",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        margin: 1rem 0;
    }
    .tab-content {
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def verificar_dependencias():
    """Verifica se as dependências estão disponíveis"""
    if not ALT_DISPONIVEL:
        st.error(f"""
        🚨 **Módulo 'alt_legibilidade' não encontrado**
        
        **Erro:** {ERRO_IMPORT}
        
        **Para usar esta aplicação, você precisa:**
        1. Instalar: `pip install alt-legibilidade`
        2. Ou colocar os arquivos do projeto ALT na mesma pasta
        
        **Estrutura necessária:**
        ```
        projeto/
        ├── app_alt.py              # Este arquivo
        ├── extrair_texto.py        # Seu arquivo
        └── alt_legibilidade/       # Sua pasta
            ├── letras.py
            ├── palavras.py  
            ├── silabas.py
            ├── frases.py
            └── palavrasComplexas.py
        ```
        """)
        st.stop()


def carregar_banco():
    """Carrega o banco de palavras uma vez"""
    if 'banco_palavras' not in st.session_state:
        try:
            with st.spinner("Carregando banco de palavras..."):
                st.session_state.banco_palavras = carregar_banco_palavras()
        except Exception as e:
            st.warning(f"Erro ao carregar banco de palavras: {e}")
            st.session_state.banco_palavras = set()
    
    return st.session_state.banco_palavras


def analisar_texto_simples(texto, banco_palavras):
    """
    Analisa um texto simples (string) usando suas funções originais
    """
    try:
        if not texto or not texto.strip():
            return None
        
        # Análise usando SUAS funções
        letras = contar_letras(texto)
        silabas = contar_silabas(texto)
        palavras = contar_palavras(texto)
        complexas = contar_palavras_complexas(texto, banco_palavras)
        sentencas = contar_frases(texto)
        
        # Evitar divisão por zero
        if palavras == 0 or sentencas == 0:
            return None
        
        # Cálculos dos índices (SUAS fórmulas exatas)
        flesch = 226 - 1.04 * palavras / sentencas - 72 * silabas / palavras
        fleschKincaid = 0.36 * palavras / sentencas + 10.4 * silabas / palavras - 18
        gunningFog = 0.49 * palavras / sentencas + 19 * complexas / palavras
        ari = 4.6 * letras / palavras + 0.44 * palavras / sentencas - 20
        cli = 5.4 * letras / palavras - 21 * sentencas / palavras - 14
        gulpease = 89 + (300 * sentencas - 10 * letras) / palavras
        resultado = (fleschKincaid + gunningFog + ari + cli) / 4
        
        # Resultado formatado
        resultado_analise = {
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
            "resultado": round(resultado, 0),
        }
        
        return resultado_analise
        
    except Exception as e:
        return None


def analisar_texto_arquivo(arquivo_bytes, nome_arquivo, banco_palavras):
    """
    Analisa um único arquivo usando suas funções originais
    """
    try:
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(nome_arquivo)[1]) as tmp:
            tmp.write(arquivo_bytes)
            tmp_path = tmp.name
        
        # Extrair texto usando SUA função
        texto = extrair_texto_arquivo(tmp_path)
        
        # Limpar arquivo temporário
        os.unlink(tmp_path)
        
        if not texto.strip():
            return None, "Texto vazio"
        
        resultado = analisar_texto_simples(texto, banco_palavras)
        if resultado:
            resultado["arquivo"] = nome_arquivo
            return resultado, "Sucesso"
        else:
            return None, "Texto muito curto"
        
    except Exception as e:
        return None, f"Erro: {str(e)[:50]}"


def carregar_planilha(uploaded_file):
    """Carrega planilha Excel ou CSV"""
    try:
        nome_arquivo = uploaded_file.name.lower()
        
        if nome_arquivo.endswith('.csv'):
            # Tentar diferentes encodings para CSV
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)  # Reset file pointer
                try:
                    df = pd.read_csv(uploaded_file, encoding='latin1')
                except:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='cp1252')
        
        elif nome_arquivo.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        
        else:
            return None, "Formato não suportado"
        
        return df, "Sucesso"
    
    except Exception as e:
        return None, f"Erro ao carregar: {str(e)[:50]}"


def analisar_coluna_planilha(df, coluna_selecionada, banco_palavras):
    """Analisa uma coluna específica da planilha"""
    resultados = []
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_linhas = len(df)
    
    for idx, row in df.iterrows():
        # Atualizar status
        status_text.text(f"Analisando linha {idx + 1} de {total_linhas}")
        
        # Obter texto da célula
        texto = str(row[coluna_selecionada]) if pd.notna(row[coluna_selecionada]) else ""
        
        if texto and texto.strip() and texto != 'nan':
            # Analisar texto
            resultado = analisar_texto_simples(texto, banco_palavras)
            
            if resultado:
                # Adicionar informações da linha
                resultado_linha = {
                    "linha": idx + 1,
                    "texto_original": texto[:100] + "..." if len(texto) > 100 else texto,
                    **resultado
                }
                resultados.append(resultado_linha)
        
        # Atualizar progress
        progress_bar.progress((idx + 1) / total_linhas)
    
    # Limpar status
    status_text.empty()
    progress_bar.empty()
    
    return resultados


def criar_metricas_resumo(resultados):
    """Cria métricas de resumo dos resultados"""
    if not resultados:
        return
    
    df = pd.DataFrame(resultados)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(resultados)}</div>
            <div class="metric-label">Textos Analisados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_flesch = df['flesch'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{avg_flesch:.1f}</div>
            <div class="metric-label">Flesch Médio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_palavras = df['palavras'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{total_palavras:,}</div>
            <div class="metric-label">Total Palavras</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_resultado = df['resultado'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{avg_resultado:.0f}</div>
            <div class="metric-label">Resultado Médio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        complexidade = "Fácil" if avg_flesch > 70 else "Médio" if avg_flesch > 50 else "Difícil"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{complexidade}</div>
            <div class="metric-label">Complexidade</div>
        </div>
        """, unsafe_allow_html=True)


def gerar_arquivo_excel(resultados, tipo="arquivo"):
    """Gera arquivo Excel dos resultados"""
    df = pd.DataFrame(resultados)
    
    if tipo == "planilha":
        # Colunas para análise de planilha
        colunas_ordenadas = [
            "linha", "texto_original", "letras", "silabas", "palavras", "sentencas", "complexas",
            "flesch", "fleschKincaid", "gunningFog", "ari", "cli", "gulpease", "resultado"
        ]
    else:
        # Colunas para análise de arquivos
        colunas_ordenadas = [
            "arquivo", "letras", "silabas", "palavras", "sentencas", "complexas",
            "flesch", "fleschKincaid", "gunningFog", "ari", "cli", "gulpease", "resultado"
        ]
    
    df = df[colunas_ordenadas]
    
    # Gerar Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Legibilidade')
    
    return output.getvalue()


def aba_arquivos():
    """Aba para análise de arquivos individuais"""
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload de Documentos</h3>
        <p>Selecione um ou múltiplos arquivos para análise</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Escolha os arquivos",
        type=['txt', 'pdf', 'docx'],
        accept_multiple_files=True,
        help="Selecione arquivos .txt, .pdf ou .docx para análise",
        key="arquivos_upload"
    )
    
    if uploaded_files:
        st.success(f"📁 {len(uploaded_files)} arquivo(s) selecionado(s)")
        
        # Botão de análise
        if st.button("🔍 Analisar Documentos", type="primary", use_container_width=True, key="analisar_arquivos"):
            banco_palavras = carregar_banco()
            
            # Inicializar resultados
            resultados = []
            erros = []
            
            # Barra de progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Processar cada arquivo
            for i, uploaded_file in enumerate(uploaded_files):
                nome_arquivo = uploaded_file.name
                status_text.text(f"Processando: {nome_arquivo}")
                
                # Ler bytes do arquivo
                arquivo_bytes = uploaded_file.read()
                
                # Analisar arquivo
                resultado, status = analisar_texto_arquivo(arquivo_bytes, nome_arquivo, banco_palavras)
                
                if resultado:
                    resultados.append(resultado)
                else:
                    erros.append(f"❌ {nome_arquivo}: {status}")
                
                # Atualizar progresso
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Limpar status
            status_text.empty()
            progress_bar.empty()
            
            # Exibir resultados
            exibir_resultados_arquivos(resultados, erros)


def aba_planilhas():
    """Aba para análise de planilhas"""
    st.markdown("""
    <div class="upload-section">
        <h3>📊 Upload de Planilha</h3>
        <p>Selecione uma planilha Excel (.xlsx, .xls) ou CSV para análise por coluna</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Escolha a planilha",
        type=['xlsx', 'xls', 'csv'],
        help="Selecione um arquivo Excel ou CSV",
        key="planilha_upload"
    )
    
    if uploaded_file:
        st.success(f"📊 Planilha carregada: {uploaded_file.name}")
        
        # Carregar planilha
        with st.spinner("Carregando planilha..."):
            df, status = carregar_planilha(uploaded_file)
        
        if df is not None:
            st.success(f"✅ Planilha carregada: {len(df)} linhas, {len(df.columns)} colunas")
            
            # Mostrar preview
            with st.expander("👀 Visualizar dados", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
            
            # Seleção de coluna
            st.markdown("### 📋 Selecione a coluna para análise:")
            
            # Filtrar apenas colunas de texto
            colunas_texto = []
            for col in df.columns:
                # Verificar se a coluna contém principalmente texto
                amostra = df[col].dropna().head(10)
                if len(amostra) > 0:
                    texto_count = sum(1 for x in amostra if isinstance(x, str) and len(str(x).strip()) > 10)
                    if texto_count >= len(amostra) * 0.5:  # Pelo menos 50% são textos
                        colunas_texto.append(col)
            
            if not colunas_texto:
                colunas_texto = list(df.columns)
                st.warning("⚠️ Nenhuma coluna de texto detectada automaticamente. Mostrando todas as colunas.")
            
            coluna_selecionada = st.selectbox(
                "Coluna para análise:",
                options=colunas_texto,
                help="Selecione a coluna que contém os textos a serem analisados"
            )
            
            if coluna_selecionada:
                # Estatísticas da coluna
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_linhas = len(df)
                    st.metric("Total de linhas", total_linhas)
                
                with col2:
                    textos_validos = df[coluna_selecionada].notna().sum()
                    st.metric("Textos válidos", textos_validos)
                
                with col3:
                    texto_medio = df[coluna_selecionada].dropna().apply(lambda x: len(str(x))).mean()
                    st.metric("Tamanho médio", f"{texto_medio:.0f} chars")
                
                # Botão de análise
                if st.button("🔍 Analisar Coluna", type="primary", use_container_width=True, key="analisar_planilha"):
                    banco_palavras = carregar_banco()
                    
                    with st.spinner("Analisando textos da planilha..."):
                        resultados = analisar_coluna_planilha(df, coluna_selecionada, banco_palavras)
                    
                    # Exibir resultados
                    exibir_resultados_planilha(resultados, coluna_selecionada)
        
        else:
            st.error(f"❌ Erro ao carregar planilha: {status}")


def exibir_resultados_arquivos(resultados, erros):
    """Exibe resultados da análise de arquivos"""
    # Exibir erros se houver
    if erros:
        with st.expander("⚠️ Arquivos com erro", expanded=False):
            for erro in erros:
                st.error(erro)
    
    # Exibir resultados se houver
    if resultados:
        st.success(f"✅ {len(resultados)} arquivo(s) processado(s) com sucesso!")
        
        # Métricas de resumo
        st.markdown("## 📈 Resumo da Análise")
        criar_metricas_resumo(resultados)
        
        # Tabela de resultados
        st.markdown("## 📋 Resultados Detalhados")
        df_resultados = pd.DataFrame(resultados)
        
        # Reordenar e formatar colunas
        colunas_exibir = {
            "arquivo": "Arquivo",
            "letras": "Letras",
            "silabas": "Sílabas", 
            "palavras": "Palavras",
            "sentencas": "Sentenças",
            "complexas": "Complexas",
            "flesch": "Flesch",
            "fleschKincaid": "F-Kincaid",
            "gunningFog": "G-Fog",
            "ari": "ARI",
            "cli": "CLI", 
            "gulpease": "Gulpease",
            "resultado": "Resultado"
        }
        
        df_display = df_resultados.rename(columns=colunas_exibir)
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Botões de download
        download_resultados(resultados, "arquivo")
    
    else:
        st.error("❌ Nenhum arquivo foi processado com sucesso.")


def exibir_resultados_planilha(resultados, coluna_nome):
    """Exibe resultados da análise de planilha"""
    if resultados:
        st.success(f"✅ {len(resultados)} texto(s) analisado(s) da coluna '{coluna_nome}'!")
        
        # Métricas de resumo
        st.markdown("## 📈 Resumo da Análise")
        criar_metricas_resumo(resultados)
        
        # Tabela de resultados
        st.markdown("## 📋 Resultados Detalhados")
        df_resultados = pd.DataFrame(resultados)
        
        # Reordenar e formatar colunas
        colunas_exibir = {
            "linha": "Linha",
            "texto_original": "Texto (Preview)",
            "letras": "Letras",
            "silabas": "Sílabas", 
            "palavras": "Palavras",
            "sentencas": "Sentenças",
            "complexas": "Complexas",
            "flesch": "Flesch",
            "fleschKincaid": "F-Kincaid",
            "gunningFog": "G-Fog",
            "ari": "ARI",
            "cli": "CLI", 
            "gulpease": "Gulpease",
            "resultado": "Resultado"
        }
        
        df_display = df_resultados.rename(columns=colunas_exibir)
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Botões de download
        download_resultados(resultados, "planilha")
    
    else:
        st.error("❌ Nenhum texto válido foi encontrado na coluna selecionada.")


def download_resultados(resultados, tipo):
    """Seção de download dos resultados"""
    st.markdown("## 💾 Exportar Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Excel
        excel_data = gerar_arquivo_excel(resultados, tipo)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        st.download_button(
            label="📊 Baixar Excel",
            data=excel_data,
            file_name=f"ALT_{tipo}_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # CSV
        df = pd.DataFrame(resultados)
        csv_data = df.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label="📄 Baixar CSV",
            data=csv_data,
            file_name=f"ALT_{tipo}_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        # JSON
        import json
        json_data = json.dumps(resultados, ensure_ascii=False, indent=2)
        st.download_button(
            label="🔧 Baixar JSON",
            data=json_data,
            file_name=f"ALT_{tipo}_{timestamp}.json",
            mime="application/json",
            use_container_width=True
        )


def main():
    """Função principal da aplicação"""
    configurar_pagina()
    verificar_dependencias()
    
    # Header
    st.markdown("""
    # 📊 ALT - Análise de Legibilidade Textual
    ### Ferramenta web para análise de legibilidade de textos e planilhas em português
    
    ---
    """)
    
    # Sidebar com informações
    with st.sidebar:
        st.markdown("""
        ## 📋 Sobre o ALT
        
        **Análise de Legibilidade Textual** é uma ferramenta que calcula índices de legibilidade para textos em português.
        
        ### 📄 Modos de Análise:
        - **Arquivos** - TXT, PDF, DOCX
        - **Planilhas** - Excel (.xlsx, .xls) e CSV
        
        ### 📈 Índices Calculados:
        - **Flesch** - Facilidade de leitura
        - **Flesch-Kincaid** - Nível escolar
        - **Gunning Fog** - Complexidade
        - **ARI** - Legibilidade automatizada
        - **CLI** - Coleman-Liau
        - **Gulpease** - Índice italiano adaptado
        
        ---
        
        ### 🔗 Links Úteis:
        - [Site Oficial](https://legibilidade.com)
        - [Artigo Científico](https://doi.org/10.48550/arXiv.2203.12135)
        - [GitHub](https://github.com/marcopolomoreno/alt-python)
        """)
    
    # Abas principais
    tab1, tab2 = st.tabs(["📁 Análise de Arquivos", "📊 Análise de Planilhas"])
    
    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        aba_arquivos()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        aba_planilhas()
        st.markdown('</div>', unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()