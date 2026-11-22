from dash import Dash, Input, Output
import pandas as pd
from components import (
    build_kpi_cards,
    chart_pertencimento_vs_desistir,
    chart_papeis_por_ies,
    chart_cursos_por_papel_100,
    chart_inatividade_por_turno,
    chart_inatividade_por_curso,
    chart_status_por_curso_100,
    chart_sunburst_ies_curso_status,
    chart_treemap_ies_curso_papel,
    chart_trabalho_por_renda,
    chart_etnia_por_ies,
    chart_desistir_por_experiencia_100,
)


def _apply_filters(
    df: pd.DataFrame,
    ies_list: list[str] | None,
    cursos: list[str] | None,
    papeis: list[str] | None,
    status_list: list[str] | None,
    turnos: list[str] | None,
) -> pd.DataFrame:
    filtered = df.copy()
    if ies_list:
        filtered = filtered[filtered["instituicao"].isin(ies_list)]
    if cursos:
        filtered = filtered[filtered["curso"].isin(cursos)]
    if papeis:
        filtered = filtered[filtered["papel"].isin(papeis)]
    if status_list:
        filtered = filtered[filtered["status"].isin(status_list)]
    if turnos:
        filtered = filtered[filtered["turno"].isin(turnos)]
    return filtered


def register_callbacks(app: Dash, df: pd.DataFrame) -> None:
    @app.callback(
        Output("filter-ies", "value"),
        Output("filter-curso", "value"),
        Output("filter-papel", "value"),
        Output("filter-status", "value"),
        Output("filter-turno", "value"),
        Input("btn-reset-filters", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_filters(_n_clicks: int):
        return None, None, None, None, None

    @app.callback(
        Output("kpi-container", "children"),
        Output("fig-pertencimento-desistir", "figure"),
        Output("fig-papeis-ies", "figure"),
        Output("fig-cursos-papel-100", "figure"),
        Output("fig-inatividade-turno", "figure"),
        Output("fig-inatividade-curso", "figure"),
        Output("fig-status-curso-100", "figure"),
        Output("fig-sunburst-ies-curso-status", "figure"),
        Output("fig-treemap-ies-curso-papel", "figure"),
        Output("fig-trabalho-renda", "figure"),
        Output("fig-etnia-ies", "figure"),
        Output("fig-desistir-experiencia-100", "figure"),
        Input("filter-ies", "value"),
        Input("filter-curso", "value"),
        Input("filter-papel", "value"),
        Input("filter-status", "value"),
        Input("filter-turno", "value"),
    )
    def update_dashboard(ies_list, cursos, papeis, status_list, turnos):
        filtered = _apply_filters(df, ies_list, cursos, papeis, status_list, turnos)

        return (
            build_kpi_cards(filtered),
            chart_pertencimento_vs_desistir(filtered),
            chart_papeis_por_ies(filtered),
            chart_cursos_por_papel_100(filtered),
            chart_inatividade_por_turno(filtered),
            chart_inatividade_por_curso(filtered),
            chart_status_por_curso_100(filtered),
            chart_sunburst_ies_curso_status(filtered),
            chart_treemap_ies_curso_papel(filtered),
            chart_trabalho_por_renda(filtered),
            chart_etnia_por_ies(filtered),
            chart_desistir_por_experiencia_100(filtered),
        )