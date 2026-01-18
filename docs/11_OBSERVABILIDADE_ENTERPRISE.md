# 11 — Observabilidade Enterprise (Back-end Java)

## 1. Objetivo

A observabilidade no FlyOnTime foi desenhada para atender requisitos corporativos de **monitoramento, auditoria e rastreabilidade**. O foco é garantir que o serviço de predição:

- seja **operacionalmente confiável** em produção;
- tenha **diagnóstico rápido** em incidentes;
- permita **correlação** entre requisições de negócio e chamadas ao serviço de ML (Python);
- gere evidências para **conformidade e governança**.

---

## 2. Estratégia de resiliência e controle de tráfego (Rate Limiting)

O FlyOnTime implementa um controle explícito de taxa de requisições no Backend Java por meio do **`RateLimitInterceptor`**.

### 2.1 Propósito corporativo

Em ambientes corporativos, a API pode ser chamada por múltiplos consumidores simultaneamente (Front-End, integrações, testes automatizados e rotinas batch). O rate limiting é essencial para:

- **proteger o serviço de ML (Python)** contra sobrecarga;
- evitar picos de consumo acidentais (ex.: loops, retries mal configurados);
- manter **latência estável**;
- reduzir risco de indisponibilidade por **DoS involuntário**.

### 2.2 Modelo de funcionamento

A interceptação ocorre antes da execução do controller e valida se o limite de chamadas está dentro da política estabelecida.

Quando o limite é excedido, o backend responde com:

- **HTTP 429 (Too Many Requests)**
- payload padronizado de erro (via `ErrorResponse`)

Essa abordagem garante previsibilidade para o consumidor e facilita o tratamento no Front-End.

---

## 3. Padronização de erros e contrato de falhas

O FlyOnTime adota um mecanismo global para centralizar falhas e manter consistência de resposta: **`GlobalExceptionHandler`**.

### 3.1 Objetivo

O objetivo do handler global é assegurar que:

- o consumidor **sempre** receba um payload de erro estruturado;
- mensagens de validação sejam claras e acionáveis;
- falhas inesperadas sejam capturadas e categorizadas;
- os logs contenham informações suficientes para investigação.

### 3.2 Modelo de resposta de erro

Os erros seguem um DTO dedicado (**`ErrorResponse`**) para padronização.

**Exemplos de eventos mapeados:**

- payload inválido / regra de negócio violada → `400 Bad Request`
- limite de requisições excedido → `429 Too Many Requests`
- falha ao integrar com serviço Python → `502 Bad Gateway` (ou `500`, dependendo do contexto)
- exceção não prevista → `500 Internal Server Error`

---

## 4. Observabilidade de saúde do serviço (Health Check)

O backend disponibiliza endpoint de saúde para integração com roteadores, balanceadores e pipelines de deployment.

### 4.1 O que o Health precisa validar

O endpoint de health check deve comprovar que o serviço está operacional, incluindo:

- **aplicação Java está em execução**;
- **pipeline/integração está pronto para uso**;
- dependências essenciais estão acessíveis (quando aplicável).

> Importante: em ambiente enterprise, health check não é somente “up/down”. É uma evidência mínima de que o serviço pode atender requisições reais.

---

## 5. Validação como mecanismo de confiabilidade

Além da observabilidade, o FlyOnTime implementa validações para evitar inconsistências que se tornam incidentes em produção.

As validações principais são:

- **`FlightPredictionRequestFutureTest`**: garante que a data informada seja futura (contrato de negócio)
- **`FlightRouteValidatorTest`**: garante que origem e destino sejam diferentes
- **`AirportCodeMapperTest`**: garante conversão consistente de códigos de aeroporto (IATA/ICAO)

Essa camada de validação reduz risco operacional e aumenta a qualidade do input entregue ao modelo.

---

## 6. Testes automatizados como evidência operacional

O módulo possui testes que reforçam a robustez corporativa:

- **Unit tests** para validação, mapper e service
- **E2E / Integration test** (`FlightPredictionE2ETest`) para validar o fluxo completo (requisição → validação → chamada ao Python → resposta)

No contexto corporativo, esses testes são fundamentais para:

- impedir regressões no contrato;
- dar segurança na evolução do backend;
- viabilizar pipelines de CI/CD.

---

## 7. Recomendações enterprise (boas práticas)

Para reforçar maturidade de produção, recomenda-se:

1. **Correlações de requisição**
   - Adicionar `X-Request-Id` propagado entre Java e Python
2. **Métricas por endpoint**
   - Latência p50/p90/p99 do `/predict`
   - Taxa de erros por código HTTP
3. **Auditoria de predição (sem PII)**
   - Persistir apenas campos técnicos necessários para debugging
4. **Alertas automatizados**
   - Alertar em aumento de `429`, `5xx` e degradação de latência

---

## 8. Resultado esperado

Com essa arquitetura, o FlyOnTime entrega uma API com postura enterprise:

- **resiliente** (proteção contra abuso e falhas externas);
- **auditável** (erros padronizados e rastreáveis);
- **operacional** (health check, testes e governança de contrato);
- **pronta para escala** (limites de tráfego e padronização de integração com ML).
