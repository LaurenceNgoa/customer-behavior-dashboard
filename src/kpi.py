# Calcul des KPI principaux à partir des datasets nettoyés
# cd src 
# python kpi.py


import os
import pandas as pd
import numpy as np
from textblob import TextBlob

def compute_kpis(
    path_reviews="../data/processed/customer_reviews_cleaned.csv",
    path_personality="../data/processed/marketing_campaign_cleaned.csv",
    output_dir="../data/scored/"
):
    """
    Calcule les 5 KPI principaux, sauvegarde les résultats et le DataFrame enrichi.
    """
    # --- Création du répertoire de sortie si inexistant ---
    os.makedirs(output_dir, exist_ok=True)

    # --- Chargement des datasets ---
    df_reviews = pd.read_csv(path_reviews)
    df_personality = pd.read_csv(path_personality)

    # ----------------------------
    # 1. Panier moyen (Average Spend)
    # ----------------------------
    amount_cols = [col for col in df_personality.columns if 'Mnt' in col or 'Amount' in col or 'Spent' in col]
    df_personality['Total_Spent'] = df_personality[amount_cols].sum(axis=1)
    avg_spend = df_personality['Total_Spent'].mean()
    print(f"Panier moyen : {avg_spend:.2f}")

    # ----------------------------
    # 2. Taux d'achat après avis positif (Conversion Rate)
    # ----------------------------
    # Analyser le sentiment avec TextBlob
    df_reviews['Sentiment'] = df_reviews['Review'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df_reviews['Positive_Review'] = (df_reviews['Sentiment'] > 0).astype(int)
    # Assurer que 'Purchased' est binaire
    df_reviews['Purchased'] = df_reviews['Purchased'].apply(lambda x: 1 if str(x).lower() in ['yes', '1'] else 0)
    conversion_rate = df_reviews[df_reviews['Positive_Review'] == 1]['Purchased'].mean() * 100
    print(f"Taux d'achat après avis positif : {conversion_rate:.2f}%")

    # ----------------------------
    # 3. Récence moyenne (Recency)
    # ----------------------------
    recency_mean = df_personality['Recency'].mean()
    print(f"Récence moyenne : {recency_mean:.2f} jours")

    # ----------------------------
    # 4. Nombre moyen d'achats par client
    # ----------------------------
    purchase_cols = [col for col in df_personality.columns if 'Num' in col or 'Purchases' in col]
    df_personality['Total_Purchases'] = df_personality[purchase_cols].sum(axis=1)
    avg_purchases = df_personality['Total_Purchases'].mean()
    print(f"Nombre moyen d'achats par client : {avg_purchases:.2f}")

    # ----------------------------
    # 5. Score moyen de satisfaction client
    # ----------------------------
    avg_sentiment = df_reviews['Sentiment'].mean()
    print(f"Score moyen de satisfaction client : {avg_sentiment:.2f}")

    # ----------------------------
    # Sauvegarde des DataFrames enrichis
    # ----------------------------
    df_personality.to_csv(os.path.join(output_dir, "marketing_campaign_scored.csv"), index=False)
    df_reviews.to_csv(os.path.join(output_dir, "customer_reviews_scored.csv"), index=False)

    # Retour des KPI dans un dictionnaire
    kpis = {
        "Average_Spend": avg_spend,
        "Conversion_Rate": conversion_rate,
        "Recency_Mean": recency_mean,
        "Average_Purchases": avg_purchases,
        "Average_Sentiment": avg_sentiment
    }

    return kpis

# Exemple d'utilisation
if __name__ == "__main__":
    kpi_results = compute_kpis()
    print("\nRésumé des KPI :")
    for k, v in kpi_results.items():
        print(f"{k} : {v:.2f}")


"""
RESULTATS obtenus :
Panier moyen : 613.80
Taux d'achat après avis positif : 45.45%
Récence moyenne : 50.84 jours
Nombre moyen d'achats par client : 20.23
Score moyen de satisfaction client : 0.05

Résumé des KPI :
Average_Spend : 613.80
Conversion_Rate : 45.45
Recency_Mean : 50.84
Average_Purchases : 20.23
Average_Sentiment : 0.05
"""