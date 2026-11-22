from dash import html
import pandas as pd


def _kpi_card(title: str, value: str, meta: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        children=[
            html.Div(title, className="kpi-title"),
            html.Div(value, className="kpi-value"),
            html.Div(meta, className="kpi-meta"),
        ],
    )


def build_kpi_cards(df: pd.DataFrame) -> html.Div:
    total = len(df)
    if total == 0:
        return html.Div(
            className="kpi-grid",
            children=[
                _kpi_card("Participantes", "0", "Sem registros no filtro atual"),
                _kpi_card("Ativas", "0", "Taxa de retenção: 0,0 pct"),
                _kpi_card("Inativas", "0", "Taxa de inatividade: 0,0 pct"),
                _kpi_card("Alto Risco", "0", "Pertencimento <= 2 e desistência >= 4"),
            ],
        )

    ativas = int((df["status"] == "ATIVA").sum())
    inativas = int((df["status"] == "INATIVA").sum())
    valid_status = ativas + inativas
    taxa_inatividade = (inativas / valid_status * 100.0) if valid_status > 0 else 0.0
    taxa_retencao = (ativas / valid_status * 100.0) if valid_status > 0 else 0.0

    alto_risco = int((df["risco_evasao"] == "Alto Risco").sum())
    pct_alto_risco = alto_risco / total * 100.0

    idade_media = df["idade"].mean()
    idade_txt = f"Idade média: {idade_media:.1f} anos" if pd.notna(idade_media) else "Idade média: N/D"

    return html.Div(
        className="kpi-grid",
        children=[
            _kpi_card("Participantes Filtradas", f"{total}", idade_txt),
            _kpi_card("Participantes Ativas", f"{ativas}", f"Retenção: {taxa_retencao:.1f} pct"),
            _kpi_card("Participantes Inativas", f"{inativas}", f"Inatividade: {taxa_inatividade:.1f} pct"),
            _kpi_card("Alto Risco de Evasão", f"{alto_risco}", f"{pct_alto_risco:.1f} pct do grupo"),
        ],
    )