import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function AtrasoPorDestino({ data, top = 40 }) {
  // Garante que data seja um objeto
  const chartData =
    data && typeof data === "object" && !Array.isArray(data)
      ? Object.entries(data).map(([key, value]) => ({
          aerodromo_destino: key,
          atraso_15m: value,
        }))
      : [];

  // Ordena decrescente e pega top N
  const topData = chartData
    .sort((a, b) => b.atraso_15m - a.atraso_15m)
    .slice(0, top);

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={topData}>
          <XAxis
            stroke="#ffffff"
            dataKey="aerodromo_destino"
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
