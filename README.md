# 📊 Dashboard Badges

Un dashboard moderne et professionnel créé avec Streamlit pour l'analyse interactive des données de badges.

## 🚀 Fonctionnalités

### 📋 Filtres Interactifs (Sidebar)
- **Filtre multi-sélection par Type** : Sélectionnez un ou plusieurs types de badges
- **Filtre multi-sélection par Structure** : Filtrez par organisation/structure
- **Filtre par intervalle de dates** : Choisissez une période spécifique

### 📊 KPIs (Indicateurs Clés)
- **Total Badges (Filtrés)** : Nombre total d'enregistrements filtrés
- **Nombre Total de Badges** : Somme des badges numériques
- **Types Uniques** : Nombre de catégories différentes
- **Structures Uniques** : Nombre d'organisations différentes

### 📈 Visualisations Professionnelles
- **Graphique en barres par Type** : Top 10 des types les plus fréquents
- **Évolution Temporelle** : Tendance des badges par date
- **Répartition par Structure** : Diagramme circulaire des organisations
- **Hiérarchie Type-Structure** : Sunburst interactif

### 📋 Tableau Interactif
- Affichage des données filtrées avec pagination
- Export CSV des données filtrées
- Réinitialisation des filtres en un clic

## 🎨 Design
- **Interface moderne** avec dégradés et animations CSS
- **Design responsive** adapté à tous les écrans
- **Coloration professionnelle** avec palette cohérente
- **Animations fluides** pour meilleure expérience utilisateur

## 📦 Installation

1. Clonez ce repository :
```bash
git clone <repository-url>
cd DASHBOARD_BADGE
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Assurez-vous que le fichier `badge_clean.csv` est dans le même répertoire

## 🏃‍♂️ Lancement

Exécutez le dashboard avec la commande :
```bash
streamlit run dashboard.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📁 Structure des Données

Le fichier `badge_clean.csv` doit contenir les colonnes suivantes :
- `nb` : Nombre de badges (numérique)
- `structure` : Nom de l'organisation/structure
- `type` : Type de badge (JOURNALISTE, PHOTOGRAPHE, etc.)
- `date` : Date au format YYYY-MM-DD

## 🔧 Personnalisation

### Modification des couleurs
Editez la fonction `load_css()` dans `dashboard.py` pour personnaliser :
- Les couleurs des cartes KPI
- Les dégradés de fond
- Les couleurs des graphiques

### Ajout de nouveaux KPIs
Ajoutez de nouvelles cartes dans la fonction `create_kpi_cards()`.

### Nouvelles visualisations
Ajoutez des graphiques supplémentaires dans la fonction `create_charts()`.

## 📊 Technologies Utilisées

- **Streamlit** : Framework d'applications web
- **Plotly** : Graphiques interactifs
- **Pandas** : Manipulation de données
- **NumPy** : Calculs numériques
- **CSS3** : Styles et animations

## 🤝 Contribuer

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 📞 Support

Pour toute question ou suggestion, veuillez créer une issue sur le repository GitHub.

---

**Créé avec ❤️ using Streamlit**
