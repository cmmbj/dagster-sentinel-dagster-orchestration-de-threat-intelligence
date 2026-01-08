import os
from dagster import Definitions, load_assets_from_modules, define_asset_job
from dotenv import load_dotenv

# Imports absolus
from my_cyber_project import assets, resources, sensors

load_dotenv()

all_assets = load_assets_from_modules([assets])

# --- NOUVEAU : On définit le job que le sensor va appeler ---
# Ce job va simplement matérialiser les assets de sécurité
cyber_job = define_asset_job(name="alert_job", selection="*") 

defs = Definitions(
    assets=all_assets,
    jobs=[cyber_job], # <--- On ajoute le job ici
    resources={
        "database": resources.DuckDBResource(
            database_path="data/cyber_data.db"
        ),
        "api_config": resources.CyberAPIResource(
            nvd_api_key=os.getenv("NVD_API_KEY", ""),
            abuseipdb_api_key=os.getenv("ABUSEIPDB_API_KEY", "")
        ),
    },
    sensors=[sensors.cve_alert_sensor],
)