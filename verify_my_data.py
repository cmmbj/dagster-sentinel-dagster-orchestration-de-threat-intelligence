import duckdb

conn = duckdb.connect("data/cyber_data.db")

print("\n--- ÉCHANTILLON DES CVE CRITIQUES RÉCUPÉRÉES ---")
# Ici ça fonctionnait déjà
print(conn.execute("SELECT cve_id, cvss_score FROM stg_cve_critical LIMIT 5").df())

print("\n--- TOP DES IPs MALVEILLANTES DÉTECTÉES ---")
# On utilise les noms exacts renvoyés par l'API
print(conn.execute("""
    SELECT ipAddress, abuseConfidenceScore 
    FROM stg_malicious_ips 
    WHERE abuseConfidenceScore > 90 
    LIMIT 5
""").df())

conn.close()