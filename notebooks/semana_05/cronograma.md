# 📘 Semana 05 — Documentação
 
Nas semanas anteriores, o projeto avançou de forma progressiva na construção da solução de Data Science, passando pelas etapas de preparação dos dados, análise exploratória, desenvolvimento de features e treinamento de modelos de Machine Learning. Ao longo desse período, o principal esforço da equipe esteve concentrado em viabilizar um fluxo funcional de predição, garantindo que o modelo pudesse ser treinado, avaliado e utilizado de forma integrada ao sistema. Esse trabalho técnico estabeleceu a base necessária para que o projeto chegasse ao estágio atual com uma solução operacional.

Com a consolidação das etapas técnicas nas semanas anteriores, o projeto entra agora em uma fase diferente, cujo foco principal não é a criação de novas funcionalidades, mas a organização, explicação e formalização do que já foi desenvolvido. Esta semana foi planejada especificamente para estruturar a documentação do projeto de Data Science, transformando o trabalho técnico realizado até aqui em material claro, compreensível e bem organizado, capaz de ser entendido tanto por avaliadores quanto por pessoas que não participaram diretamente do desenvolvimento.

O cronograma desta semana foi desenhado com um caráter guiado e pedagógico, considerando o nível de experiência da equipe e a necessidade de garantir alinhamento conceitual entre todos os membros. Cada frente de trabalho foi definida com objetivos claros, tarefas bem delimitadas e perguntas-chave que orientam a escrita da documentação, evitando improvisações e garantindo que todos estejam trabalhando a partir do mesmo entendimento do projeto. O objetivo é assegurar consistência, qualidade e clareza em todas as entregas produzidas ao longo da semana.

Ao final desta etapa, espera-se que o projeto conte com uma documentação estruturada que reflita de forma fiel as decisões tomadas, as etapas executadas e as limitações identificadas durante o desenvolvimento. Essa consolidação é fundamental não apenas para a avaliação do hackathon, mas também para a apresentação ao vivo do projeto, pois permite que a equipe comunique de forma segura e coerente o valor da solução, o raciocínio por trás das escolhas técnicas e o funcionamento geral do sistema.

---

## 🛠️ DS1 – Documentação Dataset e ETL
### Objetivo

O objetivo desta frente é documentar, de forma clara, progressiva e contextualizada, a origem dos dados utilizados no projeto e todas as etapas iniciais de preparação desses dados até que estejam prontos para serem analisados e utilizados em um modelo de Machine Learning. Essa documentação deve permitir que qualquer leitor, mesmo sem conhecimento prévio do projeto, compreenda de onde os dados vêm, qual fenômeno real eles representam, como estão organizados e quais decisões técnicas foram tomadas durante o processo de extração, transformação e limpeza.

Além disso, esta frente deve explicar como a variável alvo foi definida a partir dos dados brutos, deixando explícitas as regras de negócio adotadas e as limitações existentes já nessa etapa inicial do pipeline. O foco não é apenas descrever o que foi feito, mas justificar por que cada decisão foi necessária para garantir a qualidade e a consistência dos dados utilizados nas etapas seguintes do projeto.

---

### Tarefas

  * Ler cuidadosamente todas as células iniciais do notebook até o final do ETL
  * Identificar a fonte pública do dataset
  * Entender a estrutura dos arquivos utilizados
  * Mapear todas as transformações iniciais feitas nos dados
  * Identificar exatamente como o target foi definido

---

### Perguntas-chave
>    - Qual é a origem pública dos dados?
>    - Qual problema real esses dados representam?
>    - O que cada linha do dataset representa?
>    - Quais arquivos são carregados no projeto?
>    - Quais colunas principais existem nos dados brutos?
>    - Quais tratamentos iniciais são aplicados (limpeza, conversão, filtros)?
>    - Quais dados são descartados e por quê?
>    - Como a variável alvo “atrasado” é definida?
>    - Quais limitações já existem nos dados antes da modelagem?
---

### 🔖 Entregáveis
  * Documento explicativo 
  * Texto bem organizado
  * Linguagem simples
  * Tudo deve ser rastreável ao notebook
---

## 🧩 DS2 – Documentação EDA

### Objetivo da frente

O objetivo desta frente é documentar o processo de análise exploratória dos dados, explicando como os dados se comportam antes da modelagem e quais padrões, tendências ou problemas puderam ser identificados a partir dessa análise. A documentação deve mostrar que a EDA não foi realizada de forma automática ou superficial, mas sim como uma etapa fundamental para entender o dataset, avaliar sua qualidade e orientar decisões técnicas posteriores.

Essa seção deve ajudar o leitor a compreender quais características dos dados são mais relevantes para o problema proposto, se existe desbalanceamento entre classes, se há padrões temporais ou estruturais importantes e quais limitações foram identificadas nessa fase. O objetivo final é demonstrar que as decisões tomadas no pipeline não foram arbitrárias, mas baseadas em observações concretas obtidas durante a exploração dos dados.

---

### Tarefas

  * Ler todas as células de EDA do notebook
  * Entender o propósito de cada análise realizada
  * Identificar padrões relevantes
  * Relacionar insights com decisões do pipeline
---

### Pergunta-chave
>   - Qual era o objetivo da EDA neste projeto?
>   - Como está distribuída a variável alvo?
>   - Existe desbalanceamento entre as classes?
>   - Quais variáveis parecem mais relevantes?
>   - Existem padrões temporais importantes?
>   - Algum comportamento inesperado foi identificado?
>   - Como a EDA influenciou feature engineering ou modelagem?
>   - Quais limitações foram identificadas na fase exploratória?

---
### 🔖 Entregáveis
  * Documento explicativo 
  * Texto bem organizado
  * Linguagem simples
  * Tudo deve ser rastreável ao notebook
---


## ⚖️ DS3 – Documentação Feature Engineering

### Objetivo da frente

O objetivo desta frente é explicar, de maneira detalhada e conceitualmente clara, como os dados brutos foram transformados em variáveis adequadas para treinamento do modelo de Machine Learning. Essa documentação deve deixar evidente que o feature engineering não consiste apenas em criar novas colunas, mas em um processo estruturado de transformação, seleção e organização das informações relevantes presentes nos dados originais.

Nesta frente, espera-se que o integrante demonstre entendimento sobre por que determinadas transformações foram necessárias para permitir que o modelo capture padrões temporais, categóricos e estatísticos do problema estudado. A documentação deve explicar como variáveis relacionadas a tempo, categorias e estatísticas agregadas foram construídas, qual o papel de cada grupo de features dentro do pipeline e como essas transformações contribuem para melhorar a capacidade preditiva do modelo.

Além disso, esta seção deve evidenciar a preocupação com boas práticas de Data Science, como a prevenção de data leakage e a manutenção de um pipeline reproduzível, no qual todas as transformações são aplicadas de forma consistente tanto nos dados de treino quanto nos dados de inferência. O foco não está em detalhar código, mas em mostrar compreensão do raciocínio técnico por trás das transformações realizadas e reconhecer as limitações do conjunto de features atual.

---

### Tarefas

  * Ler todas as células de transformação de dados
  * Identificar cada grupo de features criadas
  * Entender o papel de cada transformação
  * Identificar estratégias de prevenção de data leakage
---

### Pergunta-chave
>   - Quais colunas entram no pipeline como dados brutos?
>   - Quais transformações temporais são aplicadas?
>   - Como variáveis categóricas são tratadas?
>   - Existem features agregadas? Com base em quê?
>   - Como o pipeline evita vazamento de informação?
>   - Alguma feature foi descartada? Por quê?
>   - Quais limitações ainda existem nas features?
---

### 🔖 Entregáveis
  * Documento explicativo 
  * Texto bem organizado
  * Linguagem simples
  * Tudo deve ser rastreável ao notebook
---

## 🧪 DS4 – Documentação Modelagem e Avaliação do Modelo

### Objetivo da frente

O objetivo desta frente é documentar o processo de treinamento e avaliação do modelo de Machine Learning de forma acessível, coerente e alinhada ao contexto do problema. A documentação deve permitir que um leitor sem formação aprofundada em Machine Learning compreenda qual tipo de problema está sendo resolvido, como o modelo foi treinado e de que forma seu desempenho foi avaliado.

Essa frente deve explicar as escolhas realizadas em relação ao tipo de modelo, à estratégia de divisão dos dados e às métricas de avaliação utilizadas, sempre relacionando essas decisões ao objetivo do projeto. Também é fundamental que a documentação apresente uma interpretação clara dos resultados obtidos, destacando tanto os pontos fortes quanto as limitações do modelo, demonstrando consciência crítica sobre sua aplicabilidade em um cenário real.

---

### Tarefas

  * Ler as células de treino e validação
  * Identificar modelo, métricas e estratégia de split
  * Interpretar resultados obtidos

### Pergunta-chave
>   - Qual é o tipo de problema resolvido?
>   - Qual modelo foi escolhido?
>   - Como os dados foram divididos?
>   - Por que essa estratégia de divisão foi usada?
>   - Quais métricas foram escolhidas?
>   - O que os resultados indicam?
>   - Quais são as principais limitações do modelo?

---

### 🔖 Entregáveis
  * Documento explicativo 
  * Texto bem organizado
  * Linguagem simples
  * Tudo deve ser rastreável ao notebook
---

## 🧪 DS5 – Documentação Pipeline e Script

### Objetivo da frente

O objetivo desta frente é documentar a estrutura lógica do projeto de Data Science como um todo, explicando o papel do script Python no suporte ao pipeline construído no notebook e sua importância para a organização, reutilização e manutenção do código. Essa documentação deve mostrar que o projeto não se limita a um notebook isolado, mas que foi estruturado de forma modular, separando responsabilidades e centralizando funções críticas em um arquivo específico.

Nesta frente, o integrante deve explicar como o script Python agrupa funcionalidades relacionadas à ingestão de dados, feature engineering, divisão de dados, treinamento de modelos e explicabilidade, e como essas funções são utilizadas ao longo do notebook. O objetivo não é descrever cada função linha a linha, mas fornecer uma visão arquitetural que ajude o leitor a entender como o pipeline foi pensado como um sistema integrado.

Além disso, esta documentação deve destacar como essa separação contribui para reprodutibilidade, clareza do projeto e futura integração com a API, bem como reconhecer as limitações atuais dessa arquitetura e possíveis caminhos de evolução. Essa frente é fundamental para demonstrar maturidade técnica e organização do projeto aos avaliadores.

---

### Tarefas

  * Ler o script Python inteiro
  * Identificar os principais blocos funcionais
  * Relacionar cada bloco com etapas do notebook
  * Entender como o pipeline é reutilizável

---


### Pergunta-chave
>   - Qual é o papel do script Python no projeto?
>   - Por que separar lógica em um script externo?
>   - Quais tipos de funções o script centraliza?
>   - Como o script ajuda na organização do pipeline?
>   - Como ele contribui para reprodutibilidade?
>   - Como o notebook utiliza esse script?
>   - O que o script não faz (limitações)?
>   - O que poderia ser expandido no futuro?
---

### 🔖 Entregáveis
  * Documento explicativo 
  * Texto bem organizado
  * Linguagem simples
  * Tudo deve ser rastreável ao notebook
---
## ℹ️ Observação 
Reuniões adicionais poderão ser marcadas ao longo da semana conforme a necessidade,
especialmente para alinhamentos técnicos ou validações de integração.
