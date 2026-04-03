#!/usr/bin/env python3
"""
Dashboard moderne et professionnel pour l'analyse des données de badges
Créé avec Streamlit - Design responsive et interactif
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Dashboard Badges",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
def load_css():
    css = """
    <style>
    /* Styles généraux */
    .main {
        padding-top: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Styles pour les cartes KPI */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Styles pour la sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        color: white;
    }
    
    .stSelectbox > div > div > select {
        background-color: #34495e;
        color: white;
        border-radius: 8px;
    }
    
    .stMultiSelect > div > div > div {
        background-color: #34495e;
        color: white;
        border-radius: 8px;
    }
    
    /* Styles pour les graphiques */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Styles pour le tableau */
    .dataframe {
        background: white;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Titres */
    .title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Animation de chargement */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Charger et préparer les données"""
    try:
        # Chargement des données
        file_path = "badge_clean.csv"
        if not os.path.exists(file_path):
            st.error("Le fichier badge_clean.csv n'a pas été trouvé dans le répertoire courant.")
            return None
        
        df = pd.read_csv(file_path)
        
        # Conversion de la colonne date en datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Nettoyage des données - Gestion des valeurs manquantes
        # Remplacer les NaN dans les colonnes textuelles par des valeurs par défaut
        df['structure'] = df['structure'].fillna('Non spécifié').astype(str).str.strip()
        df['type'] = df['type'].fillna('Non spécifié').astype(str).str.strip()
        
        # Remplacer les valeurs NaN dans la colonne nb par 0
        df['nb'] = df['nb'].fillna(0)
        
        return df
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

def create_kpi_cards(df_filtered, df_total):
    """Créer les cartes KPI"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_filtered = len(df_filtered)
        st.markdown(f"""
        <div class="metric-card fade-in">
            <div class="metric-value">{total_filtered:,}</div>
            <div class="metric-label">Total Badges (Filtrés)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_badges = df_filtered['nb'].sum()
        st.markdown(f"""
        <div class="metric-card fade-in" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">{total_badges:,}</div>
            <div class="metric-label">Nombre Total de Badges</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_types = df_filtered['type'].nunique()
        st.markdown(f"""
        <div class="metric-card fade-in" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">{unique_types}</div>
            <div class="metric-label">NB type de Badges</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_structures = df_filtered['structure'].nunique()
        st.markdown(f"""
        <div class="metric-card fade-in" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-value">{unique_structures}</div>
            <div class="metric-label">NB Structures</div>
        </div>
        """, unsafe_allow_html=True)

def create_charts(df_filtered):
    """Créer les visualisations"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Répartition par Type")
        
        # Graphique en barres par type
        type_counts = df_filtered.groupby("type")["nb"].sum().sort_values(ascending=False).head(10)
        fig_type = px.bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation='h',
            title="Top 10 des Types",
            color=type_counts.values,
            color_continuous_scale="viridis"
        )
        fig_type.update_layout(
            height=400,
            xaxis_title="Nombre d'occurrences",
            yaxis_title="Type",
            showlegend=False
        )
        st.plotly_chart(fig_type, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Évolution Temporelle")
        
        # Graphique temporel
        daily_counts = df_filtered.groupby(df_filtered['date'].dt.date).size().reset_index()
        daily_counts.columns = ['date', 'count']
        
        fig_time = px.line(
            daily_counts,
            x='date',
            y='count',
            title="Évolution des Badges par Date",
            markers=True,
            line_shape='spline'
        )
        fig_time.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Nombre de Badges"
        )
        fig_time.update_traces(line_color='#667eea', marker_color='#764ba2')
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Deuxième ligne de graphiques
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏢 Top 10 des Structures")
        
        # Graphique pour les structures
        structure_counts = df_filtered['structure'].value_counts().head(10)
        fig_structure = px.pie(
            values=structure_counts.values,
            names=structure_counts.index,
            title="Répartition par Structure"
        )
        fig_structure.update_layout(height=400)
        st.plotly_chart(fig_structure, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("� Distribution par Type")
        
        # Graphique alternative pour les types
        type_dist = df_filtered['type'].value_counts().head(5)
        fig_type_dist = px.bar(
            x=type_dist.index,
            y=type_dist.values,
            title="Top 5 des Types (Barres Verticales)",
            color=type_dist.values,
            color_continuous_scale="blues"
        )
        fig_type_dist.update_layout(
            height=400,
            xaxis_title="Type",
            yaxis_title="Nombre d'occurrences",
            showlegend=False
        )
        st.plotly_chart(fig_type_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def create_data_table(df_filtered):
    """Créer le tableau de données interactif"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 Données Filtrées")
    
    # Préparation des données pour l'affichage
    display_df = df_filtered.copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df = display_df.rename(columns={
        'nb': 'Nombre',
        'structure': 'Structure',
        'type': 'Type',
        'date': 'Date'
    })
    
    # Affichage du tableau avec pagination
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exporter en CSV"):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name="badges_filtres.csv",
                mime="text/csv"
            )
    
    with col2:
        st.info(f"📊 {len(display_df)} lignes affichées")
    
    with col3:
        if st.button("🔄 Réinitialiser Filtres"):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Fonction principale du dashboard"""
    # Chargement du CSS
    load_css()
    
    # Titre du dashboard
    st.markdown('<h1 class="title">📊 Dashboard Badges</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyse interactive des données de badges</p>', unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    if df is None:
        return
    
    # Sidebar avec filtres
    st.sidebar.markdown("## 🔍 Filtres")
    
    # Filtre par type
    try:
        available_types = sorted([t for t in df['type'].unique() if pd.notna(t) and t != ''])
        selected_types = st.sidebar.multiselect(
            "Filtrer par Type:",
            options=available_types,
            default=[],  # Vide par défaut
            help="Sélectionnez un ou plusieurs types à afficher"
        )
    except Exception as e:
        st.error(f"Erreur lors du chargement des types: {e}")
        available_types = []
        selected_types = []
    
    # Filtre par structure
    try:
        available_structures = sorted([s for s in df['structure'].unique() if pd.notna(s) and s != ''])
        selected_structures = st.sidebar.multiselect(
            "Filtrer par Structure:",
            options=available_structures,
            default=[],  # Vide par défaut
            help="Sélectionnez une ou plusieurs structures à afficher"
        )
    except Exception as e:
        st.error(f"Erreur lors du chargement des structures: {e}")
        available_structures = []
        selected_structures = []
    
    # Filtre par date
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Date de début:",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )
    
    with col2:
        end_date = st.date_input(
            "Date de fin:",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )
    
    # Application des filtres
    df_filtered = df.copy()  # Commence avec toutes les données
    
    # Appliquer le filtre par type seulement si des types sont sélectionnés
    if selected_types:
        df_filtered = df_filtered[df_filtered['type'].isin(selected_types)]
    
    # Appliquer le filtre par structure seulement si des structures sont sélectionnées
    if selected_structures:
        df_filtered = df_filtered[df_filtered['structure'].isin(selected_structures)]
    
    # Appliquer le filtre par date (toujours appliqué) - Conversion correcte des dates
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)
    df_filtered = df_filtered[
        (df_filtered['date'] >= start_datetime) &
        (df_filtered['date'] <= end_datetime)
    ]
    
    # Informations sur le filtrage
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Statistiques du Filtre")
    # st.sidebar.write(f"**Lignes filtrées:** {len(df_filtered):,}")
    # st.sidebar.write(f"**Total initial:** {len(df):,}")
    # st.sidebar.write(f"**Pourcentage:** {len(df_filtered)/len(df)*100:.1f}%")
    
    # Indicateurs de filtres actifs
    st.sidebar.markdown("### 🎯 Filtres Actifs")
    if selected_types:
        st.sidebar.success(f"✅ Types: {len(selected_types)} sélectionné(s)")
    else:
        st.sidebar.info("⚪ Types: Tous")
    
    if selected_structures:
        st.sidebar.success(f"✅ Structures: {len(selected_structures)} sélectionnée(s)")
    else:
        st.sidebar.info("⚪ Structures: Toutes")
    
    if start_date == min_date and end_date == max_date:
        st.sidebar.info("⚪ Dates: Toute la période")
    else:
        st.sidebar.success(f"✅ Période: {start_date} → {end_date}")
    
    # Affichage du contenu principal
    if len(df_filtered) == 0:
        st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
        return
    
    # KPIs
    create_kpi_cards(df_filtered, df)
    
    # Graphiques
    create_charts(df_filtered)
    
    # Tableau de données
    create_data_table(df_filtered)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">'
        'Dashboard créé avec ❤️ using Streamlit | '
        f'Dernière mise à jour: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
