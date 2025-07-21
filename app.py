import streamlit as st
import folium
from shapely.geometry import Point
from streamlit_folium import st_folium
import json
import os

# Fichier JSON
FICHIER_MAGASINS = "magasins.json"

# Charger les magasins
def charger_magasins():
    if os.path.exists(FICHIER_MAGASINS):
        with open(FICHIER_MAGASINS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Sauvegarder les magasins
def sauvegarder_magasins(magasins):
    with open(FICHIER_MAGASINS, "w", encoding="utf-8") as f:
        json.dump(magasins, f, indent=4, ensure_ascii=False)

# Charger données
magasins_data = charger_magasins()

# Personnalisation de la page
st.set_page_config(layout="wide")
st.title("🗺️ Carte interactive des magasins Carrefour")

# Zone repliable : ajout de magasin
with st.expander("➕ Ajouter un magasin"):
    st.markdown("Remplissez les informations pour ajouter un nouveau magasin.")
    nom = st.text_input("Nom du magasin")
    ville = st.text_input("Ville")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    radius = st.slider("Rayon (km)", 1.0, 30.0, 3.5, step=0.5)
    type_mag = st.selectbox("Type", ["Gourmet", "Market", "Hyper", "Express"])

    if st.button("Ajouter le magasin"):
        # Vérifier si le magasin existe déjà
        magasin_existant = next((m for m in magasins_data if m["nom"] == nom), None)
        
        if magasin_existant:
            # Si le magasin existe déjà, on remplace les anciennes données par les nouvelles
            magasin_existant.update({
                "ville": ville,
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "type": type_mag
            })
            st.success(f"✅ Le magasin **{nom}** a été mis à jour.")
        else:
            # Sinon, on ajoute le nouveau magasin
            nouveau = {
                "nom": nom,
                "ville": ville,
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "type": type_mag
            }
            magasins_data.append(nouveau)
            st.success(f"✅ Magasin **{nom}** ajouté avec succès.")
        
        # Sauvegarder les magasins après modification
        sauvegarder_magasins(magasins_data)

# Couleurs selon le type
type_colors = {"Gourmet": "brown", "Hyper": "blue", "Market": "red", "Express": "green"}

# Liste des villes
villes_disponibles = sorted(list(set(m["ville"] for m in magasins_data if "ville" in m)))

if villes_disponibles:
    ville_selectionnee = st.selectbox("🏙️ Choisir une ville", villes_disponibles)
    magasins_ville = [m for m in magasins_data if m["ville"] == ville_selectionnee]

    selected_names = st.multiselect(
        "🏪 Choisir les magasins",
        options=[m["nom"] for m in magasins_ville],
        default=[]
    )
    magasins = [m for m in magasins_ville if m["nom"] in selected_names]

    radius_dict = {}
    for m in magasins:
        radius = st.slider(
            f"🔵 Rayon pour {m['nom']} (km)",
            min_value=1.0,
            max_value=30.0,
            value=float(m["radius"]),
            step=0.5,
            key=f"radius_{m['nom']}"
        )
        radius_dict[m["nom"]] = radius

    if magasins:
        st.markdown("<style>.element-container iframe { width: 100% !important; }</style>", unsafe_allow_html=True)

        mymap = folium.Map(location=[magasins[0]["latitude"], magasins[0]["longitude"]], zoom_start=11)

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

        st_folium(mymap, width="100%", height=800)
else:
    st.info("ℹ️ Aucune ville disponible. Veuillez ajouter des magasins avec une ville.")
