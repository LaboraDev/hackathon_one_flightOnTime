import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function AtrasoPorEmpresa({ data, top = 40 }) {
  // Garante que data seja sempre um array
  const chartData = Array.isArray(data) ? data : [];

  // Ordena pelo atraso_15m decrescente e pega apenas o top N
  const topData = chartData
    .sort((a, b) => b.atraso_15m - a.atraso_15m)
    .slice(0, top);

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={topData}>
          <XAxis
            stroke="#ffffff"
            dataKey="empresa_aerea"
            interval={0}
            angle={-35}
            textAnchor="end"
            height={80}
          />
          <YAxis stroke="#ffffff" />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1a0028",
              border: "1px solid rgba(255,255,255,0.2)",
              borderRadius: "8px",
              color: "#fff",
            }}
            formatter={(value) => [`${value}`, "Atraso (15 min)"]}
          />
          <Bar dataKey="atraso_15m" fill="#ff7a18" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
