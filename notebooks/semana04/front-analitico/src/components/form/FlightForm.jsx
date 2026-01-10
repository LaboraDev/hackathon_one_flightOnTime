import { useState } from "react";
import { initialFormState, validateForm, buildPayload } from "./FormSchema";
import { predictFlightDelay } from "../services/api.js";
import { mapeamentoAmigavel } from "../../constants/mapeamentoAmigavel";
import "../../assets/styles/global.css"; // importar global.css
import "../../assets/styles/FlightForm.css"; // CSS específico para sobreposição e animações

export default function FlightForm() {
  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function formatarExplicacaoLocal(result) {
    return {
      status: result.label === "atrasado" ? "Atraso Provável" : "No Prazo",
      fatores_principais: [
        "Congestionamento elevado no aeroporto de origem",
        "Histórico de pontualidade da companhia aérea",
        "Sazonalidade do tráfego aéreo no horário selecionado",
      ],
    };
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setApiError(null);
    setResult(null);

    const validationErrors = validateForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      const data = await predictFlightDelay(formData);
      setResult({
        label: data.label,
        prediction: data.prediction,
        proba: data.proba_atraso,
      });
    } catch (err) {
      setApiError(err.message || "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flight-form-container">
      <div className="form-overlay">
        <h2 className="form-title">Flight Delay Prediction</h2>
        <form onSubmit={handleSubmit} className="flight-form">
          {Object.keys(formData).map((key) => {
            const fieldInfo = mapeamentoAmigavel[key];

            return (
              <div key={key} className="form-group">
                {/* SELECTS */}
                {key.includes("tipo") || key.includes("situacao") ? (
                  <>
                    <label>
                      {fieldInfo?.label || key.replaceAll("_", " ")}
                    </label>

                    <select
                      name={key}
                      value={formData[key]}
                      onChange={handleChange}
                      required
                    >
                      <option value="" disabled hidden>
                        {fieldInfo?.help || "Selecione uma opção"}
                      </option>

                      {key === "codigo_tipo_linha" && (
                        <>
                          <option value="Regular">Regular</option>
                          <option value="Não Regular">Não Regular</option>
                        </>
                      )}

                      {key === "situacao_voo" && (
                        <>
                          <option value="Realizado">Realizado</option>
                          <option value="Cancelado">Cancelado</option>
                        </>
                      )}
                    </select>
                  </>
                ) : (
                  <>
                    {/* INPUTS */}
                    <label>
                      {fieldInfo?.label || key.replaceAll("_", " ")}
                    </label>

                    <input
                      type={
                        key === "partida_prevista" ? "datetime-local" : "text"
                      }
                      name={key}
                      value={formData[key]}
                      onChange={handleChange}
                      placeholder={fieldInfo?.help || ""}
                      required
                    />
                  </>
                )}

                {/* ERRO DE VALIDAÇÃO */}
                {errors[key] && <span className="error">{errors[key]}</span>}
              </div>
            );
          })}

          <button type="submit" disabled={loading} className="btn-submit">
            {loading ? "Predizendo..." : "Prever atraso"}
          </button>

          {apiError && <p className="error">Erro: {apiError}</p>}

          {result &&
            (() => {
              const explicacao = formatarExplicacaoLocal(result);

              return (
                <div className="prediction-result">
                  <p>
                    <strong>Status do voo:</strong> {explicacao.status}
                  </p>

                  <p>
                    <strong>Probabilidade de atraso:</strong>{" "}
                    {(result.proba * 100).toFixed(2)}%
                  </p>

                  <div className="prob-bar">
                    <div
                      className={
                        result.proba >= 0.5
                          ? "prob-fill red"
                          : "prob-fill green"
                      }
                      style={{ width: `${(result.proba * 100).toFixed(2)}%` }}
                    />
                  </div>

                  {/* EXPLICABILIDADE */}
                  <div className="model-explainability">
                    <p>
                      <strong>
                        Principais fatores considerados pelo modelo:
                      </strong>
                    </p>
                    <ul>
                      {explicacao.fatores_principais.map((fator, index) => (
                        <li key={index}>{fator}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })()}
        </form>
      </div>
    </div>
  );
}
