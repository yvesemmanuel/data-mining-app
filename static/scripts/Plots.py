from matplotlib.figure import Figure
import base64
import numpy as np
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
import pandas as pd
from io import BytesIO
from statistics import mean, stdev
from static.scripts.MontaSagresSimba import *
import plotly.express as px


def regular_payments_plot(x, y):
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    ax.plot(x, y, color='black', linestyle='--', marker='o')

    avg = mean(y)
    std = stdev(y)
    lower_bound = []
    upper_bound = []
    for i in range(len(y)):
        lower_bound.append(avg - std)
        upper_bound.append(avg + std)

    ax.fill_between(x, lower_bound, upper_bound, alpha=0.2)
    fig.autofmt_xdate()

    ax.set_xlabel('Data Pagamento')
    ax.set_ylabel('Valor (R$)')

    buf = BytesIO()
    fig.savefig(buf, format='png')
    data_image = base64.b64encode(buf.getbuffer()).decode('ascii')

    image_file = open('./static/assets/plot.png', 'wb')
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def service_before_payment_plot(x, y):
    # gerar a figura (sem utilizar o pyploy)
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    # arrumar as datas no eixo X
    ax.plot(x, y, color="black", linestyle="--", marker="o")
    fig.set_size_inches(7.41, 5)

    avg = mean(y)
    std = stdev(y)

    lb = []
    ub = []
    for i in range(len(y)):
        lb.append(avg - std)
        ub.append(avg + std)

    ax.fill_between(x, lb, ub, alpha=0.2)
    fig.autofmt_xdate()

    # estilo
    ax.set_xlabel("Data Pagamento")
    ax.set_ylabel("Valor (R$)")

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def simba_plot(idx):
    lObjs = montaObjsSagresSimba(
        "../datasets/simba/SimbaGoiana.csv", "../datasets/simba/SagresGoiana.csv"
    )

    # gerar a figura (sem utilizar o pyploy)
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    barWidth = 0.25
    r1 = np.arange(12)
    r2 = [x + barWidth for x in r1]

    dictPagsSagres = lObjs[idx].dictPagsMensaisSagres
    dictPagsSimba = lObjs[idx].dictPagsMensaisSimba

    gastosSagres = []
    gastosSimba = []

    for i in range(1, 13):
        gastosSagres.append(dictPagsSagres[i])
        gastosSimba.append(dictPagsSimba[i])

    ax.bar(r1, gastosSagres, color="#6A5ACD", width=barWidth, label="Sagres")
    ax.bar(r2, gastosSimba, color="#00BFFF", width=barWidth, label="Simba")

    ax.ticklabel_format(style="plain")
    ax.set(
        title="Destino: " + str(lObjs[idx].nmFornecedor),
        xlabel="Mês",
        ylabel="Valor Mensal (R$)",
    )
    ax.set_xticklabels(
        [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]
    )
    ax.set_xticks([r + barWidth for r in range(12)])  # ,
    ax.legend(loc="upper right")

    fig.autofmt_xdate()

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def payments_delay_plot_0(x, y):
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    b = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    n, bins, patches = ax.hist(x, bins=b)
    ax.grid(color="white", lw=4.5, axis="x")

    xticks = [(bins[idx + 1] + value) / 2 for idx,
              value in enumerate(bins[:-1])]
    # xticks_labels = ["{:.2f}\nto\n{:.2f}".format(value, bins[idx + 1]) for idx, value in enumerate(bins[:-1])]
    # plt.xticks(xticks, labels = xticks_labels)

    for idx, value in enumerate(n):
        if value > 0:
            ax.text(xticks[idx], value + 5, int(value), ha='center')

    ax.set_xticks(b)

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def payments_delay_plot_1(df):
    fig = px.scatter(df, x="DIFF_LIQ_PAG", y="VALOR", color="FORNEC")
    fig.write_html("./templates/payments_delay_plot_1.html")

def geraMapaFolium(state_data):

    fig = folium.Figure(height=500)

    mapageografico = gpd.read_file('./static/datasets/geojs-26-mun.json')
    
    map = folium.Map(
        location=[-8.1959084, -37.81929747],
        tiles='OpenStreetMap', 
        zoom_start=7.55
    )

    cores = folium.Choropleth(
            geo_data=mapageografico,
            name="choropleth",
            data=state_data,
            columns=["Municipio", "Score"],
            key_on="feature.properties.name",
            fill_color="PuBu",
            fill_opacity=0.7,
            line_opacity=0.4,
            legend_name="Regularidade",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            show=True,
            overlay=True,
            nan_fill_color = "White", 
        )
    cores.add_to(map)

    valor = state_data.rename(columns = {"Municipio":"name"})
    final_df = pd.merge(mapageografico,valor, on = "name")
    print(final_df.head())
        # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
        
                                        'weight': 0.1}
        
        
        #Colocar os valores nos estados 
    NIL = folium.features.GeoJson(
            data = final_df,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['name','Score'],
                aliases=['Municipio','Score'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
    map.add_child(NIL)
    map.keep_in_front(NIL)

    folium.LayerControl().add_to(map)
    fig.add_child(map)

    return map
