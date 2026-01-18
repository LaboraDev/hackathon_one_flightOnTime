# 07 — API Python

## 1. Responsabilidade e escopo

A **FlightOnTime API** é a camada responsável por **servir o modelo de Machine Learning em produção**, expondo um contrato estável de predição e explicabilidade para consumo por aplicações externas.

De forma objetiva, esta API foi desenhada para:

- **carregar o pipeline serializado** (`flightontime_pipeline.pkl`) no startup da aplicação, garantindo consistência entre treino e inferência
- **validar o payload recebido** (estrutura e campos obrigatórios) antes de executar qualquer predição
- converter o input do usuário em um **DataFrame compatível com o pipeline**
- executar a predição e retornar também a **probabilidade associada**
- fornecer **explicabilidade local** (por requisição) e **explicabilidade global** (pré-carregada em memória)
- preservar a API com comportamento resiliente, mesmo quando componentes opcionais (como explicabilidade global) não estiverem presentes

O objetivo final é garantir que a solução seja **operacionalmente confiável**, **auditável** e **facilmente integrável** em ambientes reais, seguindo padrões de entrega corporativa para APIs de inferência.

---

## 2. Carregamento do modelo e artefatos

No startup da aplicação, a API executa o carregamento do pipeline treinado via `pickle`, garantindo que a inferência utilize exatamente o mesmo fluxo de transformação utilizado no treinamento.

Artefatos carregados pela API:

- **Pipeline do modelo**: `flightontime_pipeline.pkl`  
  Contém todo o encadeamento de transformação e o modelo final treinado.
- **Explicabilidade global**: `explain_global.json`  
  É carregada uma única vez e mantida em memória para ser retornada via endpoint dedicado e também acoplada ao `/predict`.

Essa estratégia reduz custos computacionais por requisição e evita o recálculo de estruturas globais que não dependem de input do usuário.

---

## 3. Contrato de entrada

A API define um conjunto mínimo de campos exigidos para suportar a engenharia de variáveis e manter previsibilidade no funcionamento do pipeline.

Campos obrigatórios (`REQUIRED_RAW_COLS`):

- `partida_prevista`
- `empresa_aerea`
- `aerodromo_origem`
- `aerodromo_destino`
- `codigo_tipo_linha`

Esses campos representam o núcleo operacional do voo, permitindo ao pipeline extrair sinais temporais e categóricos relevantes.

---

## 4. Endpoints expostos

### 4.1 Health Check

**GET** `/health`

Este endpoint é utilizado como verificação padrão de disponibilidade da aplicação e pode ser integrado a mecanismos de monitoramento (ex.: uptime checks, orquestradores, deploy pipelines, balanceadores).

Além de indicar que o serviço está ativo, a resposta inclui evidências básicas de sanidade operacional, como:

- status da aplicação
- confirmação de que o pipeline foi carregado com sucesso
- validação da existência do arquivo do modelo no ambiente
- versão da API

Exemplo de resposta típica:

```json
{
  "status": "UP",
  "message": "FlightOnTime API is running",
  "modelo_carregado": true,
  "modelo_path_ok": true,
  "version": "2.0"
}
```

---

### 4.2 Explicabilidade Global

**GET** `/explain/global`

Este endpoint retorna a explicação global do modelo, isto é, uma visão macro das variáveis que mais influenciam o comportamento do classificador.

Comportamento operacional:

- caso o arquivo `explain_global.json` tenha sido carregado com sucesso, ele retorna seu conteúdo no payload
- caso o arquivo não exista ou não tenha sido carregado, a API retorna erro `404`, evitando respostas inconsistentes ou falsas garantias de disponibilidade

Exemplo de resposta:

```json
{
  "explain_global": {
    "...": "conteúdo do JSON"
  }
}
```

---

### 4.3 Predição (Inferência)

**POST** `/predict`

Este é o endpoint principal de produção. Ele executa a inferência do pipeline treinado e retorna não apenas o rótulo final, mas também informações complementares para consumo por sistemas corporativos e experiência do usuário.

#### 4.3.1 Formato esperado do payload

O endpoint exige que o payload contenha a chave `dados`, que representa o registro de voo a ser avaliado.

Estrutura esperada:

```json
{
  "dados": {
    "partida_prevista": "2024-03-01 10:30:00",
    "empresa_aerea": "GLO",
    "aerodromo_origem": "SBGR",
    "aerodromo_destino": "SBRJ",
    "codigo_tipo_linha": "N"
  },
  "topk": 8
}
```

Observações importantes:

- `dados` é obrigatório
- `topk` é opcional e controla a quantidade de fatores retornados na explicabilidade local (default: 8)
- a API transforma `dados` em um `DataFrame` com 1 linha, garantindo compatibilidade com o pipeline

---

#### 4.3.2 Validações aplicadas

Antes de executar o modelo, a API realiza validações estruturais, incluindo:

- verificação da existência da chave `dados`
- validação da presença de todas as colunas obrigatórias definidas em `REQUIRED_RAW_COLS`
- caso falte qualquer campo obrigatório, a API retorna erro `400` com mensagem explícita indicando quais colunas estão ausentes

Exemplo de erro:

```json
{
  "detail": "Faltando colunas obrigatórias: ['empresa_aerea', 'codigo_tipo_linha']"
}
```

Isso garante previsibilidade operacional e evita falhas internas do pipeline causadas por inputs incompletos.

---

#### 4.3.3 Resposta do endpoint

A resposta do `/predict` foi desenhada para suportar produção e UX, retornando:

- `prediction`: classe binária prevista (0 ou 1)
- `label`: rótulo interpretável (`"atrasado"` ou `"no_prazo"`)
- `proba_atraso` (quando aplicável): probabilidade da classe positiva
- `explain_local`: explicabilidade local com top fatores (quando disponível)
- `explain_global`: explicabilidade global (padrão estável, podendo ser `null`)
- `explain_local_error` (caso ocorra falha na explicabilidade local, sem quebrar o contrato)

Exemplo de resposta:

```json
{
  "prediction": 1,
  "label": "atrasado",
  "proba_atraso": 0.78,
  "explain_global": { "...": "conteúdo global" },
  "explain_local": {
    "top_features": [
      {
        "feature": "num__media_atraso_empresa",
        "contribution": 0.12,
        "direction": "increase",
        "value": 18.4
      }
    ],
    "bias": -0.34
  }
}
```

---

## 5. Estratégia de explicabilidade em tempo de inferência

A API implementa explicabilidade como parte do contrato de saída, separando claramente dois níveis:

- **Explicabilidade Global**: carregada 1 vez do arquivo JSON e retornada de forma estática e consistente
- **Explicabilidade Local**: calculada por chamada através da função `explicar_local_xgb(pipeline, x, top_k=topk)`

Esse desenho garante:

- baixo custo de execução para o componente global
- explicações locais contextualizadas por voo, sem necessidade de manter estado por usuário
- separação entre “diagnóstico macro do modelo” e “justificativa daquela decisão específica”

---

## 6. Confiabilidade, resiliência e padrão corporativo

Esta API foi construída com foco em produção, adotando decisões explícitas para evitar indisponibilidade por falhas secundárias:

- se `explain_global.json` não existir, a API **não quebra o `/predict`**, mantendo o contrato com `explain_global = None`
- a explicabilidade local é executada dentro de `try/except`, permitindo que o endpoint continue entregando predição mesmo se a explicabilidade falhar (retornando `explain_local_error`)
- os campos obrigatórios são validados antes da inferência, reduzindo falhas internas e melhorando suporte e debugging

Essa abordagem garante que a aplicação permaneça funcional mesmo diante de variações de ambiente, ausência de artefatos opcionais ou cenários de falha controlada.
