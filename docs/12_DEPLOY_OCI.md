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

---

# FlyOnTime - Infraestrutura e Deploy (OCI)

## 5. Detalhamento da Infraestrutura (OCI)

Para suportar a arquitetura modular do **FlyOnTime**, a infraestrutura na **Oracle Cloud** será organizada da seguinte forma:

### 5.1 Redes e Segurança (Networking)

- **VCN (Virtual Cloud Network):** Criação de uma rede virtual dedicada.  
- **Sub-rede Pública:** Hospedagem do container **java-backend**, permitindo acesso via porta `8080`.  
- **Sub-rede Privada:** Hospedagem do container **python-api** na porta `5000`, garantindo que o modelo de ML não fique exposto diretamente à internet.  

**Security Lists:**
- Regra de entrada para porta `8080 (TCP)` liberada para o CIDR do frontend ou internet.  
- Regra de entrada para porta `5000 (TCP)` liberada apenas para o IP interno do backend Java.  

---

### 5.2 Armazenamento de Imagens (OCIR)

As imagens Docker serão armazenadas no **Oracle Cloud Infrastructure Registry (OCIR)** seguindo o padrão de nomenclatura:


---

## 6. Guia de Execução do Deploy

### 6.1 Preparação e Push

**Autenticação no Registro:**
```bash
docker login <region-key>.ocir.io
# Usuário: <namespace>/oracleidentitycloudservice/<username>
# Senha: <seu_auth_token>

Build e Tagging:

# Backend Java
docker build -t flyontime/java-backend .
docker tag flyontime/java-backend <region-key>.ocir.io/<namespace>/flyontime/java-backend:1.0.0

# API Python
docker build -t flyontime/python-api ./data_science/semana_04/scripts/
docker tag flyontime/python-api <region-key>.ocir.io/<namespace>/flyontime/python-api:1.0.0
docker push <region-key>.ocir.io/<namespace>/flyontime/java-backend:1.0.0
docker push <region-key>.ocir.io/<namespace>/flyontime/python-api:1.0.0

Envio para OCI:
docker push <region-key>.ocir.io/<namespace>/flyontime/java-backend:1.0.0
docker push <region-key>.ocir.io/<namespace>/flyontime/python-api:1.0.0
6.2 Provisionamento (Container Instances)
A execução será feita via OCI Container Instances, configurando:
- Shape: Mínimo de 1 OCPU e 2GB RAM para a API Python.
- Variáveis de Ambiente Críticas:
- PREDICTION_SERVICE_URL: DNS ou IP interno da instância Python.
- SPRING_PROFILES_ACTIVE: docker.
- JAVA_OPTS: -Xmx512m -Xms256m.
7. Verificação de Sucesso (Smoke Test)
Após o provisionamento, a equipe de DevOps deve validar a disponibilidade através dos endpoints corporativos padronizados:
- Acesso ao Contrato:
http://<IP_PUBLICO_OCI>:8080/swagger-ui.html
- 
- Saúde do Sistema:
http://<IP_PUBLICO_OCI>:8080/api/health
- Logs:
Validar no OCI Logging Service se não há erros de conexão 502 Bad Gateway na integração Java-Python.

Notas de Evolução
Para uma fase futura (Pós-Hackathon), recomenda-se a implementação de um API Gateway na OCI para gerenciar o Rate Limit de forma nativa na borda, desonerando o interceptor do Spring Boot.

---

Esse conteúdo já está pronto para ser colado no seu **README.md** do GitHub 🚀.  

Quer que eu também monte uma **seção inicial com badges e instruções rápidas** (exemplo: status do build, versão Docker, etc.) para deixar o README mais profissional?


