from rich import print
from petshops_scrapper import *
import os

from petshops_scrapper.mascotify import MascotifyMenu
from petshops_scrapper.pharmivet import PharmivetMenu
from petshops_scrapper.misterpet import MisterPetMenu
from petshops_scrapper.mascota_veloz import MascotaVelozMenu
from petshops_scrapper.superpet import SuperPetMenu
from rich import print

print("[orange3]Obteniendo Menus de Todas las paginas[/orange3]")
SuperPetMenu()
MascotifyMenu()
MisterPetMenu()
MascotaVelozMenu()
PharmivetMenu()


os.makedirs("raw_data/", exist_ok=True)

from petshops_scrapper import MascotaVeloz, Mascotify, MisterPet, Pharmivet, SuperPet

RUN_LOCAL_EXISTING_PRODUCTS = True
TOTAL_WORKERS = 30

MascotaVeloz(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
Mascotify(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
MisterPet(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
Pharmivet(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
SuperPet(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)


from petshops_scrapper import NAMES, DataProcessor

WORKERS_PER_COMPANY = {
    "SuperPet": 20,
    "MascotaVeloz": 10,
    "Mascotify": 3,
    "PharmiVet": 5,
    "MisterPet": 5,
}

data = DataProcessor(workers_per_company=WORKERS_PER_COMPANY, names=NAMES).process_all()
