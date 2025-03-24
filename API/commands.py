import click
import json
from.app import app, db
from .api_questionnaire import *

@app.cli.command()
def syncdb() -> None:
    """Crée les tables manquantes
    """
    db.create_all()

@app.cli.command()
def cleardb() -> None:
    """Supprime toutes les tables 
    """
    db.drop_all()

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Charge les données JSON dans la base de données
    """
    db.create_all()
    with open(filename, 'r') as f:
        data = json.load(f)
    for questionnaire in data:
        ajout_quiz(questionnaire)

    
    print('Data loaded')