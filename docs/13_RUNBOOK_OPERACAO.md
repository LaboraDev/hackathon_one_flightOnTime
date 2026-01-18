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
