import streamlit as st
import folium
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Carte des Magasins",
    layout="wide",  # <--- c'est ça qui élargit l'app
)

# Données magasins
magasins_data = [
    {"nom": "Gourmet Vélodrome", "latitude": 33.590812, "longitude": -7.646213, "radius": 3.5, "type": "Gourmet"},
    {"nom": "Gourmet Zears", "latitude": 33.974476, "longitude": -6.829226, "radius": 20, "type": "Gourmet"},
    {"nom": "Market Hassan 2", "latitude": 33.715014, "longitude": -7.344572, "radius": 3.5, "type": "Market"},
    {"nom": "Market Darb", "latitude": 33.514057, "longitude": -7.818232, "radius": 3.5, "type": "Market"},
    {"nom": "Market Yaacoub Al Mansour", "latitude": 33.573876, "longitude": -7.644541, "radius": 3.5, "type": "Market"},
    {"nom": "Market Ain Sebaa", "latitude": 33.601892, "longitude": -7.526957, "radius": 3.5, "type": "Market"},
    {"nom": "Market Ville Verte", "latitude": 33.484300, "longitude": -7.602550, "radius": 3.5, "type": "Market"},
    {"nom": "Market Taddart", "latitude": 33.554571, "longitude": -7.626517, "radius": 3.5, "type": "Market"},
    {"nom": "Market Anfa", "latitude": 33.578130, "longitude": -7.674180, "radius": 3.5, "type": "Market"},
    {"nom": "Hyper Targa", "latitude": 31.650870, "longitude": -8.059124, "radius": 15, "type": "Hyper"},
    {"nom": "Hyper Tetouan", "latitude": 35.578369, "longitude": -5.333914, "radius": 30, "type": "Hyper"},
    {"nom": "Hyper Al Mazar", "latitude": 31.592608, "longitude": -7.987111, "radius": 30, "type": "Hyper"},
    {"nom": "Hyper Temara", "latitude": 33.908473, "longitude": -6.939415, "radius": 17, "type": "Hyper"},
    {"nom": "Hyper Salé", "latitude": 34.058898, "longitude": -6.802032, "radius": 17, "type": "Hyper"},
    {"nom": "Hyper Dar Bouazza", "latitude": 33.517068, "longitude": -7.799557, "radius": 27, "type": "Hyper"},
    {"nom": "Hyper Tanger", "latitude": 35.781464, "longitude": -5.840993, "radius": 15, "type": "Hyper"},
    {"nom": "Hyper Agadir", "latitude": 30.389275, "longitude": -9.510128, "radius": 20, "type": "Hyper"},
    {"nom": "Hyper Sidi Maarouf", "latitude": 33.536066, "longitude": -7.642023, "radius": 18, "type": "Hyper"},
    {"nom": "Gourmet Carre Eden", "latitude": 31.635050, "longitude": -8.011140, "radius": 3.5, "type": "Gourmet"},
    {"nom": "Market La Fontaine", "latitude": 31.628407, "longitude": -8.002586, "radius": 3.5, "type": "Market"},
    {"nom": "Market Mehdi Ben Barka" , "latitude": 31.949701, "longitude": -6.868038, "radius": 3.5, "type": "Market"},
    {"nom": "Market Wifak", "latitude": 33.929658, "longitude": -6.928876, "radius": 3.5, "type": "Market"},
]

type_colors = {"Gourmet": "green", "Hyper": "blue", "Market": "red"}

st.title("Carte interactive des magasins Carrefour")

all_names = [m["nom"] for m in magasins_data]
selected_names = st.multiselect("Sélectionnez les magasins", all_names, default=all_names)
magasins = [m for m in magasins_data if m["nom"] in selected_names]

radius_dict = {}
for m in magasins:
    radius = st.slider(
    f"Rayon pour {m['nom']} (km)", 
    min_value=1.0, 
    max_value=30.0, 
    value=float(m["radius"]), 
    step=0.5,
    key=f"radius_{m['nom']}"
)
    radius_dict[m["nom"]] = radius

mymap = folium.Map(location=[magasins[0]["latitude"], magasins[0]["longitude"]], zoom_start=10)
circles = []

for mgs in magasins:
    radius = radius_dict[mgs["nom"]]
    folium.Circle(
        location=[mgs["latitude"], mgs["longitude"]],
        radius=radius * 1000,
        color=type_colors.get(mgs["type"], "gray"),
        fill=True,
        fill_color=type_colors.get(mgs["type"], "gray"),
        opacity=0.4
    ).add_to(mymap)
    folium.Marker(
        location=[mgs["latitude"], mgs["longitude"]],
        popup=mgs["nom"],
        tooltip=mgs["nom"]
    ).add_to(mymap)
    circles.append(Point(mgs["longitude"], mgs["latitude"]).buffer(radius))


st_folium(mymap, width="100%", height=800)
