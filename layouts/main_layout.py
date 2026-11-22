from dash import dcc, html
from components import build_filters_panel, build_kpi_cards
from data import get_filter_options
import pandas as pd


def build_main_layout(df: pd.DataFrame) -> html.Div:
    options = get_filter_options(df)

    return html.Div(
        className="app-container",
        children=[
            html.Header(
                className="app-header",
                children=[
                    html.Div(
                        children=[
                            html.H1(
                                "SWITAB — Análise Visual de Permanência e Perfil",
                                className="app-title",
                            ),
                            html.P(
                                "Disciplina TALP (PPGEC/UPE) • Modelo Aninhado de Tamara Munzner • Base: 202 registros",
                                className="app-subtitle",
                            ),
                        ]
                    ),
                    html.Div(
                        className="app-subtitle",
                        children="Pesquisa: padrões demográficos, acadêmicos e socioeconômicos para permanência acadêmica",
                    ),
                ],
            ),
            build_filters_panel(options),
            html.Div(id="kpi-container", children=build_kpi_cards(df)),
            dcc.Tabs(
                id="chart-tabs",
                value="permanencia",
                className="charts-tabs",
                children=[
                    dcc.Tab(
                        label="Permanência e evasão",
                        value="permanencia",
                        children=[
                            html.Div(
                                className="charts-grid",
                                children=[
                                    html.Div(className="chart-card full-width", children=[dcc.Graph(id="fig-pertencimento-desistir")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-inatividade-turno")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-inatividade-curso")]),
                                    html.Div(className="chart-card full-width", children=[dcc.Graph(id="fig-status-curso-100")]),
                                    html.Div(className="chart-card full-width", children=[dcc.Graph(id="fig-desistir-experiencia-100")]),
                                ],
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Participação acadêmica",
                        value="participacao",
                        children=[
                            html.Div(
                                className="charts-grid",
                                children=[
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-papeis-ies")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-cursos-papel-100")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-sunburst-ies-curso-status")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-treemap-ies-curso-papel")]),
                                ],
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Perfil socioeconômico",
                        value="perfil",
                        children=[
                            html.Div(
                                className="charts-grid",
                                children=[
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-trabalho-renda")]),
                                    html.Div(className="chart-card", children=[dcc.Graph(id="fig-etnia-ies")]),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )