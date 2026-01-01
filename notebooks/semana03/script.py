import numpy as np
import pandas as pd

from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

# Esse script contém funções para realizar splits de dados
# Parti do script_v3 da semana 02 e adaptei para as necessidades da semana 03
# Foco em splits estratificados e temporais
# Quando quiser rodar o notebook não esqueça de considerar as funções do script_v3.py que contém os métodos de carregamento e pré-processamento

TARGET_COL = "atrasado"


# ----------------------------------------------------------------------------#
# Split
# ----------------------------------------------------------------------------#

def criar_split_estratificado(
    df: pd.DataFrame,
    coluna_target: str = TARGET_COL,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split estratificado treino e/ou teste.
    """
    if coluna_target not in df.columns:
        raise ValueError(f"Target '{coluna_target}' não encontrado no DataFrame.")

    df_train, df_test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[coluna_target],
    )
    return df_train, df_test

def criar_split_temporal_train_val_test(
    df: pd.DataFrame,
    time_col: str,
    train_size: float = 0.7,
    val_size: float = 0.1,
):
    """
    Realiza split temporal respeitando a ordem do tempo.
    
    Retorna DataFrames completos (features + target),
    compatíveis com treinar_classificador.
    """
    
    # 1) Garantir ordenação temporal
    df_sorted = (
        df.sort_values(time_col)
          .reset_index(drop=True)
          .copy()
    )

    # 2) Tamanhos dos splits
    n_total = len(df_sorted)
    train_end = int(n_total * train_size)
    val_end = int(n_total * (train_size + val_size))

    # 3) Split respeitando o tempo
    df_train = df_sorted.iloc[:train_end].copy()
    df_val = df_sorted.iloc[train_end:val_end].copy()
    df_test = df_sorted.iloc[val_end:].copy()

    # 4) Sanity check mínimo
    assert df_train[time_col].max() <= df_val[time_col].min(), "Vazamento temporal treino → validação"
    assert df_val[time_col].max() <= df_test[time_col].min(), "Vazamento temporal validação → teste"

    return df_train, df_val, df_test


def criar_split_temporal_train_val_test_mod(
    df: pd.DataFrame,
    time_col: str,
    cutoff_train: str = "2022-12-31",
    cutoff_val: str = "2023-12-31",
):
    """
    Realiza split temporal respeitando datas de corte definidas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame completo com features + target.
    time_col : str
        Nome da coluna datetime usada para ordenação temporal (ex: 'partida_prevista').
    cutoff_train : str
        Data limite do conjunto de treino (formato 'YYYY-MM-DD').
    cutoff_val : str
        Data limite do conjunto de validação (val = cutoff_train < data <= cutoff_val).

    Retorna
    -------
    df_train, df_val, df_test : pd.DataFrame
        DataFrames completos (features + target)
    """

    # Converter os cutoffs para datetime
    cutoff_train = pd.to_datetime(cutoff_train)
    cutoff_val = pd.to_datetime(cutoff_val)

    # Garantir que a coluna de tempo é datetime
    df_sorted = df.copy()
    if not np.issubdtype(df_sorted[time_col].dtype, np.datetime64):
        df_sorted[time_col] = pd.to_datetime(df_sorted[time_col])

    # 1) Split por cutoff
    df_train = df_sorted[df_sorted[time_col] <= cutoff_train].copy()
    df_val   = df_sorted[(df_sorted[time_col] > cutoff_train) & (df_sorted[time_col] <= cutoff_val)].copy()
    df_test  = df_sorted[df_sorted[time_col] > cutoff_val].copy()

    # 2) Sanity checks mínimos
    assert df_train[time_col].max() <= df_val[time_col].min(), "Vazamento temporal treino → validação"
    assert df_val[time_col].max() <= df_test[time_col].min(), "Vazamento temporal validação → teste"


    return df_train, df_val, df_test