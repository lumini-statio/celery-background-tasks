import random
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Pokemon
import json
import os

from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(bind=True)
def api(self):
    try:
        poke_id = random.randint(1, 1000)
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}')
        response.raise_for_status()
        
        pokemon = response.json()
        
        name = pokemon['name']
        xp = pokemon['base_experience']
        height = pokemon['height']
        
        with open(f'{settings.MEDIA_PATH}/{name}.json', 'w', encoding='utf-8') as file:
            json.dump(pokemon, file, indent=4, ensure_ascii=False)
        
        poke_db = Pokemon(
            name=name,
            base_experience=xp,
            height=height
        )
        
        poke_db.save()
        
        logger.info(f"📝 Datos obtenidos - Nombre: {name}, XP: {xp}, Altura: {height}")
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        logger.error(error_msg)
        return {
            'status': 'ERROR',
            'message': error_msg,
            'error_type': 'UNKNOWN_ERROR'
        }


@shared_task(bind=True)
def delete_files(self):
    try:
        media = settings.MEDIA_PATH
        
        for file in os.listdir(media):
            path = os.path.join(media, file)
            
            if os.path.isfile(path):
                os.remove(path)
                logger.info(f'archivo eliminado: {file}')
    except Exception as e:
        logger.error(str(e))