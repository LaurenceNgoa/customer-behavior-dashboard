# Objectif : Script principal qui orchestre les traitements/pour exécuter ton pipeline complet
# cd src
# python main.py

# main.py
# --------------------------------------------------------
# Script principal d’orchestration du pipeline de traitement
# --------------------------------------------------------
# Étapes :
# 1️⃣ Nettoyage et prétraitement des datasets
# 2️⃣ Calcul des KPI et enrichissement des données
# 3️⃣ (Optionnel) Lancement du dashboard Streamlit / Dash
#
# Exécution :
#   python main.py
# --------------------------------------------------------

import os
import sys
from datetime import datetime

# Import des modules internes
from src.preprocessing import clean_customer_review, clean_marketing_campaign
from src.kpi import compute_kpis


def main():
    print("\n🚀 Lancement du pipeline complet : Customer Behavior Dashboard\n")
    print(f"🕒 Début du traitement : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # === 1. Nettoyage des données ===
    print("\n🧹 Étape 1 : Prétraitement des datasets...")
    try:
        df_reviews = clean_customer_review()
        df_marketing = clean_marketing_campaign()
        print("✅ Données nettoyées et enregistrées dans data/processed/")
    except Exception as e:
        print(f"❌ Erreur lors du prétraitement : {e}")
        sys.exit(1)

    # === 2. Calcul des KPI ===
    print("\n📊 Étape 2 : Calcul des KPI principaux...")
    try:
        kpi_results = compute_kpis()
        print("✅ KPI calculés et fichiers enrichis sauvegardés dans data/scored/")
    except Exception as e:
        print(f"❌ Erreur lors du calcul des KPI : {e}")
        sys.exit(1)

    # === 3. Résumé final ===
    print("\n📈 Résumé des indicateurs clés :")
    for k, v in kpi_results.items():
        print(f"   - {k} : {v:.2f}")

    # === 4. (Optionnel) Lancer le dashboard ===
    print("\n📊 Étape 3 (optionnelle) : Lancer le dashboard Streamlit")
    print("👉 Exécute manuellement : streamlit run dashboard/app.py")

    print("\n✅ Pipeline exécuté avec succès.")
    print(f"🕒 Fin du traitement : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

# === 5. Convertir le dictionnaire de KPI en DataFrame
df_kpi = pd.DataFrame(list(kpis.items()), columns=["KPI", "Valeur"])


# === 6. Sauvegarder les KPI dans un fichier CSV
kpi_path = "data/scored/kpis.csv"
df_kpi.to_csv(kpi_path, index=False)
print(f"✅ Fichier KPI sauvegardé dans {kpi_path}")



if __name__ == "__main__":
    main()





