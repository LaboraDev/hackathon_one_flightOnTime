# 📘 Semana 03 — Aprimoramento e Robustez do Modelo

Após a construção do pipeline inicial, do modelo baseline e da integração com a API, a Semana 3 será dedicada a evoluir o modelo e o pipeline de forma organizada, consistente e reproduzível. Nesta etapa, começamos a tratar o pipeline como um componente central do projeto, responsável por garantir que todo o processo, do pré-processamento à predição, funcione corretamente quando aplicado a dados novos.

O objetivo desta semana não é apenas melhorar métricas, mas assegurar que qualquer avanço realizado, seja na escolha do modelo, na criação de features ou na forma de avaliar o desempenho, esteja corretamente integrado ao pipeline. Isso é essencial porque o modelo será utilizado em um cenário próximo ao de produção, sendo acessado por meio da API e recebendo informações que não passaram por tratamentos manuais.

> **Regra fundamental:**  
> A partir desta semana, **toda transformação utilizada pelo modelo deve estar dentro do pipeline**.  
> Transformações feitas diretamente no dataframe devem ser usadas **apenas para análise**, nunca para treino ou predição.

Todas as frentes devem partir do **Notebook Consolidado da Semana 2**, reutilizando o pipeline existente e implementando ajustes **exclusivamente por meio de funções, transformers ou novas etapas no pipeline**.

---

## 🛠️ DS1 — Modelos Candidatos (Evolução do Baseline)
**Responsável:** Ana Raquel 

### Objetivo
O objetivo desta frente é verificar se a escolha do algoritmo influencia significativamente o desempenho do modelo, partindo exatamente do mesmo conjunto de dados e do mesmo pré-processamento definido na semana anterior. Em outras palavras, queremos entender se o resultado atual é limitado pelo tipo de modelo utilizado ou se o gargalo está em outras partes do pipeline.

O foco não é criar novas features, alterar os dados ou ajustar parâmetros finos dos modelos, mas sim comparar diferentes algoritmos de forma justa. Para isso, todos os modelos devem receber os dados da mesma forma, garantindo que qualquer diferença de desempenho observada esteja relacionada apenas ao algoritmo escolhido.

O pipeline deve ser mantido inalterado, com exceção do estimador final. Ao final desta frente, esperamos identificar se modelos mais robustos conseguem trazer ganhos reais em relação ao baseline atual ou se a melhoria do desempenho depende principalmente de outras estratégias, como aprimoramento de features ou validação.

### Tarefas
- Substituir o modelo atual por pelo menos **três modelos de classificação mais robustos**, como:
  - Árvores de decisão
  - KNN
  - SVM
  - Random Forest
- Treinar todos os modelos utilizando o **mesmo conjunto de features**
- Avaliar métricas básicas:
  - Acurácia
  - Precisão
  - Sensibilidade (Recall)
  - F1-Score
- Comparar os resultados com o baseline atual

### Pergunta-chave
> **Qual modelo apresenta o melhor ganho real em relação ao baseline atual?**

### 🔖 Entregáveis
- Notebook(s) com os testes dos modelos (pode ser um notebook por modelo)
- Pipeline completo com os modelos integrados
- Script `.py` com a definição do pipeline e funções auxiliares (complemente o arquivo da Semana 2, se for o caso)
- Comparação objetiva das métricas entre os modelos testados

---

## 🧩 DS2 – Validação e Métricas do Modelo 
**Responsável:** Enoque  

### Objetivo
O objetivo desta frente é verificar se o desempenho que estamos observando no modelo representa, de fato, o comportamento que ele terá quando estiver em uso real. Como estamos trabalhando com dados de voos ao longo do tempo (2021-2024), é importante lembrar que o modelo será treinado com dados do passado e utilizado para prever situações atuais. 

O foco não é melhorar o modelo ou criar novas features, mas entender se a forma como estamos separando os dados para treino e teste influencia diretamente os resultados obtidos. Em outras palavras, queremos responder se o modelo está aprendendo padrões reais ou se está apenas se beneficiando da forma como os dados foram divididos. 

Para isso, esta frente irá comparar diferentes estratégias de divisão dos dados, como a divisão estratificada (que mantém a proporção das classes entre treino e teste) e a divisão temporal (que separa os dados respeitando a ordem do tempo, treinando com dados mais antigos e testando com dados mais recentes). A partir dessa comparação, o objetivo é avaliar como o desempenho do modelo se comporta em cada cenário e definir qual estratégia de avaliação faz mais sentido para representar o uso real do modelo nas próximas etapas do projeto

### Tarefas
- Implementar os dois tipos de split
  - Split estratificado 
  - Split temporal:
- Calcular métricas para ambos os cenários
- Comparar diferenças de desempenho
- Definir qual divisão deve ser priorizada no projeto

### Pergunta-chave
> **O modelo mantém desempenho consistente em dados mais recentes ou o resultado depende do tipo de split utilizado?**

### 🔖 Entregáveis
- Notebook com comparação clara entre os tipos de validação (pode ser um notebook para cada split)
- Script `.py` com funções de avaliação
- Recomendação da melhor estratégia de validação e métrica

---

## ⚖️ DS3 – Aprimoramento de Features (Geração de Sinal) 
**Responsável:** Amélia  

### Objetivo
O objetivo desta frente é aumentar a capacidade do modelo de identificar padrões relevantes por meio da criação de novas features, utilizando os aprendizados obtidos na análise exploratória dos dados. Nesta etapa, buscamos explorar diferentes formas de representar as informações disponíveis, ajudando o modelo a capturar relações que não são evidentes nas variáveis originais.

As novas features podem ser simples ou mais elaboradas, desde que façam sentido do ponto de vista do problema e agreguem informação útil ao modelo. O ponto central desta frente é avaliar se as transformações propostas adicionam sinal real ao processo de predição, contribuindo para uma melhor separação entre os casos.

É fundamental que todas as features criadas sejam implementadas de forma consistente e reprodutível, integrando o pipeline, para garantir que o mesmo conjunto de transformações seja aplicado tanto durante o treino quanto na predição. Ao final desta etapa, esperamos identificar quais features realmente contribuem para melhorar o desempenho do modelo e quais podem ser descartadas

### Tarefas
-	Criar novas features dentro do pipeline, como por exemplo:
    - o	encoding cíclico para variáveis temporais
    - o	agrupamento de categorias pouco frequentes;
    - o	contagens de voos por companhia ou aeroporto;
    - o	agrupar os aeroportos por regiões;
-	Garantir que nenhuma feature seja criada manualmente no dataframe
-	Comparar métricas antes vs depois da inclusão das novas features

### Pergunta-chave
> **Quais novas features melhoram o desempenho do modelo sem comprometer a reprodutibilidade do pipeline?**

### 🔖 Entregáveis
- Notebook atualizado com as novas features testadas
- Pipeline completo com as features integradas
- Script `.py` com funções ou transformers criados
- Comparação objetiva de métricas

---

## 🧪 DS4 – Consolidação Técnica e Estabilidade da API 
**Responsável:** Helena  

### Objetivo
O objetivo desta frente é reunir e integrar as melhorias desenvolvidas pelas demais frentes, garantindo que o pipeline final funcione de forma estável e consistente quando utilizado pela API. Nesta etapa, o foco é verificar se todas as alterações realizadas ao longo da semana estão corretamente incorporadas ao fluxo completo, desde o pré-processamento até a predição.

Além de consolidar o pipeline, esta frente é responsável por assegurar que o modelo esteja devidamente serializado e que a API continue operando conforme o esperado, mesmo após as atualizações. O objetivo é manter o projeto organizado, reproduzível e tecnicamente coerente, preparando a base para as próximas etapas, como ajustes finos, análise de resultados e apresentação final.

### Tarefas
- Integrar o modelo escolhido (DS1) e as features aprovadas (DS3)
-	Atualizar e serializar o pipeline final (.pkl)
-	Testar a API com o pipeline atualizado
-	Garantir compatibilidade com o contrato JSON
-	Atualizar o README com:
  - o	modelo atual
  - o	features utilizadas
  - o	métrica principal
  - o	limitações conhecidas

### Pergunta-chave
> **O pipeline atualizado está estável, reproduzível e pronto para avançar sem retrabalho?**

### 🔖 Entregáveis
- Pipeline final serializado
- API funcionando com o pipeline atualizado
- README atualizado e padronizado

---

## 📅 Cronograma da Semana 3 — Datas Importantes

### 🗓️ Segunda-feira — 29/12
**Reunião de planejamento**
- Alinhamento das responsabilidades
- Dúvidas técnicas
- Checklist de arquivos
- Ajustes no cronograma

### 🗓️ Quinta-feira — 01/01
**Demonstração das entregas**
- DS1: apresenta a comparação de modelos
- DS2: mostra validação dos dados (estratificado vs temporal)
- DS3: fala sobre os impactos das novas features

### 🗓️ Sexta-feira — 26/12
**Consolidação final**
- Escolha de:
  - 1 modelo
  - 1 estratégia de validação
  - 1 conjunto final de features
- Congelamento do pipeline v2
- Documentação das decisões

---

## ℹ️ Observação Final
Planejei apenas as reuniões obrigatórias da semana, mas poderemos marcar encontros adicionais conforme necessidade da equipe, especialmente para revisar passos técnicos mais complexos. Estou a disposição de vocês.
