# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

##----------------------------------------------------------------------------

# ✈️ Flight Delay Prediction – Front-end Analítico

Este projeto corresponde ao **front-end analítico** da aplicação de **predição de atraso de voos**, desenvolvido em **React + Vite**.
Ele se comunica com uma **API FastAPI** para realizar predições e consome **arquivos JSON** gerados pela frente de Data Science (DS1) para visualização analítica.

---

## 📌 Tecnologias Utilizadas

- **React 18**
- **Vite**
- **JavaScript (ES6+)**
- **CSS (Global + Modularizado)**
- **Fetch API**
- **Chart.js / Recharts** (para gráficos)
- **Node.js** (ambiente de execução)

---

## 📁 Estrutura do Projeto (Resumo)

```
front-analitico/
├── public/
├── src/
│   ├── components/
│   │   ├── form/             # FlightForm + Schema
│   │   ├── dashboard/        # Gráficos analíticos
│   │   └── services/         # Comunicação com API
│   ├── assets/
│   │   └── styles/           # CSS global e específico
|   |   └── data/                # JSONs da DS1 (gráficos)
│   ├── App.jsx
│   └── main.jsx
├── .gitignore
├── package.json
└── vite.config.js
```

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- **Node.js (versão 18 ou superior)**
  👉 [https://nodejs.org](https://nodejs.org)

Verifique a instalação:

```bash
node -v
npm -v
```

---

## 🚀 Como rodar o projeto localmente

### 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd front-analitico
```

📌 **O que faz:**
Copia o projeto para sua máquina e acessa a pasta raiz.

---

### 2️⃣ Instalar as dependências

```bash
npm install
```

📌 **O que faz:**
Instala todas as bibliotecas necessárias definidas no `package.json`
(ex.: React, Vite, bibliotecas de gráficos).

---

### 3️⃣ Rodar o servidor de desenvolvimento

```bash
npm run dev
```

📌 **O que faz:**
Inicia o servidor local do Vite em modo desenvolvimento.

Após executar, o terminal exibirá algo como:

```
Local: http://localhost:5173
```

Acesse esse endereço no navegador.

---

## 🔌 Integração com a API (Back-end)

O front-end espera que a **API FastAPI esteja rodando** em:

```
http://localhost:8000
```

### Endpoint utilizado:

```http
POST /predict
```

📌 **Importante:**
Se a API não estiver ativa, o formulário exibirá mensagens de erro tratadas.

---

## 📊 Dados Analíticos (JSON – DS1)

Os gráficos do dashboard utilizam **exclusivamente arquivos JSON estáticos**, localizados em:

```
src/assets/data/
```

Arquivos esperados:

- `atraso_empresa.json`
- `atraso_origem.json`
- `atraso_destino.json`
- `sazonalidade_atrasos.json`
- `sazonalidade_dia_semana.json`

📌 **O que isso garante:**

- Separação clara entre **DS e Front**
- Dashboard funcional mesmo sem API ativa
- Arquitetura limpa e reprodutível

---

## 🧠 Explicabilidade do Modelo

O formulário e a resposta de predição exibem:

- Classe prevista (Atrasado / No prazo)
- Probabilidade
- Barra visual de risco
- **Explicação local simplificada**, baseada nos fatores principais:

  - Aeroporto de origem
  - Histórico da companhia
  - Sazonalidade

Essa abordagem evita jargões técnicos e melhora a interpretação pelo usuário final.

---

## 🧪 Scripts Disponíveis

```bash
npm run dev
```

▶ Executa o projeto em modo desenvolvimento

```bash
npm run build
```

▶ Gera a versão de produção (`dist/`)

```bash
npm run preview
```

▶ Visualiza o build localmente

---

## ❗ Problemas Comuns

### 🔴 Erro: `Failed to fetch`

- Verifique se a API está rodando
- Confirme a URL no arquivo `services/api.js`
- Verifique CORS no back-end

### 🔴 Erro ao carregar JSON

- Confirme se os arquivos estão em `src/assets/data/`
- Use `fetch("/data/arquivo.json")`

---

## 📌 Próximos Passos (Roadmap)

- Refinar estilização final
- Aplicar filtros interativos no dashboard
