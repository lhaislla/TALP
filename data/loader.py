from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = BASE_DIR / "data" / "SWITAB.csv"

SITUACAO_MAP = {
    "Apenas estudando.": "Apenas estudando",
    "Estágio remunerado.": "Estágio remunerado",
    "Trabalho CLT/PJ na área de Tecnologia.": "Trabalho TI (CLT/PJ)",
    "Trabalho fora da área de Tecnologia.": "Trabalho fora de TI",
    "Em busca de recolocação/desempregada.": "Sem ocupação / Em busca",
    "Não possuo trabalho no momento": "Sem ocupação / Em busca",
    "Empreendedora/Freelancer.": "Empreendedora / Freelancer",
}

RENDA_ORDER = [
    "Até 1 salário mínimo.",
    "Entre 1 e 3 salários mínimos.",
    "Entre 3 e 6 salários mínimos.",
    "Acima de 6 salários mínimos.",
]

EXPERIENCIA_ORDER = [
    "Nenhuma experiência.",
    "Menos de 1 ano.",
    "Entre 1 e 3 anos.",
    "Mais de 3 anos.",
]

LIKERT_DESISTENCIA_LABELS = {
    1: "1 - Nunca",
    2: "2 - Raramente",
    3: "3 - Às vezes",
    4: "4 - Frequentemente",
    5: "5 - Quase sempre",
}

LIKERT_PERTENCIMENTO_LABELS = {
    1: "1 - Muito Baixo",
    2: "2 - Baixo",
    3: "3 - Médio",
    4: "4 - Alto",
    5: "5 - Muito Alto",
}


def _padronizar_situacao_prof(valor: object) -> str:
    if pd.isna(valor):
        return "Não informado"
    texto = str(valor).strip()
    if texto in SITUACAO_MAP:
        return SITUACAO_MAP[texto]
    if "estágio" in texto.lower():
        return "Estágio remunerado"
    if "estudando" in texto.lower():
        return "Estudando + Projeto/Extensão"
    return "Outros"


def load_switab_data(csv_path: Path = DEFAULT_CSV_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df["instituicao"] = df["instituicao"].fillna("Não informada").astype(str).str.strip()
    df["curso"] = df["curso"].fillna("Não informado").astype(str).str.strip()
    df["papel"] = df["papel"].fillna("Não informado").astype(str).str.strip()
    df["status"] = df["status"].fillna("NÃO INFORMADO").astype(str).str.strip().str.upper()
    df["turno"] = df["turno"].fillna("Não informado").astype(str).str.strip().str.lower()
    df["etnia"] = df["etnia"].fillna("Não informada").astype(str).str.strip()
    df["renda_familiar"] = df["renda_familiar"].fillna("Não informada").astype(str).str.strip()
    df["experiencia"] = df["experiencia"].fillna("Não informada").astype(str).str.strip()
    df["cidade_padronizada"] = df["cidade_padronizada"].fillna("Não informada").astype(str).str.strip()

    df["sentimento_pertencimento"] = pd.to_numeric(df["sentimento_pertencimento"], errors="coerce")
    df["pensou_em_desistir"] = pd.to_numeric(df["pensou_em_desistir"], errors="coerce")
    df["idade"] = pd.to_numeric(df["idade"], errors="coerce")

    df["situacao_prof_padronizada"] = df["situacao_prof"].apply(_padronizar_situacao_prof)
    df["pertencimento_label"] = df["sentimento_pertencimento"].map(LIKERT_PERTENCIMENTO_LABELS)
    df["desistir_label"] = df["pensou_em_desistir"].map(LIKERT_DESISTENCIA_LABELS)
    df["is_inativa"] = np.where(df["status"] == "INATIVA", 1.0, 0.0)

    if "tipo_instituicao" not in df.columns or df["tipo_instituicao"].isna().all():
        df["tipo_instituicao"] = np.where(
            df["instituicao"].str.lower().isin(["ufpe", "upe", "ufrpe"]),
            "Pública",
            "Privada",
        )

    if "risco_evasao" not in df.columns or df["risco_evasao"].isna().all():
        cond_alto = (df["pensou_em_desistir"] >= 4) & (df["sentimento_pertencimento"] <= 2)
        cond_medio = (~cond_alto) & (
            (df["pensou_em_desistir"] >= 4) | (df["sentimento_pertencimento"] <= 2) | (df["pensou_em_desistir"] == 3)
        )
        df["risco_evasao"] = np.select([cond_alto, cond_medio], ["Alto Risco", "Médio Risco"], default="Baixo Risco")

    return df


def get_filter_options(df: pd.DataFrame) -> dict[str, list[str]]:
    return {
        "instituicoes": sorted(df["instituicao"].dropna().unique().tolist()),
        "cursos": sorted(df["curso"].dropna().unique().tolist()),
        "papeis": sorted(df["papel"].dropna().unique().tolist()),
        "status_list": sorted(df["status"].dropna().unique().tolist()),
        "turnos": sorted(df["turno"].dropna().unique().tolist()),
        "semestres": sorted(df["semestre_entrada"].dropna().astype(str).unique().tolist()),
    }