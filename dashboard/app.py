# ============================================
# Customer Behavior Dashboard - Streamlit App
# ============================================

import sys
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------------
# Gestion propre des chemins
# ----------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data", "scored")

sys.path.append(SRC_DIR)

from kpi import compute_kpis

# ----------------------------------
# Configuration Streamlit
# ----------------------------------
st.set_page_config(page_title="Customer Behavior Dashboard", layout="wide")

st.title("Customer Behavior Dashboard")

st.markdown("""
### 🎯 Objectif du Dashboard
Analyser le comportement d’achat des clients en croisant :
- leurs avis produits,
- leurs caractéristiques personnelles,
- leurs habitudes de consommation.
""")

# ----------------------------------
# Chargement des données scorées
# ----------------------------------
try:
    df_personality = pd.read_csv(os.path.join(DATA_DIR, "marketing_campaign_scored.csv"))
    df_reviews = pd.read_csv(os.path.join(DATA_DIR, "customer_reviews_scored.csv"))
except FileNotFoundError:
    st.error("❌ Les fichiers scorés sont introuvables. Lance d'abord kpi.py.")
    st.stop()

# ----------------------------------
# Calcul / récupération des KPI
# ----------------------------------
kpis = compute_kpis(
    path_reviews=os.path.join(DATA_DIR, "customer_reviews_scored.csv"),
    path_personality=os.path.join(DATA_DIR, "marketing_campaign_scored.csv"),
    output_dir=DATA_DIR
)

avg_spend = kpis["Average_Spend"]
conversion_rate = kpis["Conversion_Rate"]
recency_mean = kpis["Recency_Mean"]
avg_purchases = kpis["Average_Purchases"]
avg_sentiment = kpis["Average_Sentiment"]

# ----------------------------------
# KPI Cards
# ----------------------------------
st.header("📌 Key Performance Indicators (KPIs)")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Panier moyen", f"{avg_spend:.2f}")
col2.metric("Taux d’achat après avis positif", f"{conversion_rate:.2f}%")
col3.metric("Récence moyenne", f"{recency_mean:.2f} jours")
col4.metric("Achats moyens / client", f"{avg_purchases:.2f}")
col5.metric("Satisfaction moyenne", f"{avg_sentiment:.2f}")

st.markdown("---")
st.header("📊 Visualisations des comportements d’achat")

# ==================================================
# 1. Distribution des dépenses
# ==================================================
st.subheader("🛒 Distribution des dépenses clients")

fig, ax = plt.subplots()
ax.hist(df_personality["Total_Spent"], bins=30)
ax.set_xlabel("Montant total dépensé")
ax.set_ylabel("Nombre de clients")
ax.set_title("Répartition des dépenses clients")

st.pyplot(fig)
st.caption("➡️ Identification des petits et gros consommateurs.")

# ==================================================
# 2. Impact des avis positifs
# ==================================================
st.subheader("⭐ Impact des avis positifs sur l’achat")

conversion_df = (
    df_reviews.groupby("Positive_Review")["Purchased"]
    .mean()
    .reset_index()
)

conversion_df["Positive_Review"] = conversion_df["Positive_Review"].map({
    0: "Avis négatif / neutre",
    1: "Avis positif"
})

fig, ax = plt.subplots()
ax.bar(conversion_df["Positive_Review"], conversion_df["Purchased"] * 100)
ax.set_ylabel("Taux d'achat (%)")
ax.set_title("Taux d'achat selon le type d'avis")

st.pyplot(fig)
st.caption("➡️ Influence directe des avis sur la conversion.")

# ==================================================
# 3. Récence
# ==================================================
st.subheader("⏱️ Récence des clients")

fig, ax = plt.subplots()
ax.hist(df_personality["Recency"], bins=30)
ax.set_xlabel("Jours depuis le dernier achat")
ax.set_ylabel("Nombre de clients")
ax.set_title("Distribution de la récence")

st.pyplot(fig)
st.caption("➡️ Clients actifs vs inactifs.")

# ==================================================
# 4. Nombre d’achats
# ==================================================
st.subheader("📦 Nombre d’achats par client")

fig, ax = plt.subplots()
ax.hist(df_personality["Total_Purchases"], bins=30)
ax.set_xlabel("Nombre total d'achats")
ax.set_ylabel("Nombre de clients")
ax.set_title("Distribution des achats")

st.pyplot(fig)
st.caption("➡️ Analyse de la fidélité client.")

# ==================================================
# 5. Sentiment client
# ==================================================
st.subheader("😊 Analyse du sentiment client")

fig, ax = plt.subplots()
ax.hist(df_reviews["Sentiment"], bins=30)
ax.set_xlabel("Score de sentiment")
ax.set_ylabel("Nombre d’avis")
ax.set_title("Distribution des sentiments")

st.pyplot(fig)
st.caption("➡️ Perception globale des clients.")

# ==================================================
# Conclusion automatique
# ==================================================
st.markdown("---")
st.header("🧠 Synthèse automatique")

spend_msg = (
    "Panier élevé → clients à forte valeur."
    if avg_spend > 600 else
    "Panier modéré → potentiel de montée en gamme."
)

recency_msg = (
    "Clients actifs."
    if recency_mean < 30 else
    "Clients moyennement actifs."
)

sentiment_msg = (
    "Avis globalement positifs."
    if avg_sentiment > 0 else
    "Avis globalement neutres ou mitigés."
)

conversion_msg = (
    "Avis très influents sur l’achat."
    if conversion_rate > 50 else
    "Avis modérément influents."
)

st.success(f"""
📌 **Principaux enseignements**
- {spend_msg}
- {recency_msg}
- {sentiment_msg}
- {conversion_msg}

👉 Les avis clients combinés aux habitudes d’achat influencent clairement la décision finale.
""")

st.markdown("© 2026 – Customer Behavior Dashboard")
