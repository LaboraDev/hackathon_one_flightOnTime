# 01 — Visão Geral do Projeto

## 1. Contexto e Motivação

A previsibilidade de atrasos em voos é um tema crítico tanto para passageiros quanto para companhias aéreas. Atrasos impactam diretamente a experiência do usuário final, custos operacionais, replanejamento logístico, utilização de slots aeroportuários e eficiência do uso de aeronaves.

O projeto **[FlightOnTime](https://github.com/LaboraDev/hackathon_one_flightOnTime/tree/main)** foi desenvolvido como uma solução preditiva baseada em dados históricos para estimar, com antecedência, a probabilidade de um voo **atrasar** no momento de partida.

---

## 2. Objetivo do Projeto

O objetivo do FlyOnTime é fornecer uma predição robusta e interpretável sobre atraso de voos, entregando como resposta:

- **Classificação (Label)**: `Atrasado` ou `No prazo`
- **Probabilidade**: percentual de atraso (0% a 100%)
- **Explicabilidade Local**: fatores que mais contribuíram para a predição daquele voo, em formato gráfico
- **Explicabilidade Global**: explicação padrão baseada na importância das features no modelo em geral, disponibilizada em formato textual

---

## 3. Público-alvo

O sistema foi projetado para atender diferentes perfis de usuários e necessidades:

- **Passageiros**: estimar risco de atraso antes do embarque
- **Companhias aéreas**: suporte à tomada de decisão operacional
- **Times internos (Data/Tech/Ops)**: análise e monitoramento da performance das rotas

---

## 4. Arquitetura do Sistema (Visão de Alto Nível)

O FlyOnTime adota uma arquitetura modular, com separação entre aplicação e modelo, garantindo escalabilidade e independência de deploy.

```text
Frontend (HTML/CSS/JS)
    |
    v
Backend Java (Spring Boot)
    |
    v
API Python (FastAPI + ML Pipeline)
    |
    v
Predição + Explicabilidade (Local / Global)
```
