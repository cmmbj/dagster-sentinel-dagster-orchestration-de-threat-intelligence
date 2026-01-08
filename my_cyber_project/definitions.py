import os
from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition # 1. Ajout de l'import
from dotenv import load_dotenv

# Imports absolus
from my_cyber_project import assets, resources, sensors

load_dotenv()

all_assets = load_assets_from_modules([assets])

# On définit le job (tu l'as déjà fait)
cyber_job = define_asset_job(name="alert_job", selection="*") 

# 2. NOUVEAU : On définit le planning (Schedule)
cyber_schedule = ScheduleDefinition(
    name="cyber_schedule",
    job=cyber_job,
    cron_schedule="*/30 * * * *" # Toutes les 30 minutes
)

defs = Definitions(
    assets=all_assets,
    jobs=[cyber_job],
    resources={
        "database": resources.DuckDBResource(
            database_path="data/cyber_data.db"
        ),
        "api_config": resources.CyberAPIResource(
            nvd_api_key=os.getenv("NVD_API_KEY", ""),
            abuseipdb_api_key=os.getenv("ABUSEIPDB_API_KEY", "")
        ),
    },
    # 3. On ajoute la liste des schedules ici
    schedules=[cyber_schedule], 
    sensors=[sensors.cve_alert_sensor],
)