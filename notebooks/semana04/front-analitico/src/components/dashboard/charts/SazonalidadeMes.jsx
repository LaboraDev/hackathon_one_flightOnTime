import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function SazonalidadeMes({ data }) {
  // Garante que data seja array
  const chartData = Array.isArray(data) ? data : [];

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <XAxis
            stroke="#ffffff"
            dataKey="hora_dia"
            interval={0}
            angle={-35}
            textAnchor="end"
            height={60}
            tickFormatter={(tick) => `${tick}h`} // Ex: 0h, 1h, 2h...
          />
          <YAxis stroke="#ffffff" />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1a0028",
              border: "1px solid rgba(255,255,255,0.2)",
              borderRadius: "8px",
              color: "#fff",
            }}
            formatter={(value) => [`${value.toFixed(2)}`, "Atraso (15 min)"]}
          />
          <Bar dataKey="atraso_15m" fill="#ff7a18" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
