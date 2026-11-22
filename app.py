from dash import Dash
from dashboard.callbacks import register_callbacks
from data import load_switab_data
from layouts.main_layout import build_main_layout


def create_app() -> Dash:
    df = load_switab_data()
    app = Dash(__name__, title="SWITAB — Visualização de Dados (TALP)")
    app.layout = build_main_layout(df)
    register_callbacks(app, df)
    return app


app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=True)