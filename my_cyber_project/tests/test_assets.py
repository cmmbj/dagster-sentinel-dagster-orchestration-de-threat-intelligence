import pandas as pd
import pytest
from my_cyber_project.assets import critical_cve_filter  # On suppose que tu as cette fonction

def test_critical_cve_filter():
    """
    Test si le filtre garde bien uniquement les scores > 8.0
    """
    # 1. Préparation de données de test (Mock Data)
    mock_data = pd.DataFrame([
        {"cve_id": "CVE-1", "cvss_score": 9.8}, # Doit rester
        {"cve_id": "CVE-2", "cvss_score": 4.5}, # Doit être supprimé
        {"cve_id": "CVE-3", "cvss_score": 8.1}  # Doit rester
    ])

    # 2. Exécution de la logique (on appelle ton asset/fonction)
    result = critical_cve_filter(mock_data)

    # 3. Vérifications (Assertions)
    assert len(result) == 2, "Le filtre devrait garder 2 CVE sur 3"
    assert "CVE-2" not in result["cve_id"].values, "La CVE-2 (score 4.5) ne devrait pas être présente"
    assert result["cvss_score"].min() > 8.0, "Toutes les CVE restantes doivent avoir un score > 8.0"

def test_ip_format():
    """
    Exemple de test pour vérifier si une IP est bien formatée
    """
    # On pourrait tester ici une regex de validation d'IP
    sample_ip = "192.168.1.1"
    assert len(sample_ip.split('.')) == 4