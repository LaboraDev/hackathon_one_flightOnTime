# 🛫 Projeto de Análise e Predição de Atrasos de Voos - ANAC

## 📌 Visão Geral

Este projeto tem como objetivo analisar dados históricos de voos regulares da ANAC (Agência Nacional de Aviação Civil) para identificar padrões, fatores de risco e criar modelos preditivos de atrasos em voos domésticos brasileiros.

### 🎯 Objetivos

- **Compreender** o comportamento dos dados de voos de 2020 a 2025
- **Identificar** fatores que contribuem para atrasos (sazonalidade, companhias, aeroportos)
- **Avaliar** a qualidade dos dados e realizar tratamentos necessários
- **Preparar** features relevantes para modelagem preditiva
- **Fornecer** insights acionáveis para otimização operacional

---

## 📊 Dataset

**Fonte:** ANAC (Agência Nacional de Aviação Civil)  
**Período:** 2020 - 2025  
**Registros:** ~4 milhões de voos  
**Formato:** CSV (múltiplos arquivos anuais)

### Principais Colunas

| Coluna | Descrição | Tipo |
|--------|-----------|------|
| `empresa_aerea` | Código ICAO da companhia aérea | Texto |
| `numero_voo` | Número identificador do voo | Numérico |
| `aerodromo_origem` | Código ICAO do aeroporto de origem | Texto |
| `aerodromo_destino` | Código ICAO do aeroporto de destino | Texto |
| `partida_prevista` | Data/hora prevista de partida | Datetime |
| `partida_real` | Data/hora real de partida | Datetime |
| `chegada_prevista` | Data/hora prevista de chegada | Datetime |
| `chegada_real` | Data/hora real de chegada | Datetime |
| `situacao_voo` | Status do voo (REALIZADO, CANCELADO) | Texto |
| `atraso_partida_min` | Atraso em minutos (calculado) | Numérico |
| `situacao_partida` | Classificação do atraso | Categórico |

### Features Derivadas

- `dia_semana`: Dia da semana (0=Segunda, 6=Domingo)
- `horario_dia`: Hora do dia da partida prevista (0-23)
- `mes_ano`: Mês do ano (1-12)
- `media_atraso_empresa`: Média histórica de atraso por companhia
- `media_atraso_origem`: Média histórica de atraso por aeroporto de origem
- `media_atraso_destino`: Média histórica de atraso por aeroporto de destino
- `atrasado`: Flag binária (1 = atraso > 15 min, 0 = caso contrário)

---

## 🗂️ Estrutura do Projeto

projeto-atrasos-voos/
│
├── dados/
│ ├── dados_vra.zip # Dados brutos (54 arquivos CSV)
│ └── dados_processados/ # Dados limpos e processados
│
├── notebooks/
│ ├── etl_s01.ipynb # ETL e preparação inicial
│ ├── DS1_qualidade_dados.ipynb # Análise de qualidade
│ ├── DS2_distribuicoes.ipynb # Análise de distribuições
│ ├── DS3_correlacoes.ipynb # Análise de correlações
│ ├── DS4_sazonalidade.ipynb # Análise temporal
│ └── DS5_segmentacao.ipynb # Análise por cia/aeroportos
│
├── docs/
│ ├── README.md # Este arquivo
│ ├── DATA_DICTIONARY.md # Dicionário de dados
│ ├── METHODOLOGY.md # Metodologia detalhada
│ └── FINDINGS.md # Principais descobertas
│
├── reports/
│ ├── data_quality_report.csv # Relatório de qualidade
│ └── apresentacao_final.pdf # Slides da apresentação
│
└── requirements.txt # Dependências Python


---

## 🛠️ Tecnologias Utilizadas

### Python 3.8+
- **pandas** - Manipulação e análise de dados
- **numpy** - Operações numéricas
- **matplotlib** - Visualizações básicas
- **seaborn** - Visualizações estatísticas
- **scipy** - Testes estatísticos
- **gdown** - Download de arquivos do Google Drive
- **unidecode** - Normalização de texto

### Ambiente
- **Google Colab** - Desenvolvimento e execução
- **Jupyter Notebook** - Documentação interativa

---

## 📈 Metodologia - Semana 1 (EDA)

A análise foi dividida em **5 dimensões** complementares:

### DS1 - Qualidade e Estrutura dos Dados
- Verificação de tipos de dados
- Análise de valores ausentes
- Detecção de inconsistências e outliers
- Criação de Data Quality Report

### DS2 - Distribuições e Comportamento
- Análise de distribuições de variáveis numéricas
- Identificação de padrões em histogramas e boxplots
- Comparação entre voos atrasados e pontuais

### DS3 - Correlações e Relações
- Matriz de correlação entre variáveis
- Análise de colinearidade
- Identificação de features com maior potencial preditivo

### DS4 - Sazonalidade Temporal
- Análise de atrasos por mês do ano
- Padrões semanais (dia da semana)
- Efeito cascata ao longo do dia (horário)
- Heatmaps de interações temporais

### DS5 - Segmentação
- Ranking de companhias aéreas por desempenho
- Análise de aeroportos (origem e destino)
- Identificação de rotas críticas
- Padrões combinados (companhia × aeroporto)

---

## 🔑 Principais Descobertas

### ✅ Qualidade dos Dados
- **82%** dos registros estão completos
- Outliers extremos representam **8%** do dataset
- Principais problemas: valores nulos em `codigo_justificativa` (100%)

### 📊 Padrões Identificados

**Temporal:**
- Atrasos aumentam **progressivamente ao longo do dia** (+15 min entre manhã e noite)
- Dezembro e julho apresentam **picos sazonais**
- Sextas-feiras têm **20% mais atrasos** que segundas

**Operacional:**
- Diferença de até **35%** entre melhor e pior companhia
- Top 3 aeroportos concentram **45%** dos atrasos
- Rotas específicas têm atraso médio **3x superior** à média geral

**Correlações:**
- Nenhuma variável isolada tem correlação forte (>0.7) com atraso
- Médias históricas (empresa/aeroporto) têm correlação moderada (0.3-0.5)
- Sugere necessidade de **modelos não-lineares**

---

## 👥 Equipe

**Time de Data Science - Semana 1:**
- DS1: Helena Balbino - Qualidade de Dados
- DS2: Ana Rachel R Costa - Distribuições
- DS3: Ana Rachel R Costa - Correlações
- DS4: Amélia Conti - Sazonalidade
- DS5: Enoque Mandlate - Segmentação

**Coordenação:** Helena Balbino

---

## 📅 Cronograma

### Semana 1 (15-19/12/2025) - EDA ✅
- Segunda (15/12): Reunião de alinhamento e escolha de dimensões
- Quinta (18/12): Apresentação individual dos achados
- Sexta (19/12): Consolidação e documentação

### Próximas Etapas
- **Semana 2:** Limpeza e Feature Engineering
- **Semana 3:** Modelagem Preditiva
- **Semana 4:** Otimização e Deploy

---

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto:
- Abra uma **GitHub Issue** no repositório
- Repositório: []
- Documentação completa: [link da wiki]

---

## 📜 Licença

Este projeto utiliza dados públicos da ANAC e é destinado exclusivamente para fins educacionais e de pesquisa.

**Última atualização:** 19 de dezembro de 2025
