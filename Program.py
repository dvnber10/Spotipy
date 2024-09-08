
import requests
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#importacion de las variables de entorno
load_dotenv()

#connexión a mongo DB
Client = MongoClient(os.getenv('Mongo_Client'))
db = Client[os.getenv('Database')]
collection = db[os.getenv('collection')]
print(collection)

#Conexión con el cliente de spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('Spotify_Id'),
   client_secret=os.getenv('Spotify_secret')
))
#Obtener los datos de spotify segun el artista
def fetch_spotify_data(artist_id):
   # Por ejemplo, obtener información de un artista específico
    artist_info = sp.artist(artist_id)
    
    return artist_info
def save_to_mongodb(data):
   # Guardar datos en MongoDB
    collection.insert_one(data)
    print("guardado correctamente")

def search_artist(artist_name):
    # Buscar el artista por nombre
    result = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if result['artists']['items']:
        artist = result['artists']['items'][0]  # Tomar el primer artista encontrado
        return artist['id']  # Devolver el ID del artista
    else:
        return None

def main():
    name_artist =input("Ingrese el nombre del artista\n")
    id_artist= search_artist(name_artist)
    spotify_data = fetch_spotify_data(id_artist)
    save_to_mongodb(spotify_data)
    print("Datos guardados en MongoDB")

main()