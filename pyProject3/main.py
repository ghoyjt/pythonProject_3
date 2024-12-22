from typing import List, Dict, Any
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objs as go

from accuweather_api import fetch_location_info, fetch_forecast_for_days
from forecast_parser import parse_daily_forecast
from map_utils import build_map_figure


app: Dash = Dash(__name__)
app.title = "Weather with Map App"


app.layout = html.Div([
    html.H1("Прогноз погоды и карта маршрута", style={"textAlign": "center"}),

    html.Div([
        html.Label("Введите города (через запятую):"),
        dcc.Input(
            id="cities-input",
            type="text",
            value="Moscow, Saint Petersburg",
            style={"width": "70%"}
        ),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Срок прогноза (дней):"),
        dcc.RadioItems(
            id="days-radio",
            options=[
                {"label": "1 день", "value": 1},
                {"label": "3 дня", "value": 3},
                {"label": "5 дней", "value": 5},
            ],
            value=3,
            labelStyle={"display": "inline-block", "marginRight": "10px"}
        ),
    ], style={"marginBottom": "20px"}),

    html.Button("Показать прогноз", id="submit-button", n_clicks=0),

    dcc.Loading(
        id="loading-container",
        type="circle",
        children=html.Div(id="results-container", style={"marginTop": "30px"})
    )
], style={"width": "80%", "margin": "0 auto"})


@app.callback(
    Output("results-container", "children"),
    Input("submit-button", "n_clicks"),
    State("cities-input", "value"),
    State("days-radio", "value")
)
def update_forecast(n_clicks: int, cities_value: str, days_value: int):
    if n_clicks < 1:
        return html.Div("Пока ничего не загружено. Нажмите кнопку.")

    city_list: List[str] = [c.strip() for c in cities_value.split(",") if c.strip()]

    map_locations: List[Dict[str, Any]] = []
    graphs = []

    for city in city_list:
        try:
            loc_info = fetch_location_info(city)
            map_locations.append({
                "name": loc_info["name"],
                "lat": loc_info["lat"],
                "lon": loc_info["lon"]
            })

            forecast_data = fetch_forecast_for_days(loc_info["key"], days_value)
            parsed = parse_daily_forecast(forecast_data)

            trace_min = go.Scatter(
                x=parsed["dates"],
                y=parsed["min_temps"],
                mode="lines+markers",
                name="Min Temp (°C)"
            )
            trace_max = go.Scatter(
                x=parsed["dates"],
                y=parsed["max_temps"],
                mode="lines+markers",
                name="Max Temp (°C)"
            )
            trace_wind = go.Bar(
                x=parsed["dates"],
                y=parsed["wind_speeds"],
                name="Wind Speed",
                yaxis="y2"
            )

            layout = go.Layout(
                title=f"Прогноз: {city}",
                xaxis=dict(title="Дата"),
                yaxis=dict(title="Температура (°C)"),
                yaxis2=dict(
                    title="Скорость ветра",
                    overlaying="y",
                    side="right"
                ),
                legend=dict(x=0, y=1.2)
            )

            fig = go.Figure(data=[trace_min, trace_max, trace_wind], layout=layout)

            graphs.append(dcc.Graph(figure=fig, style={"marginBottom": "40px"}))

        except Exception as e:
            graphs.append(html.Div(
                f"Ошибка при обработке города {city}: {e}",
                style={"color": "red", "marginBottom": "20px"}
            ))

    if map_locations:
        map_fig = build_map_figure(map_locations)
        graphs.insert(0, dcc.Graph(figure=map_fig, style={"marginBottom": "50px"}))

    return html.Div(graphs)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
