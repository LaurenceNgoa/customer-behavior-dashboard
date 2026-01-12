# 🧭 Customer Behavior Dashboard

**Dashboard de suivi du comportement d’achat des clients**, croisant leurs avis, leurs caractéristiques démographiques et leurs habitudes de consommation.

---

## 🎯 Objectif du projet
Ce projet a pour but de concevoir un **tableau de bord interactif** permettant d’analyser le **comportement d’achat des clients** à partir de **deux jeux de données Kaggle**.  
L’objectif principal est de comprendre **comment les avis, les caractéristiques personnelles et les habitudes de consommation influencent les décisions d’achat**.

---

## 📊 Indicateurs Clés de Performance (KPI)
1. 💰 **Panier moyen**  
2. 🛍️ **Taux d’achat après avis positif (Conversion Rate)**  
3. ⏳ **Récence moyenne (Recency)**  
4. 👥 **Nombre moyen d’achats par client**  
5. ⭐ **Score moyen de satisfaction client**

---

## 🧰 Outils et technologies utilisés
- **Langage principal :** Python  
- **Librairies :** `pandas`, `numpy`, `seaborn`, `plotly`, `TextBlob`, `matplotlib` , `streamlit` 
- **Visualisation :** `Streamlit` 
- **Exploration des données :** `Jupyter Notebook`  
- **Outils de BI complémentaires :** Power BI, Tableau  
- **Editeur de code :** Visual Studio Code  
- **Source des données :** [Kaggle](https://www.kaggle.com)

---

## 📂 Jeux de données

### 1️⃣ Dataset : *Customer Reviews & Purchase Decisions*
Analyse du lien entre les **avis clients** et leurs **choix d’achat**.  
**Objectif :** Comprendre l’impact des avis (reviews) sur la probabilité d’achat.

### 2️⃣ Dataset : *Customer Personality Analysis*
Analyse des **profils clients** et de leurs **habitudes de consommation**.  
**Objectif :** Identifier les segments de clientèle et les comportements d’achat récurrents.

---

## 🧱 Structure du projet

- `data/` : jeux de données bruts et nettoyés
  ── raw/                # Données sources
  ── processed/          # Données nettoyées
  ── scored/             # Données enrichies + fichier kpis.csv*
- `notebooks/` : exploration & feature engineering
- `src/` : scripts de préparation
- `app_streamlit.py` : application interactive (Streamlit)
- `output/` : workbook / captures
- 'main.py'  : Script principal qui orchestre les traitements

---

## ⚙️ Installation (en local)

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre-nom-utilisateur>/customer-behaviour-dashboard.git
cd customer-behaviour-dashboard

# 2. Créer et activer un environnement virtuel
python -m venv env
# (Windows)
env\Scripts\activate
# (macOS / Linux)
source env/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer les scripts
python src/kpi.py

# 5. Exécuter le dashboard
streamlit run dashboard/app.py
