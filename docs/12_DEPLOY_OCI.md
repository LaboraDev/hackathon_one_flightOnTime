# 12 — Deploy OCI (Oracle Cloud Infrastructure)

## 1. Status atual

O Fly on Time encontra-se preparado para deploy, porém a publicação final em OCI depende de ajustes finais de validação no backend.

---

## 2. Estratégia recomendada

Deploy containerizado com:

- build de imagens Docker
- publicação em registry (OCIR)
- execução em serviço gerenciado (Container Instances ou Kubernetes)

---

## 3. Checklist corporativo de deploy

### Antes do deploy
- [ ] build local bem sucedido
- [ ] healthcheck OK (Java + Python)
- [ ] variáveis de ambiente revisadas
- [ ] testes de contrato executados
- [ ] validações de input completas

### Após deploy
- [ ] monitoramento habilitado
- [ ] logs centralizados
- [ ] rate limiting ativo
- [ ] rollback possível (versionamento de imagem)

---

## 4. Observações

O deploy deve preservar a separação entre backend e modelo, permitindo escalar cada componente conforme necessidade do ambiente.
