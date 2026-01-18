# 08 — Backend Java (Spring Boot)

## 1. Objetivo do módulo

O **Backend Java do FlyOnTime** é o componente responsável por expor uma API corporativa, estável e padronizada para consumo por aplicações internas e externas (Front-End, integrações e clientes de negócio). Ele atua como uma **camada de orquestração e governança** entre:

- **API pública do FlyOnTime (Java)** — contrato final consumido por clientes;
- **serviço de Machine Learning (Python/FastAPI)** — responsável por inferência e explicabilidade;
- **camada de validação e consistência de dados** — garantindo que o modelo receba entradas válidas.

Na prática, o serviço Java garante que o consumidor interaja com um contrato único e consistente, enquanto o contrato com a API Python permanece **privado e controlado**.

---

## 2. Arquitetura do fluxo de predição

O fluxo de execução é composto por quatro etapas principais:

1. **Entrada do cliente (HTTP/JSON)**
   - o consumidor chama o endpoint de predição do backend Java.

2. **Validação de negócio e contrato**
   - validação de obrigatoriedade de campos;
   - validação de regras de rota (origem ≠ destino);
   - normalização/mapeamento de códigos.

3. **Orquestração da inferência (Java → Python)**
   - o backend constrói um `PythonPredictionRequest` e chama a API Python via `PythonPredictionClient`.

4. **Resposta corporativa (Java)**
   - o backend retorna um `FlightPredictionResponse` com:
     - classificação (`label` / `prediction`),
     - probabilidade (quando aplicável),
     - explicabilidade local,
     - explicabilidade global (quando disponível).

Esse desenho separa responsabilidades e torna o sistema mais robusto, mantendo a API pública independente da implementação interna do modelo.

---

## 3. Estrutura do projeto

A estrutura do módulo segue um padrão de microserviço Spring Boot:

```
src/main/java/com/flightontime/api
├── client
│   └── PythonPredictionClient.java
├── config
│   ├── OpenApiConfig.java
│   ├── RestTemplateConfig.java
│   └── WebMvcConfig.java
├── controller
│   └── FlightController.java
├── dto
│   ├── ErrorResponse.java
│   ├── FlightPredictionRequest.java
│   ├── FlightPredictionResponse.java
│   ├── PythonPredictionRequest.java
│   └── PythonPredictionResponse.java
├── exception
│   └── GlobalExceptionHandler.java
├── interceptor
│   └── RateLimitInterceptor.java
├── mapper
│   ├── AirlineCodeMapper.java
│   └── AirportCodeMapper.java
├── service
│   └── FlightPredictionService.java
├── validation
│   └── FlightRouteValidator.java
└── FlightOnTimeApplication.java
```

Abaixo estão as responsabilidades principais por camada.

---

## 4. Camadas e responsabilidades

### 4.1 Controller (camada de API)

O `FlightController` concentra os endpoints públicos e delega a lógica de negócio ao serviço. Este padrão mantém a API:

- mais simples e testável;
- consistente em contratos e status HTTP;
- livre de lógica acoplada ao provider de ML.

**Responsabilidades típicas do Controller:**

- receber e validar o request (DTO);
- acionar o serviço de predição;
- retornar response padronizado;
- propagar exceptions para o handler global.

---

### 4.2 Service (lógica de negócio)

O `FlightPredictionService` é o **núcleo de orquestração** do backend. Ele é responsável por:

- aplicar regras de validação de rota e consistência;
- acionar mappers (IATA/ICAO e códigos de companhia, quando necessário);
- construir o payload para a API Python;
- chamar o `PythonPredictionClient`;
- transformar a resposta da API Python no contrato corporativo Java.

Essa abordagem garante que decisões de integração (ex.: fallback de explicabilidade global) fiquem isoladas no serviço.

---

### 4.3 Client (integração Java → Python)

O `PythonPredictionClient` encapsula a chamada HTTP ao microserviço Python.

**Boas práticas implementadas pela separação em client:**

- desacoplamento do `RestTemplate` do domínio;
- centralização de headers, URL e estratégia de comunicação;
- padronização de tratamento de erro na integração.

---

### 4.4 DTOs (contratos)

Os DTOs do módulo estão organizados em dois grupos:

**Contrato público (Java):**

- `FlightPredictionRequest`
- `FlightPredictionResponse`

**Contrato privado (Java ↔ Python):**

- `PythonPredictionRequest`
- `PythonPredictionResponse`

Além disso, existe o:

- `ErrorResponse` → envelope padrão de erro corporativo.

---

### 4.5 Validation (regras determinísticas de negócio)

A pasta `validation` concentra regras de consistência que devem ser atendidas **antes** de chamar o modelo.

Exemplo de regra essencial:

- **origem e destino não podem ser iguais** (evita rotas inválidas que degradam a inferência).

Isso evita que entradas inconsistentes gerem predições incoerentes, e reduz ruído operacional.

---

### 4.6 Mappers (normalização e compatibilidade)

Os mappers (`AirportCodeMapper`, `AirlineCodeMapper`) garantem que o backend opere com códigos padronizados e compatíveis com:

- datasets de treinamento;
- contrato da API Python;
- experiência do usuário (nome amigável x código técnico).

Esses componentes são especialmente importantes quando:

- o Front-End envia códigos em um padrão;
- o modelo espera outro padrão (por exemplo, ICAO);
- existe necessidade de fallback em caso de código desconhecido.

---

### 4.7 Interceptor (governança e proteção)

O `RateLimitInterceptor` introduz uma camada corporativa de proteção contra:

- abuso de requisições;
- sobrecarga do serviço;
- cascata de falhas (especialmente porque a predição depende do serviço Python).

O rate limit também protege o modelo de picos de tráfego e contribui para estabilidade em produção.

---

### 4.8 Exception Handling (padrão corporativo)

O `GlobalExceptionHandler` padroniza o comportamento do serviço diante de erros, garantindo:

- respostas consistentes em formato JSON;
- códigos HTTP adequados (400, 422, 500 etc.);
- mensagens claras para troubleshooting;
- redução de comportamento inesperado no Front-End.

---

## 5. Configurações e documentação (OpenAPI)

O backend possui configuração dedicada para documentação da API (Swagger/OpenAPI) via `OpenApiConfig`, suportando:

- disponibilização de documentação navegável;
- padronização corporativa de endpoints;
- apoio na integração com Front-End e ferramentas de teste.

---

## 6. Estratégia de testes

O módulo inclui testes unitários e de integração, garantindo:

- validação de regras de negócio (`validation`);
- consistência de mappers;
- validação do fluxo ponta-a-ponta (E2E), incluindo integração com a API Python.

Arquivos de teste relevantes:

- `FlightPredictionServiceTest.java`
- `FlightPredictionE2ETest.java`
- `GlobalExceptionHandlerTest.java`
- `AirportCodeMapperTest.java`
- `FlightRouteValidatorTest.java`

---

## 7. Considerações operacionais

Para operação consistente em ambiente corporativo, o backend foi projetado para:

- **falhar de forma segura** quando a API Python estiver indisponível;
- manter o contrato de resposta estável;
- suportar múltiplos ambientes via `application.properties` e `application-docker.properties`;
- permitir evolução do modelo sem exigir alteração no cliente final.

---

## 8. Próximos passos recomendados

Como evolução para um ambiente enterprise, recomenda-se:

- instrumentação com **correlation-id** e tracing distribuído;
- logs estruturados (JSON) com campos de domínio;
- timeouts e retries controlados na chamada ao serviço Python;
- circuit breaker (Resilience4j) para degradação controlada.

Essas melhorias são compatíveis com a arquitetura atual e aumentam resiliência em produção.
