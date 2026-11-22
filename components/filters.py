from dash import dcc, html


def build_filters_panel(options: dict[str, list[str]]) -> html.Div:
    return html.Div(
        className="filters-panel",
        children=[
            html.Div(
                className="filters-grid",
                children=[
                    html.Div(
                        children=[
                            html.Label("Instituição (IES)", htmlFor="filter-ies", className="filter-label"),
                            dcc.Dropdown(
                                id="filter-ies",
                                options=[{"label": v.upper(), "value": v} for v in options["instituicoes"]],
                                multi=True,
                                placeholder="Todas as IES",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label("Curso", htmlFor="filter-curso", className="filter-label"),
                            dcc.Dropdown(
                                id="filter-curso",
                                options=[{"label": v, "value": v} for v in options["cursos"]],
                                multi=True,
                                placeholder="Todos os cursos",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label("Papel no Projeto", htmlFor="filter-papel", className="filter-label"),
                            dcc.Dropdown(
                                id="filter-papel",
                                options=[{"label": v, "value": v} for v in options["papeis"]],
                                multi=True,
                                placeholder="Todos os papéis",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label("Status", htmlFor="filter-status", className="filter-label"),
                            dcc.Dropdown(
                                id="filter-status",
                                options=[{"label": v, "value": v} for v in options["status_list"]],
                                multi=True,
                                placeholder="Ativa / Inativa",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label("Turno", htmlFor="filter-turno", className="filter-label"),
                            dcc.Dropdown(
                                id="filter-turno",
                                options=[{"label": v.capitalize(), "value": v} for v in options["turnos"]],
                                multi=True,
                                placeholder="Todos os turnos",
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label("Ações", className="filter-label"),
                            html.Button("Limpar filtros", id="btn-reset-filters", n_clicks=0, className="btn-reset"),
                        ]
                    ),
                ],
            )
        ],
    )