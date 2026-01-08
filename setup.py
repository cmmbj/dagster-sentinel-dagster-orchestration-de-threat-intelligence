from setuptools import find_packages, setup

setup(
    name="my_cyber_project",
    packages=find_packages(exclude=["my_cyber_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-webserver",
        "pandas",        # Pour le nettoyage des données CVE
        "requests",      # Pour appeler les APIs NVD et AbuseIPDB
        "duckdb",        # Notre base de données de sécurité
        "python-dotenv", # Pour charger les clés API du fichier .env
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)