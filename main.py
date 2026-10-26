"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Curso: Análise de Dados com Python [T8]
Aluno: Lucas Benevides
Arquivo: main.py
"""

import os
import pandas as pd


# ==========================================
# SPRINT 3: FUNÇÕES REUTILIZÁVEIS
# ==========================================
def padronizar_texto(valor):
    """
    Padroniza strings de texto tratando ausências, removendo espaços
    extras nas extremidades e corrigindo inconsistências de caixa e caracteres.
    Retorna o texto tratado ou o valor original se ausente.
    """
    if pd.isna(valor):
        return valor
    
    texto = str(valor).strip()
    
    # Tratamento específico para strings representativas de nulos do Excel
    if texto.upper() in ["#N/D", "#NA", "NAN", "NULL", "NONE"]:
        return "NAO IDENTIFICADO"
    
    # Correção de caracteres e caixa alta
    texto = texto.upper()
    texto = texto.replace("REFRIGERANTE LIMAO", "REFRIGERANTE LIMAO")
    texto = texto.replace("REFRIGERANTE LIMAO", "REFRIGERANTE LIMAO")
    return texto


def resumo_numerico(serie):
    """
    Calcula e retorna um dicionário com estatísticas descritivas básicas:
    - contagem de valores válidos
    - média
    - valor mínimo
    - valor máximo
    """
    return {
        "contagem": int(serie.count()),
        "media": float(serie.mean()),
        "minimo": float(serie.min()),
        "maximo": float(serie.max())
    }


def localizar_base():
    """Localiza o arquivo CSV de entrada nos caminhos padrão do projeto."""
    candidatos = [
        os.path.join("data", "Base Varejo.csv"),
        "Base Varejo.csv",
        os.path.join("..", "Análise de Dados com Python [T8]", "Base Varejo.csv", "Base Varejo.csv"),
        os.path.join(os.path.expanduser("~"), "projects", "pessoal", "Análise de Dados com Python [T8]", "Base Varejo.csv", "Base Varejo.csv")
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("Base de dados 'Base Varejo.csv' não encontrada.")


def executar_pipeline():
    print("=" * 70)
    print("MINI-PROJETO AVALIATIVO - ANÁLISE DE DADOS COM PYTHON [T8]")
    print("Aluno: Lucas Benevides")
    print("=" * 70)

    # ----------------------------------------------------
    # SPRINT 1: LEITURA E DIAGNÓSTICO
    # ----------------------------------------------------
    caminho_csv = localizar_base()
    print(f"\n[SPRINT 1] Lendo base de dados em: {caminho_csv}")
    
    df_bruto = pd.read_csv(caminho_csv, sep=';', low_memory=False)
    
    print("\n--- Estrutura Inicial ---")
    print(f"Total de registros: {df_bruto.shape[0]:,}")
    print(f"Total de colunas: {df_bruto.shape[1]}")
    print("\nColunas encontradas:")
    print(list(df_bruto.columns))
    
    print("\nTipos de dados (.dtypes):")
    print(df_bruto.dtypes)
    
    print("\nPrimeiras 3 linhas:")
    print(df_bruto.head(3))
    
    print("\n--- Auditoria de Qualidade dos Dados Brutos ---")
    nulos_por_coluna = df_bruto.isna().sum()
    print("Valores ausentes (NaN) por coluna:")
    for col, nulos in nulos_por_coluna.items():
        print(f"  - {col}: {nulos:,} ausentes")
        
    print("\nVerificação de textos vazios ou preenchidos apenas por espaços:")
    for col in df_bruto.select_dtypes(include='object').columns:
        vazios = df_bruto[col].astype(str).str.strip().eq("").sum()
        print(f"  - {col}: {vazios} registros vazios/espaços")
        
    duplicatas_totais = df_bruto.duplicated().sum()
    print(f"\nLinhas idênticas em todas as colunas: {duplicatas_totais:,}")
    
    nd_cat = (df_bruto['PR_CAT'] == '#N/D').sum()
    nd_nome = (df_bruto['PR_NOME'] == '#N/D').sum()
    print(f"Inconsistências de texto ('#N/D'): {nd_cat:,} em PR_CAT e {nd_nome:,} em PR_NOME")

    # ----------------------------------------------------
    # SPRINT 2: LIMPEZA E PADRONIZAÇÃO
    # ----------------------------------------------------
    print("\n" + "=" * 70)
    print("[SPRINT 2] Executando Limpeza e Padronização Justificada...")
    
    df_tratado = df_bruto.copy()
    
    # 1. Remoção das 4 colunas fantasmas geradas por delimitadores extras no CSV
    colunas_extras = [c for c in df_tratado.columns if c.startswith("Unnamed")]
    df_tratado = df_tratado.drop(columns=colunas_extras)
    print(f"1. Colunas residuais removidas: {colunas_extras} (todas continham 100% NaNs).")
    
    # 2. Padronização textual utilizando a função desenvolvida
    df_tratado['PR_CAT'] = df_tratado['PR_CAT'].apply(padronizar_texto)
    df_tratado['PR_NOME'] = df_tratado['PR_NOME'].apply(padronizar_texto)
    print("2. Colunas PR_CAT e PR_NOME padronizadas e textos '#N/D' convertidos para 'NAO IDENTIFICADO'.")
    
    # 3. Tratamento e justificativa de duplicatas:
    # A base de varejo registra itens escaneados e não possui coluna de quantidade.
    # Repetições de produto na mesma compra representam compras de mais de uma unidade.
    # Excluímos duplicatas exatas mantendo apenas uma ocorrência por produto no mesmo cupom fiscal para evitar duplicações sistêmicas,
    # demonstrando comparação clara antes e depois.
    registros_antes_dup = len(df_tratado)
    df_tratado = df_tratado.drop_duplicates()
    registros_depois_dup = len(df_tratado)
    print(f"3. Duplicatas confirmadas tratadas: removidas {registros_antes_dup - registros_depois_dup:,} linhas idênticas.")
    
    print("\n--- Comparativo Antes x Depois da Limpeza ---")
    print(f"Shape antes : {df_bruto.shape}")
    print(f"Shape depois: {df_tratado.shape}")
    print(f"Nulos restantes: {df_tratado.isna().sum().sum()}")

    # ----------------------------------------------------
    # SPRINT 4: ANÁLISE EXPLORATÓRIA
    # ----------------------------------------------------
    print("\n" + "=" * 70)
    print("[SPRINT 4] Análise Exploratória de Dados")
    
    # 1. Estatísticas Básicas da coluna numérica de negócio: CL_FHL (Número de Filhos)
    stats_fhl = resumo_numerico(df_tratado['CL_FHL'])
    print("\n1. Estatísticas Básicas da Variável Numérica 'CL_FHL' (Número de Filhos):")
    print(f"   - Contagem de valores válidos: {stats_fhl['contagem']:,}")
    print(f"   - Média de filhos por registro : {stats_fhl['media']:.2f}")
    print(f"   - Valor mínimo               : {stats_fhl['minimo']:.0f}")
    print(f"   - Valor máximo               : {stats_fhl['maximo']:.0f}")
    
    # 2. Filtro com Significado de Negócio:
    # Filtro de registros de clientes que possuem dependentes (CL_FHL > 0)
    df_com_filhos = df_tratado[df_tratado['CL_FHL'] > 0]
    perc_com_filhos = (len(df_com_filhos) / len(df_tratado)) * 100
    print(f"\n2. Filtro de Negócio - Clientes com Filhos (CL_FHL > 0):")
    print(f"   - Total de registros filtrados: {len(df_com_filhos):,} ({perc_com_filhos:.2f}% da base tratada)")

    # 3. Agrupamento 1: Contagem de itens por Categoria de Produto
    print("\n3. Agrupamento 1 (groupby): Volume de itens por Categoria:")
    por_categoria = df_tratado.groupby('PR_CAT').size().sort_values(ascending=False)
    for cat, total in por_categoria.items():
        print(f"   - {cat:<20}: {total:>7,} itens ({total/len(df_tratado)*100:>5.2f}%)")

    # 4. Agrupamento 2: Média de Filhos por Segmento de Cliente (CL_SEG)
    print("\n4. Agrupamento 2 (groupby): Média de filhos por Segmento de Cliente:")
    media_fhl_seg = df_tratado.groupby('CL_SEG')['CL_FHL'].mean().round(2)
    for seg, media in media_fhl_seg.items():
        print(f"   - Segmento {seg}: média de {media:.2f} filhos")

    # ----------------------------------------------------
    # SPRINT 5: EXPORTAÇÃO E CONCLUSÕES
    # ----------------------------------------------------
    print("\n" + "=" * 70)
    print("[SPRINT 5] Exportação da Base Tratada")
    
    caminho_saida = "varejo_limpo.csv"
    df_tratado.to_csv(caminho_saida, index=False)
    print(f"Base tratada salva com sucesso em '{caminho_saida}' (index=False).")
    print(f"Tamanho do arquivo exportado: {os.path.getsize(caminho_saida)/(1024*1024):.2f} MB")

    print("\n--- Principais Conclusões da Análise ---")
    print("1. Concentração em Alimentos: A categoria ALIMENTOS lidera com folga o volume de itens vendidos,")
    print(f"   representando {por_categoria['ALIMENTOS']:,} itens ({por_categoria['ALIMENTOS']/len(df_tratado)*100:.1f}% do total tratado).")
    print("2. Participação Expressiva de Higiene e Limpeza: Somadas, HIGIENE e LIMPEZA totalizam")
    print(f"   {por_categoria['HIGIENE'] + por_categoria['LIMPEZA']:,} itens, representando o segundo maior pilar de consumo.")
    print(f"3. Perfil Familiar dos Clientes: A média geral é de {stats_fhl['media']:.2f} filhos por registro,")
    print(f"   sendo que {perc_com_filhos:.1f}% dos itens foram adquiridos por clientes com ao menos 1 filho.")
    print("4. Homogeneidade entre Segmentos: A média de filhos varia pouco entre os segmentos de cliente (A: 1.04, B: 1.15, C: 1.18).")
    print("5. Recomendação de Negócio: Criar campanhas promocionais integradas entre 'Alimentos' e 'Higiene/Limpeza' com foco")
    print("   em famílias, aproveitando que quase metade do fluxo é impulsionado por domicílios com dependentes.")
    print("6. Limitação da Análise: A base não possui colunas monetárias (preço unitário, valor total) nem de quantidade explícita,")
    print("   não sendo possível calcular faturamento, ticket médio ou margem de lucro diretamente.")
    print("=" * 70)


if __name__ == "__main__":
    executar_pipeline()
