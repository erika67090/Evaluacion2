import requests
import urllib.parse

URL_GEOCODIFICACION = "https://graphhopper.com/api/1/geocode?"
URL_RUTA = "https://graphhopper.com/api/1/route?"
CLAVE = "PEGUE_AQUI_SU_API_KEY"
PALABRAS_SALIR = ("s", "salir")

# Perfiles de vehículo: lo que escribe el usuario -> valor que entiende GraphHopper
PERFILES = {
    "auto": "car",
    "bicicleta": "bike",
    "a pie": "foot",
}


def quiere_salir(texto):
    """Devuelve True si el usuario escribió 's' o 'salir'."""
    return texto.strip().lower() in PALABRAS_SALIR


def geocodificar(ubicacion, clave):
    """Convierte un nombre de lugar en latitud/longitud."""
    url = URL_GEOCODIFICACION + urllib.parse.urlencode(
        {"q": ubicacion, "limit": "1", "locale": "es", "key": clave}
    )
    respuesta = requests.get(url)
    estado = respuesta.status_code
    datos = respuesta.json()

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        region = datos["hits"][0].get("state", "")
        if region and pais:
            nombre_completo = f"{nombre}, {region}, {pais}"
        elif pais:
            nombre_completo = f"{nombre}, {pais}"
        else:
            nombre_completo = nombre
        print(f"URL de la API de geocodificación para {nombre_completo}:")
        print(url)
        return estado, lat, lng, nombre_completo

    if estado != 200:
        print(f"Estado de la API de geocodificación: {estado}")
        print(f"Mensaje de error: {datos.get('message', 'sin mensaje')}")
    else:
        print(f"No se encontró la ubicación '{ubicacion}'.")
    return estado, None, None, ubicacion


while True:
    print("\n=================================================")
    print("PLANIFICADOR DE RUTAS - BIBLIOTECA NACIONAL")
    print("Perfiles de vehículo disponibles: auto, bicicleta, a pie")
    print("En cualquier momento escriba 's' o 'salir' para terminar.")
    print("=================================================")

    perfil_usuario = input("Ingrese un perfil de vehículo: ").lower().strip()
    if quiere_salir(perfil_usuario):
        print("Gracias por usar el programa. ¡Hasta pronto!")
        break
    if perfil_usuario in PERFILES:
        vehiculo = PERFILES[perfil_usuario]
    else:
        vehiculo = "car"
        perfil_usuario = "auto"
        print("No se ingresó un perfil válido. Se usará el perfil 'auto'.")

    origen = input("Ubicación de origen: ")
    if quiere_salir(origen):
        print("Gracias por usar el programa. ¡Hasta pronto!")
        break
    if origen.strip() == "":
        print("Debe ingresar una ubicación de origen.")
        continue
    datos_origen = geocodificar(origen, CLAVE)

    destino = input("Ubicación de destino: ")
    if quiere_salir(destino):
        print("Gracias por usar el programa. ¡Hasta pronto!")
        break
    if destino.strip() == "":
        print("Debe ingresar una ubicación de destino.")
        continue
    datos_destino = geocodificar(destino, CLAVE)

    print("=================================================")
    if datos_origen[0] == 200 and datos_destino[0] == 200 and datos_origen[1] is not None and datos_destino[1] is not None:
        punto_o = "&point=" + str(datos_origen[1]) + "%2C" + str(datos_origen[2])
        punto_d = "&point=" + str(datos_destino[1]) + "%2C" + str(datos_destino[2])
        url_ruta = (
            URL_RUTA
            + urllib.parse.urlencode({"key": CLAVE, "vehicle": vehiculo, "locale": "es"})
            + punto_o
            + punto_d
        )
        respuesta = requests.get(url_ruta)
        estado = respuesta.status_code
        datos = respuesta.json()

        print(f"Estado de la API de rutas: {estado}")
        print(f"URL de la API de rutas:\n{url_ruta}")
        print("=================================================")
        print(f"Indicaciones desde {datos_origen[3]} hasta {datos_destino[3]} en {perfil_usuario}")
        print("=================================================")

        if estado == 200:
            distancia_m = datos["paths"][0]["distance"]
            tiempo_ms = datos["paths"][0]["time"]

            km = distancia_m / 1000
            millas = km / 1.61
            segundos_totales = tiempo_ms / 1000
            horas = int(segundos_totales // 3600)
            minutos = int((segundos_totales % 3600) // 60)
            segundos = int(segundos_totales % 60)

            print(f"Distancia recorrida: {millas:.2f} millas / {km:.2f} km")
            print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
            print("=================================================")
            print("Narrativa del viaje (paso a paso):")
            for numero, paso in enumerate(datos["paths"][0]["instructions"], start=1):
                texto = paso["text"]
                paso_km = paso["distance"] / 1000
                paso_millas = paso_km / 1.61
                print(f"{numero}. {texto} ( {paso_km:.2f} km / {paso_millas:.2f} millas )")
            print("=================================================")
        else:
            print(f"Mensaje de error: {datos.get('message', 'sin mensaje')}")
            print("=================================================")
    else:
        print("No fue posible calcular la ruta. Revise las ubicaciones ingresadas.")