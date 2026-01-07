# Version Python du dashboard interactif

# Chargement des datasets enrichis
import pandas as pd
import streamlit as st
from kpi import compute_kpis 

# Configuration de la page Streamlit
st.set_page_config(page_title="Customer Behavior Dashboard", layout="wide")

st.title("Customer Behavior Dashboard")

# Ajout du bandeau d'introduction
st.markdown("""
### 🎯 Objectif du Dashboard
Analyser le comportement d’achat des clients en croisant :
- leurs avis produits,
- leurs caractéristiques personnelles,
- leurs habitudes de consommation.
""")

# --- Calcul des KPI à partir des fichiers scorés ---
kpis = compute_kpis(
    path_reviews="../data/scored/customer_reviews_scored.csv",
    path_personality="../data/scored/marketing_campaign_scored.csv",
    output_dir="../data/scored/"
)


# Extraction des KPI
avg_spend = kpis["Average_Spend"]
conversion_rate = kpis["Conversion_Rate"]
recency_mean = kpis["Recency_Mean"]
avg_purchases = kpis["Average_Purchases"]
avg_sentiment = kpis["Average_Sentiment"]

# Affichage des KPI (résultats globaux)
# Mise en page des KPI sur le dashboard
with st.container():
    st.header("Key Performance Indicators (KPIs)")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Panier moyen", f"{avg_spend:.2f}")
    with col2:
        st.metric("Taux d’achat après avis positif", f"{conversion_rate:.2f}%")

    with col3:
        st.metric("Récence moyenne", f"{recency_mean:.2f} jours")
    with col4:
        st.metric("Nombre moyen d'achats par client", f"{avg_purchases:.2f}")

    with col5:
        st.metric("Score moyen de satisfaction client", f"{avg_sentiment:.2f}")


# Ajout d'un séparateur visuel
# Création des graphiques interactifs
st.markdown("---")
st.header("📊 Visualisations des comportements d’achat")

# ----------------------------
# 1. Panier moyen (Average Spend)
# ----------------------------
# Histogramme des dépenses totales 'Total_Spent' par client pour montre comment les clients se répartissent (certains dépensent peu, d’autres beaucoup).
import matplotlib.pyplot as plt
import pandas as pd

plt.hist()


 
# ----------------------------
# 2. Taux d'achat après avis positif (Conversion Rate)
# ----------------------------
# Bar chart positif vs négatif pour montrer la différence de taux d’achat.


# ----------------------------
# 3. Récence moyenne (Recency)
# ----------------------------
# Histogramme des "Recency" pour montrer si les clients sont récents ou anciens.
# Récence / Recency = nombre de jours depuis le dernier achat
   
   
# ----------------------------
# 4. Nombre moyen d'achats par client
# ----------------------------
# Histogramme des achats (Total_Purchases)

    
# ----------------------------
# 5. Score moyen de satisfaction client
# -----------------------------
# Histogramme des sentiments pour montrer si les avis sont plutôt négatifs, neutres, positifs.






# Ajout des filtres interactifs