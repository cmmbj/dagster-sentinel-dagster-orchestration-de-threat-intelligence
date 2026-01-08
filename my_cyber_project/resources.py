import os
from dagster import ConfigurableResource
import duckdb

class DuckDBResource(ConfigurableResource):
    """Ressource pour gérer la connexion à DuckDB."""
    database_path: str

    def get_connection(self):
        # On s'assure que le chemin vers le fichier .db est correct
        return duckdb.connect(self.database_path)

class CyberAPIResource(ConfigurableResource):
    """Ressource pour stocker les clés API de manière sécurisée."""
    nvd_api_key: str
    abuseipdb_api_key: str