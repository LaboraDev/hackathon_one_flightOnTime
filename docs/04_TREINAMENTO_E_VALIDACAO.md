# 04 — Treinamento e Validação do Modelo

## 1. Contexto

A previsão de atraso em voos é um problema de Machine Learning com **alta dependência temporal** e sujeito a mudanças constantes no ambiente operacional. Ao longo de meses e anos, fatores como regras regulatórias, disponibilidade de infraestrutura aeroportuária, ajustes na malha aérea, estratégias das companhias, sazonalidade de demanda e até condições operacionais indiretas (ex.: picos de conexão e volume de tráfego) podem alterar significativamente o padrão de atrasos observado nos dados históricos.

Esse comportamento caracteriza um cenário clássico de drift temporal, no qual relações aprendidas pelo modelo em um período podem se enfraquecer ou mudar em outro. Por esse motivo, validações tradicionais com embaralhamento aleatório dos registros podem produzir métricas artificialmente otimistas, pois misturam exemplos do “futuro” e do “passado” dentro do mesmo conjunto, criando um cenário irreal e aumentando o risco de vazamento de informação.

Diante disso, o FlyOnTime adota **validação temporal** como padrão obrigatório, garantindo que o modelo seja avaliado de maneira mais próxima ao uso real em produção: ele é treinado com dados de períodos anteriores e testado em períodos posteriores. Essa abordagem reduz o risco de *leakage*, melhora a confiabilidade das métricas reportadas e assegura que a performance estimada represente com maior precisão o comportamento esperado do modelo em cenários reais de inferência.

---

## 2. Modelos Avaliados

Para selecionar o modelo campeão do FlyOnTime, foram treinados e comparados diferentes algoritmos de Machine Learning com níveis distintos de complexidade, interpretabilidade e capacidade de generalização. A estratégia de benchmarking foi desenhada para garantir que o modelo final não seja apenas o mais performático em métricas offline, mas também o mais adequado para operação em produção, considerando estabilidade, robustez a ruído e facilidade de manutenção.

Os modelos avaliados foram:

- **Logistic Regression**
- **Random Forest**
- **XGBoost**
- **LightGBM**

### Justificativa da escolha dos modelos

Cada algoritmo foi incluído com um objetivo específico dentro do processo de comparação:

- **Logistic Regression** foi utilizada como baseline estatístico e interpretável, permitindo estabelecer um patamar mínimo de performance e facilitar a validação de consistência das features. Além disso, esse modelo serve como referência para avaliar se o ganho de modelos mais complexos justifica o aumento de custo e complexidade.

- **Random Forest** foi avaliado como alternativa robusta baseada em árvores, capaz de capturar relações não-lineares e interações entre variáveis sem exigir forte pré-processamento. Esse modelo também tende a ser resiliente a ruídos em dados tabulares e oferece uma base sólida para comparação com ensembles mais avançados.

- **XGBoost** foi incluído por ser um dos métodos mais consolidados para dados tabulares, com excelente capacidade de capturar padrões complexos e lidar bem com variáveis heterogêneas. Sua utilização permite comparar performance em um algoritmo altamente competitivo e amplamente utilizado em aplicações industriais.

- **LightGBM** foi avaliado como uma solução moderna e eficiente de gradient boosting, frequentemente superior em velocidade e escalabilidade para grandes volumes de dados. Além do desempenho, ele tende a entregar ótima performance com menor custo computacional, sendo um forte candidato para ambientes com necessidade de inferência rápida e manutenção simplificada.

Essa comparação estruturada garante que a escolha do modelo final seja baseada em evidência, equilibrando **performance**, **robustez operacional** e **viabilidade de implantação**, com foco em entregar previsões consistentes e sustentáveis em produção.

---

## 3. Estratégia de Validação Temporal

A estratégia de validação do FlyOnTime foi estruturada com foco em **generalização temporal**, garantindo que o modelo seja avaliado em condições realistas de produção, onde previsões são feitas em períodos futuros com base em padrões aprendidos no passado.

Para isso, o processo foi conduzido em duas etapas complementares, respeitando a ordem cronológica dos registros com base em `partida_prevista`.

---

### Etapa 1 — Treino e Validação em Janela Temporal Futura

Na primeira etapa, foram treinados e comparados múltiplos algoritmos utilizando um conjunto histórico como treino e um bloco temporal posterior como validação. Essa abordagem permite medir a capacidade do modelo de generalizar para dados futuros, reduzindo o risco de métricas infladas por embaralhamento aleatório.

No pipeline executado, os períodos utilizados foram:

- **Período de treino:** `2021-01-01 00:05:00` → `2024-04-16 10:20:00`
- **Período de validação:** `2024-04-16 10:25:00` → `2024-09-09 08:00:00`

Durante essa etapa, cada modelo avaliado foi treinado e medido com a mesma estrutura de pré-processamento e as mesmas regras de remoção de colunas não elegíveis (`cols_removida_modelagem`), garantindo comparabilidade direta entre algoritmos.

**Objetivos principais desta etapa:**
- avaliar a **generalização em período futuro**
- comparar modelos em um cenário temporal realista
- reduzir risco de overfitting e dependência de padrões específicos do passado

---

### Etapa 2 — Retreinamento Expandido e Teste Final (Simulação de Produção)

Após a seleção do melhor modelo na etapa anterior (com base nas métricas de validação), foi realizado um retreinamento expandido utilizando todo o período disponível até o final da validação, formando um conjunto consolidado de treino (`train + val`) e avaliando em um bloco temporal final (*holdout*) que simula um cenário real de uso em produção.

O conjunto de treino final foi construído através da concatenação:

- `df_trainval = concat(df_train, df_val)` (ordenado por `partida_prevista`)

Com os seguintes períodos:

- **Treino final (train + val):** `2021-01-01 00:05:00` → `2024-09-09 08:00:00`
- **Teste final:** `2024-09-09 08:00:00` → `2025-07-01 07:10:00`

**Objetivos principais desta etapa:**
- simular o cenário real de produção, com inferência em janelas futuras
- validar estabilidade do modelo ao atravessar mudanças temporais do setor
- obter uma estimativa final de performance em um conjunto *out-of-time*

---

## 4. Ajuste Fino com Validação Temporal (TimeSeriesSplit)

Após a etapa de benchmarking e definição do melhor algoritmo, foi realizado um processo adicional de otimização de hiperparâmetros utilizando validação temporal com múltiplas janelas de treino/validação através do `TimeSeriesSplit`.

O pipeline de modelagem foi montado como um fluxo único e reprodutível, contendo:

1. **Criação de features temporais**
   - `DatasFeaturesTransformer(col_dt="partida_prevista", col_atraso="atraso_partida_min")`

2. **Features adicionais de alta densidade de sinal**
   - `UltimateFeatureEngineer()`
   - (inclui encoding cíclico `hora_sin`/`hora_cos` e flag estrutural `is_hub`)

3. **Médias históricas por entidade**
   - `MediaAtrasoTransformer(col_atraso="atraso_partida_min")`
   - gera features como `media_atraso_empresa`, `media_atraso_origem` e `media_atraso_destino`

4. **Remoção preventiva de colunas não elegíveis (anti-leakage)**
   - `DropColumnsTransformer(cols_removida_modelagem)`

5. **Pré-processamento final**
   - `montar_preprocessador(cfg)`

6. **Modelo campeão**
   - treinado ao final do pipeline

### Configuração da validação e métrica

O ajuste fino utilizou:

- `TimeSeriesSplit(n_splits=5)` (**5 dobras temporais**)
- métrica principal: **F1 Score** com foco na classe positiva (`pos_label=1`)
  - classe `1` representa **voo atrasado** conforme definição do target

A função de scoring utilizada foi:

- `scorer = make_scorer(f1_score, pos_label=1)`

### Justificativa

A escolha de `TimeSeriesSplit` permite que a otimização respeite a ordem cronológica e avalie o desempenho do modelo em múltiplas janelas temporais, reduzindo o risco de sobreajuste a um recorte específico do histórico.

Além disso, o uso de **F1 Score** como métrica central foi adotado para equilibrar:

- **Recall**: capacidade de identificar atrasos reais (reduzir falsos negativos)
- **Precision**: evitar alertas excessivos (reduzir falsos positivos)

Essa decisão é especialmente relevante em problemas com classes potencialmente desbalanceadas e onde a classe "atraso" possui maior impacto operacional.

---
### Grid de Hiperparâmetros Avaliado

Para maximizar o desempenho do modelo campeão sem comprometer a estabilidade temporal, foi executado um processo de **ajuste fino** via `GridSearchCV`, utilizando validação baseada em séries temporais (`TimeSeriesSplit`) e métrica principal **F1 Score** para a classe positiva (`pos_label=1`).

O objetivo do grid search foi encontrar a combinação de hiperparâmetros que melhor equilibra **capacidade de generalização**, **controle de overfitting** e **sensibilidade à classe de atraso**, garantindo desempenho consistente ao longo de janelas temporais.

O espaço de busca avaliado foi:

- `model__n_estimators`: `[500, 900]`  
  Controla a quantidade de árvores do ensemble. Valores maiores tendem a aumentar poder preditivo, porém com maior custo computacional e risco de overfitting se não houver regularização adequada.

- `model__learning_rate`: `[0.03, 0.1, 0.01]`  
  Define o tamanho do passo de aprendizado a cada iteração. Taxas menores geralmente produzem modelos mais estáveis e generalizáveis, especialmente quando combinadas com maior número de estimadores.

- `model__max_depth`: `[3, 5, 8]`  
  Define a profundidade máxima das árvores, controlando complexidade do modelo. Profundidades menores reduzem overfitting; profundidades maiores capturam interações mais complexas, porém com maior risco de memorizar padrões específicos.

- `model__subsample`: `[0.8, 1.0]`  
  Proporção de amostras utilizadas na construção de cada árvore. Valores abaixo de 1.0 introduzem aleatoriedade e atuam como regularização, aumentando robustez e reduzindo variância.

- `model__scale_pos_weight`: `[3, 4, 5]`  
  Ajusta o peso da classe positiva (atraso), auxiliando no balanceamento do problema e aumentando a sensibilidade do modelo à detecção de voos atrasados. Essa configuração é relevante em cenários de desbalanceamento, onde atrasos representam uma fração menor do total de operações.

Ao final do processo, o `GridSearchCV` seleciona automaticamente a configuração com melhor desempenho médio nas dobras temporais definidas, resultando em um modelo otimizado e mais consistente para operação em produção.

---

## 5. Métrica Principal de Entrega

A métrica principal adotada para avaliação e comparação dos modelos no FlyOnTime foi:

- **F1 Score (classe positiva: `atraso = 1`)**

A escolha do **F1 Score** é estratégica porque o problema de previsão de atraso tende a possuir assimetria entre classes, onde a classe "atraso" representa os eventos de maior impacto operacional e, ao mesmo tempo, pode ocorrer com menor frequência no dataset.

Dessa forma, utilizar apenas acurácia poderia induzir uma avaliação enganosa, pois um modelo poderia obter bons resultados prevendo majoritariamente a classe "pontual", sem necessariamente identificar atrasos com qualidade.

Ao priorizar o **F1 Score para `atraso = 1`**, o projeto garante um equilíbrio entre:

- **Sensibilidade**: reduzir o risco de atrasos reais serem ignorados (falsos negativos)
- **Precisão**: evitar que o sistema gere alertas excessivos ou inconsistentes (falsos positivos)

Essa abordagem mantém o foco do modelo no objetivo mais relevante do produto: identificar, de forma confiável, voos com probabilidade elevada de atraso dentro de um cenário realista de operação e tomada de decisão.

---

## 6. Tratamento de Desbalanceamento

O pipeline do FlyOnTime foi projetado para suportar execução com ou sem técnicas de balanceamento, incluindo a opção de oversampling por **SMOTE**, permitindo comparações controladas sob a mesma estrutura de pré-processamento e avaliação temporal.

Entretanto, apesar do suporte implementado no código, o SMOTE não foi utilizado na execução final do projeto, devido a limitações práticas de infraestrutura: a aplicação do oversampling elevaria significativamente o volume de dados em memória, ultrapassando o limite de recursos disponíveis no ambiente de execução e gerando risco de falhas por consumo excessivo de RAM.

Dessa forma, a estratégia adotada foi manter um treinamento robusto **sem oversampling**, utilizando mecanismos nativos de compensação de desbalanceamento quando aplicável, tais como:

- `class_weight="balanced"` (Logistic Regression, Random Forest e LightGBM)
- `scale_pos_weight` (XGBoost) — incluído inclusive no grid de ajuste fino

Essa decisão preserva a estabilidade do pipeline, reduz risco operacional durante o treinamento e garante maior viabilidade de manutenção e replicação do modelo em ambientes com recursos limitados. A escolha final do modelo segue sendo guiada pela métrica F1 da classe positiva e pela consistência temporal da performance.
