# Script de prétraitement des datasets Customer_Review (1) et marketing_campaign
# cd src 
# python preprocessing.py


import pandas as pd
import os

def clean_customer_review(input_path="../data/raw/Customer_Review (1).csv",
                          output_path="../data/processed/customer_reviews_cleaned.csv"):
    """
    Nettoyage du dataset "Customer_Review (1)" :
    - Suppression des doublons
    - Conversion des types
    - Standardisation des colonnes texte
    - Gestion des valeurs manquantes
    - Réinitialisation de l'index
    - Export du dataset nettoyé
    """
    # Création du dossier processed si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Lecture
    df = pd.read_csv(input_path)

    # Conversion types
    cols_to_category = ['Gender', 'Education', 'Purchased']
    for col in cols_to_category:
        df[col] = df[col].astype('category')

    # Suppression doublons
    df = df.drop_duplicates()

    # Standardisation texte
    df['Gender'] = df['Gender'].str.strip().str.capitalize()
    df['Education'] = df['Education'].str.strip().str.title()

    # Gestion valeurs manquantes (optionnel, selon besoin)
    # df['Age'] = df['Age'].fillna(df['Age'].median())
    # df['Gender'] = df['Gender'].fillna('Unknown')
    # df['Education'] = df['Education'].fillna('Unknown')
    # df['Purchased'] = df['Purchased'].fillna('No')

    # Réinitialisation de l'index
    df = df.reset_index(drop=True)

    # Export
    df.to_csv(output_path, index=False)
    print(f"Customer_Review nettoyé sauvegardé dans : {output_path}")

    return df


def clean_marketing_campaign(input_path="../data/raw/marketing_campaign.csv",
                             output_path="../data/processed/marketing_campaign_cleaned.csv"):
    """
    Nettoyage du dataset "marketing_campaign" :
    - Conversion des types
    - Suppression des doublons
    - Gestion des valeurs manquantes
    - Correction des incohérences et valeurs aberrantes
    - Standardisation des colonnes texte
    - Réinitialisation de l'index
    - Export du dataset nettoyé
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Lecture du fichier
    df = pd.read_csv(input_path, sep='\s+', on_bad_lines='skip')

    # Conversion des types
    df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
    df['Teenhome'] = pd.to_numeric(df['Teenhome'], errors='coerce')
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')

    # Suppression des doublons
    df = df.drop_duplicates(subset='ID')

    # Gestion des valeurs manquantes
    df['Income'] = df['Income'].fillna(df['Income'].median())
    df['Teenhome'] = df['Teenhome'].fillna(0)
    df['Response'] = df['Response'].fillna(0)
    df['Dt_Customer'] = df['Dt_Customer'].ffill()

    # Filtrage des valeurs aberrantes
    df = df[(df['Year_Birth'] >= 1900) & (df['Year_Birth'] <= 2025)]
    df = df[df['Income'] >= 0]
    df = df[df['Recency'] >= 0]

    # Standardisation des colonnes texte
    valid_status = ['Married', 'Together', 'Single', 'Divorced', 'Widow']
    df['Marital_Status'] = df['Marital_Status'].apply(lambda x: x if x in valid_status else 'Other')
    df['Teenhome'] = df['Teenhome'].astype(int)

    # Réinitialisation de l'index
    df = df.reset_index(drop=True)

    # Export
    df.to_csv(output_path, index=False)
    print(f"Marketing_Campaign nettoyé sauvegardé dans : {output_path}")

    return df


if __name__ == "__main__":
    # Nettoyage automatique des deux datasets
    df_reviews = clean_customer_review()
    df_marketing = clean_marketing_campaign()
