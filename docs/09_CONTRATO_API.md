# 09 — Contrato de API (Java ↔ Python)

## 1. Visão geral do contrato

O FlyOnTime opera com **dois níveis de contrato**, com responsabilidades bem definidas:

1. **Contrato público (Java / FlightOnTime API)**: interface corporativa consumida por Front-End e integrações.
2. **Contrato privado (Python / ML API)**: interface de inferência consumida exclusivamente pelo Backend Java.

A separação dos contratos permite:

- **evolução independente** do microserviço de ML (sem quebrar consumidores);
- **padronização de validações, erros e governança** no backend;
- **observabilidade e segurança centralizadas** na camada Java.

---

## 2. Contrato público (API Java)

### 2.1 Endpoint principal — Previsão de atraso

**POST** `/predict`

#### Objetivo

Receber os dados mínimos de um voo e retornar:

- classificação binária (**atrasado** ou **no_prazo**);
- probabilidade associada;
- explicabilidade local (top fatores);
- opcionalmente, explicabilidade global (visão macro do modelo).

#### Payload de entrada (FlightPredictionRequest)

O contrato público é representado pelo DTO `FlightPredictionRequest`.

Campos obrigatórios:

- `partidaPrevista` *(string/datetime)*
- `empresaAerea` *(string)*
- `aerodromoOrigem` *(string)*
- `aerodromoDestino` *(string)*
- `codigoTipoLinha` *(string)*

Regras corporativas e validações:

- **Datas devem ser futuras** (proteção contra uso indevido do modelo e consistência de negócio).
- **Origem e destino não podem ser iguais** (rota inválida).
- **Campos obrigatórios devem estar preenchidos** (input mínimo para inferência).

> As validações são centralizadas no módulo `validation`, reforçando o controle de qualidade do tráfego de entrada.

#### Exemplo de requisição

```json
{
  "partidaPrevista": "2025-12-25T14:30:00",
  "empresaAerea": "GLO",
  "aerodromoOrigem": "SBGR",
  "aerodromoDestino": "SBRJ",
  "codigoTipoLinha": "N"
}
```

#### Resposta esperada (FlightPredictionResponse)

O DTO público de saída é `FlightPredictionResponse`.

Campos principais:

- `prediction` *(int)*: 1 para atraso, 0 para no prazo
- `label` *(string)*: `"atrasado"` ou `"no_prazo"`
- `probaAtraso` *(double)*
- `explainLocal` *(objeto / lista de fatores)*
- `explainGlobal` *(objeto)* — quando habilitado

Exemplo de resposta:

```json
{
  "prediction": 1,
  "label": "atrasado",
  "probaAtraso": 0.78,
  "explainLocal": {
    "topFeatures": [
      {
        "feature": "num__media_atraso_empresa",
        "contribution": 0.12,
        "direction": "increase",
        "value": 38.0
      }
    ],
    "bias": -0.34
  },
  "explainGlobal": {
    "top_features": [
      {"feature": "num__media_atraso_empresa", "importance": 478.15}
    ]
  }
}
```

> O campo `explainLocal` é sempre retornado como parte do contrato de transparência do FlyOnTime.

---

## 3. Contrato privado (Java → Python / ML API)

O Backend Java chama o microserviço Python através do `PythonPredictionClient`.

### 3.1 Endpoint de inferência

**POST** `PYTHON_API_BASE_URL + "/predict"`

#### Payload (PythonPredictionRequest)

O contrato privado é otimizado para refletir exatamente as colunas esperadas pelo pipeline Python.

Campos mínimos enviados:

- `partida_prevista`
- `empresa_aerea`
- `aerodromo_origem`
- `aerodromo_destino`
- `codigo_tipo_linha`

Estrutura compatível com o serviço Python:

```json
{
  "dados": {
    "partida_prevista": "2025-12-25T14:30:00",
    "empresa_aerea": "GLO",
    "aerodromo_origem": "SBGR",
    "aerodromo_destino": "SBRJ",
    "codigo_tipo_linha": "N"
  },
  "topk": 8
}
```

> O parâmetro `topk` controla quantos fatores serão retornados pela explicabilidade local.

#### Resposta (PythonPredictionResponse)

O DTO de resposta do Python (consumido pela camada Java) contém:

- `prediction`
- `label`
- `proba_atraso` *(quando o modelo fornece predict_proba)*
- `explain_local`
- `explain_global` *(opcional, quando carregado no runtime do serviço Python)*

---

## 4. Conversão de contrato (Mapper)

A API pública utiliza nomenclatura orientada a domínio e padrões Java (`camelCase`).

Já o modelo Python exige o padrão de variáveis do pipeline (`snake_case`) e codificações específicas.

Para padronizar esse processo, são utilizados mappers dedicados:

- `AirportCodeMapper` — normalização/mapeamento de códigos de aeroportos
- `AirlineCodeMapper` — normalização/mapeamento de códigos de companhias aéreas

Benefícios:

- desacoplamento entre **representação de UI** e **representação do modelo**;
- controle de consistência (IATA/ICAO, normalização de entradas);
- preparação para evolução de listas de domínio (novos aeroportos/companhias).

---

## 5. Padrão de erros (ErrorResponse)

O backend mantém um contrato único e corporativo para erros.

A classe `ErrorResponse` estabelece um formato central para:

- mensagens funcionais (erro de validação)
- erros técnicos (falha em integração com Python)
- erros operacionais (rate-limit, indisponibilidade)

Exemplo de resposta de erro:

```json
{
  "message": "Faltando campos obrigatórios: [empresaAerea, aerodromoDestino]",
  "timestamp": "2026-01-18T10:15:00Z"
}
```

---

## 6. Garantias de qualidade do contrato

O FlyOnTime aplica uma estratégia de garantias para sustentar operação em produção:

- validação de payload na borda (camada Java)
- padronização de mensagens de erro via `GlobalExceptionHandler`
- proteção por **Rate Limiting** via `RateLimitInterceptor`
- testes automatizados (unitários e E2E) assegurando estabilidade do contrato

Essa abordagem reduz risco de regressões e garante previsibilidade para consumidores.
