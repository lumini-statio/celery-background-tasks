import random
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Pokemon

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
        
        poke_db = Pokemon(
            name=name,
            base_experience=xp,
            height=height
        )
        
        poke_db.save()
        
        logger.info(f"📝 Datos obtenidos - Nombre: {name}, XP: {xp}, Altura: {height}")
    
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Error de conexión con PokeAPI: {e}"
        logger.error(error_msg)
        return {
            'status': 'ERROR', 
            'message': error_msg,
            'error_type': 'HTTP_ERROR'
        }
        
    except KeyError as e:
        error_msg = f"❌ Error en estructura de datos de la API: {e}"
        logger.error(error_msg)
        return {
            'status': 'ERROR',
            'message': error_msg,
            'error_type': 'DATA_STRUCTURE_ERROR'
        }
        
    except Exception as e:
        error_msg = f"❌ Error inesperado: {e}"
        logger.error(error_msg)
        return {
            'status': 'ERROR',
            'message': error_msg,
            'error_type': 'UNKNOWN_ERROR'
        }
