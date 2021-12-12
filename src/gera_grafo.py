import json
from types import SimpleNamespace
import plotly.express as px
import pandas as pd

# Referências:
# https://stackoverflow.com/questions/43646550/how-to-use-an-update-function-to-animate-a-networkx-graph-in-matplotlib-2-0-0
# https://ankurankan.github.io/plotting-and-animating-networkx-graphs.html

def ler_grafo_json(grafo):
    with open("json/" + grafo + ".json") as g:
        return json.load(g, object_hook=lambda d: SimpleNamespace(**d)).nodes

def gerar_timelapse(anos, cor=(51, 51, 204)):
    nos_data = list()
    for ano in anos:
        nos = ler_grafo_json(ano)
        for no in nos:
            nos_data.append({"x": no.x, "y": no.y, "ano": ano, "tamanho": no.size, "cor": cor})
    df = pd.DataFrame(nos_data)
    fig = px.scatter(df, x="x", y="y", animation_frame="ano", size="tamanho", color="cor",
                    size_max=10, range_x=[df["x"].min(), df["x"].max()], range_y=[df["y"].min(), df["y"].max()], 
                    labels={
                     "x": "",
                     "y": "",
                     "cor": "Agrupamento"
                    },
                    title="Timelapse Twitter (2012 à 2021)")
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    fig.write_html("grafo.html", auto_play=False)

gerar_timelapse(["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"])