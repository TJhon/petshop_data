

Aquí tienes una versión mejorada de tu README:

---

# petshop_data

## Requisitos

- **Python** >= 3.12
- **Poetry** para la gestión de dependencias

## Instalación

1. Instala Poetry si no lo tienes ya instalado:

   ```sh
   pip install poetry
   ```

2. Instala las dependencias del proyecto:

   ```sh
   poetry install --no-root
   ```

## Configuración

Dentro del archivo `main.py`, hay dos constantes clave para personalizar el comportamiento del programa:

- **`RUN_LOCAL_EXISTING_PRODUCTS`**  
  - **Valor por defecto:** `True`  
  - **Propósito:**  
    - Si está en `True`, utiliza la lista existente de productos para extraer detalles específicos de cada uno.  
    - Si está en `False`, extrae información general de las páginas web (como enlaces y nombres) y actualiza la lista de productos.  
    - **Recomendación:** Cambiar a `False` cada dos días para mantener la lista actualizada.

- **`WORKERS_PER_COMPANY`**  
  - **Propósito:** Define el número de procesos paralelos utilizados para extraer detalles de los productos, para cada empresa.
  - **Recomendación:** No incrementar mucho los números si se requiere los datos más rapido. Ya que demasiadas peticiones hace que la pagina bloquee la IP, haciendo imposible obtener más datos y en algunos casos haciendo caer la página.

## Uso

1. Configura las constantes en `main.py` según sea necesario.  
2. Ejecuta el script principal para iniciar el proceso de extracción:

   ```sh
   python main.py
   ```

3. Una vez completada la ejecución, los datos se guardarán en la carpeta `raw_data/{name}.xlsx`, donde `{name}` corresponde al nombre comercial de la página procesada.

## Notas

- Es importante actualizar regularmente la lista de productos (cambiando `RUN_LOCAL_EXISTING_PRODUCTS` a `False`) para garantizar que se incluyan nuevos productos añadidos a las páginas web.  




<!-- - Objetivos
  - https://www.superpet.pe/
    - [x] lista_productos_id
    - [ ] obtener el excel
  - [x] h ttps://mascotify.pe/
    - bs4
  - https://pharmivet.pe/
    - [ ] Extraer productos
      - [x] funciones
      - [ ] data
    - [ ] Extraer info de products
      - [x] funciones
      - [ ] data
  - https://www.misterpet.pe/
    - extraer menu
    - extraer products
    - extraer informacion por pagina
    - extraer informacion de cada pagina
  - https://mascotaveloz.pe/
  - ` -->

## Objetivos

- Objetivos
  - Extraer el menu 
    - Identificar Categorias (Perro, gato, otros) y subCategorias (Alimentacion, medicamentos)
      - [x] SuperPet 
      - [x] Mascotify
      - [x] Pharmivet
      - [x] MisterPet
      - [x] MascotaVeloz
  - Implementar Paginacion para los que tengan
      - [x] SuperPet 
      - [x] Mascotify
      - [x] Pharmivet
      - [x] MisterPet
      - [x] MascotaVeloz
  - Extraer productos de cada pagina
      - [x] SuperPet 
      - [x] Mascotify
      - [x] Pharmivet
      - [x] MisterPet
      - [x] MascotaVeloz
  - Extraer detalles del producto
      - [x] SuperPet 
      - [x] Mascotify
      - [x] Pharmivet
      - [x] MisterPet
      - [x] MascotaVeloz
  - General el XLSX
      - [x] SuperPet 
      - [x] Mascotify
      - [x] Pharmivet
      - [x] MisterPet
      - [x] MascotaVeloz

