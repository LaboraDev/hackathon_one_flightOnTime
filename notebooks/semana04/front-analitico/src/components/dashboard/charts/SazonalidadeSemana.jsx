import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function SazonalidadeSemana({ data }) {
  // Garante que data seja objeto
  const chartData =
    data && typeof data === "object" && !Array.isArray(data)
      ? [
          { dia_semana: "Monday", atraso_15m: data.Monday || 0 },
          { dia_semana: "Tuesday", atraso_15m: data.Tuesday || 0 },
          { dia_semana: "Wednesday", atraso_15m: data.Wednesday || 0 },
          { dia_semana: "Thursday", atraso_15m: data.Thursday || 0 },
          { dia_semana: "Friday", atraso_15m: data.Friday || 0 },
          { dia_semana: "Saturday", atraso_15m: data.Saturday || 0 },
          { dia_semana: "Sunday", atraso_15m: data.Sunday || 0 },
        ]
      : [];

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <XAxis stroke="#ffffff" dataKey="dia_semana" interval={0} />
          <YAxis stroke="#ffffff" />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1a0028",
              border: "1px solid rgba(255,255,255,0.2)",
              borderRadius: "8px",
              color: "#fff",
            }}
            formatter={(value) => [`${value.toFixed(3)}`, "Atraso (15 min)"]}
          />
          <Bar dataKey="atraso_15m" fill="#ff7f0e" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
