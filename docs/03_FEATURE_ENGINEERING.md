# 03 — Engenharia de Variáveis 

## 1. Objetivo

## 1. Objetivo

O **Feature Engineering** do FlyOnTime foi estruturado com o objetivo de transformar dados operacionais brutos em variáveis com maior poder explicativo e capacidade preditiva, permitindo que o modelo identifique padrões reais associados ao risco de atraso. Essa etapa é fundamental para garantir que a predição seja baseada em sinais consistentes do ponto de vista estatístico e relevantes do ponto de vista operacional, refletindo com fidelidade a dinâmica do transporte aéreo. Todas as Feature Engineering estão disponíveis no [pipeline](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)

A estratégia de engenharia de variáveis foi desenhada para maximizar a **capacidade preditiva** e a **estabilidade temporal**, reduzindo sensibilidade a ruídos e flutuações pontuais. Para isso, as features foram construídas priorizando sinais que permanecem úteis ao longo do tempo e que fazem sentido em cenários reais de uso, como padrões de demanda ao longo do dia, sazonalidade, recorrência de atrasos por empresa e efeitos estruturais relacionados a aeroportos com maior complexidade operacional.

Em termos práticos, o conjunto de features foi desenvolvido para capturar os seguintes eixos de informação:

- **Sazonalidade e padrões temporais**, incorporando variações por dia da semana, mês, período do ano e horários com maior probabilidade de congestionamento operacional. [In[42-44](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)]
- **Comportamento histórico por companhia e aeroportos**, refletindo tendências recorrentes de performance e fatores associados à execução da malha aérea.[In[45](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)
- **Efeitos cíclicos associados ao horário**, considerando que determinadas faixas horárias tendem a concentrar maior volume de operações, conexões e atrasos encadeados.[In[40](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)
- **Características estruturais de hubs**, representando a complexidade operacional em aeroportos de grande movimentação e maior probabilidade de dependências logísticas.[In[56](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)

Além disso, o design das features seguiu princípios corporativos essenciais para garantir uso seguro e sustentável em produção:

- **Simplicidade**: variáveis interpretáveis e consistentes, facilitando validação, manutenção e comunicação com áreas de negócio.
- **Robustez**: features capazes de generalizar para novos períodos e suportar categorias inéditas (ex.: novos aeroportos ou companhias), reduzindo risco de falhas operacionais.
- **Controle de leakage**: todas as features foram construídas exclusivamente com informações disponíveis até o momento da partida planejada, garantindo que o modelo não utilize dados futuros ou impossíveis de serem conhecidos no instante da predição.

Como resultado, o Feature Engineering do FlyOnTime atua como um componente central para a confiabilidade do modelo, elevando a qualidade do aprendizado supervisionado e garantindo que as previsões possam ser utilizadas de forma consistente em cenários reais de tomada de decisão.

---

## 2. Features Temporais

As features temporais são derivadas a partir do campo `partida_prevista` e representam padrões determinísticos do calendário operacional. Como:

- `hora_dia`: hora programada da partida (0–23)
- `dia_semana`: dia da semana conforme padrão do pandas (`0=segunda ... 6=domingo`)
- `mes_ano`: mês do ano (`1–12`)
- `periodo_dia`: faixa categórica definida a partir de `hora_dia`(`Manha`, `Tarde`, `Noite`, `Madrugada`)
- `fim_de_semana`: flag binária indicando dias de maior perfil de lazer e mudanças de demanda  (`1` para **sexta, sábado e domingo** → `dia_semana ∈ {4, 5, 6}`)
- `alta_temporada`: flag binária indicando meses com maior pressão operacional e sazonalidade de demanda  (`1` para **julho e dezembro** → `mes_ano ∈ {7, 12}`)

---

### Justificativa

O desempenho e a pontualidade de uma operação aérea são altamente influenciados por fatores temporais, uma vez que a malha aérea apresenta padrões bem definidos de funcionamento ao longo do dia, da semana e do ano. Dessa forma, a inclusão de variáveis baseadas no horário programado de partida permite que o modelo capture tendências estruturais que impactam diretamente o risco de atraso, sem depender de dados futuros ou difíceis de obter em tempo real.

Entre os principais aspectos representados por essas features, destacam-se:

- **Padrões semanais de demanda**, onde dias úteis e finais de semana tendem a apresentar perfis distintos de volume, ocupação e disponibilidade operacional.
- **Picos sazonais e períodos de alta movimentação**, especialmente em meses associados a férias e feriados prolongados, nos quais há maior probabilidade de congestionamento em aeroportos e aumento da complexidade logística.
- **Janelas operacionais por horário**, considerando que determinados períodos do dia concentram conexões, maior densidade de tráfego aéreo e disputas por infraestrutura (gates, pistas e turnaround), elevando a chance de atrasos encadeados.

Além de agregarem poder preditivo, essas features possuem alto valor de engenharia por serem determinísticas, leves e altamente reprodutíveis, o que garante consistência em produção, facilidade de auditoria e baixa probabilidade de falhas durante o processo de inferência.

---

## 3. Features Históricas (Delay Priors)

Para capturar comportamento histórico, foram criadas médias por categoria:

- `media_atraso_empresa`
- `media_atraso_origem`
- `media_atraso_destino`

### Estratégia de Treino e Produção

As métricas agregadas utilizadas como features (ex.: médias históricas de atraso por companhia e aeroportos[In[46 e 50](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)) são calculadas exclusivamente a partir do conjunto de treino e posteriormente reaplicadas nos conjuntos de validação, teste e no ambiente de produção. Essa abordagem garante consistência metodológica e evita que o modelo tenha acesso indireto a informações do futuro durante o treinamento, preservando a integridade do processo de modelagem.

Como essas features dependem de chaves categóricas (por exemplo, `empresa_aerea`, `aerodromo_origem` e `aerodromo_destino`), é esperado que em produção ocorram cenários onde uma categoria não tenha sido observada anteriormente no conjunto de treino, como:

- novos aeroportos incluídos na malha operacional
- companhias aéreas recém-operantes ou com baixa frequência histórica
- rotas raras ou pouco representadas nos dados de treinamento

Para garantir robustez operacional, quando uma categoria não existe no mapeamento aprendido durante o `fit`, é aplicado automaticamente um **fallback para uma média global segura**, calculada a partir do próprio conjunto de treino. Dessa forma, o pipeline evita falhas por ausência de chaves, mantém o comportamento determinístico das features e assegura que o modelo continue produzindo previsões confiáveis mesmo em condições não vistas anteriormente.

Essa estratégia reduz significativamente o risco de erro em inferência, aumenta a resiliência do sistema em produção e contribui para uma operação mais estável e auditável ao longo do tempo.

---

## 4. Representação Cíclica do Horário

O horário de partida (`hora_dia`) é uma variável naturalmente periódica, pois representa um ciclo que se repete a cada 24 horas. Em termos de modelagem, isso significa que horários próximos ao “fim do dia” e ao “início do dia” são, na prática, vizinhos operacionais (por exemplo, **23:00** e **00:00**), embora numericamente pareçam distantes quando representados apenas como um valor inteiro.

Se utilizarmos apenas a variável linear `hora_dia` (0 a 23), o modelo pode interpretar incorretamente que existe uma grande distância entre 23 e 0, o que introduz uma descontinuidade artificial. Esse efeito pode reduzir a capacidade do modelo de capturar padrões operacionais reais que ocorrem em faixas específicas do dia, como picos de tráfego, restrições de slot, acúmulo de atrasos e efeitos de rotatividade de aeronaves.

Para corrigir essa limitação e representar corretamente a natureza circular do tempo, foi implementada uma **codificação cíclica** baseada em transformações trigonométricas, convertendo o horário para um espaço contínuo no plano (circunferência).[In[38-40](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana01/S01_Consolidado_ETL_EDA.ipynb)

Dessa forma, foram criadas as seguintes features:

- `hora_sin`
- `hora_cos`

com a definição:

- `hora_sin = sin(2π * hora_dia / 24)`
- `hora_cos = cos(2π * hora_dia / 24)`

---

### Benefício

A representação cíclica permite que o modelo interprete corretamente relações de proximidade temporal, garantindo que horários como **23h e 0h** sejam tratados como pontos adjacentes no ciclo diário. Esse recurso é especialmente relevante para capturar fenômenos típicos da aviação, como:

- **congestionamento em ondas de partida/chegada** (banking de voos)
- **efeitos de atraso encadeado** ao longo do dia (propagação operacional)
- **janelas de pico e vale** de movimentação nos aeroportos
- **comportamentos não-lineares** por faixa horária, difíceis de capturar com codificação linear simples

Além de aumentar o poder preditivo, essa abordagem reduz distorções que podem ocorrer em modelos que não lidam bem com variáveis periódicas, especialmente quando a hora é tratada como um número absoluto em vez de um ciclo.

Em resumo, as variáveis `hora_sin` e `hora_cos` introduzem um componente de modelagem mais sofisticado e consistente com a realidade operacional, sendo um diferencial técnico relevante do FlyOnTime ao melhorar a capacidade do modelo de aprender padrões temporais de forma mais estável e generalizável.

---

## 5. Feature de Hub Operacional

Foi criada a feature binária:

- `is_hub` [In[9](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana03/Consolidado_S03_splitTemporal.ipynb)

Essa variável indica se o voo está associado a um **aeroporto estrategicamente relevante (hub)**, considerando tanto o aeroporto de origem quanto o de destino. Na prática, essa feature captura um sinal estrutural importante da malha aérea: operações envolvendo hubs tendem a apresentar dinâmica operacional distinta quando comparadas a aeroportos regionais ou de baixa densidade.

### Regra de definição

A flag é definida como:

- `is_hub = 1` se `aerodromo_origem` **ou** `aerodromo_destino` pertencer ao conjunto de hubs configurados
- `is_hub = 0` caso contrário

No pipeline atual, o conjunto de hubs nacionais considerados é:

| Aeroporto | ICAO | IATA |
|----------|------|------|
| Guarulhos – Governador André Franco Montoro International Airport | SBGR | GRU |
| Rio Galeão – Tom Jobim International Airport | SBGL | GIG |
| Congonhas Airport | SBSP | CGH |
| Santos Dumont Airport | SBRJ | SDU |
| Viracopos International Airport | SBKP | VCP |
| Tancredo Neves International Airport | SBCF | CNF |
---

### Justificativa

A inclusão da feature `is_hub` é relevante porque aeroportos com maior densidade de operação apresentam padrões de atraso significativamente diferentes, influenciados por fatores como:

- **alto volume de movimentos simultâneos**, aumentando disputa por pista, taxiways e gates
- **maior concentração de conexões (voos alimentadores e distribuidores)**, elevando impacto de atrasos encadeados
- **congestionamento operacional mais frequente**, especialmente em horários de pico
- **complexidade logística superior**, incluindo turnaround mais sensível, dependência de slot e maior pressão por cumprimento de janela operacional

Dessa forma, a flag `is_hub` atua como um reforço estrutural ao modelo, permitindo capturar diferenças sistêmicas que não são totalmente explicadas apenas por variáveis temporais ou pela identificação individual do aeroporto. Como resultado, essa feature contribui para aumentar a capacidade de generalização do modelo, especialmente em rotas que envolvem os principais centros operacionais da aviação nacional.

---

## 6. Proteção contra Leakage e Colunas Não Elegíveis

Para garantir que o FlyOnTime opere de forma **confiável em produção** e mantenha integridade metodológica no treinamento, foi implementada uma etapa explícita de **proteção contra data leakage** e exclusão de colunas **não elegíveis para inferência**.[In[12](https://github.com/LaboraDev/hackathon_one_flightOnTime/blob/main/notebooks/semana_05/Consolidado_S03_splitTemporal.ipynb)

Em projetos de Machine Learning aplicados a cenários operacionais, é comum que o dataset histórico contenha variáveis que, apesar de úteis para análise retrospectiva, não estão disponíveis no momento da predição (antes do voo acontecer) ou carregam informações que introduzem vazamento indireto do target. Caso essas colunas sejam utilizadas no treinamento, o modelo pode aparentar alta performance offline, mas apresentará degradação significativa quando implantado, pois estará aprendendo padrões impossíveis de serem reproduzidos em tempo real.

Dessa forma, o pipeline remove sistematicamente variáveis que:

- **não existem no instante da inferência**, como campos baseados em execução real da operação (ex.: datas reais, horários efetivos, status pós-evento)
- **possuem correlação direta com o target**, incluindo atributos calculados a partir do atraso real ou derivados de informações posteriores
- **não pertencem ao conjunto de entrada do usuário final**, ou seja, campos técnicos e auxiliares utilizados apenas para engenharia interna, auditoria, validação e rastreabilidade
- **podem sofrer inconsistência ou indisponibilidade em produção**, afetando estabilidade do serviço ou exigindo dependências externas não garantidas

### Benefícios operacionais

A aplicação desse controle reduz o risco de discrepância entre treino e produção, fortalecendo a robustez do sistema e garantindo que:

- as previsões sejam geradas com base em informações realmente disponíveis no momento correto
- o modelo mantenha comportamento estável e auditável em diferentes períodos de operação
- a performance obtida em validação represente melhor o desempenho real esperado em produção
- a solução seja mais resiliente a mudanças no pipeline, no preenchimento dos dados e em variações de origem do input

Em resumo, essa etapa atua como um mecanismo essencial de **governança de dados e confiabilidade de inferência**, reduzindo riscos de overfitting indireto e garantindo que o FlyOnTime seja sustentável como produto preditivo em ambiente real.


