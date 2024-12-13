
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Fonction pour établir la connexion avec la base de données
def get_connection():
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD")
        )
        print("Connexion réussie à la base de données.")
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None