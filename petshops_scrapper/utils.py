import os
import json
from datetime import datetime
import pytz  
from rich import print
from bs4 import BeautifulSoup
import requests, re

def clean_numbers(text: str) -> float:
    "Extrae el primer número como flotante."
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    return None
def clean_text(text: str) -> str:
    "Elimina espacios innecesarios."
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def find_max_pages(pages: list):
    try:
        n_pages = [clean_numbers(n.get_text()) for n in pages]
        n_pages = [n for n in n_pages if n]
        total_pages = int(max(n_pages))
        return total_pages
    except:
        return None


def save_array(array, name, base_dir='info', ext="json"):
    last_dir = os.path.join(base_dir, "last")
    history_dir = os.path.join(base_dir, "history", name)
    
 
    os.makedirs(last_dir, exist_ok=True)
    os.makedirs(history_dir, exist_ok=True)

    lima_tz = pytz.timezone("America/Lima")
    current_time = datetime.now(lima_tz)
    formatted_date = current_time.strftime("%Y-%m-%d_%H")
    
    
    last_file_path = os.path.join(last_dir, f"{name}.{ext}")
    history_file_path = os.path.join(history_dir, f"{formatted_date}.{ext}")
    
    
    try:
        with open(last_file_path, "w") as last_file:
            json.dump(array, last_file, indent=4)
        with open(history_file_path, "w") as history_file:
            json.dump(array, history_file, indent=4)
        print(f"[green]Datos de {name} guardados en:\n\t- {last_file_path}\n\t- {history_file_path}[/green]")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def get_soup(url: str) -> BeautifulSoup:
    """Obtiene el contenido HTML de una URL y lo convierte en un objeto BeautifulSoup."""
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")

def load_json_menu(name="", path = "info/{type}/last", type="menu"):
    path = path.format(type=type)
    with open(os.path.join(path, name + ".json")) as f:
        data = json.load(f)
    return data
def exists_products(name="", path = "info/{type}/last", type="products"):
    path = path.format(type=type)
    file = os.path.join(path, name + ".json")
    return os.path.exists(file)
