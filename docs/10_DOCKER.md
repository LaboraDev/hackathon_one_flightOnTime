# 10 — Docker & Orquestração (FlyOnTime)

## 1. Objetivo

Este documento descreve a estratégia de execução do FlyOnTime em ambiente conteinerizado, garantindo:

- **reprodutibilidade** (mesma execução em qualquer máquina/ambiente);
- **isolamento** entre serviços (Java ↔ Python);
- **padronização operacional** para execução local, validação e entrega;
- **facilidade de troubleshooting** (healthchecks, logs e variáveis de ambiente);
- **orquestração ponta-a-ponta** do fluxo de predição.

A execução é centralizada via **Docker Compose**, que sobe os serviços do Backend (Spring Boot) e do Modelo (FastAPI) no mesmo *network bridge*, viabilizando comunicação segura por DNS interno.

---

## 2. Arquitetura de serviços

O arquivo `docker-compose.yml` define dois serviços principais:

### 2.1 `python-api` (Data Science)

Serviço responsável por disponibilizar o **pipeline de ML** via FastAPI.

**Características operacionais:**

- **Build:** `data_science/semana_04/scripts/Dockerfile`
- **Porta interna:** `5000`
- **Porta exposta no host:** `5000:5000`
- **Comando:**

```bash
uvicorn api_app:app --host 0.0.0.0 --port 5000
```

- **Healthcheck:**

```http
GET http://localhost:5000/health
```

- **Volumes para desenvolvimento:**

```yaml
- ./data_science/semana_04/scripts:/app:ro
```

> Observação corporativa: o volume está como `:ro` (*read-only*), o que reduz risco de alterações acidentais dentro do container e mantém o ambiente mais controlado.

---

### 2.2 `java-backend` (Backend)

Serviço responsável por expor o contrato público da aplicação e orquestrar chamadas ao serviço Python.

**Características operacionais:**

- **Build:** `Dockerfile` (raiz do projeto)
- **Porta interna:** `8080`
- **Porta exposta no host:** `8080:8080`

- **Healthcheck:**

```http
GET http://localhost:8080/api/health
```

- **Dependência de inicialização:**

O backend só inicia após o serviço Python estar saudável:

```yaml
depends_on:
  python-api:
    condition: service_healthy
```

Essa estratégia garante que a aplicação suba de forma consistente e evita falhas de inicialização por indisponibilidade temporária do modelo.

---

## 3. Network e comunicação entre serviços

Os serviços compartilham a rede:

```yaml
networks:
  - flightontime-network
```

Isso permite que o Java chame o Python usando o endereço interno:

```text
http://python-api:5000
```

Essa abordagem é preferível a usar `localhost` dentro de containers, pois mantém o design compatível com práticas reais de microserviços.

---

## 4. Variáveis de ambiente e perfis

### 4.1 Variáveis do `python-api`

- `PORT=5000`: porta de execução
- `PYTHONUNBUFFERED=1`: logs mais previsíveis em ambiente conteinerizado

### 4.2 Variáveis do `java-backend`

O backend utiliza variáveis explícitas para garantir previsibilidade:

- `SERVER_PORT=8080`
- `SPRING_PROFILES_ACTIVE=docker`
- `PREDICTION_SERVICE_URL=http://python-api:5000`
- `PREDICTION_SERVICE_USE_MOCK=false`
- `TZ=America/Sao_Paulo`

Além disso, há controle de memória via JVM:

```text
JAVA_OPTS=-Xmx512m -Xms256m -XX:+UseContainerSupport
```

> Boas práticas corporativas: declarar limites explícitos reduz risco de *OOM (Out Of Memory)* e mantém comportamento consistente em execução local e pipelines de CI/CD.

---

## 5. Healthchecks e política de restart

Ambos os serviços possuem:

- **healthcheck** (validação ativa)
- **restart: unless-stopped** (resiliência operacional)

Isso melhora o comportamento do ambiente em situações reais como:

- inicialização lenta do modelo
- falhas intermitentes de rede
- problemas de dependência/ordem de subida

---

## 6. Como executar (fluxo recomendado)

### 6.1 Subir a aplicação completa

```bash
docker-compose up -d
```

### 6.2 Subir com rebuild (quando houver mudanças)

```bash
docker-compose up -d --build
```

### 6.3 Ver status

```bash
docker-compose ps
```

### 6.4 Ver logs

```bash
docker-compose logs -f
```

Logs por serviço:

```bash
docker-compose logs -f java-backend
docker-compose logs -f python-api
```

### 6.5 Encerrar serviços

```bash
docker-compose stop
```

### 6.6 Encerrar e remover containers/rede

```bash
docker-compose down
```

---

## 7. Rotas úteis para validação rápida

Após subir os serviços:

- **Swagger (Java):** `http://localhost:8080/swagger-ui.html`
- **Docs (Python / FastAPI):** `http://localhost:5000/docs`

Testes rápidos:

```bash
curl http://localhost:8080/api/health
curl http://localhost:5000/health
```

---

## 8. Considerações para produção

Embora o `docker-compose.yml` seja ideal para desenvolvimento e validação local, para evolução em ambientes corporativos recomenda-se:

- separar *build pipelines* para Java e Python
- remover volume de desenvolvimento
- adicionar observabilidade (logs estruturados, tracing e métricas)
- configurar *resource limits* explícitos (CPU/memória) por serviço
- publicar imagens versionadas em registry corporativo

---

## 9. Troubleshooting (runbook rápido)

### 9.1 Backend não sobe (dependência do Python)

Validar primeiro o health do serviço Python:

```bash
curl http://localhost:5000/health
```

E em seguida confirmar o status no Compose:

```bash
docker-compose ps
```

### 9.2 Erro de comunicação Java → Python

Garantir que a variável abaixo está apontando para o DNS interno correto:

```text
PREDICTION_SERVICE_URL=http://python-api:5000
```

### 9.3 Verificar endpoints

- Java:

```bash
curl http://localhost:8080/api/health
```

- Python:

```bash
curl http://localhost:5000/health
```

