# 06 — Explicabilidade do Modelo

## 1. Objetivo

Além de prever o risco de atraso na partida, o FlyOnTime foi construído com foco em **transparência e rastreabilidade**, permitindo interpretar quais fatores exercem maior influência no comportamento do modelo campeão.

A explicabilidade é um requisito importante tanto para usuários finais quanto para equipes técnicas, pois reduz o efeito de “caixa-preta” e facilita auditorias, validação de consistência e evolução do pipeline ao longo do tempo.

A explicabilidade do projeto é entregue em dois níveis complementares:

- **Explicabilidade Local (por predição)**: explica o motivo de um voo específico ter sido classificado como atrasado (`1`) ou pontual (`0`)
- **Explicabilidade Global (visão macro)**: resume quais variáveis mais influenciam o comportamento do modelo no geral

A implementação prioriza consistência com o pipeline real de produção (**Feature Engineering + Pré-processamento + Modelo**), garantindo que as explicações sejam calculadas exatamente sobre as features utilizadas em inferência.

---

## 2. Explicabilidade Local (por predição)

A explicabilidade local no FlyOnTime foi desenhada para responder, com objetividade e rastreabilidade, à seguinte pergunta operacional:

> **“Quais fatores levaram o modelo a classificar este voo como atrasado ou pontual?”**

Em um cenário de uso real, a previsão isolada (apenas `0` ou `1`, ou mesmo uma probabilidade) não é suficiente para suportar tomada de decisão. Áreas operacionais, analistas e stakeholders precisam entender **o racional estatístico** por trás do resultado, principalmente em casos de divergência com expectativa humana (ex.: um voo previsto como “Atrasado” mesmo em condições aparentemente normais).

Por esse motivo, o FlyOnTime entrega uma explicação **por instância** (por voo), baseada diretamente no comportamento interno do modelo, permitindo identificar **quais variáveis empurraram a decisão na direção do atraso** e quais variáveis atuaram como **fatores de mitigação**.

### 2.1 Método utilizado (contribuições nativas do XGBoost)

Quando o modelo utilizado é baseado em **XGBoost**, a explicabilidade local é calculada utilizando o mecanismo nativo de contribuições por feature disponibilizado pelo próprio algoritmo. Esse método decompõe matematicamente o score do modelo em:

- **contribuições individuais por feature**, que podem ser positivas ou negativas
- um termo fixo chamado **bias**, que funciona como ponto de partida do modelo antes das contribuições acumuladas

Esse formato é altamente adequado para produção porque:

- não depende de aproximações externas
- é rápido o suficiente para execução em tempo de inferência
- é diretamente consistente com o modelo serializado em produção

Na prática, isso permite afirmar de forma auditável:  
**“O modelo classificou este voo como atrasado porque as essas features aumentaram o score final acima do limiar de decisão.”**

### 2.2 Garantia de consistência com o pipeline de produção

Um cuidado essencial do FlyOnTime é que a explicação local é calculada **sobre as mesmas features finais que chegam ao modelo no momento da predição**. Isso elimina discrepâncias comuns em projetos de ML, onde explicações acabam sendo geradas em uma representação diferente daquela usada em produção.

Para garantir essa consistência, a explicabilidade local executa obrigatoriamente a sequência completa do pipeline:

1. **Feature Engineering (`fe`)** — criação e transformação de variáveis derivadas  
2. **Pré-processamento (`pre`)** — encoding, normalizações e estrutura final do vetor numérico  
3. **Modelo (`model`)** — geração da previsão e decomposição das contribuições  

Esse desenho assegura que a explicação não seja apenas “plausível”, mas sim **tecnicamente rastreável e reproduzível**, pois reflete exatamente o que o modelo consumiu.

### 2.3 Estrutura do retorno 

A explicação local é retornada em um formato estruturado e padronizado para integração com o backend e frontend. O objetivo é permitir tanto **exibição para usuários finais** quanto **uso técnico para depuração e auditoria**.

O retorno contém:

- **Top features mais relevantes**, ordenadas por impacto absoluto
- **contribution**: impacto quantitativo da feature na decisão
- **direction**:
  - `increase` quando contribui para aumentar a chance de atraso
  - `decrease` quando reduz a chance de atraso
- **value**: valor final observado no vetor processado (após FE + PRE)
- **bias**: componente base do modelo, que representa o ponto inicial do score

Esse padrão permite que a interface apresente mensagens interpretáveis como:

- “O fator X aumentou a chance de atraso”
- “O fator Y reduziu a chance de atraso”

sem depender de heurísticas ou lógica adicional fora do pipeline.

---

## 3. Explicabilidade Global (visão macro do modelo)

A explicabilidade global no FlyOnTime tem como objetivo fornecer uma visão executiva e técnica sobre o comportamento geral do modelo, respondendo:

> **“Quais variáveis explicam a maior parte do poder preditivo do modelo?”**

Essa camada de interpretação é fundamental em ambientes corporativos porque:

- facilita alinhamento com stakeholders não técnicos
- permite justificar o modelo como ativo de decisão
- cria base para auditoria e governança
- orienta evolução do produto e manutenção do pipeline

Em outras palavras, se a explicabilidade local atende ao nível “voo a voo”, a explicabilidade global atende ao nível “modelo como sistema”.

### 3.1 Importância de features via XGBoost (gain)

Para o modelo campeão baseado em XGBoost, o FlyOnTime utiliza o mecanismo nativo do algoritmo para cálculo de importância, priorizando o critério **`gain`** .

O `gain` mede, de forma agregada, o quanto determinada variável contribuiu para melhorar as decisões das árvores durante o treinamento. Essa métrica é adequada para priorização de variáveis porque reflete **capacidade real de redução de erro**, e não apenas frequência de uso.

A saída da explicabilidade global é estruturada como um ranking das features mais importantes, permitindo que o time responda de forma objetiva:

- quais sinais dominam o comportamento do modelo
- quais variáveis merecem monitoramento específico
- quais dimensões estão sendo priorizadas pelo algoritmo

### 3.2 Rastreabilidade de nomes após pré-processamento

Como o pipeline utiliza pré-processamento (incluindo expansão de categorias), o projeto implementa uma etapa de rastreabilidade dos nomes finais das features através do método:

- `pre.get_feature_names_out()`

Isso é essencial para evitar relatórios com identificadores genéricos como `f0`, `f1`, `f2`, que seriam inadequados para documentação corporativa e auditoria.

Quando o mapeamento está disponível, o FlyOnTime entrega nomes finais padronizados, como:

- features categóricas codificadas (`cat_...`)
- features numéricas agregadas (`num_...`)
- features temporais e estruturais (`hora_sin`, `is_hub`, etc.)

Com isso, a explicabilidade global se torna **comunicável**, e não apenas técnica.

---

## 4. Explicabilidade Unificada (padrão multi-modelo e resiliência)

O FlyOnTime foi desenhado com um requisito importante de engenharia corporativa: **resiliência a mudanças de modelo sem quebrar contratos de produto**.

Em projetos reais, o modelo campeão pode variar com o tempo (ex.: troca de XGBoost por RandomForest, LightGBM), seja por restrições operacionais, custo computacional ou evolução da base de dados.

Para evitar que isso comprometa a entrega de transparência, o projeto implementa uma estratégia unificada de explicabilidade, garantindo:

- compatibilidade com modelos baseados em XGBoost
- compatibilidade com modelos de árvore do ecossistema sklearn
- padronização do retorno
- consistência de consumo pelo backend/frontend

Essa decisão eleva maturidade do pipeline e reduz risco técnico em evolução futura.

### 4.1 Local unificado

A explicabilidade local unificada entrega uma estrutura padronizada, independentemente do algoritmo final utilizado, garantindo que o produto continue oferecendo explicações por voo.

Critérios:

- Se o modelo for **XGBoost**, utiliza contribuições nativas (`pred_contribs`)
- Se o modelo for **árvore sklearn**, utiliza SHAP via `TreeExplainer`

O retorno inclui um campo adicional:

- `method`: identificador da estratégia aplicada

Isso permite rastreabilidade e debugging em produção, inclusive para confirmar qual técnica foi utilizada em cada cenário.

### 4.2 Global unificado

Da mesma forma, a explicabilidade global unificada garante um ranking corporativo de features relevantes:

- `gain` / `weight` / etc para XGBoost
- `feature_importances_` para árvores sklearn

A saída incorpora o campo `method`, assegurando que relatórios corporativos possam registrar:

- qual métrica de importância foi aplicada
- qual família de modelo estava em uso naquele ciclo de treinamento

---

## 5. Benefícios corporativos

A explicabilidade implementada no FlyOnTime fortalece o projeto nos principais pilares corporativos de modelos preditivos em produção:

- **Confiança e adoção do produto**, reduzindo rejeição por “caixa-preta”
- **Rastreabilidade técnica**, permitindo auditoria do racional do modelo
- **Depuração e manutenção**, acelerando diagnóstico de regressões e inconsistências
- **Governança e conformidade**, suportando revisão e documentação formal
- **Gestão de risco operacional**, reduzindo decisões baseadas em probabilidade sem contexto

Como resultado, o FlyOnTime entrega não apenas um classificador de atraso, mas um sistema preditivo com maturidade para uso em ambiente real, com transparência e capacidade de explicação compatíveis com padrões corporativos.
