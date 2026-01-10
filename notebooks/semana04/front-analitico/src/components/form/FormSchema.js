/**
 * Schema do formulário de entrada do voo
 * Responsável por:
 * - Definir valores iniciais
 * - Validar campos
 * - Montar o payload conforme contrato da API
 */

export const initialFormState = {
  partida_prevista: "",
  empresa_aerea: "",
  codigo_tipo_linha: "",
  aerodromo_origem: "",
  aerodromo_destino: "",
  situacao_voo: "",
};

/**
 * Validação simples e explícita
 */
export function validateForm(formData) {
  const errors = {};

  if (!formData.partida_prevista) {
    errors.partida_prevista =
      "Data e hora da partida prevista são obrigatórias.";
  }

  if (!formData.empresa_aerea) {
    errors.empresa_aerea = "Empresa aérea é obrigatória.";
  }

  if (!formData.codigo_tipo_linha) {
    errors.codigo_tipo_linha = "Tipo de linha é obrigatório.";
  }

  if (!formData.aerodromo_origem) {
    errors.aerodromo_origem = "Aeródromo de origem é obrigatório.";
  }

  if (!formData.aerodromo_destino) {
    errors.aerodromo_destino = "Aeródromo de destino é obrigatório.";
  }

  if (!formData.situacao_voo) {
    errors.situacao_voo = "Situação do voo é obrigatória.";
  }

  if (
    formData.aerodromo_origem &&
    formData.aerodromo_destino &&
    formData.aerodromo_origem === formData.aerodromo_destino
  ) {
    errors.aerodromo_destino =
      "O aeródromo de destino deve ser diferente do aeródromo de origem.";
  }

  return errors;
}

/**
 * Monta o payload final para envio à API
 */
export function buildPayload(formData) {
  return {
    dados: {
      partida_prevista: formData.partida_prevista,
      empresa_aerea: formData.empresa_aerea,
      codigo_tipo_linha: formData.codigo_tipo_linha,
      aerodromo_origem: formData.aerodromo_origem,
      aerodromo_destino: formData.aerodromo_destino,
      situacao_voo: formData.situacao_voo,
    },
  };
}
