# 13 — Runbook de Operação e Suporte

## 1. Objetivo

Este runbook define o procedimento operacional padrão para:

- validar disponibilidade do sistema
- identificar falhas rapidamente
- agir durante incidentes
- garantir continuidade do serviço

---

## 2. Checklist de saúde

### Backend Java
- checar endpoint de health
- validar resposta do swagger
- verificar logs de timeout/retry

### API Python
- checar `/health`
- checar `/docs`
- validar se modelo está carregado

---

## 3. Problemas comuns e soluções

### Erro 503 (serviço python indisponível)
Ações:
- verificar container python
- reiniciar serviço
- validar rede do compose

### Timeout em predição
Ações:
- checar carga do python
- validar cache no backend
- revisar timeout configurado

### Rate limit (429)
Ações:
- validar se tráfego está dentro do esperado
- revisar política de consumo

---

## 4. Rotina recomendada de manutenção

- revisar métricas semanalmente
- validar drift de performance mensalmente
- retreinar modelo a cada janela definida (ex.: trimestral)
## 5. Matriz de Incidentes e Resposta Rápida

| Incidente | Sintoma | Diagnóstico | Ação de Recuperação |
| :--- | :--- | :--- | :--- |
| **Erro de Conectividade** | HTTP 502 / 504 | Java não alcança o DNS `python-api` [9]. | Reiniciar o serviço `python-api` e validar a rede interna do Docker/OCI [10]. |
| **Excesso de Carga** | HTTP 429 | O `RateLimitInterceptor` bloqueou o excesso de requisições [13]. | Verificar se há comportamento anômalo ou se o limite configurado precisa de ajuste [12]. |
| **Falha de Negócio** | HTTP 400 | O `FlightRouteValidator` rejeitou a rota (ex: Origem = Destino) [12]. | Orientar o usuário/frontend sobre as regras de preenchimento de aeroportos [13]. |
| **Memória Excedida** | Container reiniciando | O serviço ultrapassou os limites de RAM definidos [9]. | Revisar a variável `JAVA_OPTS` ou o shape da instância na OCI [9][10]. |

## 6. Procedimento de Recuperação de Desastre (DR)

Caso o ambiente sofra uma queda crítica, siga os protocolos de resiliência:

1.  **Rollback de Imagem**: Se o erro ocorreu após um deploy, utilize o registry (OCIR) para fazer o deploy da tag anterior estável [10].
2.  **Modo de Contingência**: Em caso de falha persistente na API Python, habilitar temporariamente a variável `PREDICTION_SERVICE_USE_MOCK=true` no Backend Java para manter o serviço básico ativo [9][12].
3.  **Resiliência de Inicialização**: Garantir que o `depends_on` com `condition: service_healthy` esteja ativo para que o Java não suba antes do modelo estar pronto [9].

## 7. Contatos de Escalonamento e Responsabilidades

Para garantir agilidade no hackathon, os incidentes devem ser direcionados conforme a natureza do problema:

-   **Equipe de Data Science**: Problemas de inferência, acurácia do modelo, explicabilidade e erros na `API Python` [2][6].
-   **Equipe de Backend**: Erros de contrato, falhas de integração, limites de `Rate Limit` e exceptions Java [12][13].
-   **Equipe de Cloud/DevOps**: Falhas de conectividade OCI, disponibilidade de containers e problemas de rede [10].

## 8. Evidências de Sucesso Operacional

O sistema é considerado em estado "Saudável" quando apresenta:
-   **Logs de Inicialização**: `Application startup complete` no Python e `Started FlightOnTimeApplication` no Java [9][12].
-   **Healthcheck**: Resposta HTTP 200 nos endpoints `/health` (Python) e `/api/health` (Java) [13].
-   **Métricas**: Latência estável nos percentis p50/p90 para o endpoint de predição [13].

  

