# Mini-Projeto Avaliativo — Lucas Benevides — Turma T8

**Curso:** Análise de Dados com Python  
**Módulo:** 1 (Fundamentos e Manipulação de Dados com Pandas) — Semana 07  
**Aluno:** Lucas Silva Benevides  
**Repositório:** `Miniprojeto_LucasBenevides_T8`

---

## 1. Objetivo
O objetivo deste projeto é realizar uma Análise Exploratória de Dados (AED) aplicada ao setor varejista utilizando a biblioteca **Pandas**. O trabalho contempla desde a leitura da base bruta, diagnóstico detalhado de inconsistências e limpeza orientada a regras de negócio, até a criação de funções reutilizáveis, cálculos estatísticos descritivos, agrupamentos analíticos e exportação da base tratada.

---

## 2. Origem da Base de Dados
* **Fonte:** Kaggle — [Base Varejo](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)
* **Formato Original:** Arquivo CSV com 830.000 linhas, delimitado por ponto e vírgula (`;`).
* **Localização no Projeto:** O arquivo original encontra-se armazenado na pasta `data/Base Varejo.csv`.

---

## 3. Unidade da Análise
* **O que cada linha representa:** Cada registro da base representa um **item individual registrado/escaneado** dentro de uma compra/pedido (`CO_ID`), realizado por determinado cliente (`CL_ID`) e referente a um produto (`PR_ID`).
* **Atenção conceitual:** A contagem de linhas reflete o **volume de itens transacionados**, e não o número absoluto de clientes ou de pedidos distintos. A base não apresenta dados de preços unitários ou faturamento financeiro.

---

## 4. Colunas Utilizadas

| Coluna | Descrição | Tipo Original | Papel na Análise |
| :--- | :--- | :--- | :--- |
| `DATA` | Data da compra (DD/MM/AAAA) | `object` | Dimensão temporal |
| `CO_ID` | Identificador único da compra/pedido | `int64` | Identificador de transação |
| `CL_ID` | Identificador do cliente | `int64` | Identificador de cliente |
| `CL_GENERO` | Gênero do cliente (`M` ou `F`) | `object` | Dimensão demográfica |
| `CL_EC` | Estado civil do cliente (1 a 5) | `int64` | Dimensão demográfica |
| `CL_FHL` | **Número de filhos do cliente (0 a 4)** | `int64` | **Métrica numérica de negócio** |
| `CL_SEG` | Segmento de cliente (`A`, `B` ou `C`) | `object` | Segmentação comportamental |
| `PR_ID` | Código identificador do produto | `int64` | Identificador de catálogo |
| `PR_CAT` | Categoria do produto | `object` | Classificação de produto |
| `PR_NOME` | Descrição nominal do produto | `object` | Descrição de catálogo |
| `Unnamed: 10 a 13` | Colunas nulas geradas por `;` residuais | `float64` | **Removidas na limpeza** |

---

## 5. Diagnóstico de Qualidade dos Dados

Antes de qualquer manipulação, foi conduzida uma auditoria estruturada:

1. **Estrutura Bruta:** 830.000 linhas e 14 colunas.
2. **Valores Ausentes (`NaN`):**
   * As colunas `DATA` até `PR_NOME` apresentaram **0 valores ausentes**.
   * As colunas residuais `Unnamed: 10`, `Unnamed: 11`, `Unnamed: 12` e `Unnamed: 13` apresentaram **830.000 valores nulos (100% vazias)**, decorrentes de ponto e vírgulas extras ao fim de cada linha no CSV original.
3. **Textos Vazios ou com Espaços:** Utilizando a expressão `.astype(str).str.strip().eq("")`, verificou-se que não há strings em branco nas colunas categóricas.
4. **Inconsistências de Conteúdo (`#N/D`):** Identificou-se a string `'#N/D'` em **3.650 linhas** nas colunas `PR_CAT` e `PR_NOME` (associadas exclusivamente ao `PR_ID = 107`). Trata-se de um erro de lookup comum do Excel que o pandas lê como texto válido se não tratado.
5. **Duplicatas Totais:** Identificou-se a presença de **96.553 linhas idênticas** em todas as 14 colunas.

---

## 6. Decisões de Limpeza e Justificativas

| Problema Identificado | Decisão Tomada | Justificativa de Negócio |
| :--- | :--- | :--- |
| 4 Colunas `Unnamed` 100% vazias | **Remoção** (`drop`) | Não continham nenhuma informação útil e eram artefato de formatação do CSV. |
| Texto `'#N/D'` em `PR_CAT` e `PR_NOME` | **Substituição por `'NAO IDENTIFICADO'`** | Preserva a integridade da transação de compra sem inventar categorias e sem mascarar o produto não cadastrado. |
| Caracteres e caixas inconsistentes | **Padronização Textual** (`strip` + `upper`) | Uniformiza o agrupamento e previne que variações como `REFRIGERANTE LIMaO` sejam tratadas como itens distintos. |
| 96.553 Linhas Idênticas | **Remoção de Duplicatas Confirmadas** (`drop_duplicates`) | Consolida a unicidade do item escaneado na mesma transação, reduzindo o shape para 733.447 linhas sem perda de pedidos ou clientes. |

* **Comparativo de Shape:**
  * **Antes:** `(830000, 14)`
  * **Depois:** `(733447, 10)` — redução de 96.553 linhas e 4 colunas nulas.

---

## 7. Funções Reutilizáveis Criadas

Foram implementadas duas funções com parâmetros e retornos explícitos:

```python
def padronizar_texto(valor):
    """Trata ausências, remove espaços e padroniza termos não identificados."""
    if pd.isna(valor):
        return valor
    texto = str(valor).strip()
    if texto.upper() in ["#N/D", "#NA", "NAN", "NULL"]:
        return "NAO IDENTIFICADO"
    return texto.upper().replace("REFRIGERANTE LIMAO", "REFRIGERANTE LIMAO")

def resumo_numerico(serie):
    """Calcula e retorna um dicionário com contagem válida, média, mínimo e máximo."""
    return {
        "contagem": int(serie.count()),
        "media": float(serie.mean()),
        "minimo": float(serie.min()),
        "maximo": float(serie.max())
    }
```

---

## 8. Análises e Resultados

### 8.1 Estatísticas Básicas da Variável Numérica (`CL_FHL` - Número de Filhos)
* **Unidade Analisada:** Quantidade de dependentes/filhos por registro de compra.
* **Contagem de valores válidos:** 733.447 registros.
* **Média:** 1,15 filhos por registro.
* **Mínimo:** 0 filhos.
* **Máximo:** 4 filhos.
* *Interpretação:* A mediana e moda estão centradas em 0 filhos (52,5% dos clientes não possuem filhos), porém a cauda de clientes com 1 a 4 filhos eleva a média para 1,15.

### 8.2 Filtro de Negócio (Famílias com Filhos)
* **Filtro Aplicado:** `df[df['CL_FHL'] > 0]`
* **Resultado:** **348.461 itens** (**47,51%** da base tratada) pertencem a consumidores que declararam possuir 1 ou mais filhos.

### 8.3 Agrupamentos (`groupby`)
1. **Volume de Itens por Categoria de Produto (`PR_CAT`):**
   * `ALIMENTOS`: 384.197 itens (52,38%)
   * `HIGIENE`: 137.702 itens (18,77%)
   * `LIMPEZA`: 128.632 itens (17,54%)
   * `BEBIDAS`: 38.264 itens (5,22%)
   * `PET`: 28.553 itens (3,89%)
   * `ACESSORIOS`: 12.871 itens (1,75%)
   * `NAO IDENTIFICADO`: 3.228 itens (0,44%)
   * *O que mede:* O volume absoluto e percentual de movimentação física de itens no estoque por departamento.

2. **Média de Filhos por Segmento de Cliente (`CL_SEG`):**
   * **Segmento A:** Média de **1,04** filhos
   * **Segmento B:** Média de **1,15** filhos
   * **Segmento C:** Média de **1,18** filhos
   * *O que mede:* A composição média do tamanho familiar entre as diferentes faixas socioeconômicas/segmentos da base de clientes.

---

## 9. Conclusões

1. **Alimentos é o Coração do Varejo:** A categoria `ALIMENTOS` responde por mais da metade de todos os itens vendidos (**52,38%**), demonstrando que o estabelecimento atua primariamente como supermercado de conveniência diária.
2. **Cesta de Higiene e Limpeza:** Somadas, as categorias `HIGIENE` e `LIMPEZA` representam **36,31%** do volume de produtos, evidenciando alto índice de compras recorrentes voltadas para manutenção do lar.
3. **Público Familiar Significativo:** Quase metade das vendas (**47,51%**) é realizada por clientes com dependentes, indicando forte presença do público familiar no faturamento indireto do negócio.
4. **Perfil Equilibrado entre Segmentos:** O número médio de filhos varia suavemente entre os segmentos (de 1,04 no segmento A até 1,18 no segmento C), indicando que estratégias para famílias encontram demanda em todos os estratos da loja.

---

## 10. Recomendação de Negócio
Criar ações promocionais temáticas e cross-merchandising integrando **Alimentos** e **Higiene Infantil/Familiar** (ex: promoções de volta às aulas, combos de lanche e itens de cuidados pessoais), alavancando a alta representatividade (47,51%) de lares com filhos.

---

## 11. Limitação da Análise
A base de dados não contempla colunas monetárias (preço de venda, custo dos produtos ou margem) nem quantidade explícita de itens por linha. Portanto, **não é viável inferir faturamento, rentabilidade financeira ou ticket médio**, estando as análises restritas à volumetria de itens transacionados e dados demográficos.

---

## 12. Explicação do Processo de Dados
* **Leitura:** Ocorreu via `pd.read_csv("data/Base Varejo.csv", sep=";")`, corrigindo a leitura dos delimitadores de ponto e vírgula e isolando as 14 colunas originais.
* **Transformação:** Descarte de 4 colunas nulas, tratamento de strings `'#N/D'`, padronização de caracteres e deduplicação controlada.
* **Gravação:** Exportação de `varejo_limpo.csv` utilizando `to_csv(index=False)`.
* **Impacto na Qualidade:** A substituição consciente de `#N/D` por `'NAO IDENTIFICADO'` garantiu que 3.228 itens legítimos pudessem ser contabilizados no volume total sem gerar erros de cálculo nem omitir transações válidas.

---

## 13. Como Executar o Projeto

### Pré-requisitos
* Python 3.10+
* Pandas: `pip install pandas`

### Execução via Script Python
```bash
python main.py
```

### Execução via Jupyter Notebook
Abra o arquivo [`Miniprojeto_LucasBenevides_T8.ipynb`](Miniprojeto_LucasBenevides_T8.ipynb) no VS Code ou envie-o para o Google Colab e execute todas as células (`Kernel > Restart and Run All Cells`).
