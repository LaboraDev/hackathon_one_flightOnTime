# Organização da Semana 4  
Dashboard, Explicabilidade e Robustez da Aplicação

Após a construção do pipeline inicial, do modelo baseline e da integração da API de
predição, a Semana 4 será dedicada a transformar a predição em um produto analítico
compreensível para o usuário final.

Nesta etapa, o foco não está em melhorar métricas ou alterar o modelo, mas em
assegurar que o resultado da predição seja apresentado de forma clara, contextualizada
e interpretável. O objetivo é permitir que o usuário não apenas receba a resposta
“atrasado” ou “no prazo”, mas também compreenda os principais fatores que influenciaram
essa decisão e como ela se relaciona com o comportamento histórico de voos semelhantes.

A aplicação passa a ser tratada como um produto analítico completo, composto por
predição, explicabilidade e visualização de dados. Todas as frentes devem trabalhar de
forma integrada, respeitando o contrato da API já existente e reutilizando o dataset
histórico utilizado nas etapas anteriores.

---

## DS1 – Dados Analíticos para o Dashboard | Pessoa A

### Objetivo da frente

O objetivo desta frente é preparar os dados históricos que serão utilizados nos gráficos
do dashboard. Esses dados têm a função de contextualizar a previsão realizada pelo
modelo, mostrando como companhias aéreas, aeroportos e períodos do tempo costumam
se comportar em relação a atrasos.

O foco não é realizar análises exploratórias aprofundadas, mas sim gerar agregações
simples, claras e reutilizáveis, que possam ser consumidas diretamente pelo front-end
sem a necessidade de cálculos adicionais.

---

### Tarefas

• Abrir o dataset histórico de voos e identificar as colunas necessárias para a análise
  (companhia aérea, aeroporto de origem, aeroporto de destino, data/hora do voo e
  informação de atraso);

• Definir de forma clara e única o conceito de atraso que será utilizado em todos os
  gráficos (por exemplo, atraso igual ou superior a 15 minutos);

• Calcular a média e a taxa de atraso por companhia aérea, considerando todo o
  período disponível no dataset;

• Calcular a média e a taxa de atraso por aeroporto de origem;

• Calcular a média e a taxa de atraso por aeroporto de destino;

• Calcular a sazonalidade dos atrasos, agregando os dados por:
  o mês do ano;
  o dia da semana;
  o hora do dia;

• Exportar todos os resultados em arquivos JSON separados, garantindo que os dados
  estejam prontos para consumo direto pelo dashboard;

• Validar os arquivos gerados, verificando se os valores fazem sentido do ponto de
  vista do negócio (por exemplo, se existem companhias e aeroportos reais e se os
  percentuais não estão todos zerados).

---

### Principal questão a ser respondida

“Como o comportamento histórico de atrasos varia entre companhias aéreas,
aeroportos e períodos do tempo?”

---

### ENTREGÁVEL – DS1

• Arquivo JSON com atraso por companhia aérea;  
• Arquivo JSON com atraso por aeroporto de origem;  
• Arquivo JSON com atraso por aeroporto de destino;  
• Arquivo JSON com sazonalidade dos atrasos;  
• Documento curto descrevendo a regra de atraso adotada e o período dos dados.

---

## DS2 – Explicabilidade do Modelo | Pessoa B

### Objetivo da frente

O objetivo desta frente é tornar o modelo interpretável para o usuário final,
traduzindo a lógica interna da predição para uma linguagem simples e compreensível.

Nesta etapa, não buscamos justificar matematicamente o modelo, mas sim explicar,
de forma qualitativa, quais fatores mais influenciam a decisão e por que um voo específico
foi classificado como atrasado ou não.

---

### Tarefas

• Listar todas as variáveis utilizadas pelo modelo na predição;

• Criar um mapeamento entre nomes técnicos das variáveis e nomes compreensíveis
  para usuários não técnicos;

• Identificar as variáveis mais importantes para o modelo de forma global, ou seja,
  aquelas que mais influenciam as decisões no geral;

• Gerar um arquivo contendo a explicabilidade global do modelo, indicando os fatores
  mais relevantes;

• Definir um formato simples de explicação local da predição, destacando os três
  principais fatores que contribuíram para o resultado de um voo específico;

• Garantir que as explicações estejam escritas em linguagem clara, evitando termos
  técnicos e jargões de machine learning;

• Validar a explicação com exemplos reais, verificando se ela permanece consistente
  para diferentes entradas.

---

### Principal questão a ser respondida

“Quais fatores mais influenciam a decisão do modelo e como explicar essa decisão
de forma clara para o usuário final?”

---

### ENTREGÁVEL – DS2

• Arquivo JSON com a importância global das variáveis;  
• Estrutura padronizada para explicação local da predição;  
• Documento com o mapeamento entre variáveis técnicas e nomes amigáveis.

---

## DS3 – Front-end Analítico e Dashboard | Pessoa C

### Objetivo da frente

O objetivo desta frente é construir a interface visual da aplicação, integrando a
previsão do modelo com os dados históricos e a explicabilidade, de forma organizada e
intuitiva.

O dashboard deve permitir que o usuário visualize rapidamente o resultado da
predição e, ao mesmo tempo, explore informações que ajudem a interpretar esse resultado.

---

### Tarefas

• Construir a tela principal da aplicação, separando claramente:
  o formulário de entrada dos dados do voo;
  o resultado da predição;
  o dashboard analítico;

• Implementar o formulário de entrada respeitando o contrato JSON da API existente;

• Integrar o botão de predição à API, exibindo o resultado e a probabilidade de atraso;

• Criar os gráficos do dashboard utilizando exclusivamente os arquivos JSON
  produzidos na frente DS1;

• Exibir a explicabilidade do modelo utilizando os dados fornecidos pela frente DS2;

• Implementar filtros básicos no dashboard (por exemplo, por companhia ou período);

• Garantir tratamento adequado de erros, exibindo mensagens claras em caso de
  falha na API ou preenchimento incorreto dos campos.

---

### Principal questão a ser respondida

“O usuário consegue entender a previsão e o contexto do atraso apenas observando
a interface da aplicação?”

---

### ENTREGÁVEL – DS3

• Interface funcional integrada à API de predição;  
• Dashboard com gráficos carregando corretamente;  
• Evidência visual da aplicação em funcionamento (prints ou link).

---

## DS4 – Consolidação Técnica e Produto Final | Helena

### Objetivo da frente

O objetivo desta frente é consolidar todas as entregas das demais frentes,
assegurando que a aplicação final esteja coerente, estável e pronta para demonstração.

Esta frente também é responsável por alinhar o trabalho da equipe, definir o escopo
final do produto e garantir que a narrativa da apresentação esteja clara e consistente.

---

### Tarefas

• Definir o escopo final da aplicação, estabelecendo claramente o que faz parte do
  produto e o que fica fora desta entrega;

• Organizar a estrutura do projeto, garantindo padronização de pastas e arquivos;

• Validar a integração entre predição, explicabilidade e dashboard;

• Testar a aplicação com diferentes cenários de entrada, verificando estabilidade e
  consistência das respostas;

• Atualizar o README com a descrição final do produto, suas funcionalidades e
  limitações conhecidas;

• Preparar o roteiro da demonstração, organizando a apresentação do problema,
  da solução e dos principais insights obtidos.

---

### Principal questão a ser respondida

“A aplicação final está clara, estável e pronta para ser apresentada como um produto
analítico completo?”

---

### ENTREGÁVEL – DS4

• Aplicação consolidada e validada;  
• README atualizado e padronizado;  
• Roteiro final de apresentação;  
• Aprovação final para demonstração.

---

## Cronograma da Semana – Datas Importantes

### Segunda-feira
• Reunião de planejamento semanal;  
• Alinhamento das responsabilidades de cada integrante;  
• Esclarecimento de dúvidas técnicas e definição do escopo final.

### Quinta-feira
• DS1: apresentação dos dados agregados para o dashboard;  
• DS2: apresentação da explicabilidade do modelo;  
• DS3: demonstração da interface e dos gráficos.

### Sexta-feira
• Consolidação final da aplicação;  
• Revisão do README e documentação;  
• Ensaio da apresentação final.

---

### Observação

Reuniões adicionais poderão ser marcadas ao longo da semana conforme a necessidade,
especialmente para alinhamentos técnicos ou validações de integração.
