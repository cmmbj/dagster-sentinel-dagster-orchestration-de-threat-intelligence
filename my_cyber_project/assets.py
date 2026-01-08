import os
import requests
import duckdb
import pandas as pd
from dagster import asset, get_dagster_logger
from dotenv import load_dotenv

load_dotenv()

NIST_API_KEY = os.getenv("NIST_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

NIST_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/blacklist"

logger = get_dagster_logger()

# --- LOGIQUE DE FILTRAGE (Indispensable pour tes tests) ---
def critical_cve_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre les CVE pour ne garder que les scores élevés (>= 8.0)."""
    if df.empty:
        return df
    return df[df["cvss_score"] >= 8.0].copy()

# --- ASSETS : INGESTION ---

@asset(group_name="ingestion")
def raw_cve_data():
    """Extraction NIST avec injection d'une CVE de test."""
    headers = {"apiKey": NIST_API_KEY} if NIST_API_KEY else {}
    try:
        response = requests.get(NIST_API_URL, params={"resultsPerPage": 20}, headers=headers, timeout=10)
        response.raise_for_status()
        vulnerabilities = response.json().get('vulnerabilities', [])

        # --- AJOUT POUR TEST SENSOR ---
        # On simule une CVE critique qui n'existe pas encore dans l'API
        test_cve = {
            "cve": {
                "id": "CVE-2026-TEST-9999",
                "metrics": {
                    "cvssMetricV31": [{
                        "cvssData": {
                            "baseScore": 10.0,
                            "baseSeverity": "CRITICAL"
                        }
                    }]
                },
                "descriptions": [{"value": "ALERTE TEST : Simulation d'une faille Zero-Day critique pour vérifier le sensor."}]
            }
        }
        vulnerabilities.append(test_cve)
        # ------------------------------

        return vulnerabilities
    except Exception as e:
        logger.error(f"Erreur NIST : {e}")
        return []
    
"""
@asset(group_name="ingestion")

def raw_cve_data():
    #Extraction NIST utilisant la clé du .env
    headers = {"apiKey": NIST_API_KEY} if NIST_API_KEY else {}
    try:
        response = requests.get(NIST_API_URL, params={"resultsPerPage": 20}, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('vulnerabilities', [])
    except Exception as e:
        logger.error(f"Erreur NIST : {e}")
        return []
"""


@asset(group_name="ingestion")
def raw_abuse_ips():
    """Extraction AbuseIPDB utilisant la clé du .env"""
    if not ABUSEIPDB_API_KEY:
        logger.warning("Clé AbuseIPDB manquante")
        return []
        
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"  # <--- CORRIGÉ ICI
    }
    try:
        params = {"confidenceMinimum": 90}
        response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        logger.error(f"Erreur AbuseIPDB : {e}")
        return []

# --- ASSETS : TRANSFORMATION ---

@asset(group_name="transformation")
def critical_cve(raw_cve_data):
    """Prépare le DataFrame et applique le filtre de sécurité."""
    processed_list = []
    for item in raw_cve_data:
        cve = item.get('cve', {})
        metrics = cve.get('metrics', {}).get('cvssMetricV31', [{}])[0]
        cvss_score = metrics.get('cvssData', {}).get('baseScore', 0)

        processed_list.append({
            "cve_id": cve.get('id'),
            "severity": metrics.get('cvssData', {}).get('baseSeverity'),
            "cvss_score": cvss_score,
            "description": cve.get('descriptions', [{}])[0].get('value'),
        })

    df = pd.DataFrame(processed_list)
    # On utilise ici la fonction que tu as créée pour les tests !
    return critical_cve_filter(df)

@asset(group_name="transformation")
def malicious_ips(raw_abuse_ips):
    """Simple conversion des IPs brutes en DataFrame."""
    return pd.DataFrame(raw_abuse_ips)

# --- ASSET FINAL : STOCKAGE ---

@asset(group_name="storage")
def final_security_report(critical_cve: pd.DataFrame, malicious_ips: pd.DataFrame):
    import os
    import duckdb

    db_path = "data/cyber_data.db"
    conn = duckdb.connect(db_path)
    
    try:
        # On ne crée la table que si le DataFrame contient des données
        if not critical_cve.empty:
            conn.execute("CREATE OR REPLACE TABLE stg_cve_critical AS SELECT * FROM critical_cve")
        
        if not malicious_ips.empty:
            conn.execute("CREATE OR REPLACE TABLE stg_malicious_ips AS SELECT * FROM malicious_ips")
            
        return "Sauvegarde terminée (uniquement pour les données non vides)."
    finally:
        conn.close()