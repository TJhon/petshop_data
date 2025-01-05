from rich import print
from petshops_scrapper import *
import os
from petshops_scrapper.mascotify import MascotifyMenu
from petshops_scrapper.pharmivet import PharmivetMenu
from petshops_scrapper.misterpet import MisterPetMenu
from petshops_scrapper.mascota_veloz import MascotaVelozMenu
from petshops_scrapper.superpet import SuperPetMenu
from rich import print

from petshops_scrapper import MascotaVeloz, Mascotify, MisterPet, Pharmivet, SuperPet
from petshops_scrapper import NAMES, DataProcessor

print("[orange3]Obteniendo Menus de Todas las paginas[/orange3]")
SuperPetMenu()
MascotifyMenu()
MisterPetMenu()
MascotaVelozMenu()
PharmivetMenu()


os.makedirs("raw_data/", exist_ok=True)


RUN_LOCAL_EXISTING_PRODUCTS = True

MascotaVeloz(local=RUN_LOCAL_EXISTING_PRODUCTS)
Mascotify(local=RUN_LOCAL_EXISTING_PRODUCTS)
MisterPet(local=RUN_LOCAL_EXISTING_PRODUCTS)
Pharmivet(local=RUN_LOCAL_EXISTING_PRODUCTS)
SuperPet(local=RUN_LOCAL_EXISTING_PRODUCTS)


WORKERS_PER_COMPANY = {
    "SuperPet": 20,
    "MascotaVeloz": 10,
    "Mascotify": 3,
    "PharmiVet": 5,
    "MisterPet": 5,
}

data = DataProcessor(workers_per_company=WORKERS_PER_COMPANY, names=NAMES).process_all()
