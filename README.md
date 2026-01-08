#Sentinel #1 : Pipeline d'Automated Threat Intelligence

Projet Bachelor Cybersécurité - ESILV

#PRESENTATION
Sentinel #1 est une plateforme d'orchestration de données de sécurité (SOAR light)
conçue pour automatiser la veille sur les vulnérabilités et la réputation IP.
Le système collecte, filtre et centralise les menaces critiques pour assister
les analystes SOC dans leur prise de décision.

###ARCHITECTURE DU PROJET

##Arborescence des fichiers

```

my-cyber-project/
├── .env                      # Secrets et clés API
├── .gitignore                # Protection contre l'export de données sensibles
├── README.md                 # Documentation centrale
├── requirements.txt          # Dépendances logicielles
├── setup.py                  # Configuration du package Python
├── verify_my_data.py         # Script d'audit SQL rapide
├── data/                     # Couche de persistance
│   └── cyber_data.db         # Base DuckDB (Stockage final)
└── my_cyber_project/         # Cœur logique (Modules Dagster)
    ├── assets.py             # ETL : Ingestion, filtrage et transformation
    ├── resources.py          # Connecteurs et ressources partagées
    ├── sensors.py            # Automatisation et logique d'alerte
    └── definitions.py        # Point d'entrée de l'orchestrateur

```

###ROLE DES COMPOSANTS

.env
Stockage sécurisé des variables d'environnement (Clés NIST, AbuseIPDB)

assets.py
Définit les blocs de données (CVE, IPs) et gère le filtrage CVSS

sensors.py
Surveille l'état des assets et déclenche les jobs d'alerte automatiquement

definitions.py
Compile tous les modules pour l'interface de contrôle Dagster

cyber_data.db
Base de données relationnelle stockant l'historique des menaces qualifiées

verify_my_data.py
Permet une lecture directe des données sans passer par l'orchestrateur

###PIPELINE DE DONNEES

1. Ingestion
Récupération des données brutes depuis les API NIST et AbuseIPDB

2. Transformation
Utilisation de Pandas pour isoler les vulnérabilités critiques
(ex : CVE-1999-0084, score 8.4)

3. Stockage
Injection sécurisée dans DuckDB pour l'analyse SOC

4. Automation
Un capteur détecte la réussite du stockage et lance instantanément
une procédure d'alerte

###INSTALLATION ET LANCEMENT

#Configuration

```

Créer un fichier .env à la racine :

NIST_API_KEY=votre_cle
ABUSEIPDB_API_KEY=votre_cle

```

#Déploiement

```

pip install -e .
PYTHONPATH = "."
python -m dagster dev -m my_cyber_project.definitions

```

###CONCLUSION : VALEUR POUR L'EXPERT CYBER

Réduction du MTTR (Mean Time To Respond)
L'automatisation permet d'identifier une menace critique en quelques secondes

Intégrité des données
Le suivi rigoureux des versions d'assets garantit des alertes vérifiables

Scalabilité
L'architecture modulaire permet l'ajout de nouvelles sources de menaces
sans complexifier le système existant

Développé par Camille MBIANDJI en Bachelor Cybersécurité - ESILV (avec l'aide de Gemini Pro)
