import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

LIKERT_COLORS = {
    "1 - Nunca": "#15803d",
    "2 - Raramente": "#86efac",
    "3 - Às vezes": "#fde047",
    "4 - Frequentemente": "#fb923c",
    "5 - Quase sempre": "#b91c1c",
}

PAPEL_COLORS = {
    "Embaixadora": "#3b0764",
    "Mentora": "#db2777",
    "Mentorada": "#f9a8d4",
    "nao iniciou no projeto": "#94a3b8",
    "Não informado": "#cbd5e1",
}

STATUS_COLORS = {
    "ATIVA": "#15803d",
    "INATIVA": "#9f1239",
    "NÃO INFORMADO": "#94a3b8",
}

ETNIA_COLORS = {
    "Branca": "#fbcfe8",
    "Parda": "#f472b6",
    "Preta": "#9d174d",
    "Amarela": "#4c1d95",
    "Não informada": "#cbd5e1",
}


def _empty_fig(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[
            {
                "text": "Sem dados disponíveis para os filtros selecionados.",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 13, "color": "#64748b"},
            }
        ],
        template="plotly_white",
        height=380,
    )
    return fig


def chart_pertencimento_vs_desistir(df: pd.DataFrame) -> go.Figure:
    sub = df.dropna(subset=["sentimento_pertencimento", "pensou_em_desistir"]).copy()
    if sub.empty:
        return _empty_fig("Pertencimento vs. Frequência de Pensamento em Desistir")

    sub["pert_num"] = sub["sentimento_pertencimento"].astype(int)
    sub["des_num"] = sub["pensou_em_desistir"].astype(int)
    sub["pert_label"] = sub["pert_num"].map(
        {
            1: "1 - Muito Baixo",
            2: "2 - Baixo",
            3: "3 - Médio",
            4: "4 - Alto",
            5: "5 - Muito Alto",
        }
    )
    sub["des_label"] = sub["des_num"].map(
        {
            1: "1 - Nunca",
            2: "2 - Raramente",
            3: "3 - Às vezes",
            4: "4 - Frequentemente",
            5: "5 - Quase sempre",
        }
    )

    agg = (
        sub.groupby(["pert_num", "pert_label", "des_num", "des_label"], as_index=False)
        .size()
        .rename(columns={"size": "qtd"})
    )
    totais = agg.groupby("pert_num")["qtd"].transform("sum")
    agg["pct"] = agg["qtd"] / totais * 100.0
    agg = agg.sort_values(["pert_num", "des_num"])

    fig = px.bar(
        agg,
        x="pct",
        y="pert_label",
        color="des_label",
        orientation="h",
        category_orders={
            "pert_label": [
                "1 - Muito Baixo",
                "2 - Baixo",
                "3 - Médio",
                "4 - Alto",
                "5 - Muito Alto",
            ],
            "des_label": [
                "1 - Nunca",
                "2 - Raramente",
                "3 - Às vezes",
                "4 - Frequentemente",
                "5 - Quase sempre",
            ],
        },
        color_discrete_map=LIKERT_COLORS,
        custom_data=["qtd", "pct"],
        title="Sentimento de Pertencimento vs. Pensamento em Desistir (100%)",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Desistir: %{fullData.name}<br>Proporção: %{customdata[1]:.1f} pct (n=%{customdata[0]})<extra></extra>"
    )
    fig.update_layout(
        barmode="stack",
        xaxis_title="Proporção de Alunas (pct)",
        yaxis_title="Sentimento de Pertencimento",
        legend_title="Pensou em Desistir",
        template="plotly_white",
        height=390,
    )
    return fig


def chart_papeis_por_ies(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Distribuição dos Papéis por IES")

    agg = df.groupby(["instituicao", "papel"], as_index=False).size().rename(columns={"size": "qtd"})
    ordem_ies = (
        agg.groupby("instituicao")["qtd"]
        .sum()
        .sort_values(ascending=True)
        .index.tolist()
    )

    fig = px.bar(
        agg,
        x="qtd",
        y="instituicao",
        color="papel",
        barmode="group",
        orientation="h",
        category_orders={"instituicao": ordem_ies},
        color_discrete_map=PAPEL_COLORS,
        title="Distribuição dos Papéis das Participantes por IES",
    )
    fig.update_layout(
        xaxis_title="Número de Participantes",
        yaxis_title="Instituição de Ensino (IES)",
        legend_title="Papel no Projeto",
        template="plotly_white",
        height=390,
    )
    return fig


def chart_cursos_por_papel_100(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Proporção de Papéis por Curso Acadêmico")

    agg = df.groupby(["curso", "papel"], as_index=False).size().rename(columns={"size": "qtd"})
    totais = agg.groupby("curso")["qtd"].transform("sum")
    agg["pct"] = agg["qtd"] / totais * 100.0
    ordem_cursos = agg.groupby("curso")["qtd"].sum().sort_values(ascending=True).index.tolist()

    fig = px.bar(
        agg,
        x="pct",
        y="curso",
        color="papel",
        barmode="stack",
        orientation="h",
        category_orders={"curso": ordem_cursos},
        color_discrete_map=PAPEL_COLORS,
        custom_data=["qtd", "pct"],
        title="Distribuição Proporcional dos Papéis por Curso (100%)",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Papel: %{fullData.name}<br>Proporção: %{customdata[1]:.1f} pct (n=%{customdata[0]})<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Proporção de Participantes (pct)",
        yaxis_title="Curso Acadêmico",
        legend_title="Papel",
        template="plotly_white",
        height=410,
    )
    return fig


def _dot_plot_inatividade(df: pd.DataFrame, group_col: str, title: str, y_label: str) -> go.Figure:
    valid = df[df["status"].isin(["ATIVA", "INATIVA"])]
    if valid.empty:
        return _empty_fig(title)

    agg = (
        valid.groupby(group_col, as_index=False)
        .agg(total=("status", "count"), inativas=("is_inativa", "sum"))
    )
    agg["taxa_inatividade"] = agg["inativas"] / agg["total"] * 100.0
    agg = agg.sort_values("taxa_inatividade", ascending=True)

    fig = go.Figure()
    for _, row in agg.iterrows():
        fig.add_shape(
            type="line",
            x0=0,
            x1=row["taxa_inatividade"],
            y0=row[group_col],
            y1=row[group_col],
            line={"color": "#94a3b8", "width": 2},
        )

    fig.add_trace(
        go.Scatter(
            x=agg["taxa_inatividade"],
            y=agg[group_col],
            mode="markers",
            marker={"size": 11, "color": "#9d174d"},
            customdata=agg[["inativas", "total"]],
            hovertemplate="<b>%{y}</b><br>Inatividade: %{x:.1f} pct (%{customdata[0]:.0f}/%{customdata[1]:.0f})<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Taxa de Inatividade (pct)",
        yaxis_title=y_label,
        xaxis={"range": [0, max(35.0, float(agg["taxa_inatividade"].max()) + 5.0)]},
        showlegend=False,
        template="plotly_white",
        height=390,
    )
    return fig


def chart_inatividade_por_turno(df: pd.DataFrame) -> go.Figure:
    return _dot_plot_inatividade(
        df,
        group_col="turno",
        title="Taxa de Inatividade por Turno Acadêmico",
        y_label="Turno Acadêmico",
    )


def chart_inatividade_por_curso(df: pd.DataFrame) -> go.Figure:
    return _dot_plot_inatividade(
        df,
        group_col="curso",
        title="Taxa de Inatividade por Curso Acadêmico",
        y_label="Curso",
    )


def chart_status_por_curso_100(df: pd.DataFrame) -> go.Figure:
    valid = df[df["status"].isin(["ATIVA", "INATIVA"])]
    if valid.empty:
        return _empty_fig("Proporção de Alunas Ativas vs. Inativas por Curso")

    agg = valid.groupby(["curso", "status"], as_index=False).size().rename(columns={"size": "qtd"})
    totais = agg.groupby("curso")["qtd"].transform("sum")
    agg["pct"] = agg["qtd"] / totais * 100.0

    inativas_pct = (
        agg[agg["status"] == "INATIVA"]
        .set_index("curso")["pct"]
        .reindex(agg["curso"].unique(), fill_value=0.0)
        .sort_values(ascending=True)
    )
    ordem_cursos = inativas_pct.index.tolist()

    fig = px.bar(
        agg,
        x="pct",
        y="curso",
        color="status",
        barmode="stack",
        orientation="h",
        category_orders={"curso": ordem_cursos, "status": ["ATIVA", "INATIVA"]},
        color_discrete_map=STATUS_COLORS,
        custom_data=["qtd", "pct"],
        title="Proporção de Alunas Ativas vs. Inativas por Curso (100%)",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Status: %{fullData.name}<br>Proporção: %{customdata[1]:.1f} pct (n=%{customdata[0]})<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Proporção (pct)",
        yaxis_title="Curso",
        legend_title="Status",
        template="plotly_white",
        height=410,
    )
    return fig


def chart_sunburst_ies_curso_status(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Hierarquia de Participação: IES, Curso e Status (Sunburst)")

    agg = df.groupby(["instituicao", "curso", "status"], as_index=False).size().rename(columns={"size": "qtd"})
    fig = px.sunburst(
        agg,
        path=["instituicao", "curso", "status"],
        values="qtd",
        color="status",
        color_discrete_map=STATUS_COLORS,
        title="Hierarquia de Participação: IES, Curso e Status",
    )
    fig.update_layout(template="plotly_white", height=440)
    return fig


def chart_treemap_ies_curso_papel(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Hierarquia Proporcional: IES, Curso e Papel (Treemap)")

    agg = df.groupby(["instituicao", "curso", "papel"], as_index=False).size().rename(columns={"size": "qtd"})
    fig = px.treemap(
        agg,
        path=["instituicao", "curso", "papel"],
        values="qtd",
        color="papel",
        color_discrete_map=PAPEL_COLORS,
        title="Hierarquia Proporcional: IES, Curso e Papel",
    )
    fig.update_layout(template="plotly_white", height=440)
    return fig


def chart_trabalho_por_renda(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Situação de Trabalho por Faixa de Renda Familiar")

    agg = (
        df.groupby(["renda_familiar", "situacao_prof_padronizada"], as_index=False)
        .size()
        .rename(columns={"size": "qtd"})
    )
    fig = px.bar(
        agg,
        x="renda_familiar",
        y="qtd",
        color="situacao_prof_padronizada",
        barmode="group",
        category_orders={"renda_familiar": [r for r in ["Até 1 salário mínimo.", "Entre 1 e 3 salários mínimos.", "Entre 3 e 6 salários mínimos.", "Acima de 6 salários mínimos."] if r in agg["renda_familiar"].unique()]},
        title="Situação de Trabalho Remunerado por Faixa de Renda Familiar",
    )
    fig.update_layout(
        xaxis_title="Faixa de Renda Familiar",
        yaxis_title="Número de Participantes",
        legend_title="Situação Profissional",
        template="plotly_white",
        height=400,
    )
    return fig


def chart_etnia_por_ies(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_fig("Composição Étnico-Racial por IES")

    agg = df.groupby(["instituicao", "etnia"], as_index=False).size().rename(columns={"size": "qtd"})
    ordem_ies = agg.groupby("instituicao")["qtd"].sum().sort_values(ascending=True).index.tolist()

    fig = px.bar(
        agg,
        x="qtd",
        y="instituicao",
        color="etnia",
        barmode="stack",
        orientation="h",
        category_orders={"instituicao": ordem_ies, "etnia": ["Branca", "Parda", "Preta", "Amarela", "Não informada"]},
        color_discrete_map=ETNIA_COLORS,
        title="Composição Étnico-Racial das Participantes por IES",
    )
    fig.update_layout(
        xaxis_title="Número de Participantes",
        yaxis_title="Instituição de Ensino",
        legend_title="Etnia",
        template="plotly_white",
        height=390,
    )
    return fig


def chart_desistir_por_experiencia_100(df: pd.DataFrame) -> go.Figure:
    sub = df.dropna(subset=["pensou_em_desistir"]).copy()
    if sub.empty:
        return _empty_fig("Pensamento em Desistir Conforme Experiência Prévia")

    sub["des_num"] = sub["pensou_em_desistir"].astype(int)
    sub["des_label"] = sub["des_num"].map(
        {
            1: "1 - Nunca",
            2: "2 - Raramente",
            3: "3 - Às vezes",
            4: "4 - Frequentemente",
            5: "5 - Quase sempre",
        }
    )

    agg = sub.groupby(["experiencia", "des_num", "des_label"], as_index=False).size().rename(columns={"size": "qtd"})
    totais = agg.groupby("experiencia")["qtd"].transform("sum")
    agg["pct"] = agg["qtd"] / totais * 100.0
    agg = agg.sort_values("des_num")

    ordem_exp = [e for e in ["Mais de 3 anos.", "Entre 1 e 3 anos.", "Menos de 1 ano.", "Nenhuma experiência."] if e in agg["experiencia"].unique()]
    restantes = [e for e in agg["experiencia"].unique() if e not in ordem_exp]
    ordem_exp = ordem_exp + restantes

    fig = px.bar(
        agg,
        x="pct",
        y="experiencia",
        color="des_label",
        barmode="stack",
        orientation="h",
        category_orders={
            "experiencia": ordem_exp,
            "des_label": [
                "1 - Nunca",
                "2 - Raramente",
                "3 - Às vezes",
                "4 - Frequentemente",
                "5 - Quase sempre",
            ],
        },
        color_discrete_map=LIKERT_COLORS,
        custom_data=["qtd", "pct"],
        title="Frequência de Pensamento em Desistir por Experiência Prévia (100%)",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Desistir: %{fullData.name}<br>Proporção: %{customdata[1]:.1f} pct (n=%{customdata[0]})<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Proporção de Alunas (pct)",
        yaxis_title="Experiência Prévia em Programação",
        legend_title="Pensou em Desistir",
        template="plotly_white",
        height=390,
    )
    return fig