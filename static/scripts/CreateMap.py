import folium
import pandas as pd
import numpy as np
import geopandas as gpd


def criar_mapa_1(filename):
    mapa = folium.Map(location=[-8.4319084, -37.60809747],
                      tiles="OpenStreetMap", zoom_start=7.33)
    mapageografico = gpd.read_file("./static/datasets/geojs-26-mun.json")

    geoJSON_muni = list(mapageografico.name.values)

    # state_data = pd.read_csv("./static/datasets/Score_por_Municipio.csv", sep=";")
    state_data = pd.read_csv(filename)

    dados_muni = list(state_data.Municipio.values)
    muni_faltantes = np.setdiff1d(geoJSON_muni, dados_muni)

    for i in muni_faltantes:
        indice = mapageografico[mapageografico["name"] == i].index

        antes = state_data.iloc[0:indice[0]]
        depois = state_data.iloc[indice[0]:]
        juncao = pd.concat(
            [antes, pd.Series({"Municipio": i, "Score": 0})], ignore_index=True)
        state_data = pd.concat([juncao, depois])

    folium.Choropleth(
        geo_data=mapageografico,
        name="choropleth",
        data=state_data,
        columns=["Municipio", "Score"],
        key_on="feature.properties.name",
        # line_color = "#0000",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Regularidade",
        smooth_factor=0,
        Highlight=True,
        show=True,
        overlay=True,
        nan_fill_color="White"
    ).add_to(mapa)

    valor = state_data.rename(columns={"Municipio": "name"})
    final_df = pd.merge(mapageografico, valor, on="name")

    # Add hover functionality.
    def style_function(x): return {
        "fillColor": "transparent", "color": "#8a8a8a", "fillOpacity": 0.1, "weight": 0.1}
    def highlight_function(x): return {
        "fillColor": "#000000", "color": "#000000", "fillOpacity": 0.50, "weight": 0.1}

    # Colocar os valores nos estados
    NIL = folium.features.GeoJson(
        data=final_df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["name", "Score"],
            aliases=["Municipio", "Score"],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )

    mapa.add_child(NIL)
    mapa.keep_in_front(NIL)

    # Add dark and light mode.
    folium.TileLayer("cartodbdark_matter", name="modo escuro",
                     control=True).add_to(mapa)
    folium.TileLayer("cartodbpositron", name="modo claro",
                     control=True).add_to(mapa)
    folium.LayerControl().add_to(mapa)

    mapa.save("./templates/mapa_atrasos.html")


def criar_mapa_2():
    state_unemployment = "./static/datasets/Indice_por_Municipio.csv"
    state_data = pd.read_csv(state_unemployment, sep=";")

    fig = folium.Figure(height=500)

    mapageografico = gpd.read_file("./static/datasets/geojs-26-mun.json")

    mapa = folium.Map(location=[-8.4319084, -37.60809747],
                      tiles="OpenStreetMap", zoom_start=7.33)

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
        Highlight=True,
        line_color="#0000",
        show=True,
        overlay=True,
        nan_fill_color="White",
    )

    cores.add_to(mapa)

    valor = state_data.rename(columns={"Municipio": "name"})
    valor2 = pd.DataFrame(valor)
    final_df = pd.merge(mapageografico, valor, on="name")

    # Add hover functionality.
    def style_function(x): return {"fillColor": "#ffffff",
                                   "color": "#000000",
                                   "fillOpacity": 0.1,
                                   "weight": 0.1}

    def highlight_function(x): return {"fillColor": "#000000",
                                       "color": "#000000",
                                       "fillOpacity": 0.50,

                                       "weight": 0.1}

    # Colocar os valores nos estados
    NIL = folium.features.GeoJson(
        data=final_df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["name", "Score"],
            aliases=["Municipio", "Score"],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    mapa.add_child(NIL)
    mapa.keep_in_front(NIL)

    folium.LayerControl().add_to(mapa)
    fig.add_child(mapa)

    mapa.save("./templates/mapa_filas.html")
