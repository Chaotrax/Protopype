# script that draws the circles
# ich brauche: alle shapes, koordinaten in latlng, map


import plotly as px
import numpy as np
import plotly.graph_objects as go


def draw(shapelist):
    longs = []
    lats = []
    for i in shapelist:
        for j in i.shape:
            longs.append(j[1])
            lats.append(j[0])
        longs.append(None)
        lats.append(None)

    fig = go.Figure(go.Scattermapbox(
        mode="lines", fill="toself",
        lon=longs,
        lat=lats))

    fig.update_layout(
        mapbox={'style': "stamen-terrain", 'center': {'lon': longs[0], 'lat': lats[0]}, 'zoom': 2},
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

    fig.show()


