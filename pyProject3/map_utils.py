from typing import List, Dict, Any
import plotly.graph_objs as go

def build_map_figure(locations: List[Dict[str, Any]]) -> go.Figure:
    fig = go.Figure(go.Scattermapbox(
        lat=[loc["lat"] for loc in locations],
        lon=[loc["lon"] for loc in locations],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=12,
            color="red"
        ),
        text=[loc["name"] for loc in locations],
        hoverinfo="text"
    ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=2,
        mapbox_center={"lat": 50.0, "lon": 10.0},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=500
    )
    return fig
