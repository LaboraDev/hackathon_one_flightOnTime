const API_URL = "http://127.0.0.1:8000"; // base da API

/**
 * Envia dados do voo para predição de atraso
 * @param {Object} flightData - dados do voo conforme o payload da API
 * @returns {Promise<Object>} - resposta da API: prediction, label, proba_atraso
 */
export async function predictFlightDelay(flightData) {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ dados: flightData }),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || "Erro ao chamar a API.");
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error("Erro na predição do voo:", err);
    throw err;
  }
}

/**
 * Exemplo de função para buscar históricos de voos ou métricas
 * @param {string} endpoint - nome do endpoint (ex: "/metrics")
 * @returns {Promise<Object>}
 */
export async function fetchMetrics(endpoint) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`);
    if (!response.ok) throw new Error("Falha ao buscar métricas");
    return await response.json();
  } catch (err) {
    console.error("Erro ao buscar métricas:", err);
    throw err;
  }
}
