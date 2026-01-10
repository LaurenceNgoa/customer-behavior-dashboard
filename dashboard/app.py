# Version Python du dashboard interactif

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from kpi import compute_kpis

# ----------------------------------
# Configuration de la page Streamlit
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
df_personality = pd.read_csv("../data/scored/marketing_campaign_scored.csv")
df_reviews = pd.read_csv("../data/scored/customer_reviews_scored.csv")

# ----------------------------------
# Calcul des KPI
# ----------------------------------
kpis = compute_kpis(
    path_reviews="../data/scored/customer_reviews_scored.csv",
    path_personality="../data/scored/marketing_campaign_scored.csv",
    output_dir="../data/scored/"
)

avg_spend = kpis["Average_Spend"]
conversion_rate = kpis["Conversion_Rate"]
recency_mean = kpis["Recency_Mean"]
avg_purchases = kpis["Average_Purchases"]
avg_sentiment = kpis["Average_Sentiment"]

# ----------------------------------
# Affichage des KPI
# ----------------------------------
with st.container():
    st.header("📌 Key Performance Indicators (KPIs)")
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Panier moyen", f"{avg_spend:.2f}")
    col2.metric("Taux d’achat après avis positif", f"{conversion_rate:.2f}%")
    col3.metric("Récence moyenne", f"{recency_mean:.2f} jours")
    col4.metric("Achats moyens / client", f"{avg_purchases:.2f}")
    col5.metric("Satisfaction moyenne", f"{avg_sentiment:.2f}")

st.markdown("---")
st.header("📊 Visualisations des comportements d’achat")

# ==========================================================
# 1. Panier moyen – Distribution des dépenses
# ==========================================================
st.subheader("🛒 Distribution des dépenses clients")

fig1, ax1 = plt.subplots()
ax1.hist(df_personality["Total_Spent"], bins=30)
ax1.set_xlabel("Montant total dépensé")
ax1.set_ylabel("Nombre de clients")
ax1.set_title("Répartition des dépenses clients")

st.pyplot(fig1)

st.caption("➡️ Permet d’identifier les petits vs gros consommateurs.")

# ==========================================================
# 2. Taux d’achat après avis positif
# ==========================================================
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

fig2, ax2 = plt.subplots()
ax2.bar(conversion_df["Positive_Review"], conversion_df["Purchased"] * 100)
ax2.set_ylabel("Taux d'achat (%)")
ax2.set_title("Taux d'achat selon le type d'avis")

st.pyplot(fig2)

st.caption("➡️ Montre l’influence directe des avis clients sur la conversion.")

# ==========================================================
# 3. Récence moyenne
# ==========================================================
st.subheader("⏱️ Récence des clients")

fig3, ax3 = plt.subplots()
ax3.hist(df_personality["Recency"], bins=30)
ax3.set_xlabel("Nombre de jours depuis le dernier achat")
ax3.set_ylabel("Nombre de clients")
ax3.set_title("Distribution de la récence")

st.pyplot(fig3)

st.caption("➡️ Permet d’identifier les clients actifs vs inactifs.")

# ==========================================================
# 4. Nombre moyen d’achats par client
# ==========================================================
st.subheader("📦 Nombre d’achats par client")

fig4, ax4 = plt.subplots()
ax4.hist(df_personality["Total_Purchases"], bins=30)
ax4.set_xlabel("Nombre total d'achats")
ax4.set_ylabel("Nombre de clients")
ax4.set_title("Distribution des achats clients")

st.pyplot(fig4)

st.caption("➡️ Met en évidence la fidélité et la récurrence d’achat.")

# ==========================================================
# 5. Score de satisfaction client
# ==========================================================
st.subheader("😊 Analyse du sentiment client")

fig5, ax5 = plt.subplots()
ax5.hist(df_reviews["Sentiment"], bins=30)
ax5.set_xlabel("Score de sentiment")
ax5.set_ylabel("Nombre d’avis")
ax5.set_title("Distribution des sentiments clients")

st.pyplot(fig5)

st.caption("➡️ Permet de visualiser la perception globale des clients.")

st.markdown("---")
st.success("Dashboard opérationnel ✅")
st.markdown("© 2026 - Tous droits réservés.")


# ==================================
# Conclusion automatique
# ==================================
st.markdown("---")
st.header("🧠 Synthèse & interprétation automatique")

# Interprétation du panier moyen
if avg_spend > 600:
    spend_msg = "Les clients analysés présentent un panier moyen élevé, indiquant une forte valeur client."
elif avg_spend > 300:
    spend_msg = "Le panier moyen est modéré, laissant un potentiel de montée en gamme."
else:
    spend_msg = "Le panier moyen est faible, ce qui suggère un comportement d'achat occasionnel."

# Interprétation de la récence
if recency_mean < 30:
    recency_msg = "Les clients sont globalement récents et actifs."
elif recency_mean < 90:
    recency_msg = "Les clients sont moyennement actifs."
else:
    recency_msg = "Une partie significative des clients semble inactive ou à risque de churn."

# Interprétation du sentiment
if avg_sentiment > 0.1:
    sentiment_msg = "Les avis clients sont majoritairement positifs, traduisant une bonne satisfaction."
elif avg_sentiment > -0.05:
    sentiment_msg = "Les avis clients sont globalement neutres."
else:
    sentiment_msg = "Les avis clients révèlent une insatisfaction potentielle."

# Interprétation du taux de conversion
if conversion_rate > 50:
    conversion_msg = "Les avis positifs ont un fort impact sur la décision d’achat."
elif conversion_rate > 30:
    conversion_msg = "Les avis influencent modérément les décisions d’achat."
else:
    conversion_msg = "Les avis semblent avoir un impact limité sur la conversion."

# Message final
st.success(f"""
📌 **Principaux enseignements**

- {spend_msg}
- {recency_msg}
- {sentiment_msg}
- {conversion_msg}

👉 Ces résultats montrent que **les avis clients, combinés aux habitudes de consommation**, jouent un rôle clé dans les décisions d’achat.
""")
