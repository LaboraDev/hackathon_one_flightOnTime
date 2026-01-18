# 05 — Modelo Campeão e Métricas

## 1. Objetivo

Este documento consolida e formaliza os principais resultados do processo experimental do FlyOnTime, registrando de forma clara e auditável as decisões técnicas e os critérios adotados para seleção do modelo final. O conteúdo apresentado aqui tem como finalidade garantir rastreabilidade do ciclo de modelagem, além de servir como referência para manutenção e evolução futura do projeto.

De forma objetiva, este documento apresenta:

- o **modelo campeão**, selecionado para uso em produção
- as **métricas finais** obtidas no teste temporal (*out-of-time*)
- os **critérios de escolha** utilizados durante a comparação entre algoritmos
- as **limitações identificadas** e as **recomendações operacionais** para garantir robustez e consistência em ambiente real

---

## 2. Critério de Seleção do Campeão

O modelo campeão do FlyOnTime foi definido a partir de um processo estruturado de comparação entre algoritmos sob **validação temporal**, priorizando desempenho na classe positiva (`atraso = 1`) e estabilidade em cenários futuros.

A seleção ocorreu em duas camadas:

1. **Ranking inicial por desempenho na validação temporal (`df_val`)**  
   Todos os modelos candidatos foram treinados utilizando o período histórico (`df_train`) e avaliados em uma janela posterior (`df_val`). O critério objetivo de ranqueamento foi o **F1 Score da classe positiva**, registrado como `f1_pos`, com ordenação decrescente.

2. **Confirmação no teste final (treino expandido + teste out-of-time)**  
   Após identificar o melhor modelo na validação, o algoritmo campeão foi retreinado com a base consolidada (`df_train + df_val`) e avaliado no conjunto final (`df_test`), simulando o cenário real de produção (inferência no futuro).

Dessa forma, o modelo é considerado campeão apenas se apresentar:

- **melhor desempenho na validação temporal**, com foco em `f1_pos`
- **capacidade de generalização no teste final out-of-time**
- **consistência ao longo da otimização temporal** via `TimeSeriesSplit(n_splits=5)` aplicada durante o ajuste fino (GridSearch)

> Resultado formalizado no notebook: o melhor modelo identificado no estágio de validação foi o **XGBoost**, posteriormente retreinado e otimizado via GridSearchCV com validação temporal.

---
## 3. Métricas Exigidas

A avaliação do modelo campeão segue um padrão corporativo de métricas voltado a classificar o desempenho geral do classificador e, principalmente, sua eficiência em detectar a classe positiva (`atraso = 1`), que representa o evento operacional de maior impacto, no caso do projeto identificar os voos com atrasos.

As métricas oficiais reportadas para os experimentos são extraídas da modelagem de forma padronizada e incluem:

- **Accuracy**
- **Precision (classe positiva / `atraso = 1`)**
- **Recall (classe positiva / `atraso = 1`)**
- **F1 Score (classe positiva / `atraso = 1`)**
- **F1 Macro** (média não ponderada entre classes)
- **F1 Weighted** (média ponderada pelo suporte das classes)
- **ROC-AUC** (quando aplicável e disponível via `predict_proba`)
- **Matriz de Confusão (`cm`)** no conjunto de teste final (*out-of-time*)

A métrica primária do projeto permanece sendo:

- **F1 Score da classe positiva (`f1_pos`)**

pois ela reflete o equilíbrio entre **Precision** e **Recall** para o evento de atraso, evitando que o modelo seja otimizado apenas para acurácia global em um problema com potencial desbalanceamento de classes.

---
## 4. Comparativo entre Modelos (Validação Temporal)

A comparação entre modelos foi realizada em regime de **validação temporal**, garantindo que o processo reflita um cenário realista de produção (treinar no passado e avaliar no futuro). Para assegurar consistência metodológica, todos os modelos passaram pelo mesmo pipeline, incluindo:

- aplicação das mesmas regras de feature engineering
- remoção de colunas não elegíveis (`cols_removida_modelagem`)
- avaliação com foco na classe positiva (`positive_label="1"`)

O ranking oficial foi definido pela ordenação decrescente de `f1_pos` (F1 da classe atraso).

### Resultados do ranking (Validação)

| Modelo               | F1 (classe 1) | Recall (classe 1) | Precision (classe 1) | Observações |
|----------------------|---------------|-------------------|----------------------|------------|
| XGBoost              | 0.3283        | 0.3214            | 0.3356               | melhor desempenho em validação temporal |
| LightGBM             | 0.3275        | 0.4397            | 0.2609               | recall mais alto, porém com queda de precision |
| Random Forest        | 0.3130        | 0.5213            | 0.2237               | recall elevado, maior volume de falsos positivos |
| Logistic Regression  | 0.2976        | 0.5492            | 0.2041               | baseline simples, alta sensibilidade e baixa precisão |

✅ **Campeão na validação:** **XGBoost**

> Nota: os valores oficiais foram obtidos diretamente do notebook através do dataframe `df_val_resultados`, ordenado por `f1_pos`.

---

## 5. Relatório do Teste Final (Out-of-Time)

Após identificar o modelo líder na validação temporal (**XGBoost**), o pipeline executou o retreinamento do modelo utilizando uma base expandida (`df_train + df_val`) e realizou a avaliação no conjunto final de teste (`df_test`), configurado como um **holdout temporal**.

Esse teste final representa o principal indicador de generalização do modelo em um cenário real de operação, pois mede o desempenho em uma janela totalmente futura, sem reutilização de dados no treinamento.

### Resultado do campeão no teste final 

As métricas consolidadas registradas no teste final foram:

- **Accuracy:** 0.7366  
- **Precision (classe 1):** 0.3123  
- **Recall (classe 1):** 0.4031  
- **F1 Score (classe 1):** 0.3519  
- **F1 Macro:** 0.5933  
- **F1 Weighted:** 0.7490  
- **ROC-AUC:** 0.6753  
- **Matriz de Confusão (`cm`):**  
  `[[484701, 114805], [77188, 52127]]`

Esses resultados confirmam a capacidade do modelo de manter generalização em janela futura, especialmente considerando que o comportamento operacional da malha aérea pode variar ao longo do tempo (*drift temporal*).

### Análise de padrões de erro (FP/FN)

A matriz de confusão evidencia o trade-off característico da classe positiva:

- **Falsos positivos (FP):** casos onde o modelo sinaliza atraso, mas o voo ocorre como pontual  
- **Falsos negativos (FN):** casos onde o modelo não identifica atrasos reais (maior risco operacional)

Como a métrica principal do projeto é `f1_pos`, o objetivo do pipeline é equilibrar a sensibilidade (Recall) sem gerar explosão de alertas (Precision).

---

## 6. Decisão Final e Formalização do Pipeline

Após a validação temporal do baseline e a confirmação do desempenho no teste final out-of-time, o modelo campeão passou por uma etapa adicional de **otimização via GridSearchCV**, respeitando validação temporal com `TimeSeriesSplit(n_splits=5)` e métrica-alvo de seleção:

- **F1 Score (classe positiva / `pos_label = 1`)**

O ajuste fino foi executado com:

- **108 combinações de hiperparâmetros**
- **5 dobras temporais**
- total de **540 fits**
- objetivo de maximizar o desempenho na detecção de atrasos mantendo consistência temporal

### Melhor configuração encontrada no GridSearch

O GridSearch formalizou como melhor combinação:

- `model__learning_rate = 0.1`
- `model__max_depth = 5`
- `model__n_estimators = 900`
- `model__scale_pos_weight = 5`
- `model__subsample = 0.8`

O melhor score médio em validação temporal (`best_score_`) foi registrado como:

- **F1 (CV): 0.3477**

### Resultado no teste final com modelo otimizado 

O modelo otimizado foi avaliado novamente no teste final (`df_test`) para medir o impacto real do ajuste fino no cenário out-of-time.

- **Accuracy:** 0.6830  
- **Precision (classe 1):** 0.2853  
- **Recall (classe 1):** 0.5225  
- **F1 Score (classe 1):** 0.3690  
- **F1 Macro:** 0.5787  
- **F1 Weighted:** 0.7139  
- **ROC-AUC:** 0.6769  

### Interpretação da decisão final

O ajuste fino demonstrou melhoria no objetivo principal do projeto (**F1 da classe positiva**), com aumento relevante de **Recall**, indicando maior capacidade de identificar atrasos reais (reduz falsos negativos). Em contrapartida, observou-se redução em **Precision** e **Accuracy**, refletindo o trade-off natural ao tornar o modelo mais sensível à classe positiva.

A formalização do modelo campeão para produção segue o pipeline oficial treinado e validado temporalmente, sendo o estimador resultante do GridSearch (`best_estimator_`) o artefato utilizado na serialização e consumo na aplicação.

### Entregável oficial

O pipeline final do FlyOnTime é formalizado como:

- **Feature Engineering + Pré-processamento + Modelo XGBoost otimizado**
- compatível com execução reprodutível em batch e inferência em produção
- preparado para serialização e disponibilização via **API Python**
