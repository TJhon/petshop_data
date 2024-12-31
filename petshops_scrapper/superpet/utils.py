import os
import json
from datetime import datetime
import pytz  

def save_array(array, name, ext="json"):
    base_dir = "info"
    last_dir = os.path.join(base_dir, "last")
    history_dir = os.path.join(base_dir, "history", name)
    
 
    os.makedirs(last_dir, exist_ok=True)
    os.makedirs(history_dir, exist_ok=True)

    lima_tz = pytz.timezone("America/Lima")
    current_time = datetime.now(lima_tz)
    formatted_date = current_time.strftime("%Y-%m-%d_%H-%M")
    
    
    last_file_path = os.path.join(last_dir, f"{name}.{ext}")
    history_file_path = os.path.join(history_dir, f"{formatted_date}.{ext}")
    
    
    try:
        with open(last_file_path, "w") as last_file:
            json.dump(array, last_file, indent=4)
        with open(history_file_path, "w") as history_file:
            json.dump(array, history_file, indent=4)
        print(f"Datos guardados en:\n- {last_file_path}\n- {history_file_path}")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")