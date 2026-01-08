import duckdb
import os

# S'assurer que le dossier data existe
os.makedirs('data', exist_ok=True)

# Connexion (crée le fichier s'il n'existe pas)
con = duckdb.connect('data/cyber_data.db')

print("Création des tables dans cyber_data.db...")

# Création de la table pour les CVE
con.execute("""
    CREATE TABLE IF NOT EXISTS stg_cve_critical (
        cve_id VARCHAR PRIMARY KEY,
        cvss_score DOUBLE,
        severity VARCHAR,
        description TEXT,
        published_at TIMESTAMP,
        is_exploited BOOLEAN DEFAULT FALSE
    );
""")

# Création de la table pour les IPs malveillantes
con.execute("""
    CREATE TABLE IF NOT EXISTS stg_malicious_ips (
        ip_address VARCHAR PRIMARY KEY,
        abuse_score INTEGER,
        country_code VARCHAR,
        last_reported TIMESTAMP,
        label VARCHAR
    );
""")

con.close()
print("Base de données initialisée avec succès dans data/cyber_data.db !")