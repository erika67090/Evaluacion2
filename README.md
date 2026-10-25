# Evaluacion2

## Descripción del proyecto

Planificador de rutas desarrollado en Python como parte de la Evaluación Parcial N° 2
de la asignatura *Telepresencia y Entornos Innovadores de Colaboración Humana* (CUY6142).

El programa usa la API REST de **GraphHopper Directions** para:

- Convertir el nombre de un lugar en coordenadas (geocodificación).
- Calcular una ruta entre un origen y un destino según el tipo de vehículo.
- Mostrar la distancia (en millas y kilómetros, con máximo 2 decimales) y la duración del viaje.
- Imprimir la narrativa del viaje paso a paso en español.

Todos los textos de interacción están en español. Para terminar el programa se puede
escribir `s` o `salir` en cualquier pregunta.

## Requisitos

- Python 3
- Librería `requests` (`pip3 install requests`)
- Una API key de GraphHopper (gratuita en https://www.graphhopper.com)

## Cómo ejecutar el script

1. Clonar el repositorio:
   ```
   git clone https://github.com/erika67090/Evaluacion2.git
   ```
2. Entrar a la carpeta:
   ```
   cd Evaluacion2
   ```
3. Abrir `graphhopper_es.py` y reemplazar `PEGUE_AQUI_SU_API_KEY` por su API key de GraphHopper.
4. Ejecutar el script:
   ```
   python3 graphhopper_es.py
   ```
5. Ingresar los datos que solicita el programa:
   - Perfil de vehículo: `auto`, `bicicleta` o `a pie`
   - Ubicación de origen (ejemplo: `Santiago, Chile`)
   - Ubicación de destino (ejemplo: `Valparaíso, Chile`)
6. Para salir, escribir `s` o `salir`.

## Autores

- Erika Vidarte
- Sebastian Abarca