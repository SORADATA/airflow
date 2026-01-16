from airflow.sdk import task
import pandas as pd

# 1. Tache d'Extraction
@task()
def extract_data():
    print("Extraction des donnéées météo depuis l'API")
    return {
        "date": "2023-01-01",
        "city": "NYC",
        "weather": {
            "temps": 33,
            "conditions": "Light snow and wind"
        }
    }

# 2. Tache de transformation
@task()
def transform_data(raw_data):
    transformed_data = [
        [
            raw_data.get("date"),
            raw_data.get("location"),
            raw_data.get("weather").get("temp"),
            raw_data.get("weather").get("conditions")
        ]
    ]
    return transformed_data

    # 3. Tache de chargement
    @task()
    def load_data(transformed_data):
        loaded_data = pd.DataFrame(transformed_data)
        loaded_data.columns = [
            "date",
            "location",
            "weather_temp",
            "weather_conditions"
        ]
        print(loaded_data)

