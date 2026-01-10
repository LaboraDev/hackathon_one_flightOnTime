import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./assets/styles/global.css"; // <-- importa o CSS global
import "./assets/styles/FlightForm.css"; // CSS específico para sobreposição e animações
import "./assets/styles/layout.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
