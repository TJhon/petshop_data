from rich import print
from petshops_scrapper import *
import os

from petshops_scrapper.mascotify import MascotifyMenu
from petshops_scrapper.pharmivet import PharmivetMenu
from petshops_scrapper.misterpet import MisterPetMenu
from petshops_scrapper.mascota_veloz import MascotaVelozMenu
from petshops_scrapper.superpet import SuperPetMenu
from rich import print

# print("[orange3]Obteniendo Menus de Todas las paginas[/orange3]")
# SuperPetMenu()
# MascotifyMenu()
# MisterPetMenu()
# MascotaVelozMenu()
# PharmivetMenu()


os.makedirs('raw_data/', exist_ok=True)

RUN_LOCAL_EXISTING_PRODUCTS = True
TOTAL_WORKERS = 30

m1 = MascotaVeloz(local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
m2 = Mascotify   (local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
m3 = MisterPet   (local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
m4 = Pharmivet   (local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
m5 = SuperPet    (local=RUN_LOCAL_EXISTING_PRODUCTS, n_workers=TOTAL_WORKERS)
# print(data_i)
m1.fetch_all_information()
m2.fetch_all_information()
m3.fetch_all_information()
m4.fetch_all_information()
m5.fetch_all_information()