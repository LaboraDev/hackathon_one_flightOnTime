import React, { useState } from "react";

// Importação dos componentes de gráfico
import AtrasoPorEmpresa from "./charts/AtrasoPorEmpresa";
import AtrasoPorOrigem from "./charts/AtrasoPorOrigem";
import AtrasoPorDestino from "./charts/AtrasoPorDestino";
import SazonalidadeMes from "./charts/SazonalidadeMes";
import SazonalidadeSemana from "./charts/SazonalidadeSemana";

// Importação direta dos JSON (dentro de src/assets/data)
import atrasoEmpresa from "../../assets/data/atraso_empresa.json";
import atrasoOrigem from "../../assets/data/atraso_origem.json";
import atrasoDestino from "../../assets/data/atraso_destino.json";
import sazonalidadeMes from "../../assets/data/sazonalidade_atrasos.json";
import sazonalidadeSemana from "../../assets/data/sazonalidade_dia_semana.json";

export default function Dashboard() {
  const [error] = useState(null);

  return (
    <div className="section">
      <h2 className="section-title">Análise Exploratória dos Atrasos</h2>

      <div className="section">
        <div className="card">
          <h3>Atraso por Companhia Aérea</h3>
          <AtrasoPorEmpresa data={atrasoEmpresa} />
        </div>
      </div>

      <div className="section">
        <div className="card">
          <h3>Atraso por Aeroporto de Origem</h3>
          <AtrasoPorOrigem data={atrasoOrigem} />
        </div>
      </div>

      <div className="section">
        <div className="card">
          <h3>Atraso por Aeroporto de Destino</h3>
          <AtrasoPorDestino data={atrasoDestino} />
        </div>
      </div>

      <div className="section">
        <div className="card">
          <h3>Sazonalidade por Hora</h3>
          <SazonalidadeMes data={sazonalidadeMes} />
        </div>
      </div>

      <div className="section">
        <div className="card">
          <h3>Sazonalidade Semanal</h3>
          <SazonalidadeSemana data={sazonalidadeSemana} />
        </div>
      </div>
    </div>
  );
}
