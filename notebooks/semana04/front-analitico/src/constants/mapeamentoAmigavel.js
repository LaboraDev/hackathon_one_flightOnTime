export const mapeamentoAmigavel = {
  empresa_aerea: {
    label: "Nome da Companhia Aérea",
    help: "Companhias diferentes possuem históricos distintos de pontualidade.",
  },
  aerodromo_origem: {
    label: "Aeroporto de Partida",
    help: "Alguns aeroportos apresentam maior incidência de atrasos.",
  },
  aerodromo_destino: {
    label: "Aeroporto de Chegada",
    help: "O aeroporto de destino também influencia o risco de atraso.",
  },
  codigo_tipo_linha: {
    label: "Tipo de Operação",
    help: "Voos regulares e não regulares possuem comportamentos distintos.",
  },
  hora_dia: {
    label: "Horário do Voo",
    help: "Voos em horários de pico tendem a sofrer mais atrasos.",
  },
  dia_semana: {
    label: "Dia da Semana",
    help: "Certos dias apresentam maior congestionamento aéreo.",
  },
  media_atraso_empresa: {
    label: "Frequência Histórica de Atrasos da Empresa",
    help: "Média histórica de atrasos associados à companhia aérea.",
  },
  media_atraso_origem: {
    label: "Índice de Atrasos no Aeroporto de Origem",
    help: "Histórico de atrasos registrados neste aeroporto.",
  },
  media_atraso_destino: {
    label: "Índice de Atrasos no Aeroporto de Destino",
    help: "Atrasos médios associados ao aeroporto de chegada.",
  },
  janela_critica: {
    label: "Período de Pico no Tráfego",
    help: "Indica se o voo ocorre em um período crítico de tráfego aéreo.",
  },
};
