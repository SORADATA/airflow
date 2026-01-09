# 🌪️ Projet Airflow : Weather ETL Orchestration

Pipeline de données automatisé pour l'extraction, la transformation et le chargement de données météorologiques, orchestré via Apache Airflow et déployé avec la CLI Astronomer.

---

## 📋 Table des matières

- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [Configuration du DAG](#️-configuration-du-dag)
- [Utilisation](#-utilisation)
- [Développement](#-développement)
- [Notes importantes](#-notes-importantes)

---

## 🔧 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** : Environnement de développement
- **Docker Desktop** : Pour l'exécution des conteneurs Airflow (Webserver, Scheduler, Database)
- **Astro CLI** : Interface en ligne de commande pour gérer l'environnement Airflow

---

## 🚀 Installation

### 1. Installation de la CLI Astronomer

**Linux/macOS :**
```bash
curl -sSL install.astronomer.io | sudo bash -s
```

**Windows :**  
Consultez la [documentation officielle](https://www.astronomer.io/docs/astro/cli/install-cli?tab=windows)

### 2. Initialisation du projet

```bash
# Cloner le dépôt
git clone <votre-repo>
cd <nom-du-projet>

# Initialiser l'environnement Airflow (si pas déjà fait)
astro dev init

# Démarrer l'environnement
astro dev start
```

### 3. Accès à l'interface

Une fois démarré, accédez à l'interface Airflow : **http://localhost:8080**

**Identifiants par défaut :**
- Username : `admin`
- Password : `admin`

---

## 📁 Structure du projet

```
.
├── dags/                    # DAGs Python (cœur du pipeline)
│   └── weather_etl.py       # DAG principal pour les données météo
├── include/                 # Fichiers auxiliaires (SQL, scripts)
├── plugins/                 # Hooks et opérateurs personnalisés
├── tests/                   # Tests unitaires pour validation
├── Dockerfile               # Image Docker personnalisée
├── packages.txt             # Dépendances système (OS-level)
├── requirements.txt         # Bibliothèques Python
└── airflow_settings.yaml    # Configuration Airflow personnalisée
```

### Description des répertoires

- **dags/** : Contient tous vos workflows Airflow
- **include/** : Scripts SQL, fichiers de configuration, utilitaires
- **plugins/** : Extensions Airflow personnalisées
- **tests/** : Tests unitaires et d'intégration
- **requirements.txt** : Spécifiez ici vos dépendances Python (ex: `requests`, `pandas`, `sqlalchemy`)

---

## ⚙️ Configuration du DAG

Le DAG `weather_etl` est configuré pour une exécution quotidienne avec les paramètres suivants :

```python
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="weather_etl",
    start_date=datetime(2024, 1, 1, 9, 0),
    schedule="@daily",                        # Exécution quotidienne à 9h
    catchup=True,                             # Rattrapage des dates passées
    max_active_runs=1,                        # Une seule instance simultanée
    render_template_as_native_obj=True,       # Rendu natif des templates Jinja
    tags=["weather", "ETL", "production"],
) as dag:
    # Définition des tâches ci-dessous
    pass
```

### Paramètres clés

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `schedule` | `@daily` | Exécution automatique chaque jour |
| `catchup` | `True` | Rattrape les exécutions manquées depuis `start_date` |
| `max_active_runs` | `1` | Empêche les conflits en limitant les exécutions parallèles |

---

## 🎯 Utilisation

### Commandes essentielles

| Commande | Description |
|----------|-------------|
| `astro dev start` | Démarre l'environnement Airflow local |
| `astro dev stop` | Arrête tous les conteneurs Docker |
| `astro dev restart` | Redémarre l'environnement (nécessaire après modification de `requirements.txt`) |
| `astro dev ps` | Affiche l'état des services Airflow |
| `astro dev logs` | Consulte les logs en temps réel |
| `astro dev bash` | Ouvre un shell dans le conteneur webserver |

### Workflow typique

```bash
# 1. Modifier votre DAG
vim dags/weather_etl.py

# 2. Redémarrer pour appliquer les changements
astro dev restart

# 3. Vérifier les logs
astro dev logs -f scheduler
```

---

## 🛠️ Développement

### Ajouter une dépendance Python

1. Éditez `requirements.txt` :
```txt
requests==2.31.0
pandas==2.1.0
```

2. Redémarrez l'environnement :
```bash
astro dev restart
```

### Ajouter un package système

Éditez `packages.txt` pour installer des dépendances OS (ex: bibliothèques système) :
```txt
build-essential
libpq-dev
```

### Tester votre DAG localement

```bash
# Tester l'import du DAG
astro dev bash
python -c "from dags.weather_etl import dag"

# Tester une tâche spécifique
airflow tasks test weather_etl ma_tache 2024-01-01
```

---

## 📝 Notes importantes

### Backfilling

Grâce à `catchup=True`, Airflow exécutera automatiquement toutes les dates manquées entre `start_date` et aujourd'hui. Pour désactiver ce comportement :

```python
catchup=False  # Ne rattrape pas les exécutions passées
```

### Variables et connexions

Configurez vos variables et connexions via l'interface Airflow ou le fichier `airflow_settings.yaml` :

```yaml
airflow:
  connections:
    - conn_id: weather_api
      conn_type: http
      host: https://api.weather.com
  variables:
    - variable_name: api_key
      variable_value: your_secret_key
```

### Bonnes pratiques

- Utilisez des **Variables** Airflow pour les configurations sensibles
- Activez `max_active_runs=1` pour les DAGs manipulant des ressources partagées
- Testez toujours vos DAGs localement avant le déploiement
- Documentez vos tâches avec des `doc_md` pour faciliter la maintenance

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour proposer des améliorations :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

---

## 📚 Ressources

- [Documentation Apache Airflow](https://airflow.apache.org/docs/)
- [Documentation Astronomer](https://www.astronomer.io/docs/)
- [Tutoriels Airflow](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

---

**Développé avec ☁️ par [SISSOKO Moussa]**