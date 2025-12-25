import os
import glob
import zipfile
import pandas as pd
import numpy as np
from typing import Tuple

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import pickle

# Funcões de ETL

def baixar_e_extrair_dados(zip_path: str, extract_folder: str, file_id: str) -> None:
    """
    Baixa o arquivo .zip do Google Drive (se ainda não existir)
    e extrai o conteúdo para uma pasta.

    Parâmetros
    ----------
    zip_path : str
        Caminho onde o arquivo .zip será salvo.
    extract_folder : str
        Pasta onde os arquivos serão extraídos.
    file_id : str
        ID do arquivo no Google Drive.
    """
    import gdown  # import local para evitar erro se não for usar em outro ambiente

    if not os.path.exists(zip_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, zip_path, quiet=False)

    if not os.path.exists(extract_folder):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_folder)


def carregar_vra(pasta: str,
                 padrao: str = "VRA_*.csv",
                 sep: str = ";",
                 encoding: str = "latin-1",
                 skiprows: int = 1) -> pd.DataFrame:
    """
    Carrega todos os arquivos VRA_*.csv de uma pasta e concatena
    em um único DataFrame.

    Retorna
    -------
    DataFrame com todos os voos concatenados.
    """
    caminho_busca = os.path.join(pasta, padrao)
    arquivos = sorted(glob.glob(caminho_busca))

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em {caminho_busca}")

    dfs = []
    for arquivo in arquivos:
        df_temp = pd.read_csv(arquivo, sep=sep, encoding=encoding, skiprows=skiprows)
        dfs.append(df_temp)

    df_final = pd.concat(dfs, ignore_index=True)
    return df_final




def renomear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes das colunas para snake_case em português simples.
    """
    df = df.copy()

    # Garante que acentos sejam lidos corretamente
    df.columns = [c.encode("latin1").decode("utf-8") for c in df.columns]

    mapa_colunas = {
        "ICAO Empresa Aérea": "empresa_aerea",
        "Número Voo": "numero_voo",
        "Código Autorização (DI)": "codigo_autorizacao_di",
        "Código Tipo Linha": "codigo_tipo_linha",
        "ICAO Aeródromo Origem": "aerodromo_origem",
        "ICAO Aeródromo Destino": "aerodromo_destino",
        "Partida Prevista": "partida_prevista",
        "Partida Real": "partida_real",
        "Chegada Prevista": "chegada_prevista",
        "Chegada Real": "chegada_real",
        "Situação Voo": "situacao_voo",
        "Código Justificativa": "codigo_justificativa",
    }

    df = df.rename(columns=mapa_colunas)
    return df


def criar_flags_qualidade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria flags de qualidade para datas inválidas e períodos extremos.

    - Converte 'partida_prevista' e 'partida_real' para datetime.
    - Marca linhas com datas fora do período esperado.
    - Marca voos com diferença de horário muito alta (> 24h).
    """
    df = df.copy()

    df["partida_prevista"] = pd.to_datetime(
        df["partida_prevista"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )
    df["partida_real"] = pd.to_datetime(
        df["partida_real"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    df["flag_partida_prevista_ausente"] = df["partida_prevista"].isna()
    df["flag_partida_real_ausente"] = df["partida_real"].isna()
    df["flag_aerodromo_origem_ausente"] = df["aerodromo_origem"].isna()

    df["flag_data_partida_fora_periodo"] = (
        df["partida_prevista"].notna()
        & (
            (df["partida_prevista"].dt.year < 2021)
            | (df["partida_prevista"].dt.year > 2025)
        )
    )

    limite_horas = 24
    delta_h = (df["partida_real"] - df["partida_prevista"]).dt.total_seconds() / 3600
    df["flag_partida_muito_alto"] = (
        df["partida_prevista"].notna()
        & df["partida_real"].notna()
        & (delta_h.abs() > limite_horas)
    )

    return df



# Funções de Features

def criar_target_atrasado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a coluna 'atrasado' (0 = pontual, 1 = atraso > 15 minutos).

    - Calcula 'atraso_partida_min' (diferença entre partida_real e partida_prevista).
    - Filtra linhas inválidas com base nas flags de qualidade.
    - Cria a coluna binária 'atrasado'.
    """
    df = df.copy()

    df["atraso_partida_min"] = (
        (df["partida_real"] - df["partida_prevista"]).dt.total_seconds() / 60
    )

    filtros_validos = (
        ~df["flag_partida_prevista_ausente"]
        & ~df["flag_partida_real_ausente"]
        & ~df["flag_data_partida_fora_periodo"]
        & ~df["flag_partida_muito_alto"]
    )

    df = df[filtros_validos].copy()
    df["atrasado"] = (df["atraso_partida_min"] > 15).astype(int)

    return df


def criar_features_temporais(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hora_dia"] = df["partida_prevista"].dt.hour
    df["dia_semana"] = df["partida_prevista"].dt.dayofweek
    df["mes_ano"] = df["partida_prevista"].dt.month

    def classificar_periodo(hora: int) -> str:
        if 5 <= hora < 12: return "Manha"
        if 12 <= hora < 18: return "Tarde"
        if 18 <= hora < 22: return "Noite"
        return "Madrugada"

    df["periodo_dia"] = df["hora_dia"].apply(classificar_periodo)
    df["fim_de_semana"] = df["dia_semana"].isin([4, 5, 6]).astype(int)
    df["alta_temporada"] = df["mes_ano"].isin([7, 12]).astype(int)

    # --- NOVO (Requisito DS2): Transformações Log e Caps ---
    df["atraso_log"] = np.log1p(np.maximum(df["atraso_partida_min"], 0))
    df["atraso_capped"] = np.clip(df["atraso_partida_min"], 0, 120)

    return df


class FeaturesTemporaisCiclicas(BaseEstimator, TransformerMixin):
    """
    Cria features temporais cíclicas a partir de 'partida_prevista':
    - hora_sin, hora_cos (período 24)
    - dow_sin, dow_cos (período 7)
    - mes_sin, mes_cos (período 12)

    Isso ajuda modelos lineares a entender que 23h é próximo de 0h, etc.
    """

    def __init__(self, coluna_datetime=COL_PARTIDA):
        self.coluna_datetime = coluna_datetime

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        dt = pd.to_datetime(X[self.coluna_datetime], errors="coerce")

        # Hora
        hora = dt.dt.hour.fillna(0).astype(int)
        X["hora_sin"] = np.sin(2 * np.pi * hora / 24)
        X["hora_cos"] = np.cos(2 * np.pi * hora / 24)

        # Dia da semana
        dow = dt.dt.dayofweek.fillna(0).astype(int)
        X["dow_sin"] = np.sin(2 * np.pi * dow / 7)
        X["dow_cos"] = np.cos(2 * np.pi * dow / 7)

        # Mês (1-12 -> 0-11)
        mes = (dt.dt.month.fillna(1).astype(int) - 1)
        X["mes_sin"] = np.sin(2 * np.pi * mes / 12)
        X["mes_cos"] = np.cos(2 * np.pi * mes / 12)

        return X


class MediaHistoricaAtrasoPorCategoria(BaseEstimator, TransformerMixin):
    """
    Para colunas com MUITAS categorias (empresa e aeródromos):
    - No fit: aprende a média do TARGET por categoria (usando apenas treino)
    - No transform: cria novas colunas numéricas com fallback na média global

    Exemplo:
      empresa_aerea="AZU" -> media_atraso_empresa_aerea=12.3
    """

    def __init__(self, colunas_categoricas, nome_target=TARGET):
        self.colunas_categoricas = colunas_categoricas
        self.nome_target = nome_target

        self.media_global_ = None
        self.mapas_ = {}

    def fit(self, X, y):
        y = pd.Series(y)
        self.media_global_ = float(y.mean())

        X_ = X.copy()

        # Para cada coluna, cria um dicionário: categoria -> media do atraso
        for col in self.colunas_categoricas:
            # Usando groupby com y alinhado pelo índice (sem vazamento se X for treino)
            medias = y.groupby(X_[col]).mean()
            self.mapas_[col] = medias.to_dict()

        return self

    def transform(self, X):
        X = X.copy()

        for col in self.colunas_categoricas:
            nova = f"media_atraso_{col}"
            X[nova] = X[col].map(self.mapas_[col]).fillna(self.media_global_)

        return X



class MediaAtrasoTransformer(BaseEstimator, TransformerMixin):
    """
    Cria três features numéricas com médias de atraso (em minutos):

    - media_atraso_empresa
    - media_atraso_origem
    - media_atraso_destino

    Importante:
    - Usa 'atraso_partida_min' apenas no treino (fit).
    - Na produção, o transformer reutiliza as médias aprendidas.
    """

    def __init__(self) -> None:
        self.medias_empresa = {}
        self.medias_origem = {}
        self.medias_destino = {}
        self.media_global = 0.0

    def fit(self, X: pd.DataFrame, y=None):
        # Calcula médias por empresa, origem e destino
        self.medias_empresa = (
            X.groupby("empresa_aerea")["atraso_partida_min"].mean().to_dict()
        )
        self.medias_origem = (
            X.groupby("aerodromo_origem")["atraso_partida_min"].mean().to_dict()
        )
        self.medias_destino = (
            X.groupby("aerodromo_destino")["atraso_partida_min"].mean().to_dict()
        )
        self.media_global = float(X["atraso_partida_min"].mean())
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        X["media_atraso_empresa"] = (
            X["empresa_aerea"].map(self.medias_empresa).fillna(self.media_global)
        )
        X["media_atraso_origem"] = (
            X["aerodromo_origem"].map(self.medias_origem).fillna(self.media_global)
        )
        X["media_atraso_destino"] = (
            X["aerodromo_destino"].map(self.medias_destino).fillna(self.media_global)
        )

        return X


# Funções de Amostragem

def criar_amostra_estratificada(
    df: pd.DataFrame,
    coluna_target: str = "atrasado",
    frac: float = 0.1,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Cria uma amostra estratificada simples, mantendo a proporção de atrasos.

    Parâmetros
    ----------
    frac : float
        Fração desejada (ex: 0.1 = 10% da base).
    """
    df_amostra, _ = train_test_split(
        df,
        test_size=1 - frac,
        random_state=random_state,
        stratify=df[coluna_target],
    )
    return df_amostra



def criar_split_estratificado(
    df: pd.DataFrame,
    coluna_target: str = "atrasado",
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cria um split estratificado em treino e teste, mantendo a proporção do target.

    Parâmetros
    ----------
    test_size : float
        Proporção do conjunto de teste (ex: 0.2 = 20%).
    """
    df_train, df_test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[coluna_target],
    )

    return df_train, df_test



# Funções de Transformação

def montar_pipeline_preprocessamento():
    """
    Cria o pipeline de pré-processamento com:
    - Imputação de nulos para numéricas (mediana) + StandardScaler
    - Imputação de nulos para categóricas (DESCONHECIDO) + OrdinalEncoder
    """
    numeric_features_final = NUMERIC_FEATURES_BASE + [
        "media_atraso_empresa",
        "media_atraso_origem",
        "media_atraso_destino",
    ]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="constant", fill_value="DESCONHECIDO"),
            ),
            (
                "encoder",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features_final),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )

    return preprocessor

import json

def realizar_analise_impacto(X_proc, y_val, nomes_colunas):
    """Gera o relatório de impacto das features (DS2)."""
    df_temp = pd.DataFrame(X_proc, columns=nomes_colunas)
    correlacao = df_temp.corrwith(pd.Series(y_val)).abs().sort_values(ascending=False)
    print("\n--- TOP 5 FEATURES POR IMPACTO ---")
    print(correlacao.head(5))

def salvar_documentacao_json(arquivo="documentacao_ds1_ds2.json"):
    """Cria o registro das features para o time de integração."""
    dados_doc = {
        "features": ["hora_dia", "mes_ano", "atraso_log", "atraso_capped", "media_atraso_empresa"],
        "target": "atrasado (1 para atraso > 15min)",
        "responsaveis": "Equipe DS1 e DS2"
    }
    with open(arquivo, "w") as f:
        json.dump(dados_doc, f, indent=4)



