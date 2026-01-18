# 02 — Dataset (ANAC/VRA) e Preparação

## 1. Fonte de Dados

O dataset utilizado para o treinamento do modelo preditivo do **[FlightOnTime](https://github.com/LaboraDev/hackathon_one_flightOnTime/tree/main)** foi construído a partir do **VRA (Voos Regulares Ativos)**, base oficial disponibilizada pela **[ANAC](https://www.gov.br/anac/pt-br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/voo-regular-ativo-vra) (Agência Nacional de Aviação Civil Brasileira)**, contemplando o período de **janeiro/2021 até dezembro/2024**. A escolha por uma fonte institucional e padronizada garante maior confiabilidade e consistência dos dados, além de permitir que as análises reflitam com precisão o comportamento real das operações aéreas no Brasil.

Por se tratar de um conjunto de informações originado diretamente de registros regulatórios, o VRA oferece rastreabilidade completa das operações, cobrindo variáveis essenciais como identificação do voo, aeroportos de origem e destino, companhias aéreas e características operacionais relevantes para a previsão de atrasos. Isso permite que o modelo seja treinado com base em um cenário aderente ao ambiente produtivo, reduzindo vieses de amostras artificiais e aumentando o potencial de generalização das previsões.

Além disso, a amplitude temporal da base, que abrange múltiplos anos e diferentes contextos contribui para capturar sazonalidades, padrões de demanda e variações do setor, fortalecendo a robustez estatística do treinamento. Como resultado, o uso do VRA como fonte de dados proporciona uma base sólida para a construção de um modelo com aplicação prática e alinhamento direto às necessidades do monitoramento operacional e tomada de decisão no transporte aéreo brasileiro.

---

## 2. Estrutura do Dataset

O dataset original foi composto por colunas operacionais e de registro de eventos do voo, incluindo:

- Identificação da empresa aérea
- Identificação do voo e tipo de linha
- Aeródromo de origem e destino
- Partida e chegada prevista
- Partida e chegada real
- Situação do voo e justificativas de ocorrência

A padronização e consistência de nomes foram tratadas no [pipeline](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb).

---

## 3. Higienização e Qualidade dos Dados

Uma etapa essencial do projeto foi garantir que apenas registros válidos fossem utilizados na criação do target[In[6]](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana_05/Consolidado_S03_splitTemporal.ipynb) e no treinamento do modelo.

### Flags de qualidade

Foram criadas flags para classificação de registros inconsistentes:

- `flag_partida_prevista_ausente`
- `flag_partida_real_ausente`
- `flag_data_fora_periodo`

Estas flags possuem um papel fundamental tanto do ponto de vista operacional quanto de auditoria e governança de dados, pois permitem identificar de forma objetiva e padronizada os registros que apresentam inconsistências ou ausência de informações críticas. Ao invés de simplesmente descartar linhas “problemáticas” de maneira silenciosa, a classificação por flags garante rastreabilidade completa sobre cada decisão de tratamento, viabilizando análises posteriores e validações com maior transparência.

Além disso, essa abordagem facilita o monitoramento contínuo da qualidade do dataset, possibilitando mensurar a frequência de cada tipo de inconsistência, entender padrões recorrentes e apoiar ações corretivas na origem dos dados. Como consequência, o processo de limpeza se torna mais confiável e reprodutível, reduzindo riscos de vieses no treinamento e aumentando a credibilidade do pipeline de preparação de dados utilizado no FlyOnTime.

---

## 4. Definição da Variável Target (Atraso)

O problema foi modelado como uma tarefa de **classificação binária**, onde o objetivo do modelo é identificar se um voo deve ser considerado **pontual** ou **atrasado** a partir das informações operacionais disponíveis antes da execução do voo.

A variável target foi definida como:

- **`atrasado ∈ {0, 1}`**

### Critério internacional de pontualidade (regra dos 15 minutos)

Para alinhar o FlyOnTime a práticas amplamente utilizadas na indústria da aviação, foi adotada a definição operacional baseada no conceito de **[On-Time Performance (OTP)](https://www.cirium.com/resources/on-time-performance/on-time-performance-faq/)**, em que um voo é considerado **pontual** quando a diferença entre o horário real de partida e o horário programado permanece dentro de uma janela de tolerância de até **15 minutos**.

De forma prática, o atraso é reconhecido apenas quando a operação ultrapassa esse limite. Isso reflete o entendimento de que **pequenos desvios** (por exemplo, variações de alguns minutos) são inerentes à operação aérea e podem ocorrer por fatores normais como fluxo de embarque, ajustes de solo, ocupação de gate, pushback e pequenas variações de tráfego, sendo tratados como **variações operacionais aceitáveis** e não como impacto relevante ao passageiro ou à performance operacional.

Esse critério é amplamente reportado em rankings e métricas do setor, nos quais um voo é considerado “on-time” quando **parte ou chega dentro de 15 minutos do horário programado**.

### Regra de definição do target

- `atrasado = 1` **se** o horário de partida real exceder o horário de partida previsto em **mais de 15 minutos**
- `atrasado = 0` **caso contrário** (voo tratado como pontual dentro da tolerância operacional)

---

### Regra de definição do target

A variável target foi definida a partir do **atraso de partida em minutos** e posteriormente convertida para uma classificação binária (`0` ou `1`), permitindo o enquadramento do problema como **classificação supervisionada**.

#### 1 Cálculo do atraso de partida (em minutos)

O atraso de partida é calculado por:

- `atraso_partida_min = partida_real - partida_prevista` (em minutos)

onde:

- `partida_prevista`: horário programado de partida (agendado)
- `partida_real`: horário efetivo de partida (real)

#### 2 Classificação binária do atraso (target final)

Com base no valor calculado em `atraso_partida_min`, o target final foi definido como:

- `atrasado = 1` **se** `atraso_partida_min > 15` (**voo classificado como atrasado**)
- `atrasado = 0` **se** `atraso_partida_min <= 15` (**voo classificado como pontual**, dentro da tolerância operacional)

Essa transformação garante consistência no treinamento do modelo, reduzindo ruídos causados por pequenas variações operacionais e focando apenas em atrasos efetivamente relevantes do ponto de vista de performance.

---

## 5. Dataset Pré-processado

Após o processamento inicial, o dataset pré-processado resultou em:

- **3.968.417 linhas**
- **17 colunas**

Esse dataset é a base para a etapa de engenharia de variáveis, modelagem e validação temporal.

---

## 6. Considerações de Governança

O dataset do **[FlightOnTime](https://github.com/LaboraDev/hackathon_one_flightOnTime/tree/main)** foi construído com foco em **governança, confiabilidade e conformidade**, assegurando que todo o [pipeline](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb) de dados e modelagem permaneça rastreável, consistente e apropriado para uso em um contexto real de operação aérea.

### Dados públicos e conformidade com a LGPD

O dataset é composto exclusivamente por **metadados operacionais** de aeronaves, voos e aeroportos extraídos de fontes públicas oficiais, não havendo, em nenhum momento, coleta, armazenamento ou processamento de dados pessoais de passageiros. Dessa forma, o projeto mantém alinhamento com os princípios de privacidade e segurança da informação, garantindo conformidade com a Lei Geral de Proteção de Dados ([LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)).

### Princípios adotados no pipeline de dados

A estrutura do dataset e as regras de tratamento foram projetadas para garantir:

- **Reprodutibilidade**: a aplicação das mesmas regras e parâmetros gera consistentemente o mesmo dataset final, permitindo replicação completa do processo de preparação.
- **Auditabilidade**: todas as etapas de limpeza, criação do target e remoção de inconsistências são explicitamente definidas e rastreáveis, facilitando validações e revisões técnicas.
- **Robustez operacional**: foram implementadas validações e flags de qualidade para impedir que o modelo seja treinado ou execute inferências com registros incompletos, inválidos ou fora do padrão esperado.

Por fim, recomenda-se que qualquer evolução futura do projeto preserve esse padrão de rastreabilidade e controle, assegurando a integridade do processo de treinamento e a confiabilidade das previsões geradas em produção.
