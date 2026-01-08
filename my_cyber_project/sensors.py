from dagster import asset_sensor, AssetKey, SensorEvaluationContext, RunRequest

# On surveille la fin de la chaîne (le rapport final)
@asset_sensor(asset_key=AssetKey("final_security_report"), job_name="alert_job")
def cve_alert_sensor(context: SensorEvaluationContext, asset_event):
    """
    Ce sensor surveille l'asset final. 
    Dès qu'il est mis à jour, il déclenche le job d'alerte.
    """
    context.log.info("Le sensor a détecté une mise à jour du rapport final !")
    
    yield RunRequest(
        run_key=context.cursor,
        run_config={} 
    )